"""
Auto-Completion System for Macro DSL
Provides intelligent command and variable suggestions
"""
from PyQt5.Qsci import QsciAPIs


class MacroAutoComplete:
    """Auto-completion system for macro DSL"""

    def __init__(self, lexer):
        """
        Initialize auto-completion

        Args:
            lexer: The MacroDSLLexer instance
        """
        self.api = QsciAPIs(lexer)
        self._load_commands()
        self._load_variables()
        self._load_settings()
        self.api.prepare()

    def _load_commands(self):
        """Load all macro commands with signatures"""
        commands = {
            # Keyboard commands
            'press,key': 'Press a keyboard key',
            'press,key,duration': 'Press and hold a key for duration (ms)',
            'hotkey,key1+key2': 'Press keyboard shortcut (e.g., ctrl+c)',
            'type,text': 'Type text string',
            'keydown,key': 'Hold key down',
            'keyup,key': 'Release key',

            # Mouse commands
            'click,x,y': 'Click at position',
            'click,x,y,button': 'Click at position with button (left/right/middle)',
            'lmc': 'Quick left mouse click',
            'rmc': 'Quick right mouse click',
            'mmc': 'Quick middle mouse click',
            'mousemove,x,y': 'Move mouse to position',
            'mousemove,x,y,duration': 'Move mouse smoothly over duration (ms)',
            'drag,x1,y1,x2,y2': 'Drag from position to position',
            'scroll,direction,amount': 'Scroll mouse wheel (up/down)',

            # Control commands
            'wait,milliseconds': 'Wait/pause for duration',
            'echo,message': 'Print message to console',
            'input,prompt': 'Ask user for input',

            # Loop commands
            'loop,count': 'Start loop block (count times)',
            'loop,infinite': 'Start infinite loop',
            'endloop': 'End loop block',
            'next': 'Alternative end loop marker',
            'break': 'Exit loop early',
            'continue': 'Skip to next iteration',

            # While loop
            'while,condition': 'Start while loop',
            'endwhile': 'End while loop',

            # Conditional commands
            'if,condition': 'Start conditional block',
            'elseif,condition': 'Else-if branch',
            'else': 'Else branch',
            'endif': 'End conditional block',

            # Function commands
            'function,name': 'Define function',
            'endfunction': 'End function definition',
            'call,function_name': 'Call defined function',
            'return': 'Return from function',

            # Debug commands
            'breakpoint': 'Debug breakpoint',
        }

        for cmd, description in commands.items():
            # Add command with description as tooltip
            self.api.add(f"{cmd}  # {description}")

    def _load_variables(self):
        """Load system variables"""
        variables = [
            ('$mouse_x', 'Current mouse X position'),
            ('$mouse_y', 'Current mouse Y position'),
            ('$screen_width', 'Screen width in pixels'),
            ('$screen_height', 'Screen height in pixels'),
            ('$timestamp', 'Current timestamp'),
            ('$random', 'Random number'),
            ('$i', 'Loop counter variable'),
        ]
        for var, desc in variables:
            self.api.add(f"{var}  # {desc}")

    def _load_settings(self):
        """Load settings/decorators"""
        settings = [
            ('@speed', 'Execution speed multiplier'),
            ('@iterations', 'Number of macro iterations'),
            ('@delay', 'Delay between actions'),
            ('@retry', 'Retry attempts on failure'),
        ]
        for setting, desc in settings:
            self.api.add(f"{setting}  # {desc}")

    def add_user_function(self, function_name):
        """
        Dynamically add user-defined function to autocomplete

        Args:
            function_name: Name of the function to add
        """
        self.api.add(f"call,{function_name}")
        self.api.prepare()

    def add_user_variable(self, variable_name):
        """
        Dynamically add user-defined variable

        Args:
            variable_name: Name of the variable (with $ prefix)
        """
        if not variable_name.startswith('$'):
            variable_name = f"${variable_name}"
        self.api.add(variable_name)
        self.api.prepare()
