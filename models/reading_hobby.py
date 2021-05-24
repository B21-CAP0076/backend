from abc import ABC
from typing import Optional, List

from bson import ObjectId
from odmantic import EmbeddedModel
from pydantic import BaseModel


# For get and put
class ReadingHobby(EmbeddedModel, ABC):
    previous_books: Optional[List[ObjectId]] = None
    genre_preferences: Optional[List[ObjectId]] = None


# For partial update
class ReadingHobbyUpdate(BaseModel):
    previous_books: Optional[List[ObjectId]]
    genre_preferences: Optional[List[ObjectId]]
