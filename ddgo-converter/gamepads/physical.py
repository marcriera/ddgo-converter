from enum import Enum
from hashlib import sha1

class PhysicalGamepad:

    class GamepadType(Enum):
        UNKNOWN = 0
        CLASSIC = 1
        NSWITCH = 2

    def __init__(self, vid, pid, name):
        super().__init__()
        self.vid = vid
        self.pid = pid
        self.name = name
        self.id = self._get_gamepad_id()
        self.hash = self._get_gamepad_hash()
        self.type = self.get_gamepad_type()
        self.config = []

    def _get_gamepad_id(self):
        vid = format(self.vid, "x").zfill(4)
        pid = format(self.pid, "x").zfill(4)
        id = str(vid + ":" + pid)
        return id

    def _get_gamepad_hash(self):
        hash = sha1(str(self.id + ":" + self.name).encode('utf-8')).hexdigest()
        return hash

    def get_gamepad_type(self):
        match self.vid, self.pid:
            case 0x0f0d, 0x00c1:
                return self.GamepadType.NSWITCH
        return self.GamepadType.UNKNOWN
