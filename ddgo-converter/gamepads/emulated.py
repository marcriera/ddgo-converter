from enum import Enum
from hashlib import sha1

class EmulatedGamepad:
    
    class GamepadType(Enum):
        DGOC44U = 0
        PS1 = 1

    def __init__(self):
        super().__init__()
        self.type
