from abc import ABC
from typing import Optional
from datetime import datetime

from odmantic import Model, Reference
from pydantic import BaseModel

from models.reading_commitment import ReadingCommitment


# For get and put
class BookSummary(Model, ABC):
    reading_commitment: ReadingCommitment = Reference()
    creation_date: datetime
    summary: str


class BookSummaryCreate(BaseModel):
    summary: str


# For partial update
class BookSummaryUpdate(BaseModel):
    summary: Optional[str]
