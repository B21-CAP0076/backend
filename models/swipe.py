from abc import ABC

from odmantic import Model, Reference

from models.reading_commitment import ReadingCommitment
from choice.swipe import SwipeStatus


class Swipe(Model, ABC):
    commitment_1: ReadingCommitment = Reference()
    commitment_2: ReadingCommitment = Reference()
    status: SwipeStatus
