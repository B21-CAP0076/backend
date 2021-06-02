from fastapi import APIRouter, Depends, HTTPException
from odmantic import AIOEngine, ObjectId

from db.mongodb import mongo_engine
from models.genre import Genre

router = APIRouter(
    tags=["genre"],
    prefix="/genre"
)


@router.get("/")
async def get_all(engine: AIOEngine = Depends(mongo_engine)):
    genres = await engine.find(Genre)
    return genres


@router.get("/{id}")
async def get(id: ObjectId, engine: AIOEngine = Depends(mongo_engine)):
    genre = await engine.find_one(Genre, Genre.id == id)
    if genre is None:
        raise HTTPException(404)
    return genre