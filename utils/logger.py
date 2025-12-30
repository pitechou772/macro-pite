"""
Logging Utilities Module
Centralized logging with timestamps and levels
"""
import datetime


class MacroLogger:
    """Centralized logger for macro execution"""

    def __init__(self, callback=None):
        """
        Initialize logger

        Args:
            callback: Optional GUI callback function for displaying logs
        """
        self.callback = callback
        self.history = []

    def log(self, message, level="INFO"):
        """
        Log a message with timestamp and level

        Args:
            message: Message to log
            level: Log level (INFO, ERROR, DEBUG, ECHO)
        """
        timestamp = datetime.datetime.now().strftime('%H:%M:%S')
        formatted_message = f"[{timestamp}] {message}"

        self.history.append((timestamp, level, message))

        if self.callback:
            self.callback(formatted_message)

    def log_command(self, command):
        """Log an executed command"""
        self.log(command, "INFO")

    def log_error(self, message):
        """Log an error message"""
        self.log(f"[ERREUR] {message}", "ERROR")

    def log_debug(self, message, variables=None):
        """
        Log debug information with optional variable state

        Args:
            message: Debug message
            variables: Optional dict of variables to display
        """
        if variables:
            vars_str = ", ".join([f"{k}={v}" for k, v in variables.items()])
            self.log(f"[DEBUG] {message} | Variables: {vars_str}", "DEBUG")
        else:
            self.log(f"[DEBUG] {message}", "DEBUG")

    def get_history(self):
        """Get log history"""
        return self.history

    def clear(self):
        """Clear log history"""
        self.history = []
