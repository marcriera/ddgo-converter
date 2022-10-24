from enum import IntEnum
from events.input import InputEvent
from evdev import ecodes, UInput, AbsInfo

class EmulatedGamepad:
    
    class GamepadType(IntEnum):
        PC2HANDLE = 0
        PS1 = 1
        N64 = 2
        SAT = 3

class PC2HandleGamepad(EmulatedGamepad):

    # Mapping
    # A: BTN_EAST
    # B: BTN_SOUTH
    # C: BTN_NORTH
    # D: BTN_WEST
    # SL: BTN_SELECT
    # ST: BTN_START
    # BRAKE: ABS_X
    # POWER: ABS_Y

    def __init__(self):
        self.type = self.GamepadType.PC2HANDLE
        self.capabilities = {
                            ecodes.EV_KEY : [ecodes.BTN_NORTH, ecodes.BTN_SOUTH, ecodes.BTN_EAST, ecodes.BTN_WEST, ecodes.BTN_SELECT, ecodes.BTN_START],
                            ecodes.EV_ABS : [(ecodes.ABS_X, AbsInfo(0x79, 0, 255, 0, 0, 0)), (ecodes.ABS_Y, AbsInfo(0x81, 0, 255, 0, 0, 0))]
        }
        self.brake_notches = (0x79, 0x8A, 0x94, 0x9A, 0xA2, 0xA8, 0xAF, 0xB2, 0xB5, 0xB9)
        self.power_notches = (0x81, 0x6D, 0x54, 0x3F, 0x21, 0x00)

    def start(self):
        self.ui = UInput(self.capabilities, vendor=0x0AE4, product=0x0003, name='Emulated DGOC-44U')

    def stop(self):
        self.ui.close()

    def write_input(self, event):
        match event.type:
            case (InputEvent.EventType.RELEASE_BUTTON | InputEvent.EventType.PRESS_BUTTON):
                match event.data:
                    case InputEvent.Button.BUTTON_A:
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_EAST, event.type)
                    case InputEvent.Button.BUTTON_B:
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_SOUTH, event.type)
                    case InputEvent.Button.BUTTON_C:
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_NORTH, event.type)
                    case InputEvent.Button.BUTTON_D:
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_WEST, event.type)
                    case InputEvent.Button.BUTTON_SELECT:
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_SELECT, event.type)
                    case InputEvent.Button.BUTTON_START:
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_START, event.type)
                    case InputEvent.Button.BUTTON_UP:
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_SELECT, event.type)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_WEST, event.type)
                    case InputEvent.Button.BUTTON_DOWN:
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_SELECT, event.type)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_SOUTH, event.type)
                    case InputEvent.Button.BUTTON_LEFT:
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_SELECT, event.type)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_EAST, event.type)
                    case InputEvent.Button.BUTTON_RIGHT:
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_SELECT, event.type)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_NORTH, event.type)
            case InputEvent.EventType.BRAKE_NOTCH:
                self.ui.write(ecodes.EV_ABS, ecodes.ABS_X, self.brake_notches[event.data])
            case InputEvent.EventType.POWER_NOTCH:
                self.ui.write(ecodes.EV_ABS, ecodes.ABS_Y, self.power_notches[event.data])
        self.ui.syn()

