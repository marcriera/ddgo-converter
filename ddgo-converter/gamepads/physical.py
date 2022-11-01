from enum import IntEnum
import evdev
from hashlib import sha1
from events.input import InputEvent
from select import select

def create_gamepad(vid, pid, name):
    match vid, pid:
        case (0x0f0d, 0x00c1) | (0x33dd, 0x0002):
            return SwitchGamepad(vid, pid, name)
    return PhysicalGamepad(vid, pid, name)

class PhysicalGamepad:

    class GamepadType(IntEnum):
        UNKNOWN = 0
        CLASSIC = 1
        SWITCH = 2

    def __init__(self, vid, pid, name):
        super().__init__()
        self.vid = vid
        self.pid = pid
        self.name = name
        self.id = self._get_gamepad_id()
        self.hash = self._get_gamepad_hash()
        self.type = self.GamepadType.UNKNOWN
        self.config = []

    def _get_gamepad_id(self):
        vid = format(self.vid, "x").zfill(4)
        pid = format(self.pid, "x").zfill(4)
        id = str(vid + ":" + pid)
        return id

    def _get_gamepad_hash(self):
        hash = sha1(str(self.id + ":" + self.name).encode('utf-8')).hexdigest()
        return hash

    def _get_device(self):
        for device in [evdev.InputDevice(path) for path in evdev.list_devices()]:
            dev_name = [device.info.vendor, device.info.product, device.name]  
            if dev_name == [self.vid, self.pid, self.name]:
                return device

