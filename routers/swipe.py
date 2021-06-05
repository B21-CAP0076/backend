from fastapi import APIRouter, Depends, HTTPException
from odmantic import AIOEngine, ObjectId

from db.mongodb import mongo_engine
from models.swipe import Swipe
from models.reading_commitment import ReadingCommitment
from choice.swipe import SwipeState, SwipeStatus
from routers.user import oauth2_scheme

router = APIRouter(
    tags=["swipe"],
    prefix="/swipe"
)


@router.post("/")
async def swipe(
        commitment_1_id: ObjectId,
        commitment_2_id: ObjectId,
        state: SwipeState,
        engine: AIOEngine = Depends(mongo_engine),
        token: str = Depends(oauth2_scheme),
):
    try:
        swipe_obj = await engine.find_one(
            Swipe,
            Swipe.commitment_1 == commitment_1_id,
            Swipe.commitment_2 == commitment_2_id
        )

        commitment_1 = await engine.find_one(ReadingCommitment, ReadingCommitment.id == commitment_1_id)
        commitment_2 = await engine.find_one(ReadingCommitment, ReadingCommitment.id == commitment_2_id)

        if swipe_obj is None:
            status = SwipeStatus.RIGHT_SWIPED if state == SwipeState.RIGHT else SwipeStatus.LEFT_SWIPED
            new_swipe = Swipe(commitment_1=commitment_1, commitment_2=commitment_2, status=status)
            await engine.save(new_swipe)
            return new_swipe

        else:
            if swipe_obj.status == SwipeStatus.RIGHT_SWIPED and state == SwipeState.RIGHT:
                partner_field = "partner"
                setattr(commitment_1, partner_field, commitment_2.owner)
                await engine.save(commitment_1)
                setattr(commitment_2, partner_field, commitment_1.owner)
                await engine.save(commitment_2)

            await engine.delete(swipe_obj)
            return swipe_obj

    except:
        raise HTTPException(400, detail="Invalid path/query parameters")
