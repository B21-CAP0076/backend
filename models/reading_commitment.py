from abc import ABC
from typing import Optional
from datetime import datetime
from bson import ObjectId

from odmantic import Model, Reference
from pydantic import BaseModel

from models.user import User
from models.book import Book


class ReadingCommitment(Model, ABC):
    owner: User = Reference()
    partner: Optional[User] = None
    creation_date: datetime
    end_date: datetime
    book: Book = Reference()


class ReadingCommitmentUpdate(BaseModel):
    partner: Optional[User]
    creation_date: Optional[datetime]
    end_date: Optional[datetime]
    book: Optional[Book]
