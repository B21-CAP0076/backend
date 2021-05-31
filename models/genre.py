from abc import ABC
from typing import Optional

from odmantic import Model
from pydantic import BaseModel


# For get and put
class Genre(Model, ABC):
    name: str


# # For partial update
# class GenreUpdate(BaseModel):
#     name: Optional[str]
