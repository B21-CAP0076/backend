from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from odmantic import AIOEngine, ObjectId
from odmantic.engine import AIOCursor

from db.mongodb import mongo_engine
from models.book_summary import BookSummary
from models.reading_commitment import ReadingCommitment, ReadingCommitmentCreate
from models.swipe import Swipe
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
@router.get("/user/potential_match")
async def get_all_user_potential_match(
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
                # Only include reading commitment that haven't matched to anyone yet
                {"partner": {"$eq": None}}
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


@router.get("/{id}")
async def get(id: ObjectId, engine: AIOEngine = Depends(mongo_engine)):
    reading_commitment = await engine.find_one(ReadingCommitment, ReadingCommitment.id == id)
    if reading_commitment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return reading_commitment


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

    creation_date = datetime.utcnow()

    reading_commitment = ReadingCommitment(
        owner=owner,
        creation_date=creation_date,
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
    for book_summary in referenced_book_summary:
        await engine.delete(book_summary)

    # Delete swipe that referenced to deleted reading_commitment
    referenced_swipe = await engine.find(
        Swipe,
        (Swipe.commitment_1 == ObjectId(id)) | (Swipe.commitment_2 == ObjectId(id))
    )
    for swipe in referenced_swipe:
        await engine.delete(swipe)

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
# @router.put("/create_dummy", response_model=ReadingCommitment)
# async def create_dummy(reading_commitment: ReadingCommitment, engine: AIOEngine = Depends(mongo_engine)):
#     await engine.save(reading_commitment)
#     return reading_commitment

# WHILE DEBUGGING, DELETE DATA DIRECTLY FROM DATABASE FOR CONVENIENCE
