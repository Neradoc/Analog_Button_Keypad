"""
Test for analog-coded gamepad buttons. (Resistor ladder)

Can we convert the current value into buckets centered around the buttons values ?
Maybe not, that would take more time than testing all.

Should we add some test, waiting for the analog to settle when reading
if the value is moving too much ?
"""
import analogio
import board
import time
import atexit
import ansi_escape_code
from analog_button import AnalogKeypad, NO_KEY

red = ansi_escape_code.ANSIColors.fg.red
green = ansi_escape_code.ANSIColors.fg.green
grey = ansi_escape_code.ANSIColors.fg.lightgrey
dark = ansi_escape_code.ANSIColors.fg.darkgrey
blue = ansi_escape_code.ANSIColors.fg.cyan
pink = ansi_escape_code.ANSIColors.fg.pink
yellow = ansi_escape_code.ANSIColors.fg.yellow
bg_orange = ansi_escape_code.ANSIColors.bg.orange
bg_grey = ansi_escape_code.ANSIColors.bg.lightgrey
bg_black = ansi_escape_code.ANSIColors.bg.black
reset = ansi_escape_code.ANSIColors.reset

atexit.register(lambda: print(reset))

analog_green = analogio.AnalogIn(board.A0)
buttons_green_board = (361, 26341, 39235, 52123, 65371)
keys_A = AnalogKeypad(analog_green, *buttons_green_board)
keys_A.status = NO_KEY

analog_red = analogio.AnalogIn(board.A1)
buttons_red_board = (65371, 447, 9865, 20072, 31831, 50329)
keys_B = AnalogKeypad(analog_red, *buttons_red_board)
keys_B.status = NO_KEY

def test_button(keys, name, color=green, off=red, neutral=grey, background=bg_black):
    button = keys.button
    status = keys.status
    if status != button:
        if button >= 0:
            print(f"{background}{color} {name}{button:<4} ", end="") # pressed
        elif button < 0 and status >= 0:
            print(f"{background}{off} {name}{status}|{button:<2} ", end="") # released
        else:
            print(f"{background}{neutral} {name}{button:<4} ", end="") # no button or unstable state
    keys.status = button

while True:
    test_button(keys_A, "A", neutral=dark, background=bg_grey)
    test_button(keys_B, "B", color=blue, off=pink)
