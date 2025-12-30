"""
Execution Context Module
Manages variables, functions, and system state during macro execution
"""
import tkinter as tk
from pynput.mouse import Controller as MController


class ExecutionContext:
    """Manages all state during macro execution"""

    def __init__(self):
        """Initialize execution context"""
        self.variables = {}           # User-defined variables ($name = value)
        self.loop_vars = {}           # Loop counters ($i)
        self.system_vars = {}         # System variables ($mouse_x, $mouse_y, etc.)
        self.special_vars = {}        # Special variables (@speed, @iterations)
        self.functions = {}           # Function definitions (name -> body)
        self._screen_size = None      # Cached screen size
        self._mouse_controller = MController()

    def set_variable(self, name, value):
        """Set a user variable"""
        self.variables[name] = value

    def get_variable(self, name, default=None):
        """Get a variable value (checks all variable types)"""
        # Check in order: loop vars, special vars, user vars, system vars
        if name in self.loop_vars:
            return self.loop_vars[name]
        if name in self.special_vars:
            return self.special_vars[name]
        if name in self.variables:
            return self.variables[name]
        if name in self.system_vars:
            return self.system_vars[name]
        return default

    def variable_exists(self, name):
        """Check if a variable exists"""
        return (name in self.variables or
                name in self.loop_vars or
                name in self.system_vars or
                name in self.special_vars)

    def update_system_vars(self):
        """Update system variables with current values"""
        # Get mouse position
        x, y = self._mouse_controller.position

        # Get screen size (cache it)
        if not self._screen_size:
            try:
                root = tk.Tk()
                root.withdraw()
                w = root.winfo_screenwidth()
                h = root.winfo_screenheight()
                root.destroy()
                self._screen_size = (w, h)
            except Exception:
                self._screen_size = (0, 0)

        w, h = self._screen_size

        # Update system variables
        self.system_vars = {
            '$mouse_x': int(x),
            '$mouse_y': int(y),
            '$screen_width': int(w),
            '$screen_height': int(h)
        }

    def replace_variables(self, text):
        """
        Replace all variables in text with their values

        Args:
            text: String containing variable references

        Returns:
            String with variables replaced
        """
        result = text

        # Replace all variable types
        all_vars = {}
        all_vars.update(self.variables)
        all_vars.update(self.loop_vars)
        all_vars.update(self.system_vars)
        all_vars.update(self.special_vars)

        for var_name, var_value in all_vars.items():
            result = result.replace(var_name, str(var_value))

        return result

    def register_function(self, name, body):
        """
        Register a function definition

        Args:
            name: Function name
            body: List of actions in the function
        """
        self.functions[name] = body

    def get_function(self, name):
        """
        Get a function body

        Args:
            name: Function name

        Returns:
            List of actions or None if not found
        """
        return self.functions.get(name)

    def set_loop_var(self, name, value):
        """Set a loop variable"""
        self.loop_vars[name] = value

    def set_special_var(self, name, value):
        """Set a special variable"""
        self.special_vars[name] = value

    def clear_loop_vars(self):
        """Clear loop variables"""
        self.loop_vars = {}

    def get_all_variables(self):
        """Get all variables for debugging"""
        all_vars = {}
        all_vars.update(self.variables)
        all_vars.update(self.loop_vars)
        all_vars.update(self.system_vars)
        all_vars.update(self.special_vars)
        return all_vars
