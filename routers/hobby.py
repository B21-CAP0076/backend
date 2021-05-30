from fastapi import APIRouter, Depends, HTTPException
from odmantic import AIOEngine, ObjectId

from db.mongodb import mongo_engine
from models.hobby import Hobby, HobbyUpdate

router = APIRouter(
    tags=["hobby"],
    prefix="/hobby"
)


@router.get("/")
async def get_all(page: int = 1, engine: AIOEngine = Depends(mongo_engine)):
    skip: int = 20 * (page - 1)
    hobbies = await engine.find(Hobby, skip=skip, limit=20)
    return hobbies


@router.get("/{id}")
async def get(id: ObjectId, engine: AIOEngine = Depends(mongo_engine)):
    hobby = await engine.find_one(Hobby, Hobby.id == id)
    if hobby is None:
        raise HTTPException(404)
    return hobby


# @router.put("/", response_model=Hobby)
# async def create(hobby: Hobby, engine: AIOEngine = Depends(mongo_engine)):
#     await engine.save(hobby)
#     return hobby
#
#
# @router.patch("/{id}", response_model=Hobby)
# async def update(id: ObjectId, patch: HobbyUpdate, engine: AIOEngine = Depends(mongo_engine)):
#     hobby = await engine.find_one(Hobby, Hobby.id == id)
#     if hobby is None:
#         raise HTTPException(404)
#
#     patch_dict = patch.dict(exclude_unset=True)
#     for name, value in patch_dict.items():
#         setattr(hobby, name, value)
#     await engine.save(hobby)
#     return hobby
#
#
# @router.delete("/{id}")
# async def delete(id: ObjectId, engine: AIOEngine = Depends(mongo_engine)):
#     hobby = await engine.find_one(Hobby, Hobby.id == id)
#     if hobby is None:
#         raise HTTPException(404)
#     await engine.delete(hobby)
#     return hobby
