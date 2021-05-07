from functools import lru_cache
from typing import Optional

from fastapi import FastAPI

import settings

app = FastAPI()

@lru_cache
def get_settings():
    return settings.Settings

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}