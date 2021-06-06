from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from odmantic import AIOEngine, ObjectId
from odmantic.query import QueryExpression

from db.mongodb import mongo_engine
from models.hobby import Hobby

router = APIRouter(
    tags=["hobby"],
    prefix="/hobby"
)


@router.get("/")
async def get_all(
        page: int = 1,
        name: Optional[str] = None,
        engine: AIOEngine = Depends(mongo_engine)
):
    queries = []
    if name:
        qe = QueryExpression({'name': {'$regex': name, '$options': 'i'}})
        queries.append(qe)

    skip: int = 50 * (page - 1)
    hobbies = await engine.find(Hobby, *queries, skip=skip, limit=50)
    return hobbies


@router.get("/{id}")
async def get(id: ObjectId, engine: AIOEngine = Depends(mongo_engine)):
    hobby = await engine.find_one(Hobby, Hobby.id == id)
    if hobby is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return hobby
