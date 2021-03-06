from abc import ABC
from typing import List, Optional

from odmantic import Model
from pydantic import BaseModel, EmailStr

from choice.education import EducationChoice
from models.book import Book
from models.genre import Genre
from models.hobby import Hobby


# For get and put
class User(Model, ABC):
    email: EmailStr
    picture: str
    name: str
    age: Optional[int] = None
    education: Optional[EducationChoice] = None
    hobbies: Optional[List[Hobby]] = None
    previous_books: Optional[List[Book]] = None
    genre_preferences: Optional[List[Genre]] = None
    reading_cluster: Optional[int] = None


# For partial update
class UserUpdate(BaseModel):
    age: Optional[int]
    education: Optional[EducationChoice]
    hobbies: Optional[List[Hobby]]
    previous_books: Optional[List[Book]]
    genre_preferences: Optional[List[Genre]]
    reading_cluster: Optional[int]
