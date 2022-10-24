from evdev import InputDevice, list_devices, ecodes as e, UInput, AbsInfo
import threading
import events.input as input_events
import gamepads.physical as gamepad_physical
import gamepads.emulated as gamepad_emulated

class GamepadHandler:
    def __init__(self):
        super().__init__()

    def find_gamepads():
        gamepads = []
        devices = [InputDevice(path) for path in list_devices()]
        for device in devices:
            gamepads.append(gamepad_physical.create_gamepad(device.info.vendor, device.info.product, device.name))
        return gamepads
    
    def run_gamepad_emulator(gamepad, emulated_gamepad, stop_event):
        gamepad.start()
        emulated_gamepad.start()
        while not stop_event.is_set():
            events = gamepad.read_input()
            if events is not None:
                for event in events:
                    if event.type == input_events.InputEvent.EventType.ERROR:
                        break
                    emulated_gamepad.write_input(event)
        emulated_gamepad.stop()
        gamepad.stop()
