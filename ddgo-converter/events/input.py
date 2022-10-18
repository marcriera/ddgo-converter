from enum import IntEnum

class InputEvent:
    
    class EventType(IntEnum):
        RELEASE_BUTTON = 0
        PRESS_BUTTON = 1
        BRAKE_NOTCH = 2
        POWER_NOTCH = 3
        ERROR = 4

    class Button(IntEnum):
        BUTTON_SELECT = 0
        BUTTON_START = 1
        BUTTON_A = 2
        BUTTON_B = 3
        BUTTON_C = 4
        BUTTON_D = 5
        BUTTON_UP = 6
        BUTTON_DOWN = 7
        BUTTON_LEFT = 8
        BUTTON_RIGHT = 9
        BUTTON_LDOOR = 10
        BUTTON_RDOOR = 11


    def __init__(self, type, data):
        self.type = type
        self.data = data