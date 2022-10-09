import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem
from gui.main_ui import Ui_MainWindow
from handlers.gamepad import Gamepad

class MainWindow(QMainWindow):
    def __init__(self, gamepad_handler):
        super().__init__()

        self._gamepad_handler = gamepad_handler
        self._gui = Ui_MainWindow()
        self._gui.setupUi(self)

        self._gui.pushButton_physicalControllerRefresh.clicked.connect(self.controller_list_refresh)

    def controller_list_refresh(self):
        self._gui.tableWidget_physicalControllerList.setRowCount(0)
        for gamepad in self._gamepad_handler.find_gamepads():
            rowCount = self._gui.tableWidget_physicalControllerList.rowCount()
            self._gui.tableWidget_physicalControllerList.insertRow(rowCount)
            self._gui.tableWidget_physicalControllerList.setItem(rowCount , 1, QTableWidgetItem(gamepad.name))