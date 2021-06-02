from abc import ABC
from typing import List

from odmantic import Model

from models.author import Author
from models.genre import Genre


# For get and put
class Book(Model, ABC):
    img: str
    title: str
    authors: List[Author]
    genres: List[Genre]