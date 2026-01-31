from machine import Pin
import time
import sys

# GoType Palm Keyboard -> USB HID Firmware
# Protocol: pulse-width encoding, ~410us per unit, all patterns sum to 9 units
# Matching on raw microsecond deltas for better accuracy

pin = Pin(1, Pin.IN)

# Reference raw deltas (microseconds) for each key
# Taken from consistent multi-burst captures
KEYMAP_RAW = {
    # Letters - (reference_deltas, key_name)
    'a': (390, 415, 410, 1230, 1230),
    'b': (400, 415, 415, 830, 395, 415, 830),
    'c': (400, 835, 410, 410, 415, 410, 830),
    'd': (420, 2060, 1250),
    'e': (810, 410, 850, 390, 1270),
    'f': (2470, 415, 830),
    'g': (395, 415, 1650, 410, 815),
    'h': (800, 415, 1250, 415, 815),
    'i': (400, 415, 410, 410, 1250, 415, 415),
    'j': (375, 415, 2065, 412, 425),
    'k': (810, 412, 1650, 415, 415),
    'l': (382, 832, 1650, 420, 400),
    'm': (822, 420, 415, 412, 822, 415, 415),
    'n': (810, 1240, 410, 415, 830),
    'o': (800, 840, 1230, 415, 425),
    'p': (400, 415, 830, 830, 1230),
    'q': (2070, 415, 1230),
    'r': (400, 835, 835, 415, 1230),
    's': (810, 1650, 1230),
    't': (1210, 415, 415, 415, 1230),
    'u': (1215, 415, 1245, 415, 410),
    'v': (1210, 835, 415, 415, 830),
    'w': (400, 415, 1240, 415, 1230),
    'x': (810, 415, 415, 415, 415, 415, 830),
    'y': (400, 415, 415, 415, 415, 415, 1230),
    'z': (400, 415, 830, 415, 415, 415, 830),
    # Numbers
    '1': (810, 415, 2470),
    '2': (400, 835, 2470),
    '3': (1215, 415, 2070),
    '4': (400, 415, 410, 415, 2070),
    '5': (810, 835, 2070),
    '6': (400, 1240, 2070),
    '7': (395, 1235, 1240, 415, 425),
    '8': (1640, 410, 830, 415, 415),
    '9': (395, 415, 830, 415, 825, 415, 415),
    '0': (400, 835, 415, 415, 1650),
    # Special
    'space': (400, 835, 835, 835, 830),
    'enter': (1640, 415, 415, 415, 830),
    'backspace': (810, 835, 415, 835, 830),
    'tab': (400, 1650, 1650),
    'shift_l': (400, 835, 415, 835, 415, 415, 415),
    'shift_r': (1210, 1240, 415, 415, 415),
    'ctrl': (400, 2060, 415, 415, 415),
    'alt': (400, 415, 415, 1240, 415, 415, 415),
    'caps': (400, 415, 1650, 835, 400),
    'up': (810, 415, 415, 1240, 830),
    'down': (400, 835, 415, 1240, 830),
    'left': (400, 1240, 415, 835, 830),
    'right': (810, 2060, 830),
    'period': (415, 415, 1240, 830, 830),
    'comma': (2060, 835, 830),
    'slash': (810, 415, 835, 835, 830),
    'semicolon': (2890, 415, 415),
    'quote': (395, 2480, 830),
    'dash': (1215, 835, 835, 415, 415),
    'equals': (400, 415, 415, 835, 1650),
    'bracketl': (400, 400, 415, 830, 835, 415, 415),
    'bracketr': (400, 835, 415, 835, 1230),
    'backslash': (1230, 1230, 1230),
    'tilda': (400, 415, 2895),
    'numlock': (800, 415, 1240, 835, 415),
    'shortcut': (810, 835, 835, 835, 415),
    'f1': (400, 1650, 835, 415, 415),
    'f2': (2060, 415, 415, 415, 415),
    'f3': (400, 415, 1240, 415, 415, 415, 415),
    'f4': (1650, 835, 415, 415, 415),
    'f5': (400, 415, 835, 835, 415, 415, 415),
    'f6': (810, 415, 415, 835, 415, 415, 415),
}

