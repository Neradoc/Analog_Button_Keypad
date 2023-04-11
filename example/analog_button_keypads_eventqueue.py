"""
Test for analog-coded gamepad buttons. (Resistor ladder)
"""
import analogio
import board
import time
from analog_button import AnalogKeypad, NO_KEY

analog_green = analogio.AnalogIn(board.A0)
buttons_green_board = (361, 26341, 39235, 52123, 65371)
keys_A = AnalogKeypad(analog_green, *buttons_green_board)
keys_A.status = NO_KEY

analog_red = analogio.AnalogIn(board.A1)
buttons_red_board = (65371, 447, 9865, 20072, 31831, 50329)
keys_B = AnalogKeypad(analog_red, *buttons_red_board)
keys_B.status = NO_KEY

while True:
    keys_A.update()
    keys_B.update()
    if event := keys_A.events.get():
        print(event)
    if event := keys_B.events.get():
        print(event)
