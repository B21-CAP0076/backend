from fastapi import APIRouter, Depends, HTTPException
from odmantic import AIOEngine, ObjectId

from db.mongodb import mongo_engine
from models.user import User, UserUpdate

router = APIRouter(
    tags=["user"],
    prefix="/user"
)


@router.get("/")
async def get_all(page: int = 1, engine: AIOEngine = Depends(mongo_engine)):
    skip: int = 20 * (page - 1)
    users = await engine.find(User, skip=skip, limit=20)
    return users


@router.get("/{id}")
async def get(id: ObjectId, engine: AIOEngine = Depends(mongo_engine)):
    user = await engine.find_one(User, User.id == id)
    if user is None:
        raise HTTPException(404)
    return user


@router.put("/", response_model=User)
async def create(user: User, engine: AIOEngine = Depends(mongo_engine)):
    await engine.save(user)
    return user


@router.patch("/{id}", response_model=User)
async def update(id: ObjectId, patch: UserUpdate, engine: AIOEngine = Depends(mongo_engine)):
    user = await engine.find_one(User, User.id == id)
    if user is None:
        raise HTTPException(404)

    patch_dict = patch.dict(exclude_unset=True)
    for name, value in patch_dict.items():
        setattr(user, name, value)
    await engine.save(user)
    return user


@router.delete("/{id}")
async def delete(id: ObjectId, engine: AIOEngine = Depends(mongo_engine)):
    user = await engine.find_one(User, User.id == id)
    if user is None:
        raise HTTPException(404)
    await engine.delete(user)
    return user
