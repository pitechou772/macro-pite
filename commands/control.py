"""
Control Commands Module
Handles control flow and utility commands
"""
import time


class ControlCommands:
    """Executes control commands"""

    def __init__(self):
        """Initialize control commands"""
        pass

    def wait(self, seconds, speed=1.0):
        """
        Wait for a specified duration

        Args:
            seconds: Duration to wait in seconds
            speed: Speed multiplier
        """
        actual_duration = seconds / speed
        time.sleep(actual_duration)

    def echo(self, message, log_callback=None):
        """
        Log a message to console

        Args:
            message: Message to log
            log_callback: Optional callback function for logging
        """
        if log_callback:
            log_callback(f"[ECHO] {message}")
