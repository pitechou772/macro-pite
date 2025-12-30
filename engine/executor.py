"""
Macro Executor Module
Executes parsed action trees with support for debug mode, functions, and advanced conditions
"""
import threading
import time
from commands.keyboard import KeyboardCommands
from commands.mouse import MouseCommands
from commands.control import ControlCommands
from utils.color import PixelDetector
from utils.safe_eval import safe_eval_expr


class MacroExecutor:
    """Executes macro action trees"""

    def __init__(self, context, gui_callback=None):
        """
        Initialize executor

        Args:
            context: ExecutionContext instance
            gui_callback: Optional GUI callback for user interaction
        """
        self.context = context
        self.gui_callback = gui_callback

        # Command modules
        self.kb_commands = KeyboardCommands()
        self.mouse_commands = MouseCommands()
        self.ctrl_commands = ControlCommands()
        self.pixel_detector = PixelDetector()

        # Control events
        self.stop_event = threading.Event()
        self.pause_event = threading.Event()

        # Debug mode
        self.debug_mode = False
        self.breakpoints = set()          # Set of line numbers
        self.current_line = 0
        self.step_mode = False
        self.step_event = threading.Event()

    def execute(self, actions, speed=1.0, log_callback=None):
        """
        Execute an action tree

        Args:
            actions: List of actions from parser
            speed: Speed multiplier
            log_callback: Optional logging callback
        """
        try:
            # Update special variables
            self.context.set_special_var('@speed', speed)

            # Update system variables
            self.context.update_system_vars()

            # Execute actions
            self._execute_actions(actions, {}, speed, log_callback)

            if log_callback:
                log_callback("✅ Macro terminée" if not self.stop_event.is_set() else "⏹ Macro arrêtée")

        except Exception as e:
            if log_callback:
                log_callback(f"[ERREUR GLOBALE] {e}")

    def _execute_actions(self, actions, loop_vars, speed, log_callback):
        """
        Recursively execute actions with control flow

        Args:
            actions: List of actions to execute
            loop_vars: Current loop variables
            speed: Speed multiplier
            log_callback: Logging callback

        Returns:
            'BREAK' or 'CONTINUE' if encountered, None otherwise
        """
        i = 0
        while i < len(actions):
            # Check for stop signal
            if self.stop_event.is_set():
                return

            # Handle pause
            while self.pause_event.is_set():
                time.sleep(0.1)

            action = actions[i]

            # Extract line number if present
            if isinstance(action, tuple) and len(action) >= 2:
                line_num = action[-1]  # Last element is always line number
                self.current_line = line_num
            else:
                line_num = None

            # Debug mode: check for breakpoint
            if self.debug_mode and line_num and line_num in self.breakpoints:
                self.step_mode = True
                if self.gui_callback and hasattr(self.gui_callback, 'on_breakpoint_hit'):
                    self.gui_callback.on_breakpoint_hit(line_num, self.context.get_all_variables())

            # Debug mode: wait for step signal
            if self.debug_mode and self.step_mode:
                if log_callback:
                    log_callback(f"[DEBUG] Paused at line {line_num}")
                self.step_event.wait()
                self.step_event.clear()

            # Handle control structures (tuples)
            if isinstance(action, tuple):
                cmd_type = action[0]

                # LOOP
                if cmd_type == 'LOOP':
                    count, block = action[1], action[2]

                    # Resolve count if it's a variable reference
                    if isinstance(count, str) and count.startswith('$'):
                        # Replace variable
                        count_str = self.context.replace_variables(count)
                        try:
                            count = float(count_str)
                        except ValueError:
                            if log_callback:
                                log_callback(f"[ERREUR] Loop count variable '{count}' invalid: {count_str}")
                            count = 1  # Default to 1 iteration

                    # Infinite loop
                    if count == float('inf'):
                        idx = 0
                        while not self.stop_event.is_set():
                            lv = dict(loop_vars)
                            lv['$i'] = str(idx)
                            self.context.loop_vars = lv

                            result = self._execute_actions(block, lv, speed, log_callback)
                            if result == 'BREAK':
                                break
                            idx += 1
                    # Finite loop
                    else:
                        for idx in range(int(count)):
                            if self.stop_event.is_set():
                                break

                            lv = dict(loop_vars)
                            lv['$i'] = str(idx)
                            self.context.loop_vars = lv

                            result = self._execute_actions(block, lv, speed, log_callback)
                            if result == 'BREAK':
                                break

                    i += 1
                    continue

                # WHILE
                elif cmd_type == 'WHILE':
                    cond, block = action[1], action[2]
                    loops = 0

                    while True:
                        if self.stop_event.is_set():
                            return

                        # Update system variables for condition evaluation
                        self.context.update_system_vars()

                        # Evaluate condition
                        try:
                            cond_eval = self._evaluate_condition(cond)
                        except Exception as e:
                            if log_callback:
                                log_callback(f"[ERREUR] Condition WHILE invalide: {cond} -> {e}")
                            break

                        if not cond_eval:
                            break

                        result = self._execute_actions(block, loop_vars, speed, log_callback)
                        if result == 'BREAK':
                            break

                        loops += 1
                        # Safety limit
                        if loops > 100000:
                            if log_callback:
                                log_callback("[ERREUR] Boucle WHILE trop longue, coupée")
                            break

                    i += 1
                    continue

                # IF
                elif cmd_type == 'IF':
                    branches = action[1]
                    executed = False

                    for cond, block, _line in branches:
                        if cond == 'else':
                            if not executed:
                                self._execute_actions(block, loop_vars, speed, log_callback)
                                executed = True
                                break
                        else:
                            # Update system variables
                            self.context.update_system_vars()

                            try:
                                cond_eval = self._evaluate_condition(cond)
                            except Exception as e:
                                if log_callback:
                                    log_callback(f"[ERREUR] Condition IF invalide: {cond} -> {e}")
                                cond_eval = False

                            if cond_eval:
                                self._execute_actions(block, loop_vars, speed, log_callback)
                                executed = True
                                break

                    i += 1
                    continue

                # BREAK
                elif cmd_type == 'BREAK':
                    return 'BREAK'

                # CONTINUE
                elif cmd_type == 'CONTINUE':
                    return 'CONTINUE'

                # BREAKPOINT (debug mode)
                elif cmd_type == 'BREAKPOINT':
                    if self.debug_mode:
                        self.step_mode = True
                        if self.gui_callback and hasattr(self.gui_callback, 'on_breakpoint_hit'):
                            self.gui_callback.on_breakpoint_hit(line_num, self.context.get_all_variables())
                    i += 1
                    continue

                # CALL_FUNCTION
                elif cmd_type == 'CALL_FUNCTION':
                    func_name = action[1]
                    func_body = self.context.get_function(func_name)

                    if func_body:
                        if log_callback:
                            log_callback(f"[FUNCTION] Calling {func_name}()")

                        self._execute_actions(func_body, loop_vars, speed, log_callback)
                    else:
                        if log_callback:
                            log_callback(f"[ERREUR] Function '{func_name}' not found")

                    i += 1
                    continue

            # String action (command)
            if isinstance(action, tuple) and len(action) == 2:
                line, line_num = action
            else:
                line = action
                line_num = None

            # Replace variables
            self.context.update_system_vars()
            line = self.context.replace_variables(line)

            if log_callback:
                log_callback(f"{line}")

            # Execute command
            try:
                self._execute_command(line, speed, log_callback)
            except Exception as e:
                if log_callback:
                    log_callback(f"[ERREUR] {line} → {e}")

            i += 1

    def _execute_command(self, line, speed, log_callback):
        """
        Execute a single command

        Args:
            line: Command line
            speed: Speed multiplier
            log_callback: Logging callback
        """
        parts = [p.strip() for p in line.split(',')]
        cmd = parts[0].lower()

        # Keyboard commands
        if cmd == 'press':
            keys_str = parts[1]
            dur_str = parts[2]
            duration = float(dur_str)
            self.kb_commands.press(keys_str, duration, speed)

        elif cmd == 'hotkey':
            keys_str = parts[1]
            self.kb_commands.hotkey(keys_str)

        elif cmd == 'type':
            text = parts[1]
            self.kb_commands.type_text(text, speed)

        # Mouse commands
        elif cmd in ['lmc', 'rmc', 'mmc']:
            self.mouse_commands.click_button(cmd)

        elif cmd == 'click':
            x, y = int(parts[1]), int(parts[2])
            btn = parts[3] if len(parts) > 3 else 'left'
            self.mouse_commands.click_at(x, y, btn)

        elif cmd == 'move':
            x, y = int(parts[1]), int(parts[2])
            self.mouse_commands.move(x, y)

        elif cmd == 'drag':
            x1, y1 = int(parts[1]), int(parts[2])
            x2, y2 = int(parts[3]), int(parts[4])
            self.mouse_commands.drag(x1, y1, x2, y2)

        elif cmd == 'scroll':
            direction = parts[1]
            amount = int(parts[2])
            self.mouse_commands.scroll(direction, amount)

        elif cmd == 'on':
            btn = parts[1]
            self.mouse_commands.button_down(btn)

        elif cmd == 'off':
            btn = parts[1]
            self.mouse_commands.button_up(btn)

        # Control commands
        elif cmd == 'wait':
            seconds = float(parts[1])
            self.ctrl_commands.wait(seconds, speed)

        elif cmd == 'echo':
            message = ','.join(parts[1:])
            self.ctrl_commands.echo(message, log_callback)

        elif cmd == 'input' or cmd == 'input_var':
            # Handle both: input,"prompt",$var and input_var,$var,"prompt"
            if cmd == 'input_var':
                var_name = parts[1].strip()
                prompt = parts[2].strip().strip('"') if len(parts) > 2 else "Enter value"
            else:
                prompt = parts[1].strip('"')
                var_name = parts[2] if len(parts) > 2 else None

            # Ask for input via GUI callback
            if self.gui_callback and hasattr(self.gui_callback, 'ask_input'):
                val = self.gui_callback.ask_input(prompt)
            else:
                val = input(f"{prompt}: ")

            if val is None:
                val = ""

            if var_name and var_name.startswith('$'):
                self.context.set_variable(var_name, val)
                if log_callback:
                    log_callback(f"[INPUT] {var_name} = {val}")

        else:
            if log_callback:
                log_callback(f"[UNKNOWN CMD] {cmd}")

    def _evaluate_condition(self, condition):
        """
        Evaluate a condition (including pixel, exists)

        Args:
            condition: Condition string

        Returns:
            Boolean result
        """
        # Replace variables in condition
        cond_text = self.context.replace_variables(condition)

        # Check for special conditions
        parts = [p.strip() for p in cond_text.split(',')]

        # pixel,x,y,#RRGGBB
        if parts[0].lower() == 'pixel' and len(parts) >= 4:
            x, y = int(parts[1]), int(parts[2])
            color = parts[3]
            tolerance = int(parts[4]) if len(parts) > 4 else 10
            return self.pixel_detector.check_pixel(x, y, color, tolerance)

        # exists,$var
        if parts[0].lower() == 'exists' and len(parts) >= 2:
            var_name = parts[1]
            return self.context.variable_exists(var_name)

        # Standard expression
        return bool(safe_eval_expr(cond_text, {}))

    # Control methods
    def stop(self):
        """Stop execution"""
        self.stop_event.set()

    def pause(self):
        """Pause execution"""
        self.pause_event.set()

    def resume(self):
        """Resume execution"""
        self.pause_event.clear()

    # Debug methods
    def enable_debug_mode(self, enabled=True):
        """Enable or disable debug mode"""
        self.debug_mode = enabled

    def add_breakpoint(self, line_number):
        """Add a breakpoint at line number"""
        self.breakpoints.add(line_number)

    def remove_breakpoint(self, line_number):
        """Remove a breakpoint"""
        self.breakpoints.discard(line_number)

    def clear_breakpoints(self):
        """Clear all breakpoints"""
        self.breakpoints.clear()

    def step_next(self):
        """Step to next instruction in debug mode"""
        self.step_event.set()

    def get_current_state(self):
        """
        Get current execution state for debugging

        Returns:
            Dict with current line, variables, etc.
        """
        return {
            'line': self.current_line,
            'variables': self.context.get_all_variables(),
            'breakpoints': list(self.breakpoints),
            'debug_mode': self.debug_mode,
            'step_mode': self.step_mode
        }
