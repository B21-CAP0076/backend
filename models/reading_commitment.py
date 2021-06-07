from abc import ABC
from typing import Optional
from datetime import datetime

from odmantic import Model, Reference
from pydantic import BaseModel

from choice.reading_commitment import ReadingCommitmentStatus
from models.user import User
from models.book import Book


class ReadingCommitment(Model, ABC):
    owner: User = Reference()
    owner_reading_cluster: Optional[int] = None
    creation_date: datetime = datetime.utcnow()
    end_date: datetime
    book: Book = Reference()
    status: ReadingCommitmentStatus = ReadingCommitmentStatus.OPEN


class ReadingCommitmentCreate(BaseModel):
    end_date: datetime
    book: Book
