import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QHeaderView
from gui.main_ui import Ui_MainWindow
from handlers.gamepad import Gamepad
from models.gamepad import GamepadModel

class MainWindow(QMainWindow):
    def __init__(self, gamepad_handler, config_handler):
        super().__init__()

        self._gamepad_handler = gamepad_handler
        self._config_handler = config_handler
        self._gui = Ui_MainWindow()
        self._gui.setupUi(self)

        self.gamepad_model = GamepadModel(self._gamepad_handler.find_gamepads())
        self._gui.tableView_physicalControllerList.setModel(self.gamepad_model)
        self._gui.tableView_physicalControllerList.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self._gui.tableView_physicalControllerList.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self._gui.tableView_physicalControllerList.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)

        self._gui.pushButton_physicalControllerRefresh.clicked.connect(self.controller_list_refresh)
        self._gui.pushButton_physicalControllerConfig.clicked.connect(self.save)

    def controller_list_refresh(self):
        self.gamepad_model.beginResetModel()
        self.gamepad_model.gamepads = self._gamepad_handler.find_gamepads()
        self.gamepad_model.endResetModel()

    def save(self):
        self._config_handler.save()