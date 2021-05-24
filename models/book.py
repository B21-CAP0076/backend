from abc import ABC
from typing import List, Optional

from bson import ObjectId
from odmantic import Model
from pydantic import BaseModel


# For get and put
class Book(Model, ABC):
    img: str
    title: str
    author_ids: List[ObjectId]
    genre_ids: List[ObjectId]
    rating: float


# For partial update
class BookUpdate(BaseModel):
    img: Optional[str]
    title: Optional[str]
    author_ids: Optional[List[ObjectId]]
    genre_ids: Optional[List[ObjectId]]
    rating: Optional[float]
