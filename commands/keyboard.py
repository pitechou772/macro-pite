"""
Keyboard Commands Module
Handles all keyboard-related macro commands
"""
from pynput.keyboard import Controller as KController, Key
import time


class KeyboardCommands:
    """Executes keyboard commands"""

    def __init__(self):
        """Initialize keyboard controller"""
        self.controller = KController()

    def press(self, keys_str, duration, speed=1.0):
        """
        Press key(s) for a duration

        Args:
            keys_str: Key or key combination (e.g., 'a' or 'ctrl+c')
            duration: Duration to hold in seconds
            speed: Speed multiplier
        """
        # Adjust duration by speed
        actual_duration = duration / speed

        # Parse keys (support combinations like ctrl+c)
        keys = []
        for k in keys_str.split('+'):
            k = k.strip()
            # Try to get special key from Key enum, otherwise use character
            key = getattr(Key, k, k)
            keys.append(key)

        # Press all keys
        for k in keys:
            self.controller.press(k)

        # Hold
        time.sleep(actual_duration)

        # Release in reverse order
        for k in reversed(keys):
            self.controller.release(k)

    def hotkey(self, keys_str):
        """
        Execute a keyboard shortcut (press and release immediately)

        Args:
            keys_str: Key combination (e.g., 'alt+tab')
        """
        # Parse keys
        keys = []
        for k in keys_str.split('+'):
            k = k.strip()
            key = getattr(Key, k, k)
            keys.append(key)

        # Press all
        for k in keys:
            self.controller.press(k)

        # Release all in reverse order
        for k in reversed(keys):
            self.controller.release(k)

    def type_text(self, text, speed=1.0):
        """
        Type text character by character

        Args:
            text: Text to type
            speed: Speed multiplier
        """
        delay = 0.03 / speed

        for char in text:
            self.controller.press(char)
            self.controller.release(char)
            time.sleep(delay)
