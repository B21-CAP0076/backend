from fastapi import APIRouter, Depends, HTTPException
from odmantic import AIOEngine, ObjectId

from db.mongodb import mongo_engine
from models.user import User, UserUpdate

router = APIRouter(
    tags=["user"],
    prefix="/user"
)


@router.get("/")
async def get_all_users(engine: AIOEngine = Depends(mongo_engine)):
    users = await engine.find(User)
    return users


@router.get("/{id}")
async def get_user(id: ObjectId, engine: AIOEngine = Depends(mongo_engine)):
    user = await engine.find_one(User, User.id == id)
    if user is None:
        raise HTTPException(404)
    return user


@router.put("/", response_model=User)
async def create_user(user: User, engine: AIOEngine = Depends(mongo_engine)):
    await engine.save(user)
    return user


@router.patch("/{id}", response_model=User)
async def update_user(id: ObjectId, patch: UserUpdate, engine: AIOEngine = Depends(mongo_engine)):
    user = await engine.find_one(User, User.id == id)
    if user is None:
        raise HTTPException(404)

    patch_dict = patch.dict(exclude_unset=True)
    for name, value in patch_dict.items():
        setattr(user, name, value)
    await engine.save(user)
    return user


@router.delete("/{id}")
async def delete_user(id: ObjectId, engine: AIOEngine = Depends(mongo_engine)):
    user = await engine.find_one(User, User.id == id)
    if user is None:
        raise HTTPException(404)
    await engine.delete(user)
    return user


