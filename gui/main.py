import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem
from gui.main_ui import Ui_MainWindow
from handlers.gamepad import Gamepad
from models.gamepad import GamepadModel

class MainWindow(QMainWindow):
    def __init__(self, gamepad_handler):
        super().__init__()

        self._gamepad_handler = gamepad_handler
        self._gui = Ui_MainWindow()
        self._gui.setupUi(self)

        model = GamepadModel(gamepad_handler.find_gamepads())
        self._gui.tableView_physicalControllerList.setModel(model)

        self._gui.tableView_physicalControllerList.resizeColumnsToContents()

        self._gui.pushButton_physicalControllerRefresh.clicked.connect(self.controller_list_refresh)

    def controller_list_refresh(self):
        return
