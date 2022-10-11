from hashlib import sha1
from PyQt5.QtCore import Qt, QVariant, QAbstractTableModel
from handlers.gamepad import Gamepad

headers = ["ID", "Name", "Status"]

class GamepadModel(QAbstractTableModel):
    def __init__(self, gamepads=None):
        super(GamepadModel, self).__init__()
        self.gamepads = gamepads or []

    def data(self, index, role):
        if role == Qt.DisplayRole:
            match index.column():
                case 0:
                    return self.get_gamepad_id(index)
                case 1:
                    return self.gamepads[index.row()].name
                case 2:
                    return self.get_gamepad_hash(index)
                case _:
                    return None

    def rowCount(self, index):
        return len(self.gamepads)
    
    def columnCount(self, index):
        return len(headers)

    def headerData(self, section, orientation, role):
        if role != Qt.DisplayRole or orientation != Qt.Horizontal:
            return QVariant()
        return headers[section]

    def get_gamepad_id(self, index):
        vid = format(self.gamepads[index.row()].vid, "x").zfill(4)
        pid = format(self.gamepads[index.row()].pid, "x").zfill(4)
        id = str(vid + ":" + pid)
        return id

    def get_gamepad_hash(self, index):
        id = self.get_gamepad_id(index)
        name = self.gamepads[index.row()].name
        hash = sha1(str(id + ":" + name).encode('utf-8')).hexdigest()
        return hash
