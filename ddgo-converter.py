#!/usr/bin/env python

from evdev import InputDevice, list_devices, ecodes as e, UInput, AbsInfo

cap = {
    e.EV_KEY : [e.BTN_NORTH, e.BTN_SOUTH, e.BTN_EAST, e.BTN_WEST, e.BTN_SELECT, e.BTN_START],
    e.EV_ABS : [(e.ABS_X, AbsInfo(0, 0, 255, 0, 0, 0)),(e.ABS_Y, AbsInfo(0, 0, 255, 0, 0, 0)) ]
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
            case 313: # START
                ui.write(e.EV_KEY, e.BTN_START, event.value)
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
