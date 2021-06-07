import enum


class ReadingCommitmentStatus(str, enum.Enum):
    OPEN = "open"
    CLOSED = "closed"
