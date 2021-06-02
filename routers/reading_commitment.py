from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from odmantic import AIOEngine, ObjectId
from odmantic.query import QueryExpression

from db.mongodb import mongo_engine

from models.reading_commitment import ReadingCommitment, ReadingCommitmentUpdate

router = APIRouter(
    tags=["reading_commitment"],
    prefix="/reading_commitment"
)


@router.get("/")
async def get_all(
        page: int = 1,
        owner_id: Optional[ObjectId] = None,
        partner_id: Optional[ObjectId] = None,
        owner_reading_cluster: Optional[int] = None,
        engine: AIOEngine = Depends(mongo_engine)
):
    skip: int = 20 * (page - 1)

    queries = []
    # Owner query
    if owner_id:
        qe = QueryExpression({'owner': owner_id})
        queries.append(qe)

    # Partner query
    if partner_id:
        qe = QueryExpression({'partner.id': partner_id})
        queries.append(qe)

    if owner_reading_cluster:
        qe = QueryExpression({'owner.reading_cluster': owner_reading_cluster})
        queries.append(qe)

    reading_commitments = await engine.find(ReadingCommitment, *queries, skip=skip, limit=20)
    return reading_commitments


@router.get("/{id}")
async def get(id: ObjectId, engine: AIOEngine = Depends(mongo_engine)):
    reading_commitment = await engine.find_one(ReadingCommitment, ReadingCommitment.id == id)
    if reading_commitment is None:
        raise HTTPException(404)
    return reading_commitment


@router.put("/", response_model=ReadingCommitment)
async def create(reading_commitment: ReadingCommitment, engine: AIOEngine = Depends(mongo_engine)):
    await engine.save(reading_commitment)
    return reading_commitment


@router.patch("/{id}", response_model=ReadingCommitment)
async def update(id: ObjectId, patch: ReadingCommitmentUpdate, engine: AIOEngine = Depends(mongo_engine)):
    reading_commitment = await engine.find_one(ReadingCommitment, ReadingCommitment.id == id)
    if reading_commitment is None:
        raise HTTPException(404)

    patch_dict = patch.dict(exclude_unset=True)
    for name, value in patch_dict.items():
        setattr(reading_commitment, name, value)
    await engine.save(reading_commitment)
    return reading_commitment


@router.delete("/{id}")
async def delete(id: ObjectId, engine: AIOEngine = Depends(mongo_engine)):
    reading_commitment = await engine.find_one(ReadingCommitment, ReadingCommitment.id == id)
    if reading_commitment is None:
        raise HTTPException(404)
    await engine.delete(reading_commitment)
    return reading_commitment
