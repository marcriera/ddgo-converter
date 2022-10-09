import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
from gui.main_ui import Ui_MainWindow

class MainWindow(QMainWindow):
    def __init__(self, main_controller):
        super().__init__()

        self._main_controller = main_controller
        self._gui = Ui_MainWindow()
        self._gui.setupUi(self)

        self._gui.pushButton_emulatedControllerStart.clicked.connect(self.startPressed)

    def startPressed(self):
        self._gui.statusbar.showMessage("Hello!")
