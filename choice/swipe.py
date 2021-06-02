import enum


class SwipeState(str, enum.Enum):
    RIGHT = "right"
    LEFT = "left"


class SwipeStatus(str, enum.Enum):
    RIGHT_SWIPED = "right_swiped"
    LEFT_SWIPED = "left_swiped"
