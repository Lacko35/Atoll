from enum import Enum

class eTile(Enum):
    Invalid = -1,
    Playable = 0,
    Player1 = 1,
    Player2 = 2,
    Connected = 3,