from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from odmantic import AIOEngine, ObjectId
from odmantic.query import QueryExpression

from db.mongodb import mongo_engine
from models.genre import Genre

router = APIRouter(
    tags=["genre"],
    prefix="/genre"
)


@router.get("/")
async def get_all(page: int = 1, name: Optional[str] = None, engine: AIOEngine = Depends(mongo_engine)):
    skip: int = 50 * (page - 1)

    queries = []
    if name:
        qe = QueryExpression({'name': {'$regex': name, '$options': 'i'}})
        queries.append(qe)

    genres = await engine.find(Genre, *queries, skip=skip, limit=50)
    return genres


@router.get("/{id}")
async def get(id: ObjectId, engine: AIOEngine = Depends(mongo_engine)):
    genre = await engine.find_one(Genre, Genre.id == id)
    if genre is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return genre
