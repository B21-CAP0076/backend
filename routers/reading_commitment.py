from fastapi import APIRouter, Depends, HTTPException, status
from odmantic import AIOEngine, ObjectId
from odmantic.engine import AIOCursor

from choice.reading_commitment import ReadingCommitmentStatus
from db.mongodb import mongo_engine
from models.book_summary import BookSummary
from models.match import Match
from models.reading_commitment import ReadingCommitment, ReadingCommitmentCreate
from models.user import User
from routers.user import get_current_user

router = APIRouter(
    tags=["reading_commitment"],
    prefix="/reading_commitment"
)


@router.get("/user")
async def get_all_user_reading_commitment(
        page: int = 1,
        owner: User = Depends(get_current_user),
        engine: AIOEngine = Depends(mongo_engine)
):
    skip: int = 50 * (page - 1)

    reading_commitment = await engine.find(
        ReadingCommitment,
        ReadingCommitment.owner == owner.id,
        skip=skip,
        limit=50
    )
    return reading_commitment


# Query reading_commitment for matchmaking
# Sort reading_commitment by nearest value of ReadingCommitment.owner_reading_cluster with owner.reading_cluster)
@router.get("/potential_match")
async def get_all_user_reading_commitment_potential_match(
        page: int = 1,
        owner: User = Depends(get_current_user),
        engine: AIOEngine = Depends(mongo_engine)
):
    if owner.reading_cluster is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User.reading_cluster is none, predict User.reading_cluster using machine learning first"
        )

    skip: int = 50 * (page - 1)

    motor_collection = engine.get_collection(ReadingCommitment)

    pipeline = [
        # Initial query
        {"$match": {
            "$and": [
                # Exclude others owner's reading_commitment to prevent self-match
                {"owner": {"$ne": owner.id}},
                # Only include reading commitment that have "open" status
                {"status": {"$eq": ReadingCommitmentStatus.OPEN}}
            ]
        }},
        # Add temporary "diff" field to compute absolute value of reading cluster difference
        {"$addFields": {"diff": {
            "$abs": {"$subtract": [owner.reading_cluster, ++ReadingCommitment.owner_reading_cluster]}
        }}},
        # Sort based on absolute value of reading cluster difference
        {"$sort": {"diff": 1}},
        # Pagination
        {"$skip": skip},
        {"$limit": 50}
    ]

    # Solve reference object recursively
    pipeline.extend(AIOEngine._cascade_find_pipeline(ReadingCommitment))

    # Aggregate
    motor_cursor = motor_collection.aggregate(pipeline)

    aio_cursor = AIOCursor(ReadingCommitment, motor_cursor)

    reading_commitment = await aio_cursor

    return reading_commitment


@router.get("/match/{match_id}/own")
async def get_own_reading_commitment_within_match(
        match_id: str,
        owner: User = Depends(get_current_user),
        engine: AIOEngine = Depends(mongo_engine)
):
    match = await engine.find_one(Match, Match.id == ObjectId(match_id))

    if match is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    if match.commitment_1.owner.id == owner.id:
        return match.commitment_1

    if match.commitment_2.owner.id == owner.id:
        return match.commitment_2

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.get("/match/{match_id}/partner")
async def get_partner_reading_commitment_within_match(
        match_id: str,
        owner: User = Depends(get_current_user),
        engine: AIOEngine = Depends(mongo_engine)
):
    match = await engine.find_one(Match, Match.id == ObjectId(match_id))

    if match is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    # Return the opposite
    if match.commitment_1.owner.id == owner.id:
        return match.commitment_2

    if match.commitment_2.owner.id == owner.id:
        return match.commitment_1

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.put("/create")
async def create(
        reading_commitment_create: ReadingCommitmentCreate,
        owner: User = Depends(get_current_user),
        engine: AIOEngine = Depends(mongo_engine)
):
    if owner.reading_cluster is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User.reading_cluster is none, predict User.reading_cluster using machine learning first"
        )

    reading_commitment = ReadingCommitment(
        owner=owner,
        end_date=reading_commitment_create.end_date,
        owner_reading_cluster=owner.reading_cluster,
        book=reading_commitment_create.book
    )

    await engine.save(reading_commitment)

    return reading_commitment


@router.delete("/delete/{id}")
async def delete(
        id: str,
        owner: User = Depends(get_current_user),
        engine: AIOEngine = Depends(mongo_engine)
):
    reading_commitment = await engine.find_one(
        ReadingCommitment,
        ReadingCommitment.id == ObjectId(id)
    )

    if reading_commitment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    if reading_commitment.owner.id != owner.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Credentials error")

    # Delete related data

    # Delete book_summary that referenced to deleted reading_commitment
    referenced_book_summary = await engine.find(BookSummary, BookSummary.reading_commitment == ObjectId(id))
    for bs in referenced_book_summary:
        await engine.delete(bs)

    # Delete match that referenced to deleted reading_commitment
    referenced_match = await engine.find(
        Match,
        (Match.commitment_1 == ObjectId(id)) | (Match.commitment_2 == ObjectId(id))
    )
    for m in referenced_match:
        await engine.delete(m)

    # Delete reading_commitment
    await engine.delete(reading_commitment)

    return reading_commitment


# ENDPOINT FOR DEBUGGING

# @router.get("/")
# async def get_all(page: int = 1, engine: AIOEngine = Depends(mongo_engine)):
#     skip: int = 50 * (page - 1)
#     reading_commitment = await engine.find(ReadingCommitment, skip=skip, limit=50)
#     return reading_commitment
#
#
# @router.get("/{id}")
# async def get(id: ObjectId, engine: AIOEngine = Depends(mongo_engine)):
#     reading_commitment = await engine.find_one(ReadingCommitment, ReadingCommitment.id == id)
#     if reading_commitment is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
#     return reading_commitment
#
#
# @router.put("/create_dummy", response_model=ReadingCommitment)
# async def create_dummy(reading_commitment: ReadingCommitment, engine: AIOEngine = Depends(mongo_engine)):
#     await engine.save(reading_commitment)
#     return reading_commitment


# WHILE DEBUGGING, DELETE DATA DIRECTLY FROM DATABASE
