from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from odmantic import AIOEngine, ObjectId
from odmantic.query import QueryExpression

from google.oauth2 import id_token
from google.auth.transport import requests

from config import settings
from db.mongodb import mongo_engine
from models.user import User, UserUpdate

router = APIRouter(
    tags=["user"],
    prefix="/user"
)


@router.post("/gauth")
async def gauth(token: str, engine: AIOEngine = Depends(mongo_engine)):
    try:
        id_info = id_token.verify_oauth2_token(token, requests.Request(), settings.CLIENT_ID)
        user_id = id_info["sub"]

        user = await engine.find_one(User, User.g_id == user_id)
        if user is None:
            username = id_info["name"]
            email = id_info["email"]
            img = id_info["picture"]

            new_user = User(
                g_id=user_id,
                img=img,
                username=username,
                email=email
            )
            await engine.save(new_user)
            return new_user

        # old user
        else:
            return user

    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unable to validate Google login")


@router.get("/")
async def get_all(
        page: int = 1,
        reading_cluster: Optional[int] = None,
        engine: AIOEngine = Depends(mongo_engine)
):
    skip: int = 50 * (page - 1)

    queries = []

    if reading_cluster:
        qe = QueryExpression({'reading_cluster': {'$eq': reading_cluster}})
        queries.append(qe)

    users = await engine.find(User, *queries, skip=skip, limit=50)
    return users


@router.get("/{id}")
async def get(id: ObjectId, engine: AIOEngine = Depends(mongo_engine)):
    user = await engine.find_one(User, User.id == id)
    if user is None:
        raise HTTPException(404)
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