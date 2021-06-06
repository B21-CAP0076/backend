from typing import Optional
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from odmantic import AIOEngine, ObjectId
from odmantic.query import QueryExpression
from starlette import status

from db.mongodb import mongo_engine
from models.reading_commitment import ReadingCommitment
from models.user import User
from models.book_summary import BookSummary, BookSummaryCreate, BookSummaryUpdate
from routers.user import get_current_user

router = APIRouter(
    tags=["book_summary"],
    prefix="/book_summary"
)


@router.get("/user")
async def get_all_within_user_reading_commitment(
        reading_commitment_id: str,
        page: int = 1,
        owner: User = Depends(get_current_user),
        engine: AIOEngine = Depends(mongo_engine)
):
    skip: int = 50 * (page - 1)

    reading_commitment = await engine.find_one(
        ReadingCommitment,
        ReadingCommitment.id == ObjectId(reading_commitment_id)
    )

    if reading_commitment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reading commitment not found")

    if reading_commitment.owner.id != owner.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Credentials error")

    book_summaries = await engine.find(
        BookSummary,
        BookSummary.reading_commitment == ObjectId(reading_commitment_id),
        skip=skip,
        limit=50
    )

    return book_summaries


@router.get("/{id}")
async def get(id: ObjectId, engine: AIOEngine = Depends(mongo_engine)):
    book_summary = await engine.find_one(BookSummary, BookSummary.id == id)
    if book_summary is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return book_summary


@router.put("/create")
async def create(
        reading_commitment_id: str,
        book_summary_create: BookSummaryCreate,
        owner: User = Depends(get_current_user),
        engine: AIOEngine = Depends(mongo_engine)
):
    reading_commitment = await engine.find_one(
        ReadingCommitment,
        ReadingCommitment.id == ObjectId(reading_commitment_id),
        ReadingCommitment.owner == owner.id
    )

    if reading_commitment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    creation_date = datetime.utcnow()

    book_summary = BookSummary(
        reading_commitment=reading_commitment,
        creation_date=creation_date,
        summary=book_summary_create.summary
    )

    await engine.save(book_summary)
    return book_summary


@router.patch("/update/{id}", response_model=BookSummary)
async def update(
        id: str,
        patch: BookSummaryUpdate,
        owner: User = Depends(get_current_user),
        engine: AIOEngine = Depends(mongo_engine)
):
    book_summary = await engine.find_one(
        BookSummary,
        BookSummary.id == ObjectId(id)
    )

    if book_summary is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    reading_commitment = await engine.find_one(
        ReadingCommitment,
        ReadingCommitment.id == book_summary.reading_commitment.id
    )

    if reading_commitment.owner.id != owner.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Credentials error")

    patch_dict = patch.dict(exclude_unset=True)
    for name, value in patch_dict.items():
        setattr(book_summary, name, value)
    await engine.save(book_summary)

    return book_summary


@router.delete("/delete/{id}")
async def delete(
        id: str,
        owner: User = Depends(get_current_user),
        engine: AIOEngine = Depends(mongo_engine)
):
    book_summary = await engine.find_one(
        BookSummary,
        BookSummary.id == ObjectId(id)
    )

    if book_summary is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    reading_commitment = await engine.find_one(
        ReadingCommitment,
        ReadingCommitment.id == book_summary.reading_commitment.id
    )

    if reading_commitment.owner.id != owner.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Credentials error")

    await engine.delete(book_summary)
    return book_summary


# ENDPOINT FOR DEBUGGING

# @router.get("/")
# async def get_all(page: int = 1, reading_commitment_id: Optional[str] = None, engine: AIOEngine = Depends(mongo_engine)):
#     skip: int = 50 * (page - 1)
#
#     queries = []
#
#     if reading_commitment_id:
#         qe = QueryExpression({'reading_commitment': ObjectId(reading_commitment_id)})
#         queries.append(qe)
#
#     book_summaries = await engine.find(BookSummary, *queries, skip=skip, limit=50)
#     return book_summaries
#
#
# @router.put("/create_dummy", response_model=BookSummary)
# async def create_dummy(book_summary: BookSummary, engine: AIOEngine = Depends(mongo_engine)):
#     await engine.save(book_summary)
#     return book_summary

# WHILE DEBUGGING, DELETE DATA DIRECTLY FROM DATABASE FOR CONVENIENCE
