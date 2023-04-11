"""
Code to calibrate the step values of a resistor ladder keypad.
"""
import analogio
import board
import time

analog_0 = analogio.AnalogIn(board.A0)
analog_1 = analogio.AnalogIn(board.A1)

def calibration(pin):
    values = []
    input("Release all buttons and press enter: ")
    value = 0
    for i in range(10):
        value += pin.value / 10
        time.sleep(0.005)
    value = int(value)
    values.append(value)
    print(f"No button pressed: {value}")
    do_continue = True
    button_number = 0
    while do_continue:
        response = input(f"Press and hold button {button_number} and press enter\nEnter F to finish: ")
        if "F" in response.upper():
            break
        value = 0
        for i in range(50):
            value += pin.value / 50
            time.sleep(0.005)
        value = int(value)
        values.append(value)
        print(f"Button {button_number} pressed: {value}")
        button_number += 1
    print("Button analog step values:")
    print("")
    print("button_steps =", tuple(values))
    print("")
    print(f"keys = AnalogKeypad(analogin, *button_steps)")
    print("")

print("Analog A0")
calibration(analog_0)

print("Analog A1")
calibration(analog_1)
