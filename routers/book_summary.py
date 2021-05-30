from fastapi import APIRouter, Depends, HTTPException
from odmantic import AIOEngine, ObjectId

from db.mongodb import mongo_engine
from models.book_summary import BookSummary, BookSummaryUpdate

router = APIRouter(
    tags=["book_summary"],
    prefix="/book_summary"
)


@router.get("/")
async def get_all(page: int = 1, engine: AIOEngine = Depends(mongo_engine)):
    skip: int = 20 * (page - 1)
    book_summaries = await engine.find(BookSummary, skip=skip, limit=20)
    return book_summaries


@router.get("/{id}")
async def get(id: ObjectId, engine: AIOEngine = Depends(mongo_engine)):
    book_summary = await engine.find_one(BookSummary, BookSummary.id == id)
    if book_summary is None:
        raise HTTPException(404)
    return book_summary


@router.put("/", response_model=BookSummary)
async def create(book_summary: BookSummary, engine: AIOEngine = Depends(mongo_engine)):
    await engine.save(book_summary)
    return book_summary


@router.patch("/{id}", response_model=BookSummary)
async def update(id: ObjectId, patch: BookSummaryUpdate, engine: AIOEngine = Depends(mongo_engine)):
    book_summary = await engine.find_one(BookSummary, BookSummary.id == id)
    if book_summary is None:
        raise HTTPException(404)

    patch_dict = patch.dict(exclude_unset=True)
    for name, value in patch_dict.items():
        setattr(book_summary, name, value)
    await engine.save(book_summary)
    return book_summary


@router.delete("/{id}")
async def delete(id: ObjectId, engine: AIOEngine = Depends(mongo_engine)):
    book_summary = await engine.find_one(BookSummary, BookSummary.id == id)
    if book_summary is None:
        raise HTTPException(404)
    await engine.delete(book_summary)
    return book_summary
