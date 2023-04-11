from supervisor import ticks_ms
import time

NO_KEY = -1
UNKNOWN = -2
UNSTABLE = -3

class Event:
    """
    A key transition event.

    :param int key_number: the key number
    :param bool pressed: ``True`` if the key was pressed; ``False`` if it was released.
    :param int timestamp: The time in milliseconds that the keypress occurred in the
                          `supervisor.ticks_ms` time system.  If specified as None,
                          the current value of `supervisor.ticks_ms` is used.
    """

    def __init__(self, key: int, pressed: bool, timestamp: int = None):
        self.key_number = key
        """The key number."""
        self.timestamp = timestamp or ticks_ms()
        """The timestamp."""
        self.pressed = pressed
        """True if the event represents a key down (pressed) transition.
        The opposite of released."""

    @property
    def released(self) -> bool:
        """True if the event represents a key up (released) transition.
        The opposite of pressed."""
        return not self.pressed

    def __eq__(self, other: object) -> bool:
        """Two Event objects are equal if their key_number and pressed/released values
        are equal. Note that this does not compare the event timestamps."""
        return self.key_number == other.key_number and self.pressed == other.pressed

    def __hash__(self) -> int:
        """Returns a hash for the Event, so it can be used in dictionaries, etc..
        Note that as events with different timestamps compare equal,
        they also hash to the same value."""
        return self.key_number << 1 + int(self.pressed)

    def __repr__(self) -> str:
        """Human readble repr."""
        pressed = "pressed" if self.pressed else "released"
        return f"<Event {self.key_number} {pressed} {self.timestamp}>"

class EventQueue:
    """
    A queue of Event objects, filled by a scanner.
    """

    def __init__(self):  # , max_events=64):
        self._outq = []
        self._inq = []

    def append(self, event: Event) -> None:
        """Append an event at the end of the queue"""
        self._inq.append(event)

    def get(self) -> Event:
        """
        Return the next key transition event.
        Return None if no events are pending.
        """
        if self._outq:
            return self._outq.pop()
        if len(self._inq) == 1:
            return self._inq.pop()
        if self._inq:
            self._outq = list(reversed(self._inq))
            self._inq.clear()
            return self._outq.pop()
        return None

    def get_into(self, event: Event) -> bool:
        """
        Store the next key transition event in the supplied event, if available,
        and return True. If there are no queued events, do not touch event
        and return False.
        Note: in python this does not optimize to avoid allocating.
        """
        next_event = self.get()
        if next_event:
            event.key_number = next_event.key_number
            event.timestamp = next_event.timestamp
            event.pressed = next_event.pressed
            return True
        return False

    def clear(self) -> None:
        """Clear any queued key transition events."""
        self._outq.clear()
        self._inq.clear()

    def __bool__(self) -> bool:
        """
        True if len() is greater than zero.
        This is an easy way to check if the queue is empty.
        """
        return len(self) > 0

    def __len__(self) -> int:
        """
        Return the number of events currently in the queue.
        Used to implement len().
        """
        return len(self._outq) + len(self._inq)

class AnalogKeypad:
    def __init__(self, pin, neutral, *buttons, tolerance=0x400, stability_delay=0.002):
        if hasattr(pin, "value"):
            self.analog = lambda: pin.value
        elif callable(pin):
            self.analog = pin
        self._steps = (neutral,) + buttons
        self.tolerance = tolerance
        self.delay = stability_delay
        self.events = EventQueue()
        self._status = NO_KEY

    @property
    def button(self):
        delay = self.delay
        value = self.analog()
        time.sleep(delay)
        temp = self.analog()
        if abs(value - temp) > self.tolerance:
            return UNSTABLE
        for btn, step in enumerate(self._steps):
            if abs(value - step) < self.tolerance:
                return btn - 1
        return UNKNOWN

    @property
    def buttons(self):
        button = self.button
        if button >= 0:
            return [button]
        return []

    def update(self, value=None):
        timestamp = ticks_ms()
        status = self._status
        if value is not None:
            current_button = value
        else:
            current_button = self.button
        if status != current_button:
            if status >= 0:
                self.events.append(Event(status, False, timestamp))
            if current_button >= 0:
                self.events.append(Event(current_button, True, timestamp))
        self._status = current_button

