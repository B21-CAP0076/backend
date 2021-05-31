from abc import ABC
from typing import List, Optional


from odmantic import Model
from pydantic import BaseModel

from models.author import Author
from models.genre import Genre


# For get and put
class Book(Model, ABC):
    img: str
    title: str
    authors: List[Author]
    genres: List[Genre]


# For partial update
# class BookUpdate(BaseModel):
#     img: Optional[str]
#     title: Optional[str]
#     authors: Optional[List[Author]]
#     genres: Optional[List[Book]]