class PS1Gamepad(EmulatedGamepad):

    def __init__(self):
        self.type = self.GamepadType.PS1
        self.capabilities = {
                            ecodes.EV_KEY : [ecodes.BTN_NORTH, ecodes.BTN_SOUTH, ecodes.BTN_EAST, ecodes.BTN_WEST, ecodes.BTN_TL, ecodes.BTN_TR,
                                            ecodes.BTN_TL2, ecodes.BTN_TR2, ecodes.BTN_SELECT, ecodes.BTN_START, ecodes.BTN_THUMBL, ecodes.BTN_THUMBR,
                                            ecodes.BTN_MODE, ecodes.BTN_DPAD_UP, ecodes.BTN_DPAD_DOWN, ecodes.BTN_DPAD_LEFT, ecodes.BTN_DPAD_RIGHT],
                            ecodes.EV_ABS : [(ecodes.ABS_X, AbsInfo(128, 0, 255, 0, 0, 0)), (ecodes.ABS_Y, AbsInfo(128, 0, 255, 0, 0, 0)),
                                            (ecodes.ABS_RX, AbsInfo(128, 0, 255, 0, 0, 0)), (ecodes.ABS_RY, AbsInfo(128, 0, 255, 0, 0, 0))]
        }

    def start(self):
        self.ui = UInput(self.capabilities, vendor=0x54C, product=0x268, name='Sony PLAYSTATION(R)3 Controller')

    def stop(self):
        self.ui.close()

    def write_input(self, event):
        self.ui.write(ecodes.EV_KEY, ecodes.BTN_DPAD_UP, 0)
        self.ui.write(ecodes.EV_KEY, ecodes.BTN_DPAD_DOWN, 0)
        self.ui.write(ecodes.EV_KEY, ecodes.BTN_DPAD_UP, 1)
        self.ui.write(ecodes.EV_KEY, ecodes.BTN_DPAD_DOWN, 1)
        match event.type:
            case (InputEvent.EventType.RELEASE_BUTTON | InputEvent.EventType.PRESS_BUTTON):
                match event.data:
                    case InputEvent.Button.BUTTON_A:
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_WEST, event.type)
                    case InputEvent.Button.BUTTON_B:
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_SOUTH, event.type)
                    case InputEvent.Button.BUTTON_C:
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_EAST, event.type)
                    case InputEvent.Button.BUTTON_SELECT:
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_SELECT, event.type)
                    case InputEvent.Button.BUTTON_START:
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_START, event.type)
            case InputEvent.EventType.BRAKE_NOTCH:
                match event.data:
                    case 0:
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_TL, 0)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_TL2, 1)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_TR, 1)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_TR2, 1)
                    case 1:
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_TL, 1)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_TL2, 0)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_TR, 1)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_TR2, 1)
                    case 2:
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_TL, 0)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_TL2, 0)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_TR, 1)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_TR2, 1)
                    case 3:
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_TL, 1)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_TL2, 1)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_TR, 0)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_TR2, 1)
                    case 4:
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_TL, 0)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_TL2, 1)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_TR, 0)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_TR2, 1)
                    case 5:
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_TL, 1)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_TL2, 0)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_TR, 0)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_TR2, 1)
                    case 6:
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_TL, 0)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_TL2, 0)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_TR, 0)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_TR2, 1)
                    case 7:
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_TL, 1)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_TL2, 1)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_TR, 1)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_TR2, 0)
                    case 8:
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_TL, 0)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_TL2, 1)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_TR, 1)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_TR2, 0)
                    case 9:
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_TL, 0)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_TL2, 0)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_TR, 0)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_TR2, 0)
            case InputEvent.EventType.POWER_NOTCH:
                match event.data:
                    case 0:
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_NORTH, 0)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_DPAD_LEFT, 1)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_DPAD_RIGHT, 1)
                    case 1:
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_NORTH, 1)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_DPAD_LEFT, 0)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_DPAD_RIGHT, 1)
                    case 2:
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_NORTH, 0)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_DPAD_LEFT, 0)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_DPAD_RIGHT, 1)
                    case 3:
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_NORTH, 1)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_DPAD_LEFT, 1)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_DPAD_RIGHT, 0)
                    case 4:
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_NORTH, 0)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_DPAD_LEFT, 1)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_DPAD_RIGHT, 0)
                    case 5:
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_NORTH, 1)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_DPAD_LEFT, 0)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_DPAD_RIGHT, 0)
        self.ui.syn()

