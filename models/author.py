from abc import ABC

from odmantic import Model


# For get and put
class Author(Model, ABC):
    name: str