HID_CODES = {
    'a': 0x04, 'b': 0x05, 'c': 0x06, 'd': 0x07, 'e': 0x08, 'f': 0x09,
    'g': 0x0A, 'h': 0x0B, 'i': 0x0C, 'j': 0x0D, 'k': 0x0E, 'l': 0x0F,
    'm': 0x10, 'n': 0x11, 'o': 0x12, 'p': 0x13, 'q': 0x14, 'r': 0x15,
    's': 0x16, 't': 0x17, 'u': 0x18, 'v': 0x19, 'w': 0x1A, 'x': 0x1B,
    'y': 0x1C, 'z': 0x1D,
    '1': 0x1E, '2': 0x1F, '3': 0x20, '4': 0x21, '5': 0x22, '6': 0x23,
    '7': 0x24, '8': 0x25, '9': 0x26, '0': 0x27,
    'enter': 0x28, 'backspace': 0x2A, 'tab': 0x2B, 'space': 0x2C,
    'dash': 0x2D, 'equals': 0x2E, 'bracketl': 0x2F, 'bracketr': 0x30,
    'backslash': 0x31, 'semicolon': 0x33, 'quote': 0x34,
    'tilda': 0x35, 'comma': 0x36, 'period': 0x37, 'slash': 0x38,
    'caps': 0x39,
    'f1': 0x3A, 'f2': 0x3B, 'f3': 0x3C, 'f4': 0x3D, 'f5': 0x3E, 'f6': 0x3F,
    'numlock': 0x53,
    'up': 0x52, 'down': 0x51, 'left': 0x50, 'right': 0x4F,
    'shortcut': 0x65,
}

HID_MODIFIERS = {
    'shift_l': 0x02,
    'shift_r': 0x20,
    'ctrl': 0x01,
    'alt': 0x04,
}

def read_deltas():
    while pin.value() == 0:
        pass

    transitions = []
    start = time.ticks_us()
    last_val = 1
    transitions.append((0, 1))

    while True:
        val = pin.value()
        if val != last_val:
            t = time.ticks_diff(time.ticks_us(), start)
            transitions.append((t, val))
            last_val = val
            if t > 5000:
                break
        if time.ticks_diff(time.ticks_us(), start) > 10000:
            break

    deltas = []
    for i in range(1, len(transitions)):
        deltas.append(transitions[i][0] - transitions[i-1][0])

    return tuple(deltas)


def lookup_key(deltas):
    best_match = None
    best_score = 999999

    for key, ref in KEYMAP_RAW.items():
        if len(ref) != len(deltas):
            continue

        # Calculate total absolute difference
        total_diff = 0
        ok = True
        for r, d in zip(ref, deltas):
            diff = abs(r - d)
            # Each pulse must be within 150us of reference
            if diff > 150:
                ok = False
                break
            total_diff += diff

        if ok and total_diff < best_score:
            best_score = total_diff
            best_match = key

    return best_match


print("GoType Palm Keyboard -> USB Adapter")
print("Listening for keypresses...")
print()

active_modifiers = 0
last_key = None
last_key_time = 0

while True:
    deltas = read_deltas()

    # Sanity check
    total = sum(deltas)
    if total < 2500 or total > 5000:
        continue

    # Filter out release glitches: 3-element patterns with short first pulse
    # and a ~2900us middle section
    if len(deltas) == 3 and deltas[1] > 2500:
        continue

    key = lookup_key(deltas)
    now = time.ticks_ms()

    if key:
        if key == last_key and time.ticks_diff(now, last_key_time) < 80:
            last_key_time = now
            continue

        if key in HID_MODIFIERS:
            mod = HID_MODIFIERS[key]
            active_modifiers ^= mod
            print("MOD: {} ({})  mods=0x{:02X}".format(
                key, "ON" if active_modifiers & mod else "OFF", active_modifiers))
        elif key in HID_CODES:
            hid = HID_CODES[key]
            print("KEY: {}  hid=0x{:02X}  mods=0x{:02X}".format(key, hid, active_modifiers))

        last_key = key
        last_key_time = now
    else:
        print("UNRECOGNIZED: deltas={} total={}".format(deltas, total))
