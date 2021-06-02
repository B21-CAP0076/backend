from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from odmantic import AIOEngine, ObjectId
from odmantic.query import QueryExpression

from db.mongodb import mongo_engine
from models.book import Book

router = APIRouter(
    tags=["book"],
    prefix="/book"
)


@router.get("/")
async def get_all(
        page: int = 1,
        title: Optional[str] = None,
        author: Optional[str] = None,
        genre: Optional[str] = None,
        engine: AIOEngine = Depends(mongo_engine)
):
    skip: int = 50 * (page - 1)

    queries = []
    if title:
        qe = QueryExpression({'title': {'$eq': title}})
        queries.append(qe)

    if author:
        qe = QueryExpression({'authors': {'$elemMatch': {'name': author}}})
        queries.append(qe)

    if genre:
        qe = QueryExpression({'genres': {'$elemMatch': {'name': genre}}})
        queries.append(qe)

    books = await engine.find(Book, *queries, skip=skip, limit=50)

    return books


@router.get("/{id}")
async def get(id: ObjectId, engine: AIOEngine = Depends(mongo_engine)):
    book = await engine.find_one(Book, Book.id == id)
    if book is None:
        raise HTTPException(404)
    return book
