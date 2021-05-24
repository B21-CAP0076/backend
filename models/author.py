from abc import ABC
from typing import Optional

from odmantic import EmbeddedModel
from pydantic import BaseModel


# For get and put
class Author(EmbeddedModel, ABC):
    name: str


# For partial update
class AuthorUpdate(BaseModel):
    name: Optional[str]



