from enum import Enum
from hashlib import sha1
import time

def create_gamepad(vid, pid, name):
    match vid, pid:
        case 0x0f0d, 0x00c1:
            return SwitchGamepad(vid, pid, name)
    return PhysicalGamepad(vid, pid, name)

class PhysicalGamepad:

    class GamepadType(Enum):
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

class SwitchGamepad(PhysicalGamepad):

    def __init__(self, * args):
        super().__init__(* args)
        self.type = self.GamepadType.SWITCH
        self.config = []

    def read_input(self):
        time.sleep(5)
        print("Read from ZKNS-001 correct")
        return 0
