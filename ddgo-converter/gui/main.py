import sys
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QHeaderView
import threading
from gui.main_ui import Ui_MainWindow
import gamepads.physical as gamepad_physical
import gamepads.emulated as gamepad_emulated
from models.gamepad import GamepadModel

class MainWindow(QMainWindow):
    def __init__(self, gamepad_handler):
        super().__init__()

        self._gamepad_handler = gamepad_handler
        self._gui = Ui_MainWindow()
        self._gui.setupUi(self)
        self._emuthread = None
        self._emuthread_stop = threading.Event()

        self.gamepad_model = GamepadModel(self._gamepad_handler.find_gamepads())
        self._gui.tableView_physicalControllerList.setModel(self.gamepad_model)
        self._gui.tableView_physicalControllerList.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self._gui.tableView_physicalControllerList.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self._gui.tableView_physicalControllerList.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self._gui.tableView_physicalControllerList.selectionModel().selectionChanged.connect(self.controller_list_selection_changed)
        self._gui.tableView_physicalControllerList.selectRow(0)

        self._gui.pushButton_physicalControllerRefresh.clicked.connect(self.controller_list_refresh)
        self._gui.pushButton_emulatedControllerStart.clicked.connect(self.controller_emulator_start)
        self._gui.pushButton_emulatedControllerStop.clicked.connect(self.controller_emulator_stop)

        self._gui.pushButton_emulatedControllerStop.setVisible(False)
        self.populate_controller_combobox()

    def closeEvent(self, event):
        self._emuthread_stop.set()

    def populate_controller_combobox(self):
        self._gui.comboBox_emulatedControllerModel.addItem("PC two-handle controller (DGOC-44U)", gamepad_emulated.PC2HandleGamepad())
        self._gui.comboBox_emulatedControllerModel.setCurrentIndex(0)
        self._gui.comboBox_emulatedControllerModel.addItem("Sony PlayStation two-handle controller (SLPH-00051)", gamepad_emulated.PS1Gamepad())
        self._gui.comboBox_emulatedControllerModel.addItem("Nintendo 64 two-handle controller (TCPP-20003)", gamepad_emulated.N64Gamepad())
        self._gui.comboBox_emulatedControllerModel.addItem("SEGA Saturn two-handle controller (TC-5175290)", gamepad_emulated.SATGamepad())
        self._gui.comboBox_emulatedControllerModel.model().sort(0)

    def controller_list_refresh(self):
        self.gamepad_model.beginResetModel()
        self.gamepad_model.gamepads = self._gamepad_handler.find_gamepads()
        self.gamepad_model.endResetModel()
        self.controller_list_selection_changed()

    def controller_list_selection_changed(self):
        enabled = False
        rows = self._gui.tableView_physicalControllerList.selectionModel().selectedRows()
        if rows and self.gamepad_model.gamepads[rows[0].row()].type != gamepad_physical.PhysicalGamepad.GamepadType.UNKNOWN:
            enabled = True
        self._gui.pushButton_emulatedControllerStart.setEnabled(enabled)

    def lock_interface(self,):
        self._gui.pushButton_emulatedControllerStart.setVisible(False)
        self._gui.pushButton_emulatedControllerStop.setVisible(True)
        self._gui.tableView_physicalControllerList.setEnabled(False)
        self._gui.pushButton_physicalControllerRefresh.setEnabled(False)
        self._gui.pushButton_physicalControllerConfig.setEnabled(False)
        self._gui.comboBox_emulatedControllerModel.setEnabled(False)
    
    def unlock_interface(self,):
        self._gui.pushButton_emulatedControllerStart.setVisible(True)
        self._gui.pushButton_emulatedControllerStop.setVisible(False)
        self._gui.tableView_physicalControllerList.setEnabled(True)
        self._gui.pushButton_physicalControllerRefresh.setEnabled(True)
        self._gui.pushButton_physicalControllerConfig.setEnabled(True)
        self._gui.comboBox_emulatedControllerModel.setEnabled(True)

    def controller_emulator_start(self):
        self.lock_interface()
        self._gui.statusbar.showMessage("Gamepad emulator running...")
        rows = self._gui.tableView_physicalControllerList.selectionModel().selectedRows()
        if rows:
            gamepad = self.gamepad_model.gamepads[rows[0].row()]
            emulated_gamepad = self._gui.comboBox_emulatedControllerModel.itemData(self._gui.comboBox_emulatedControllerModel.currentIndex())
            self._emuthread = threading.Thread(target=self._gamepad_handler.run_gamepad_emulator, args=(gamepad, emulated_gamepad, self._emuthread_stop))
            self._emuthread.start()

    def controller_emulator_stop(self):
        self._gui.statusbar.showMessage("Stopping gamepad emulator...")
        self._emuthread_stop.set()
        self._emuthread.join(timeout=0.05)
        if self._emuthread.is_alive():
            QTimer.singleShot(50, self.controller_emulator_stop)
            return
        self._emuthread_stop.clear()
        self.unlock_interface()
        self.controller_list_refresh()
        self._gui.statusbar.showMessage("Gamepad emulator stopped successfully!", 5000)

