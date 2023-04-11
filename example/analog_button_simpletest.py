"""
Setup a resitor ladder on a breadboard.
This is using a Feather RP2040.
"""
import analogio
import board
import time
from analog_button import AnalogKeypad

analog_input = analogio.AnalogIn(board.A0)
buttons_values = (0, 26310, 39300, 52100, 65535)
keys = AnalogKeypad(analog_input, *buttons_values)

current_button = 0
while True:
    button = keys_A.button
    if current_button != button:
        if button >= 0:
            print(f"Button {button} pressed")
        elif button < 0 and current_button >= 0:
            print(f"Button {button} released")
    current_button = button
