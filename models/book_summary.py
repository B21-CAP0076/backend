from abc import ABC
from datetime import datetime
from typing import Optional

from odmantic import Model, Reference
from pydantic import BaseModel

from models.reading_commitment import ReadingCommitment


# For get and put
class BookSummary(Model, ABC):
    reading_commitment: ReadingCommitment = Reference()
    creation_date: datetime
    summary: str


# For partial update
class BookSummaryUpdate(BaseModel):
    reading_commitment: Optional[ReadingCommitment] = Reference()
    creation_date: Optional[datetime]
    summary: Optional[str]
