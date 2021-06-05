from typing import Optional
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from odmantic import AIOEngine, ObjectId
from odmantic.query import QueryExpression

from db.mongodb import mongo_engine

from models.reading_commitment import ReadingCommitment, ReadingCommitmentCreate
from models.user import User
from models.book_summary import BookSummary
from models.swipe import Swipe
from routers.user import get_current_user

router = APIRouter(
    tags=["reading_commitment"],
    prefix="/reading_commitment"
)


@router.get("/")
async def get_all(
        page: int = 1,
        owner_id: Optional[str] = None,
        partner_id: Optional[str] = None,
        owner_reading_cluster: Optional[int] = None,
        engine: AIOEngine = Depends(mongo_engine)
):
    skip: int = 50 * (page - 1)

    queries = []
    # Owner query
    if owner_id:
        qe = QueryExpression({'owner': ObjectId(owner_id)})
        queries.append(qe)

    # Partner query
    if partner_id:
        qe = QueryExpression({'partner.id': ObjectId(partner_id)})
        queries.append(qe)

    if owner_reading_cluster:
        qe = QueryExpression({'owner.reading_cluster': owner_reading_cluster})
        queries.append(qe)

    reading_commitments = await engine.find(ReadingCommitment, *queries, skip=skip, limit=50)
    return reading_commitments


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


@router.get("/{id}")
async def get(id: ObjectId, engine: AIOEngine = Depends(mongo_engine)):
    reading_commitment = await engine.find_one(ReadingCommitment, ReadingCommitment.id == id)
    if reading_commitment is None:
        raise HTTPException(404)
    return reading_commitment


@router.put("/create")
async def create(
        reading_commitment_create: ReadingCommitmentCreate,
        owner: User = Depends(get_current_user),
        engine: AIOEngine = Depends(mongo_engine)
):
    creation_date = datetime.utcnow()

    reading_commitment = ReadingCommitment(
        owner=owner,
        creation_date=creation_date,
        end_date=reading_commitment_create.end_date,
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
        raise HTTPException(404)

    if reading_commitment.owner.id != owner.id:
        raise HTTPException(403, detail="Credentials error")

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
