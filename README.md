# Densha de GO! Controller Converter

This tool allows using a physical _Densha de GO!_ controller with a game that does not officially support it. It is Linux only (check https://autotraintas.hariko.com/ if you use Windows).

## How it works

The program reads input from a real controller, translates it and sends it to an emulated controller, which is picked up by the game.

## Installation

The executable is ready to use. However, you will need read AND write permissions on `/dev/uinput` for the program to work.

**NOTE:** Currently, this fails to launch on the Steam Deck in Gaming Mode. It works fine in Desktop Mode, but you need to disable Steam Input (or close Steam entirely).

## Supported controllers

### Physical (input)

- One-handle controller for PC (DGC-255)
- Two-handle controller for PC (DGOC-44U)
- One-handle controller for Nintendo Switch (ZKNS-001)

### Emulated (output)

- Two-handle controller for PC (DGOC-44U)
- Two-handle controller for Sony PlayStation (SLPH-00051)
- Two-handle controller for Nintendo 64 (TCPP-20003)
- Two-handle controller for SEGA Saturn (TC-5175290)

## Notes

When emulating console controllers, an emulated Sony PlayStation 3 controller is used for easier mapping. On RetroArch, everything should work out of the box.

_Densha de GO! 64_ requires connecting the controller to Port 3 and enabling **Independent C-button Controls**.
