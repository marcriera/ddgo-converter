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
                    return self.gamepads[index.row()].id
                case 1:
                    return self.gamepads[index.row()].name
                case 2:
                    if self.gamepads[index.row()].type == Gamepad.GamepadType.UNKNOWN:
                        return "Not configured"
                    else:
                        return "Configured"
        elif role == Qt.TextAlignmentRole and index.column() != 1:
            return Qt.AlignCenter

    def rowCount(self, index):
        return len(self.gamepads)
    
    def columnCount(self, index):
        return len(headers)

    def headerData(self, section, orientation, role):
        if role != Qt.DisplayRole or orientation != Qt.Horizontal:
            return QVariant()
        return headers[section]
