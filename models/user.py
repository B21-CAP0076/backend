from abc import ABC
from typing import List, Optional

from bson import ObjectId
from odmantic import Model
from pydantic import BaseModel, EmailStr

from choice.education import EducationChoice


# For get and put
class User(Model, ABC):
    username: str
    email: EmailStr
    education: EducationChoice
    hobby_ids: Optional[List[ObjectId]] = None
    previous_books_ids: Optional[List[ObjectId]] = None
    genre_preferences_ids: Optional[List[ObjectId]] = None
    reading_clusters: Optional[int] = None


# For partial update
class UserUpdate(BaseModel):
    username: Optional[str]
    email: Optional[EmailStr]
    education: Optional[EducationChoice]
    hobby_ids: Optional[List[ObjectId]]
    previous_books_ids: Optional[List[ObjectId]]
    genre_preferences_ids: Optional[List[ObjectId]]
    reading_clusters: Optional[int]
