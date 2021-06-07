import enum


class MatchStatus(str, enum.Enum):
    MATCH = "match"
    PENDING = "pending"
    REJECTED = "rejected"


class MatchAction(str, enum.Enum):
    SWIPE_RIGHT = "swipe_right"
    SWIPE_LEFT = "swipe_left"
