from fastapi import APIRouter, Depends, HTTPException
from odmantic import AIOEngine, ObjectId

from db.mongodb import mongo_engine
from models.genre import Genre, GenreUpdate

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


# @router.put("/", response_model=Genre)
# async def create(genre: Genre, engine: AIOEngine = Depends(mongo_engine)):
#     await engine.save(genre)
#     return genre
#
#
# @router.patch("/{id}", response_model=Genre)
# async def update(id: ObjectId, patch: GenreUpdate, engine: AIOEngine = Depends(mongo_engine)):
#     genre = await engine.find_one(Genre, Genre.id == id)
#     if genre is None:
#         raise HTTPException(404)
#
#     patch_dict = patch.dict(exclude_unset=True)
#     for name, value in patch_dict.items():
#         setattr(genre, name, value)
#     await engine.save(genre)
#     return genre
#
#
# @router.delete("/{id}")
# async def delete(id: ObjectId, engine: AIOEngine = Depends(mongo_engine)):
#     genre = await engine.find_one(Genre, Genre.id == id)
#     if genre is None:
#         raise HTTPException(404)
#     await engine.delete(genre)
#     return genre
