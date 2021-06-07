from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from odmantic import AIOEngine, ObjectId
from odmantic.query import QueryExpression

from db.mongodb import mongo_engine
from models.book import Book

router = APIRouter(
    tags=["book"],
    prefix="/book"
)


@router.get("/")
async def get_all(page: int = 1, title: Optional[str] = None, engine: AIOEngine = Depends(mongo_engine)):
    skip: int = 50 * (page - 1)

    queries = []
    if title:
        qe = QueryExpression({'title': {'$regex': title, '$options': 'i'}})
        queries.append(qe)

    books = await engine.find(Book, *queries, skip=skip, limit=50)

    return books


@router.get("/{id}")
async def get(id: ObjectId, engine: AIOEngine = Depends(mongo_engine)):
    book = await engine.find_one(Book, Book.id == id)
    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return book
