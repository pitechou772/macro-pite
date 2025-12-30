"""
Mouse Commands Module
Handles all mouse-related macro commands
"""
from pynput.mouse import Controller as MController, Button
import time


class MouseCommands:
    """Executes mouse commands"""

    def __init__(self):
        """Initialize mouse controller"""
        self.controller = MController()

    def click_button(self, button_name):
        """
        Click a mouse button at current position

        Args:
            button_name: 'lmc', 'rmc', or 'mmc'
        """
        button_map = {
            'lmc': Button.left,
            'rmc': Button.right,
            'mmc': Button.middle
        }

        button = button_map.get(button_name, Button.left)
        self._click(button)

    def click_at(self, x, y, button_name='left'):
        """
        Move to position and click

        Args:
            x: X coordinate
            y: Y coordinate
            button_name: 'left', 'right', or 'middle'
        """
        # Move to position
        self.controller.position = (x, y)

        # Map button name
        button_map = {
            'left': Button.left,
            'right': Button.right,
            'middle': Button.middle
        }

        button = button_map.get(button_name, Button.left)
        self._click(button)

    def move(self, x, y):
        """
        Move mouse to position

        Args:
            x: X coordinate
            y: Y coordinate
        """
        self.controller.position = (x, y)

    def drag(self, x1, y1, x2, y2):
        """
        Drag from (x1, y1) to (x2, y2) with smooth interpolation

        Args:
            x1: Start X coordinate
            y1: Start Y coordinate
            x2: End X coordinate
            y2: End Y coordinate
        """
        # Move to start position
        self.controller.position = (x1, y1)
        time.sleep(0.05)

        # Press left button
        self.controller.press(Button.left)
        time.sleep(0.05)

        # Smooth dragging with interpolation
        steps = 10
        for i in range(steps + 1):
            t = i / steps
            x = int(x1 + (x2 - x1) * t)
            y = int(y1 + (y2 - y1) * t)
            self.controller.position = (x, y)
            time.sleep(0.01)

        # Release button
        self.controller.release(Button.left)
        time.sleep(0.05)

    def scroll(self, direction, amount):
        """
        Scroll mouse wheel

        Args:
            direction: 'up' or 'down'
            amount: Number of scroll units
        """
        scroll_amount = amount if direction == 'up' else -amount
        self.controller.scroll(0, scroll_amount)

    def button_down(self, button_name):
        """
        Press and hold a mouse button

        Args:
            button_name: 'lmc', 'left', 'rmc', 'right'
        """
        button = Button.left if button_name in ['lmc', 'left'] else Button.right
        self.controller.press(button)

    def button_up(self, button_name):
        """
        Release a mouse button

        Args:
            button_name: 'lmc', 'left', 'rmc', 'right'
        """
        button = Button.left if button_name in ['lmc', 'left'] else Button.right
        self.controller.release(button)

    def get_position(self):
        """
        Get current mouse position

        Returns:
            Tuple of (x, y) coordinates
        """
        return self.controller.position

    def _click(self, button):
        """Internal helper to perform a click"""
        self.controller.press(button)
        time.sleep(0.05)
        self.controller.release(button)
