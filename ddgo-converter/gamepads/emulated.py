from enum import Enum
from hashlib import sha1

class EmulatedGamepad:
    
    class GamepadType(Enum):
        PC2HANDLE = 0
        PS1 = 1

class PC2HandleGamepad(EmulatedGamepad):

    def __init__(self):
        self.type = self.GamepadType.PC2HANDLE

    def write_input(self):
        print("Output to emulated DGOC-44U correct")
        return 0

