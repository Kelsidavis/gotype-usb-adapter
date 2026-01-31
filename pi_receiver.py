#!/usr/bin/env python3
"""
GoType Palm Keyboard -> Raspberry Pi receiver

Reads key events from RP2040 over UART serial and injects them
as keyboard input via uinput (using libevdev).

Wiring: RP2040 GP0 (TX) -> Pi GPIO15 (RXD), shared GND

Setup on Pi:
  1. Enable UART: sudo raspi-config -> Interface Options -> Serial Port
     - Login shell over serial: No
     - Serial port hardware: Yes
  2. Run: sudo python3 pi_receiver.py
     (sudo needed for /dev/uinput access)
"""

import sys
import serial
import libevdev

SERIAL_PORT = '/dev/serial0'
BAUD_RATE = 9600

# Map key names from the RP2040 firmware to libevdev keycodes
KEY_MAP = {
    'a': libevdev.EV_KEY.KEY_A, 'b': libevdev.EV_KEY.KEY_B,
    'c': libevdev.EV_KEY.KEY_C, 'd': libevdev.EV_KEY.KEY_D,
    'e': libevdev.EV_KEY.KEY_E, 'f': libevdev.EV_KEY.KEY_F,
    'g': libevdev.EV_KEY.KEY_G, 'h': libevdev.EV_KEY.KEY_H,
    'i': libevdev.EV_KEY.KEY_I, 'j': libevdev.EV_KEY.KEY_J,
    'k': libevdev.EV_KEY.KEY_K, 'l': libevdev.EV_KEY.KEY_L,
    'm': libevdev.EV_KEY.KEY_M, 'n': libevdev.EV_KEY.KEY_N,
    'o': libevdev.EV_KEY.KEY_O, 'p': libevdev.EV_KEY.KEY_P,
    'q': libevdev.EV_KEY.KEY_Q, 'r': libevdev.EV_KEY.KEY_R,
    's': libevdev.EV_KEY.KEY_S, 't': libevdev.EV_KEY.KEY_T,
    'u': libevdev.EV_KEY.KEY_U, 'v': libevdev.EV_KEY.KEY_V,
    'w': libevdev.EV_KEY.KEY_W, 'x': libevdev.EV_KEY.KEY_X,
    'y': libevdev.EV_KEY.KEY_Y, 'z': libevdev.EV_KEY.KEY_Z,
    '1': libevdev.EV_KEY.KEY_1, '2': libevdev.EV_KEY.KEY_2,
    '3': libevdev.EV_KEY.KEY_3, '4': libevdev.EV_KEY.KEY_4,
    '5': libevdev.EV_KEY.KEY_5, '6': libevdev.EV_KEY.KEY_6,
    '7': libevdev.EV_KEY.KEY_7, '8': libevdev.EV_KEY.KEY_8,
    '9': libevdev.EV_KEY.KEY_9, '0': libevdev.EV_KEY.KEY_0,
    'space': libevdev.EV_KEY.KEY_SPACE, 'enter': libevdev.EV_KEY.KEY_ENTER,
    'backspace': libevdev.EV_KEY.KEY_BACKSPACE, 'tab': libevdev.EV_KEY.KEY_TAB,
    'caps': libevdev.EV_KEY.KEY_CAPSLOCK,
    'up': libevdev.EV_KEY.KEY_UP, 'down': libevdev.EV_KEY.KEY_DOWN,
    'left': libevdev.EV_KEY.KEY_LEFT, 'right': libevdev.EV_KEY.KEY_RIGHT,
    'period': libevdev.EV_KEY.KEY_DOT, 'comma': libevdev.EV_KEY.KEY_COMMA,
    'slash': libevdev.EV_KEY.KEY_SLASH, 'semicolon': libevdev.EV_KEY.KEY_SEMICOLON,
    'quote': libevdev.EV_KEY.KEY_APOSTROPHE, 'dash': libevdev.EV_KEY.KEY_MINUS,
    'equals': libevdev.EV_KEY.KEY_EQUAL, 'bracketl': libevdev.EV_KEY.KEY_LEFTBRACE,
    'bracketr': libevdev.EV_KEY.KEY_RIGHTBRACE, 'backslash': libevdev.EV_KEY.KEY_BACKSLASH,
    'tilda': libevdev.EV_KEY.KEY_GRAVE, 'escape': libevdev.EV_KEY.KEY_ESC,
    'super': libevdev.EV_KEY.KEY_LEFTMETA,
    'f1': libevdev.EV_KEY.KEY_F1, 'f2': libevdev.EV_KEY.KEY_F2,
    'f3': libevdev.EV_KEY.KEY_F3, 'f4': libevdev.EV_KEY.KEY_F4,
    'f5': libevdev.EV_KEY.KEY_F5, 'f6': libevdev.EV_KEY.KEY_F6,
}

MOD_MAP = {
    'shift_l': libevdev.EV_KEY.KEY_LEFTSHIFT,
    'shift_r': libevdev.EV_KEY.KEY_RIGHTSHIFT,
    'ctrl': libevdev.EV_KEY.KEY_LEFTCTRL,
    'alt': libevdev.EV_KEY.KEY_LEFTALT,
}

ALL_KEYS = list(KEY_MAP.values()) + list(MOD_MAP.values())


def main():
    dev = libevdev.Device()
    dev.name = 'gotype-keyboard'
    for key in ALL_KEYS:
        dev.enable(key)

    uinput = dev.create_uinput_device()
    print(f'GoType uinput device: {uinput.devnode}')

    port = SERIAL_PORT
    if len(sys.argv) > 1:
        port = sys.argv[1]

    print(f'GoType Pi Receiver - listening on {port}')
    ser = serial.Serial(port, BAUD_RATE, timeout=None)

    def press(keycode):
        uinput.send_events([
            libevdev.InputEvent(keycode, value=1),
            libevdev.InputEvent(libevdev.EV_SYN.SYN_REPORT, value=0),
        ])

    def release(keycode):
        uinput.send_events([
            libevdev.InputEvent(keycode, value=0),
            libevdev.InputEvent(libevdev.EV_SYN.SYN_REPORT, value=0),
        ])

    try:
        while True:
            line = ser.readline().decode('utf-8', errors='ignore').strip()
            if not line or ':' not in line:
                continue

            cmd, key = line.split(':', 1)

            if cmd == 'P' and key in KEY_MAP:
                press(KEY_MAP[key])
            elif cmd == 'R' and key in KEY_MAP:
                release(KEY_MAP[key])
            elif cmd == 'M+' and key in MOD_MAP:
                press(MOD_MAP[key])
            elif cmd == 'M-' and key in MOD_MAP:
                release(MOD_MAP[key])
    except KeyboardInterrupt:
        print('\nExiting.')
    finally:
        ser.close()


if __name__ == '__main__':
    main()
