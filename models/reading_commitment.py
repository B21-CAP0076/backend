from abc import ABC
from typing import Optional
from datetime import datetime

from odmantic import Model, Reference
from pydantic import BaseModel

from models.user import User
from models.book import Book
from models.reading_hobby import ReadingHobby


# For get and put
class ReadingCommitment(Model, ABC):
    reading_hobby: ReadingHobby = Reference()
    partner: Optional[User] = None
    creation_date: datetime
    completion_date: datetime
    book: Book


# For partial update
class ReadingCommitmentUpdate(BaseModel):
    reading_hobby: Optional[ReadingHobby] = Reference()
    partner: Optional[User]
    creation_date: Optional[datetime]
    completion_date: Optional[datetime]
    book: Optional[Book]
