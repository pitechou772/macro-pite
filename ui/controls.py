"""
Control Panel Module (PyQt5 version)
Console output, control buttons, speed slider, and debug panel
"""
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QTextEdit, QPushButton, QSlider, QSpinBox, QFrame)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor, QPalette
import datetime


class ControlPanel(QWidget):
    """Control panel with console, buttons, and debug features"""

    def __init__(self, parent, callbacks):
        """
        Initialize control panel

        Args:
            parent: Parent widget
            callbacks: Dict of callback functions {execute, pause, stop, etc.}
        """
        super().__init__(parent)

        self.callbacks = callbacks

        # Variables
        self.speed_value = 1.0
        self.iterations_value = 1

        # Debug panel visibility
        self.debug_panel_visible = False

        self._build_ui()

    def _build_ui(self):
        """Build control panel UI"""
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 5, 10, 5)

        # Console section
        console_label = QLabel("Console:")
        layout.addWidget(console_label)

        # Console text area with dark theme
        self.console = QTextEdit()
        self.console.setReadOnly(True)
        self.console.setMinimumHeight(150)
        self.console.setMaximumHeight(250)
        self.console.setFont(QFont("Consolas", 10))

        # Dark console theme
        palette = self.console.palette()
        palette.setColor(QPalette.Base, QColor("#222222"))
        palette.setColor(QPalette.Text, QColor("#00FF00"))
        self.console.setPalette(palette)

        layout.addWidget(self.console)

        # Control buttons section
        controls_layout = QHBoxLayout()

        # Speed control
        controls_layout.addWidget(QLabel("Vitesse:"))

        self.speed_slider = QSlider(Qt.Horizontal)
        self.speed_slider.setMinimum(1)  # 0.1x
        self.speed_slider.setMaximum(50)  # 5.0x
        self.speed_slider.setValue(10)  # 1.0x
        self.speed_slider.setTickPosition(QSlider.TicksBelow)
        self.speed_slider.setTickInterval(5)
        self.speed_slider.setMinimumWidth(150)
        self.speed_slider.valueChanged.connect(self._update_speed_label)
        controls_layout.addWidget(self.speed_slider)

        self.speed_label = QLabel("1.0")
        self.speed_label.setMinimumWidth(40)
        controls_layout.addWidget(self.speed_label)

        # Iterations control
        controls_layout.addWidget(QLabel("Itérations:"))

        self.iterations_spin = QSpinBox()
        self.iterations_spin.setMinimum(1)
        self.iterations_spin.setMaximum(99999)
        self.iterations_spin.setValue(1)
        self.iterations_spin.setMinimumWidth(60)
        self.iterations_spin.valueChanged.connect(self._update_iterations)
        controls_layout.addWidget(self.iterations_spin)

        # Spacer
        controls_layout.addStretch()

        # Execution buttons
        self.btn_stop = QPushButton("⏹ Arrêter")
        self.btn_stop.clicked.connect(lambda: self._call('stop'))
        controls_layout.addWidget(self.btn_stop)

        self.btn_pause = QPushButton("⏸ Pause")
        self.btn_pause.clicked.connect(lambda: self._call('pause'))
        controls_layout.addWidget(self.btn_pause)

        self.btn_execute = QPushButton("▶ Exécuter")
        self.btn_execute.clicked.connect(lambda: self._call('execute'))
        controls_layout.addWidget(self.btn_execute)

        layout.addLayout(controls_layout)

        # Debug panel (initially hidden)
        self.debug_frame = QFrame()
        self.debug_frame.setFrameStyle(QFrame.StyledPanel | QFrame.Sunken)
        self._build_debug_panel()
        self.debug_frame.hide()

        layout.addWidget(self.debug_frame)

        self.setLayout(layout)

    def _build_debug_panel(self):
        """Build debug panel (hidden by default)"""
        layout = QVBoxLayout()

        # Debug label
        debug_label = QLabel("Debug Mode")
        debug_label.setFont(QFont("Arial", 10, QFont.Bold))
        layout.addWidget(debug_label)

        # Debug buttons
        debug_buttons_layout = QHBoxLayout()

        step_btn = QPushButton("⏭ Step")
        step_btn.clicked.connect(lambda: self._call('step_next'))
        debug_buttons_layout.addWidget(step_btn)

        toggle_bp_btn = QPushButton("🔴 Toggle Breakpoint")
        toggle_bp_btn.clicked.connect(lambda: self._call('toggle_breakpoint'))
        debug_buttons_layout.addWidget(toggle_bp_btn)

        clear_bp_btn = QPushButton("Clear Breakpoints")
        clear_bp_btn.clicked.connect(lambda: self._call('clear_breakpoints'))
        debug_buttons_layout.addWidget(clear_bp_btn)

        debug_buttons_layout.addStretch()

        layout.addLayout(debug_buttons_layout)

        # Variable inspector
        var_label = QLabel("Variables:")
        layout.addWidget(var_label)

        self.variable_list = QTextEdit()
        self.variable_list.setReadOnly(True)
        self.variable_list.setMaximumHeight(100)
        self.variable_list.setFont(QFont("Consolas", 9))

        # Light theme for variables
        palette = self.variable_list.palette()
        palette.setColor(QPalette.Base, QColor("#F9F9F9"))
        palette.setColor(QPalette.Text, QColor("#000000"))
        self.variable_list.setPalette(palette)

        layout.addWidget(self.variable_list)

        self.debug_frame.setLayout(layout)

    def _update_speed_label(self, value):
        """Update speed label when slider changes"""
        self.speed_value = value / 10.0
        self.speed_label.setText(f"{self.speed_value:.1f}")

    def _update_iterations(self, value):
        """Update iterations value"""
        self.iterations_value = value

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
        formatted = f"[{timestamp}] {message}"

        self.console.append(formatted)

        # Auto-scroll to bottom
        scrollbar = self.console.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def clear_console(self):
        """Clear console output"""
        self.console.clear()

    def get_speed(self):
        """Get speed multiplier"""
        return self.speed_value

    def get_iterations(self):
        """Get iteration count"""
        return self.iterations_value

    def show_debug_panel(self, show=True):
        """
        Show or hide debug panel

        Args:
            show: True to show, False to hide
        """
        if show:
            self.debug_frame.show()
            self.debug_panel_visible = True
        else:
            self.debug_frame.hide()
            self.debug_panel_visible = False

    def update_variables(self, variables):
        """
        Update variable inspector

        Args:
            variables: Dict of variables to display
        """
        self.variable_list.clear()

        if variables:
            for var_name, var_value in sorted(variables.items()):
                self.variable_list.append(f"{var_name} = {var_value}")
        else:
            self.variable_list.append("(No variables)")
