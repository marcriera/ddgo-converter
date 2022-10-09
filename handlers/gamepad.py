from evdev import InputDevice, list_devices, ecodes as e, UInput, AbsInfo

class GamepadHandler:
    def __init__(self):
        super().__init__()

    def find_gamepads():
        gamepads = []
        devices = [InputDevice(path) for path in list_devices()]
        for device in devices:
            gamepads.append(Gamepad(device.info.vendor, device.info.product, device.name))
        return gamepads

class Gamepad:

    def __init__(self, vid, pid, name):
        super().__init__()
        self.vid = vid
        self.pid = pid
        self.name = name



""" cap = {
    e.EV_KEY : [e.BTN_NORTH, e.BTN_SOUTH, e.BTN_EAST, e.BTN_WEST, e.BTN_SELECT, e.BTN_START],
    e.EV_ABS : [(e.ABS_X, AbsInfo(0, 0, 255, 0, 0, 0)), (e.ABS_Y, AbsInfo(0, 0, 255, 0, 0, 0))]
}

# Mapping
# A: BTN_EAST
# B: BTN_SOUTH
# C: BTN_NORTH
# D: BTN_WEST
# SL: BTN_SELECT
# ST: BTN_START
# BRAKE: ABS_X
# POWER: ABS_Y

mascon_switch = None
devices = [InputDevice(path) for path in list_devices()]
for device in devices:
    dev_name = [device.info.vendor, device.info.product, device.name]  
    if dev_name == [0x0f0d, 0x00c1, "One Handle MasCon for Nintendo Switch"]:
        mascon_switch = device
        break

if mascon_switch is None:
    print("No supported controller found.")
    exit()

ui = UInput(cap, vendor=0x0AE4, product=0x0003, name='Emulated DGOC-44U')

mascon_switch.grab()
for event in mascon_switch.read_loop():
    if event.type == e.EV_KEY:
        match event.code:
            case 304: # Y
                ui.write(e.EV_KEY, e.BTN_EAST, event.value)
                ui.syn()
            case 305: # B
                ui.write(e.EV_KEY, e.BTN_SOUTH, event.value)
                ui.syn()
            case 306: # A
                ui.write(e.EV_KEY, e.BTN_NORTH, event.value)
                ui.syn()
            case 307: # X
                ui.write(e.EV_KEY, e.BTN_WEST, event.value)
                ui.syn()
            case 312: # MINUS
                ui.write(e.EV_KEY, e.BTN_SELECT, event.value)
                ui.syn()
            case 313: # PLUS
                ui.write(e.EV_KEY, e.BTN_START, event.value)
                ui.syn()
    if event.type == e.EV_ABS and event.code == e.ABS_HAT0X:
        match event.value:
            case -1: # LEFT
                ui.write(e.EV_KEY, e.BTN_SELECT, 1)
                ui.write(e.EV_KEY, e.BTN_EAST, 1)
                ui.write(e.EV_KEY, e.BTN_NORTH, 0)
                ui.syn()
            case 1: # RIGHT
                ui.write(e.EV_KEY, e.BTN_SELECT, 1)
                ui.write(e.EV_KEY, e.BTN_EAST, 0)
                ui.write(e.EV_KEY, e.BTN_NORTH, 1)
                ui.syn()
            case _: # NONE
                ui.write(e.EV_KEY, e.BTN_SELECT, 0)
                ui.write(e.EV_KEY, e.BTN_EAST, 0)
                ui.write(e.EV_KEY, e.BTN_NORTH, 0)
                ui.syn()
    if event.type == e.EV_ABS and event.code == e.ABS_HAT0Y:
        match event.value:
            case -1: # UP
                ui.write(e.EV_KEY, e.BTN_SELECT, 1)
                ui.write(e.EV_KEY, e.BTN_WEST, 1)
                ui.write(e.EV_KEY, e.BTN_SOUTH, 0)
                ui.syn()
            case 1: # DOWN
                ui.write(e.EV_KEY, e.BTN_SELECT, 1)
                ui.write(e.EV_KEY, e.BTN_WEST, 0)
                ui.write(e.EV_KEY, e.BTN_SOUTH, 1)
                ui.syn()
            case _: # NONE
                ui.write(e.EV_KEY, e.BTN_SELECT, 0)
                ui.write(e.EV_KEY, e.BTN_WEST, 0)
                ui.write(e.EV_KEY, e.BTN_SOUTH, 0)
                ui.syn()
    if event.type == e.EV_ABS and event.code == e.ABS_Y:
        match event.value:
            case 0x0: # EMG
                ui.write(e.EV_ABS, e.ABS_X, 0xB9)
                ui.write(e.EV_ABS, e.ABS_Y, 0x81)
                ui.syn()
            case 0x5:
                ui.write(e.EV_ABS, e.ABS_X, 0xB5)
                ui.write(e.EV_ABS, e.ABS_Y, 0x81)
                ui.syn()
            case 0x13:
                ui.write(e.EV_ABS, e.ABS_X, 0xB2)
                ui.write(e.EV_ABS, e.ABS_Y, 0x81)
                ui.syn()
            case 0x20:
                ui.write(e.EV_ABS, e.ABS_X, 0xAF)
                ui.write(e.EV_ABS, e.ABS_Y, 0x81)
                ui.syn()
            case 0x2E:
                ui.write(e.EV_ABS, e.ABS_X, 0xA8)
                ui.write(e.EV_ABS, e.ABS_Y, 0x81)
                ui.syn()
            case 0x3C:
                ui.write(e.EV_ABS, e.ABS_X, 0xA2)
                ui.write(e.EV_ABS, e.ABS_Y, 0x81)
                ui.syn()
            case 0x49:
                ui.write(e.EV_ABS, e.ABS_X, 0x9A)
                ui.write(e.EV_ABS, e.ABS_Y, 0x81)
                ui.syn()
            case 0x57:
                ui.write(e.EV_ABS, e.ABS_X, 0x94)
                ui.write(e.EV_ABS, e.ABS_Y, 0x81)
                ui.syn()
            case 0x65:
                ui.write(e.EV_ABS, e.ABS_X, 0x8A)
                ui.write(e.EV_ABS, e.ABS_Y, 0x81)
                ui.syn()
            case 0x80:
                ui.write(e.EV_ABS, e.ABS_X, 0x79)
                ui.write(e.EV_ABS, e.ABS_Y, 0x81)
                ui.syn()
            case 0x9F:
                ui.write(e.EV_ABS, e.ABS_X, 0x79)
                ui.write(e.EV_ABS, e.ABS_Y, 0x6D)
                ui.syn()
            case 0xB7:
                ui.write(e.EV_ABS, e.ABS_X, 0x79)
                ui.write(e.EV_ABS, e.ABS_Y, 0x54)
                ui.syn()
            case 0xCE:
                ui.write(e.EV_ABS, e.ABS_X, 0x79)
                ui.write(e.EV_ABS, e.ABS_Y, 0x3F)
                ui.syn()
            case 0xE6:
                ui.write(e.EV_ABS, e.ABS_X, 0x79)
                ui.write(e.EV_ABS, e.ABS_Y, 0x21)
                ui.syn()
            case 0xFF:
                ui.write(e.EV_ABS, e.ABS_X, 0x79)
                ui.write(e.EV_ABS, e.ABS_Y, 0x00)
                ui.syn()
 """