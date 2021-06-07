from abc import ABC

from odmantic import Model, Reference

from choice.match import MatchStatus
from models.reading_commitment import ReadingCommitment


class Match(Model, ABC):
    commitment_1: ReadingCommitment = Reference()
    commitment_2: ReadingCommitment = Reference()
    status: MatchStatus
