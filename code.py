import board
import time
import pulseio
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

pin_pulses = pulseio.PulseIn(board.GP1, maxlen=40, idle_state=False)
kbd = Keyboard(usb_hid.devices)
UNIT = 414

KEYMAP = {
    # Letters
    (1, 1, 1, 3, 3): 'a',
    (1, 1, 1, 2, 1, 1, 2): 'b',
    (1, 2, 1, 1, 1, 1, 2): 'c',
    (1, 5, 3): 'd',
    (2, 1, 2, 1, 3): 'e',
    (6, 1, 2): 'f',
    (1, 1, 4, 1, 2): 'g',
    (2, 1, 3, 1, 2): 'h',
    (1, 3, 1, 1, 3): 'i',
    (1, 2, 3, 1, 2): 'j',
    (3, 1, 2, 1, 2): 'k',
    (1, 1, 1, 1, 2, 1, 2): 'l',
    (1, 4, 1, 1, 2): 'm',
    (2, 3, 1, 1, 2): 'n',
    (4, 2, 3): 'o',
    (1, 1, 2, 2, 3): 'p',
    (5, 1, 3): 'q',
    (1, 2, 2, 1, 3): 'r',
    (2, 4, 3): 's',
    (3, 1, 1, 1, 3): 't',
    (2, 2, 1, 1, 3): 'u',
    (3, 2, 1, 1, 2): 'v',
    (1, 1, 3, 1, 3): 'w',
    (2, 1, 1, 1, 1, 1, 2): 'x',
    (1, 1, 1, 1, 1, 1, 3): 'y',
    (1, 1, 2, 1, 1, 1, 2): 'z',
    # Numlock-mode aliases
    (1, 1, 5, 1, 1): 'j',
    (2, 1, 4, 1, 1): 'k',
    (1, 2, 4, 1, 1): 'l',
    (3, 1, 3, 1, 1): 'u',
    (1, 1, 1, 1, 3, 1, 1): 'i',
    (2, 2, 3, 1, 1): 'o',
    (3, 5, 1): 'm',
    (2, 1, 1, 1, 2, 1, 1): 'n',
    # Numbers
    (2, 1, 6): '1',
    (1, 2, 6): '2',
    (3, 1, 5): '3',
    (1, 1, 1, 1, 5): '4',
    (2, 2, 5): '5',
    (1, 3, 5): '6',
    (4, 1, 4): '7',
    (1, 1, 2, 1, 4): '8',
    (2, 1, 1, 1, 4): '9',
    (1, 2, 1, 1, 4): '0',
    # Special keys
    (1, 2, 2, 2, 2): 'space',
    (4, 1, 1, 1, 2): 'enter',
    (2, 2, 1, 2, 2): 'backspace',
    (1, 4, 4): 'tab',
    (1, 2, 1, 2, 1, 1, 1): 'shift_l',
    (3, 3, 1, 1, 1): 'shift_r',
    (1, 5, 1, 1, 1): 'ctrl',
    (1, 1, 1, 3, 1, 1, 1): 'alt',
    (1, 1, 4, 2, 1): 'caps',
    (2, 1, 1, 3, 2): 'up',
    (1, 2, 1, 3, 2): 'down',
    (1, 3, 1, 2, 2): 'left',
    (2, 5, 2): 'right',
    (1, 1, 3, 2, 2): 'period',
    (5, 2, 2): 'comma',
    (2, 1, 2, 2, 2): 'slash',
    (2, 2, 2, 1, 2): 'semicolon',
    (1, 3, 2, 1, 2): 'quote',
    (3, 2, 4): 'dash',
    (1, 1, 1, 2, 4): 'equals',
    (2, 1, 1, 2, 3): 'bracketl',
    (1, 2, 1, 2, 3): 'bracketr',
    (3, 3, 3): 'backslash',
    (1, 1, 7): 'tilda',
    (2, 1, 3, 2, 1): 'escape',
    (2, 2, 2, 2, 1): 'super',
    # Function keys
    (1, 4, 2, 1, 1): 'f1',
    (5, 1, 1, 1, 1): 'f2',
    (1, 1, 3, 1, 1, 1, 1): 'f3',
    (4, 2, 1, 1, 1): 'f4',
    (1, 1, 2, 2, 1, 1, 1): 'f5',
    (2, 1, 1, 2, 1, 1, 1): 'f6',
}