class N64Gamepad(EmulatedGamepad):

    def __init__(self):
        self.type = self.GamepadType.N64
        self.capabilities = {
                            ecodes.EV_KEY : [ecodes.BTN_NORTH, ecodes.BTN_SOUTH, ecodes.BTN_EAST, ecodes.BTN_WEST, ecodes.BTN_TL, ecodes.BTN_TR,
                                            ecodes.BTN_TL2, ecodes.BTN_TR2, ecodes.BTN_SELECT, ecodes.BTN_START, ecodes.BTN_THUMBL, ecodes.BTN_THUMBR,
                                            ecodes.BTN_MODE, ecodes.BTN_DPAD_UP, ecodes.BTN_DPAD_DOWN, ecodes.BTN_DPAD_LEFT, ecodes.BTN_DPAD_RIGHT],
                            ecodes.EV_ABS : [(ecodes.ABS_X, AbsInfo(128, 0, 255, 0, 0, 0)), (ecodes.ABS_Y, AbsInfo(128, 0, 255, 0, 0, 0)),
                                            (ecodes.ABS_RX, AbsInfo(128, 0, 255, 0, 0, 0)), (ecodes.ABS_RY, AbsInfo(128, 0, 255, 0, 0, 0))]
        }

    def start(self):
        self.ui = UInput(self.capabilities, vendor=0x54C, product=0x268, name='Sony PLAYSTATION(R)3 Controller')

    def stop(self):
        self.ui.close()

    def write_input(self, event):
        match event.type:
            case (InputEvent.EventType.RELEASE_BUTTON | InputEvent.EventType.PRESS_BUTTON):
                match event.data:
                    case InputEvent.Button.BUTTON_A:
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_WEST, event.type)
                    case InputEvent.Button.BUTTON_B:
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_SOUTH, event.type)
                    case InputEvent.Button.BUTTON_C:
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_SELECT, event.type)
                    case InputEvent.Button.BUTTON_SELECT:
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_TR2, event.type)
                    case InputEvent.Button.BUTTON_START:
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_START, event.type)
            case InputEvent.EventType.BRAKE_NOTCH:
                match event.data:
                    case 0:
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_TR, 0)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_TL, 1)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_EAST, 1)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_NORTH, 1)
                    case 1:
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_TR, 1)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_TL, 0)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_EAST, 1)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_NORTH, 1)
                    case 2:
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_TR, 0)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_TL, 0)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_EAST, 1)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_NORTH, 1)
                    case 3:
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_TR, 1)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_TL, 1)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_EAST, 0)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_NORTH, 1)
                    case 4:
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_TR, 0)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_TL, 1)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_EAST, 0)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_NORTH, 1)
                    case 5:
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_TR, 1)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_TL, 0)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_EAST, 0)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_NORTH, 1)
                    case 6:
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_TR, 0)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_TL, 0)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_EAST, 0)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_NORTH, 1)
                    case 7:
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_TR, 1)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_TL, 1)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_EAST, 1)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_NORTH, 0)
                    case 8:
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_TR, 0)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_TL, 1)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_EAST, 1)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_NORTH, 0)
                    case 9:
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_TR, 0)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_TL, 0)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_EAST, 0)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_NORTH, 0)
            case InputEvent.EventType.POWER_NOTCH:
                match event.data:
                    case 0:
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_DPAD_RIGHT, 0)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_DPAD_UP, 1)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_TL2, 1)
                    case 1:
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_DPAD_RIGHT, 1)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_DPAD_UP, 0)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_TL2, 1)
                    case 2:
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_DPAD_RIGHT, 0)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_DPAD_UP, 0)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_TL2, 1)
                    case 3:
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_DPAD_RIGHT, 1)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_DPAD_UP, 1)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_TL2, 0)
                    case 4:
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_DPAD_RIGHT, 0)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_DPAD_UP, 1)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_TL2, 0)
                    case 5:
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_DPAD_RIGHT, 1)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_DPAD_UP, 0)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_TL2, 0)
        self.ui.syn()

