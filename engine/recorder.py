"""
Action Recorder Module
Records keyboard and mouse actions to generate DSL scripts
"""
from pynput import keyboard, mouse
import threading
import time


class ActionRecorder:
    """Records user actions and generates macro scripts"""

    def __init__(self):
        """Initialize recorder"""
        self.recording = False
        self.actions = []  # List of (timestamp, action_type, data) tuples
        self.start_time = None

        self.kb_listener = None
        self.mouse_listener = None

        self.last_mouse_move = None
        self.last_key_press = None

    def start_recording(self):
        """Start recording actions"""
        if self.recording:
            return

        self.recording = True
        self.actions = []
        self.start_time = time.time()

        # Start keyboard listener
        self.kb_listener = keyboard.Listener(
            on_press=self._on_key_press,
            on_release=self._on_key_release
        )
        self.kb_listener.start()

        # Start mouse listener
        self.mouse_listener = mouse.Listener(
            on_click=self._on_mouse_click,
            on_move=self._on_mouse_move
        )
        self.mouse_listener.start()

    def stop_recording(self):
        """Stop recording and return actions"""
        if not self.recording:
            return []

        self.recording = False

        # Stop listeners
        if self.kb_listener:
            self.kb_listener.stop()
        if self.mouse_listener:
            self.mouse_listener.stop()

        return self.actions

    def generate_script(self):
        """
        Generate DSL script from recorded actions

        Returns:
            Script text
        """
        if not self.actions:
            return "# No actions recorded"

        script_lines = ["# Recorded macro"]
        script_lines.append(f"# Total actions: {len(self.actions)}\n")

        prev_time = 0

        for timestamp, action_type, data in self.actions:
            # Calculate wait time
            wait_time = timestamp - prev_time
            if wait_time > 0.1:  # Only add significant waits
                script_lines.append(f"wait,{wait_time:.2f}")

            # Generate command based on action type
            if action_type == 'key_press':
                key_name, duration = data
                script_lines.append(f"press,{key_name},{duration:.2f}")

            elif action_type == 'mouse_click':
                x, y, button = data
                button_name = 'left' if button == mouse.Button.left else 'right'
                script_lines.append(f"click,{x},{y},{button_name}")

            elif action_type == 'mouse_move':
                x, y = data
                script_lines.append(f"move,{x},{y}")

            prev_time = timestamp

        return '\n'.join(script_lines)

    def _on_key_press(self, key):
        """Handle key press event"""
        if not self.recording:
            return

        timestamp = time.time() - self.start_time

        # Store key press time
        try:
            key_name = key.char if hasattr(key, 'char') else key.name
        except:
            key_name = str(key)

        self.last_key_press = (timestamp, key_name)

    def _on_key_release(self, key):
        """Handle key release event"""
        if not self.recording or not self.last_key_press:
            return

        timestamp = time.time() - self.start_time

        # Calculate press duration
        press_time, key_name = self.last_key_press
        duration = timestamp - press_time

        # Record action
        self.actions.append((press_time, 'key_press', (key_name, duration)))
        self.last_key_press = None

    def _on_mouse_click(self, x, y, button, pressed):
        """Handle mouse click event"""
        if not self.recording or not pressed:
            return

        timestamp = time.time() - self.start_time
        self.actions.append((timestamp, 'mouse_click', (x, y, button)))

    def _on_mouse_move(self, x, y):
        """Handle mouse move event"""
        if not self.recording:
            return

        timestamp = time.time() - self.start_time

        # Throttle mouse move events (record every 0.5 seconds)
        if self.last_mouse_move:
            last_time, _, _ = self.last_mouse_move
            if timestamp - last_time < 0.5:
                return

        self.actions.append((timestamp, 'mouse_move', (x, y)))
        self.last_mouse_move = (timestamp, x, y)

    def clear(self):
        """Clear recorded actions"""
        self.actions = []
