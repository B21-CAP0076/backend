from fastapi import APIRouter, Depends
from odmantic import AIOEngine, ObjectId, query

from choice.match import MatchStatus, MatchAction
from choice.reading_commitment import ReadingCommitmentStatus
from db.mongodb import mongo_engine
from models.match import Match
from models.reading_commitment import ReadingCommitment
from models.user import User
from routers.user import get_current_user

router = APIRouter(
    tags=["match"],
    prefix="/match"
)


@router.post("/")
async def matchmaking(
        commitment_1_id: ObjectId,
        commitment_2_id: ObjectId,
        action: MatchAction,
        engine: AIOEngine = Depends(mongo_engine),
        owner: User = Depends(get_current_user)
):
    match = await engine.find_one(
        Match,
        Match.commitment_1 == commitment_1_id,
        Match.commitment_2 == commitment_2_id
    )

    if match is None:
        commitment_1 = await engine.find_one(ReadingCommitment, ReadingCommitment.id == commitment_1_id)
        commitment_2 = await engine.find_one(ReadingCommitment, ReadingCommitment.id == commitment_2_id)

        match_status = MatchStatus.PENDING if action == MatchAction.SWIPE_RIGHT else MatchStatus.REJECTED
        new_match = Match(commitment_1=commitment_1, commitment_2=commitment_2, status=match_status)

        await engine.save(new_match)
        return new_match

    else:
        # Case: match, both user swipe right
        if match.status == MatchStatus.PENDING and action == MatchAction.SWIPE_RIGHT:
            # Update reading_commitment status to "closed"
            setattr(match.commitment_1, "status", ReadingCommitmentStatus.CLOSED)
            await engine.save(match.commitment_1)

            setattr(match.commitment_2, "status", ReadingCommitmentStatus.CLOSED)
            await engine.save(match.commitment_2)

            # Update match status to "match"
            setattr(match, "status", MatchStatus.MATCH)
            await engine.save(match)

            return match

        elif match.status == MatchStatus.MATCH:
            return match

        else:
            await engine.delete(match)
            return match


@router.get("/user")
async def get_all_user_match(owner: User = Depends(get_current_user), engine: AIOEngine = Depends(mongo_engine)):
    reading_commitment = await engine.find(ReadingCommitment, ReadingCommitment.owner == owner.id)
    reading_commitment_ids = [rc.id for rc in reading_commitment]

    match = await engine.find(
        Match,
        (((query.in_(Match.commitment_1, reading_commitment_ids))
         | (query.in_(Match.commitment_2, reading_commitment_ids))) & query.eq(Match.status, MatchStatus.MATCH))
    )

    return match
