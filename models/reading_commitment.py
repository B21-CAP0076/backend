from abc import ABC
from typing import Optional
from datetime import datetime

from odmantic import Model, Reference
from pydantic import BaseModel

from models.user import User
from models.book import Book


class ReadingCommitment(Model, ABC):
    owner: User = Reference()
    partner: Optional[User] = None
    creation_date: datetime
    end_date: datetime
    owner_reading_cluster: Optional[int] = None
    book: Book = Reference()


class ReadingCommitmentCreate(BaseModel):
    end_date: datetime
    book: Book
