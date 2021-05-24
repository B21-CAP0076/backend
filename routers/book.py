from typing import List

from fastapi import APIRouter, Depends, HTTPException
from odmantic import AIOEngine, ObjectId

from db.mongodb import mongo_engine
from models.book import Book, BookUpdate

router = APIRouter(
    tags=["book"],
    prefix="/user"
)


@router.get("/")
async def get_all_books(engine: AIOEngine = Depends(mongo_engine)):
    books = await engine.find(Book)
    return books


@router.get("/{id}")
async def get_book(id: ObjectId, engine: AIOEngine = Depends(mongo_engine)):
    book = await engine.find_one(Book, Book.id == id)
    if book is None:
        raise HTTPException(404)
    return book


@router.put("/create_all", response_model=List[Book])
async def create_all_books(books: List[Book], engine: AIOEngine = Depends(mongo_engine)):
    await engine.save_all(books)
    return books


@router.put("/", response_model=Book)
async def create_book(book: Book, engine: AIOEngine = Depends(mongo_engine)):
    await engine.save(book)
    return book


@router.patch("/{id}", response_model=Book)
async def update_book(id: ObjectId, patch: BookUpdate, engine: AIOEngine = Depends(mongo_engine)):
    book = await engine.find_one(Book, Book.id == id)
    if book is None:
        raise HTTPException(404)

    patch_dict = patch.dict(exclude_unset=True)
    for name, value in patch_dict.items():
        setattr(book, name, value)
    await engine.save(book)
    return book


@router.delete("/{id}")
async def delete_book(id: ObjectId, engine: AIOEngine = Depends(mongo_engine)):
    book = await engine.find_one(Book, Book.id == id)
    if book is None:
        raise HTTPException(404)
    await engine.delete(book)
    return book
