"""
Setup a resitor ladder on a breadboard.
This is using a Feather RP2040.
"""
import analogio
import board
import time
from analog_button import AnalogKeypad, NO_KEY

analog_input = analogio.AnalogIn(board.A0)
buttons_values = (0, 26310, 39300, 52100, 65535)
keys = AnalogKeypad(analog_input, *buttons_values)

current_button = NO_KEY
while True:
    button = keys.button
    if current_button != button:
        if button >= 0:
            print(f"Button {button} pressed")
        elif button < 0 and current_button >= 0:
            print(f"Button {current_button} released")
    current_button = button
