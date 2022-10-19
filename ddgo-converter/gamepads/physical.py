from enum import IntEnum
import evdev
from hashlib import sha1
from events.input import InputEvent
from select import select

def create_gamepad(vid, pid, name):
    match vid, pid:
        case 0x0f0d, 0x00c1:
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
                return input_events
        except OSError:
            return [InputEvent(InputEvent.EventType.ERROR, None)]
