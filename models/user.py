from datetime import datetime

from abc import ABC
from typing import List, Optional

from bson import ObjectId
from odmantic import Model
from pydantic import BaseModel, EmailStr

from choice.education import EducationChoice
from models.reading_hobby import ReadingHobby


# For get and put
class User(Model, ABC):
    username: str
    email: EmailStr
    birth_date: datetime
    education: EducationChoice

    hobby_ids: Optional[List[ObjectId]] = None
    reading_hobby: Optional[ReadingHobby] = None


# For partial update
class UserUpdate(BaseModel):
    username: Optional[str]
    email: Optional[EmailStr]
    birth_date: Optional[datetime]
    education: Optional[EducationChoice]

    hobby_ids: Optional[List[ObjectId]]
    reading_hobby: Optional[ReadingHobby]
