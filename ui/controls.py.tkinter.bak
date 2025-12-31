"""
Control Panel Module
Console output, control buttons, speed slider, and debug panel
"""
import tkinter as tk
from tkinter import ttk
import datetime


class ControlPanel(tk.Frame):
    """Control panel with console, buttons, and debug features"""

    def __init__(self, parent, callbacks, **kwargs):
        """
        Initialize control panel

        Args:
            parent: Parent widget
            callbacks: Dict of callback functions {execute, pause, stop, etc.}
            **kwargs: Additional frame arguments
        """
        super().__init__(parent, **kwargs)

        self.callbacks = callbacks

        # Variables
        self.speed_var = tk.DoubleVar(value=1.0)
        self.iterations_var = tk.IntVar(value=1)

        # Debug panel visibility
        self.debug_panel_visible = False

        self._build_ui()

    def _build_ui(self):
        """Build control panel UI"""
        # Console section
        console_frame = tk.Frame(self)
        console_frame.pack(fill='both', expand=True, padx=10, pady=5)

        ttk.Label(console_frame, text="Console :").pack(anchor='w')

        # Console with scrollbar
        console_container = tk.Frame(console_frame)
        console_container.pack(fill='both', expand=True)

        self.console = tk.Text(
            console_container,
            height=10,
            state='disabled',
            bg='#222',
            fg='#0f0',
            font=('Consolas', 10),
            wrap='word'
        )
        self.console.pack(side='left', fill='both', expand=True)

        console_scrollbar = ttk.Scrollbar(console_container, command=self.console.yview)
        console_scrollbar.pack(side='right', fill='y')
        self.console.config(yscrollcommand=console_scrollbar.set)

        # Control buttons section
        controls = ttk.Frame(self)
        controls.pack(fill='x', pady=5, padx=10)

        # Speed control
        ttk.Label(controls, text="Vitesse :").pack(side='left', padx=5)
        ttk.Scale(
            controls,
            from_=0.1,
            to=5.0,
            variable=self.speed_var,
            orient='horizontal',
            length=150
        ).pack(side='left', fill='x', expand=False, padx=5)

        ttk.Label(controls, textvariable=self.speed_var, width=4).pack(side='left')

        # Iterations control
        ttk.Label(controls, text="Itérations :").pack(side='left', padx=(20, 5))
        ttk.Entry(
            controls,
            textvariable=self.iterations_var,
            width=6
        ).pack(side='left', padx=5)

        # Spacer
        tk.Frame(controls).pack(side='left', fill='x', expand=True)

        # Execution buttons
        self.btn_execute = ttk.Button(
            controls,
            text="▶ Exécuter",
            command=lambda: self._call('execute')
        )
        self.btn_execute.pack(side='right', padx=2)

        self.btn_pause = ttk.Button(
            controls,
            text="⏸ Pause",
            command=lambda: self._call('pause')
        )
        self.btn_pause.pack(side='right', padx=2)

        self.btn_stop = ttk.Button(
            controls,
            text="⏹ Arrêter",
            command=lambda: self._call('stop')
        )
        self.btn_stop.pack(side='right', padx=2)

        # Debug panel (initially hidden)
        self.debug_frame = tk.Frame(self, relief='sunken', borderwidth=1)
        self._build_debug_panel()

    def _build_debug_panel(self):
        """Build debug panel (hidden by default)"""
        ttk.Label(self.debug_frame, text="Debug Mode", font=('Arial', 10, 'bold')).pack(anchor='w', padx=5, pady=5)

        # Debug buttons
        debug_buttons = ttk.Frame(self.debug_frame)
        debug_buttons.pack(fill='x', padx=5, pady=5)

        ttk.Button(
            debug_buttons,
            text="⏭ Step",
            command=lambda: self._call('step_next')
        ).pack(side='left', padx=2)

        ttk.Button(
            debug_buttons,
            text="🔴 Toggle Breakpoint",
            command=lambda: self._call('toggle_breakpoint')
        ).pack(side='left', padx=2)

        ttk.Button(
            debug_buttons,
            text="Clear Breakpoints",
            command=lambda: self._call('clear_breakpoints')
        ).pack(side='left', padx=2)

        # Variable inspector
        inspector_frame = tk.Frame(self.debug_frame)
        inspector_frame.pack(fill='both', expand=True, padx=5, pady=5)

        ttk.Label(inspector_frame, text="Variables:").pack(anchor='w')

        # Variable list with scrollbar
        var_container = tk.Frame(inspector_frame)
        var_container.pack(fill='both', expand=True)

        self.variable_list = tk.Text(
            var_container,
            height=5,
            state='disabled',
            bg='#f9f9f9',
            font=('Consolas', 9),
            wrap='none'
        )
        self.variable_list.pack(side='left', fill='both', expand=True)

        var_scrollbar = ttk.Scrollbar(var_container, command=self.variable_list.yview)
        var_scrollbar.pack(side='right', fill='y')
        self.variable_list.config(yscrollcommand=var_scrollbar.set)

    def _call(self, callback_name):
        """Call a callback if it exists"""
        if callback_name in self.callbacks:
            self.callbacks[callback_name]()

    def log(self, message):
        """
        Log message to console

        Args:
            message: Message to log
        """
        timestamp = datetime.datetime.now().strftime('%H:%M:%S')
        formatted = f"[{timestamp}] {message}\n"

        self.console.config(state='normal')
        self.console.insert('end', formatted)
        self.console.see('end')
        self.console.config(state='disabled')

    def clear_console(self):
        """Clear console output"""
        self.console.config(state='normal')
        self.console.delete('1.0', 'end')
        self.console.config(state='disabled')

    def get_speed(self):
        """Get speed multiplier"""
        return self.speed_var.get()

    def get_iterations(self):
        """Get iteration count"""
        return self.iterations_var.get()

    def show_debug_panel(self, show=True):
        """
        Show or hide debug panel

        Args:
            show: True to show, False to hide
        """
        if show and not self.debug_panel_visible:
            self.debug_frame.pack(fill='x', padx=10, pady=5, before=self.winfo_children()[0])
            self.debug_panel_visible = True
        elif not show and self.debug_panel_visible:
            self.debug_frame.pack_forget()
            self.debug_panel_visible = False

    def update_variables(self, variables):
        """
        Update variable inspector

        Args:
            variables: Dict of variables to display
        """
        self.variable_list.config(state='normal')
        self.variable_list.delete('1.0', 'end')

        if variables:
            for var_name, var_value in sorted(variables.items()):
                self.variable_list.insert('end', f"{var_name} = {var_value}\n")
        else:
            self.variable_list.insert('end', "(No variables)")

        self.variable_list.config(state='disabled')
