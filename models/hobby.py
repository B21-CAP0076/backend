from abc import ABC

from odmantic import Model


# For get and put
class Hobby(Model, ABC):
    name: str
