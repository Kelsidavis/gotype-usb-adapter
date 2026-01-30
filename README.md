# GoType Palm pilot Keyboard from landware USB Adapter

Converts a GoType Palm keyboard into a standard USB HID keyboard using a Raspberry Pi Pico (RP2040) running CircuitPython.

The GoType communicates via a single-wire serial protocol using pulse-width encoding. Each key produces a burst of HIGH/LOW pulses where each pulse duration is a multiple of ~414 microseconds. Every key pattern sums to exactly 9 units.

## Hardware

- **Keyboard**: GoType Palm portable keyboard
- **Microcontroller**: Raspberry Pi Pico (RP2040)
- **CircuitPython**: 9.2.4
- **Library**: `adafruit_hid`

### Wiring

The GoType connector has three wires:

| GoType Wire | Connect To | Function |
|---|---|---|
| Red wire | GP1 | Data (serial signal) |
| Thick black wire | GND | Ground |
| Thin black wire | VBUS (5V) | Power |

## Features

- Full key mapping: 26 letters, 10 digits, punctuation, arrows, function keys (F1-F6)
- **Simultaneous key combos**: Shift+A, Alt+Tab, Ctrl+C etc. detected from overlapping pulse bursts using a sum=9 splitting algorithm
- **One-shot modifiers**: Press Shift/Ctrl/Alt alone, then press a key — modifier auto-releases after the next keypress (fallback when combo detection misses)
- **Key hold/repeat**: Holding a key sends continuous repeats, matching the GoType's repeat burst behavior (120ms timeout)
- **NumLock transparency**: GoType has an internal NumLock mode that sends different patterns for j, k, l, u, i, o, m — both pattern sets are mapped so keys work regardless of NumLock state
- **Remapped keys**: Physical NumLock → Escape, physical Shortcut → Super/GUI

## Protocol Details

The GoType sends data as pulse-width encoded bursts on a single wire (idle LOW):

- Each burst is a sequence of HIGH/LOW transitions
- Pulse durations are multiples of ~414µs (1 unit)
- Every key pattern sums to exactly 9 units
- Example: `a` = `(1, 1, 1, 3, 3)` → 414µs HIGH, 414µs LOW, 414µs HIGH, 1242µs LOW, 1242µs HIGH

For simultaneous key presses, the GoType sends both key bursts back-to-back with a ~1400µs gap between them. The firmware detects this by first trying a single-key lookup, then falling back to splitting the burst at sum=9 boundaries.

## Installation

1. Flash CircuitPython 9.2.4 onto the Pico
2. Copy the `adafruit_hid` library to `CIRCUITPY/lib/`
3. Copy `code.py` to `CIRCUITPY/code.py`
4. Connect the GoType data line to GP1
