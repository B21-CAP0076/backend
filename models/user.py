from abc import ABC
from datetime import datetime
from typing import List, Optional

from bson import ObjectId
from odmantic import Model
from pydantic import BaseModel, EmailStr

from choice.education import EducationChoice
from models.hobby import Hobby
from models.book import Book
from models.genre import Genre


# For get and put
class User(Model, ABC):
    g_id: str
    img: str
    username: str
    email: EmailStr
    birthdate: Optional[datetime]
    education: Optional[EducationChoice] = None
    hobbies: Optional[List[Hobby]] = None
    previous_books: Optional[List[Book]] = None
    genre_preferences: Optional[List[Genre]] = None
    reading_cluster: Optional[int] = None


# For partial update
class UserUpdate(BaseModel):
    birthdate: Optional[datetime]
    education: Optional[EducationChoice]
    hobbies: Optional[List[Hobby]]
    previous_books: Optional[List[Book]]
    genre_preferences: Optional[List[Genre]]
    reading_clusters: Optional[int]