HID_MAP = {
    'a': Keycode.A, 'b': Keycode.B, 'c': Keycode.C, 'd': Keycode.D,
    'e': Keycode.E, 'f': Keycode.F, 'g': Keycode.G, 'h': Keycode.H,
    'i': Keycode.I, 'j': Keycode.J, 'k': Keycode.K, 'l': Keycode.L,
    'm': Keycode.M, 'n': Keycode.N, 'o': Keycode.O, 'p': Keycode.P,
    'q': Keycode.Q, 'r': Keycode.R, 's': Keycode.S, 't': Keycode.T,
    'u': Keycode.U, 'v': Keycode.V, 'w': Keycode.W, 'x': Keycode.X,
    'y': Keycode.Y, 'z': Keycode.Z,
    '1': Keycode.ONE, '2': Keycode.TWO, '3': Keycode.THREE,
    '4': Keycode.FOUR, '5': Keycode.FIVE, '6': Keycode.SIX,
    '7': Keycode.SEVEN, '8': Keycode.EIGHT, '9': Keycode.NINE,
    '0': Keycode.ZERO,
    'space': Keycode.SPACE, 'enter': Keycode.ENTER,
    'backspace': Keycode.BACKSPACE, 'tab': Keycode.TAB,
    'caps': Keycode.CAPS_LOCK,
    'up': Keycode.UP_ARROW, 'down': Keycode.DOWN_ARROW,
    'left': Keycode.LEFT_ARROW, 'right': Keycode.RIGHT_ARROW,
    'period': Keycode.PERIOD, 'comma': Keycode.COMMA,
    'slash': Keycode.FORWARD_SLASH, 'semicolon': Keycode.SEMICOLON,
    'quote': Keycode.QUOTE, 'dash': Keycode.MINUS,
    'equals': Keycode.EQUALS, 'bracketl': Keycode.LEFT_BRACKET,
    'bracketr': Keycode.RIGHT_BRACKET, 'backslash': Keycode.BACKSLASH,
    'tilda': Keycode.GRAVE_ACCENT, 'escape': Keycode.ESCAPE,
    'super': Keycode.GUI,
    'f1': Keycode.F1, 'f2': Keycode.F2, 'f3': Keycode.F3,
    'f4': Keycode.F4, 'f5': Keycode.F5, 'f6': Keycode.F6,
}

MODIFIER_MAP = {
    'shift_l': Keycode.LEFT_SHIFT,
    'shift_r': Keycode.RIGHT_SHIFT,
    'ctrl': Keycode.LEFT_CONTROL,
    'alt': Keycode.LEFT_ALT,
}

def decode_pulses():
    n = len(pin_pulses)
    if n == 0:
        return []
    raw = [pin_pulses[i] for i in range(n)]

    # Skip overflow at start
    start = 0
    while start < len(raw) and raw[start] > 5000:
        start += 1
    if start >= len(raw):
        return []

    # Quantize all pulses to units
    burst = raw[start:]
    all_units = []
    for d in burst:
        if d > 5000:
            break
        u = round(d / UNIT)
        if u < 1:
            u = 1
        all_units.append(u)

    total = tuple(all_units)

    # Try single-key decode first (most reliable)
    key = KEYMAP.get(total, None)
    if key is not None:
        return [key]

    # No single match — try combo split using sum=9 rule.
    # Every GoType key sums to 9 units. For combos, the burst
    # contains key1 + gap_pulse + key2. We greedily consume
    # units to sum=9, skip one gap pulse, and repeat.
    keys = []
    i = 0
    while i < len(all_units):
        seg = []
        s = 0
        while i < len(all_units) and s + all_units[i] <= 9:
            seg.append(all_units[i])
            s += all_units[i]
            i += 1
            if s == 9:
                break
        if s == 9 and seg:
            pattern = tuple(seg)
            k = KEYMAP.get(pattern, None)
            if k is not None:
                keys.append(k)
            # Skip gap pulse
            if i < len(all_units):
                i += 1
        else:
            break
    if keys:
        return keys

    return []

active_modifiers = set()
oneshot_modifiers = set()

while True:
    pin_pulses.clear()
    while len(pin_pulses) == 0:
        pass
    time.sleep(0.010)

    keys = decode_pulses()
    if not keys:
        continue

    if len(keys) == 1:
        key = keys[0]
        # Single key: same behavior as before
        if key in MODIFIER_MAP:
            kc = MODIFIER_MAP[key]
            if kc in active_modifiers:
                kbd.release(kc)
                active_modifiers.discard(kc)
                oneshot_modifiers.discard(kc)
            else:
                kbd.press(kc)
                active_modifiers.add(kc)
                oneshot_modifiers.add(kc)
        elif key in HID_MAP:
            kc = HID_MAP[key]
            kbd.press(kc)
            # Hold detection
            while True:
                pin_pulses.clear()
                deadline = time.monotonic() + 0.12
                while len(pin_pulses) == 0:
                    if time.monotonic() >= deadline:
                        break
                if len(pin_pulses) == 0:
                    break
                time.sleep(0.010)
                repeat_keys = decode_pulses()
                if repeat_keys != [key]:
                    break
            kbd.release(kc)
            # One-shot modifier release
            if oneshot_modifiers:
                for mod in list(oneshot_modifiers):
                    kbd.release(mod)
                    active_modifiers.discard(mod)
                oneshot_modifiers.clear()
    else:
        # Combo press: multiple keys arrived simultaneously
        mods = [k for k in keys if k in MODIFIER_MAP]
        regs = [k for k in keys if k not in MODIFIER_MAP and k in HID_MAP]

        # Press modifiers first, then regular keys
        for m in mods:
            kbd.press(MODIFIER_MAP[m])
        for r in regs:
            kbd.press(HID_MAP[r])

        # Hold detection for combo
        key_set = set(keys)
        while True:
            pin_pulses.clear()
            deadline = time.monotonic() + 0.12
            while len(pin_pulses) == 0:
                if time.monotonic() >= deadline:
                    break
            if len(pin_pulses) == 0:
                break
            time.sleep(0.010)
            repeat_keys = decode_pulses()
            if set(repeat_keys) != key_set:
                break

        # Release regular keys first, then modifiers
        for r in regs:
            kbd.release(HID_MAP[r])
        for m in mods:
            kbd.release(MODIFIER_MAP[m])
        # Clear any one-shot state since combo handled its own modifiers
        oneshot_modifiers.clear()
        active_modifiers.clear()

    time.sleep(0.01)