class SATGamepad(EmulatedGamepad):

    def __init__(self):
        self.type = self.GamepadType.SAT
        self.capabilities = {
                            ecodes.EV_KEY : [ecodes.BTN_NORTH, ecodes.BTN_SOUTH, ecodes.BTN_EAST, ecodes.BTN_WEST, ecodes.BTN_TL, ecodes.BTN_TR,
                                            ecodes.BTN_TL2, ecodes.BTN_TR2, ecodes.BTN_SELECT, ecodes.BTN_START, ecodes.BTN_THUMBL, ecodes.BTN_THUMBR,
                                            ecodes.BTN_MODE, ecodes.BTN_DPAD_UP, ecodes.BTN_DPAD_DOWN, ecodes.BTN_DPAD_LEFT, ecodes.BTN_DPAD_RIGHT],
                            ecodes.EV_ABS : [(ecodes.ABS_X, AbsInfo(128, 0, 255, 0, 0, 0)), (ecodes.ABS_Y, AbsInfo(128, 0, 255, 0, 0, 0)),
                                            (ecodes.ABS_RX, AbsInfo(128, 0, 255, 0, 0, 0)), (ecodes.ABS_RY, AbsInfo(128, 0, 255, 0, 0, 0))]
        }

    def start(self):
        self.ui = UInput(self.capabilities, vendor=0x54C, product=0x268, name='Sony PLAYSTATION(R)3 Controller')

    def stop(self):
        self.ui.close()

    def write_input(self, event):
        match event.type:
            case (InputEvent.EventType.RELEASE_BUTTON | InputEvent.EventType.PRESS_BUTTON):
                match event.data:
                    case InputEvent.Button.BUTTON_A:
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_SOUTH, event.type)
                    case InputEvent.Button.BUTTON_B:
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_EAST, event.type)
                    case InputEvent.Button.BUTTON_C:
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_TR, event.type)
                    case InputEvent.Button.BUTTON_START:
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_START, event.type)
            case InputEvent.EventType.BRAKE_NOTCH:
                match event.data:
                    case 0:
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_TL2, 0)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_TR2, 1)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_DPAD_DOWN, 1)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_DPAD_LEFT, 1)
                    case 1:
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_TL2, 1)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_TR2, 0)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_DPAD_DOWN, 1)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_DPAD_LEFT, 1)
                    case 2:
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_TL2, 0)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_TR2, 0)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_DPAD_DOWN, 1)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_DPAD_LEFT, 1)
                    case 3:
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_TL2, 1)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_TR2, 1)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_DPAD_DOWN, 0)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_DPAD_LEFT, 1)
                    case 4:
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_TL2, 0)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_TR2, 1)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_DPAD_DOWN, 0)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_DPAD_LEFT, 1)
                    case 5:
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_TL2, 1)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_TR2, 0)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_DPAD_DOWN, 0)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_DPAD_LEFT, 1)
                    case 6:
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_TL2, 0)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_TR2, 0)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_DPAD_DOWN, 0)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_DPAD_LEFT, 1)
                    case 7:
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_TL2, 1)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_TR2, 1)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_DPAD_DOWN, 1)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_DPAD_LEFT, 0)
                    case 8:
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_TL2, 0)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_TR2, 1)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_DPAD_DOWN, 1)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_DPAD_LEFT, 0)
                    case 9:
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_TL2, 0)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_TR2, 0)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_DPAD_DOWN, 0)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_DPAD_LEFT, 0)
            case InputEvent.EventType.POWER_NOTCH:
                match event.data:
                    case 0:
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_WEST, 0)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_NORTH, 1)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_TL, 1)
                    case 1:
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_WEST, 1)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_NORTH, 0)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_TL, 1)
                    case 2:
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_WEST, 0)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_NORTH, 0)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_TL, 1)
                    case 3:
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_WEST, 1)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_NORTH, 1)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_TL, 0)
                    case 4:
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_WEST, 0)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_NORTH, 1)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_TL, 0)
                    case 5:
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_WEST, 1)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_NORTH, 0)
                        self.ui.write(ecodes.EV_KEY, ecodes.BTN_TL, 0)
        self.ui.syn()