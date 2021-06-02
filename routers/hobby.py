from fastapi import APIRouter, Depends, HTTPException
from odmantic import AIOEngine, ObjectId

from db.mongodb import mongo_engine
from models.hobby import Hobby

router = APIRouter(
    tags=["hobby"],
    prefix="/hobby"
)


@router.get("/")
async def get_all(engine: AIOEngine = Depends(mongo_engine)):
    hobbies = await engine.find(Hobby)
    return hobbies


@router.get("/{id}")
async def get(id: ObjectId, engine: AIOEngine = Depends(mongo_engine)):
    hobby = await engine.find_one(Hobby, Hobby.id == id)
    if hobby is None:
        raise HTTPException(404)
    return hobby
