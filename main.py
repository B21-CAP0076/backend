from fastapi import FastAPI

from routers.user import router as user_router
from routers.hobby import router as hobby_router
from routers.book import router as book_router
from routers.genre import router as genre_router
from routers.reading_commitment import router as reading_commitment_router
from routers.swipe import router as swipe_router
from routers.book_summary import router as book_summary_router


app = FastAPI()

app.include_router(user_router)
app.include_router(hobby_router)
app.include_router(book_router)
app.include_router(genre_router)
app.include_router(reading_commitment_router)
app.include_router(swipe_router)
app.include_router(book_summary_router)