class SwitchGamepad(PhysicalGamepad):

    def __init__(self, * args):
        super().__init__(* args)
        self.type = self.GamepadType.SWITCH
        self.config = []
        self.device = self._get_device()

    def start(self):
        try:
            self.device.grab()
        except:
            return

    def stop(self):
        try:
            self.device.ungrab()
        except:
            return

    def read_input(self):
        # time.sleep(5)
        # print("Read from ZKNS-001 correct")
        # return InputEvent(InputEvent.EventType.PRESS_BUTTON, InputEvent.Button.BUTTON_A)
        select([self.device], [], [], 5)
        try:
            event = self.device.read_one()
            input_events = []
            if event is not None:
                if event.type == evdev.ecodes.EV_KEY:
                    match event.code:
                        case 304: # Y
                            input_events.append(InputEvent(InputEvent.EventType(event.value), InputEvent.Button.BUTTON_A))
                        case 305: # B
                            input_events.append(InputEvent(InputEvent.EventType(event.value), InputEvent.Button.BUTTON_B))
                        case 306: # A
                            input_events.append(InputEvent(InputEvent.EventType(event.value), InputEvent.Button.BUTTON_C))
                        case 307: # X
                            input_events.append(InputEvent(InputEvent.EventType(event.value), InputEvent.Button.BUTTON_D))
                        case 312: # MINUS
                            input_events.append(InputEvent(InputEvent.EventType(event.value), InputEvent.Button.BUTTON_SELECT))
                        case 313: # PLUS
                            input_events.append(InputEvent(InputEvent.EventType(event.value), InputEvent.Button.BUTTON_START))
                if event.type == evdev.ecodes.EV_ABS and event.code == evdev.ecodes.ABS_HAT0X:
                    match event.value:
                        case -1: # LEFT
                            input_events.append(InputEvent(InputEvent.EventType.RELEASE_BUTTON, InputEvent.Button.BUTTON_RIGHT))
                            input_events.append(InputEvent(InputEvent.EventType.PRESS_BUTTON, InputEvent.Button.BUTTON_LEFT))
                        case 1: # RIGHT
                            input_events.append(InputEvent(InputEvent.EventType.RELEASE_BUTTON, InputEvent.Button.BUTTON_LEFT))
                            input_events.append(InputEvent(InputEvent.EventType.PRESS_BUTTON, InputEvent.Button.BUTTON_RIGHT))
                        case _: # NONE
                            input_events.append(InputEvent(InputEvent.EventType.RELEASE_BUTTON, InputEvent.Button.BUTTON_LEFT))
                            input_events.append(InputEvent(InputEvent.EventType.RELEASE_BUTTON, InputEvent.Button.BUTTON_RIGHT))
                if event.type == evdev.ecodes.EV_ABS and event.code == evdev.ecodes.ABS_HAT0Y:
                    match event.value:
                        case -1: # UP
                            input_events.append(InputEvent(InputEvent.EventType.RELEASE_BUTTON, InputEvent.Button.BUTTON_DOWN))
                            input_events.append(InputEvent(InputEvent.EventType.PRESS_BUTTON, InputEvent.Button.BUTTON_UP))
                        case 1: # DOWN
                            input_events.append(InputEvent(InputEvent.EventType.RELEASE_BUTTON, InputEvent.Button.BUTTON_UP))
                            input_events.append(InputEvent(InputEvent.EventType.PRESS_BUTTON, InputEvent.Button.BUTTON_DOWN))
                        case _: # NONE
                            input_events.append(InputEvent(InputEvent.EventType.RELEASE_BUTTON, InputEvent.Button.BUTTON_UP))
                            input_events.append(InputEvent(InputEvent.EventType.RELEASE_BUTTON, InputEvent.Button.BUTTON_DOWN))
                if event.type == evdev.ecodes.EV_ABS and event.code == evdev.ecodes.ABS_Y:
                    match event.value:
                        case 0x0: # EMG
                            input_events.append(InputEvent(InputEvent.EventType.BRAKE_NOTCH, 9))
                            input_events.append(InputEvent(InputEvent.EventType.POWER_NOTCH, 0))
                        case 0x5:
                            input_events.append(InputEvent(InputEvent.EventType.BRAKE_NOTCH, 8))
                            input_events.append(InputEvent(InputEvent.EventType.POWER_NOTCH, 0))
                        case 0x13:
                            input_events.append(InputEvent(InputEvent.EventType.BRAKE_NOTCH, 7))
                            input_events.append(InputEvent(InputEvent.EventType.POWER_NOTCH, 0))
                        case 0x20:
                            input_events.append(InputEvent(InputEvent.EventType.BRAKE_NOTCH, 6))
                            input_events.append(InputEvent(InputEvent.EventType.POWER_NOTCH, 0))
                        case 0x2E:
                            input_events.append(InputEvent(InputEvent.EventType.BRAKE_NOTCH, 5))
                            input_events.append(InputEvent(InputEvent.EventType.POWER_NOTCH, 0))
                        case 0x3C:
                            input_events.append(InputEvent(InputEvent.EventType.BRAKE_NOTCH, 4))
                            input_events.append(InputEvent(InputEvent.EventType.POWER_NOTCH, 0))
                        case 0x49:
                            input_events.append(InputEvent(InputEvent.EventType.BRAKE_NOTCH, 3))
                            input_events.append(InputEvent(InputEvent.EventType.POWER_NOTCH, 0))
                        case 0x57:
                            input_events.append(InputEvent(InputEvent.EventType.BRAKE_NOTCH, 2))
                            input_events.append(InputEvent(InputEvent.EventType.POWER_NOTCH, 0))
                        case 0x65:
                            input_events.append(InputEvent(InputEvent.EventType.BRAKE_NOTCH, 1))
                            input_events.append(InputEvent(InputEvent.EventType.POWER_NOTCH, 0))
                        case 0x80: # N
                            input_events.append(InputEvent(InputEvent.EventType.BRAKE_NOTCH, 0))
                            input_events.append(InputEvent(InputEvent.EventType.POWER_NOTCH, 0))
                        case 0x9F:
                            input_events.append(InputEvent(InputEvent.EventType.BRAKE_NOTCH, 0))
                            input_events.append(InputEvent(InputEvent.EventType.POWER_NOTCH, 1))
                        case 0xB7:
                            input_events.append(InputEvent(InputEvent.EventType.BRAKE_NOTCH, 0))
                            input_events.append(InputEvent(InputEvent.EventType.POWER_NOTCH, 2))
                        case 0xCE:
                            input_events.append(InputEvent(InputEvent.EventType.BRAKE_NOTCH, 0))
                            input_events.append(InputEvent(InputEvent.EventType.POWER_NOTCH, 3))
                        case 0xE6:
                            input_events.append(InputEvent(InputEvent.EventType.BRAKE_NOTCH, 0))
                            input_events.append(InputEvent(InputEvent.EventType.POWER_NOTCH, 4))
                        case 0xFF: # P5
                            input_events.append(InputEvent(InputEvent.EventType.BRAKE_NOTCH, 0))
                            input_events.append(InputEvent(InputEvent.EventType.POWER_NOTCH, 5))
                return input_events
        except OSError:
            return [InputEvent(InputEvent.EventType.ERROR, None)]
