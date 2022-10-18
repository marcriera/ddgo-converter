from enum import IntEnum
from events.input import InputEvent

class EmulatedGamepad:
    
    class GamepadType(IntEnum):
        PC2HANDLE = 0
        PS1 = 1

class PC2HandleGamepad(EmulatedGamepad):

    def __init__(self):
        self.type = self.GamepadType.PC2HANDLE

    def write_input(self, event: InputEvent):
        print(str(event.type) + ": " + str(event.data))

