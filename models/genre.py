from abc import ABC

from odmantic import Model


# For get and put
class Genre(Model, ABC):
    name: str
