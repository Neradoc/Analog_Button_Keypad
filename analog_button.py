import time

NO_KEY = 0
UNKNOWN = -1
UNSTABLE = -2

class AnalogKeypad:
    def __init__(self, pin, neutral, *buttons, tolerance=0x400, stability_delay=0.002):
        if hasattr(pin, "value"):
            self.analog = lambda: pin.value
        elif callable(pin):
            self.analog = pin
        self._steps = (neutral,) + buttons
        self.tolerance = tolerance
        self.delay = stability_delay
        self.status = 0

    @property
    def button(self):
        delay = self.delay
        value = self.analog()
        time.sleep(delay)
        temp = self.analog()
        if abs(value - temp) > self.tolerance:
            return UNSTABLE
        # print(f"{value:5d} {value >> 8:3d} <{value:04X}> [{value:016b}] B: {button}")
        for btn, step in enumerate(self._steps):
            if abs(value - step) < self.tolerance:
                return btn
        return UNKNOWN

