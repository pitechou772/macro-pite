"""
Script Parser Module
Parses the DSL macro language into an action tree
Supports: variables, loops, conditions, functions, breakpoints
"""
from utils.safe_eval import safe_eval_expr


class ScriptParser:
    """Parses macro scripts into executable action trees"""

    def __init__(self, context):
        """
        Initialize parser

        Args:
            context: ExecutionContext instance for variable storage
        """
        self.context = context

    def parse(self, script):
        """
        Parse a macro script

        Args:
            script: Script text to parse

        Returns:
            List of actions (action tree)
        """
        raw_lines = script.splitlines()
        lines = []

        # First pass: extract variables and prepare lines
        for line_num, raw in enumerate(raw_lines, 1):
            if not raw.strip() or raw.strip().startswith('#'):
                continue

            indent = len(raw) - len(raw.lstrip(' '))
            line = raw.strip()

            # Handle variable declarations
            if line.startswith('$') and '=' in line:
                name, expr = line.split('=', 1)
                name = name.strip()
                expr = expr.strip()

                # Special case: input command
                if expr.strip().startswith('input,'):
                    input_parts = expr.split(',', 1)
                    if len(input_parts) > 1:
                        prompt = input_parts[1].strip().strip('"')
                        action_line = f"input_var,{name},{prompt}"
                        lines.append((indent, action_line, line_num))
                    continue

                # Evaluate expression with known variables
                try:
                    value = safe_eval_expr(expr, self.context.variables)
                    self.context.set_variable(name, value)
                except Exception:
                    # If evaluation fails, store as string
                    self.context.set_variable(name, expr)
                continue

            # Add line with line number for debug tracking
            lines.append((indent, line, line_num))

        # Second pass: build action tree
        actions, _ = self._parse_block(lines, 0, 0)
        return actions

    def _parse_block(self, lines, start, base_indent):
        """
        Recursively parse a block of indented lines

        Args:
            lines: List of (indent, line, line_num) tuples
            start: Starting index
            base_indent: Base indentation level

        Returns:
            Tuple of (actions list, next index)
        """
        actions = []
        i = start

        while i < len(lines):
            indent, line, line_num = lines[i]

            # If indent is less than base, we've exited this block
            if indent < base_indent:
                break

            parts = [p.strip() for p in line.split(',')]
            cmd = parts[0].lower()

            # LOOP command
            if cmd == 'loop':
                loop_count = parts[1] if len(parts) > 1 else '1'
                infinite = loop_count.lower() == 'infinite'

                # Store as string - executor will resolve variables at runtime
                if infinite:
                    count = float('inf')
                else:
                    # Try to parse as number, otherwise keep as string (variable reference)
                    try:
                        count = float(loop_count)
                    except ValueError:
                        # It's a variable reference, keep as string
                        count = loop_count

                block, new_i = self._parse_block(lines, i + 1, indent + 1)
                actions.append(('LOOP', count, block, line_num))
                i = new_i

            # END LOOP markers
            elif cmd in ['endloop', 'next']:
                return actions, i + 1

            # WHILE command
            elif cmd == 'while':
                cond = ','.join(parts[1:]).strip()
                if not cond:
                    raise SyntaxError(f"While requires a condition at line {line_num}")

                block, new_i = self._parse_block(lines, i + 1, indent + 1)
                actions.append(('WHILE', cond, block, line_num))
                i = new_i

            # END WHILE marker
            elif cmd == 'endwhile':
                return actions, i + 1

            # IF command
            elif cmd == 'if':
                branches = []  # List of (condition, block) tuples
                cond = ','.join(parts[1:]).strip()
                if not cond:
                    raise SyntaxError(f"If requires a condition at line {line_num}")

                # Parse first if block
                block, new_i = self._parse_block(lines, i + 1, indent + 1)
                branches.append((cond, block, line_num))
                i = new_i

                # Look for elseif/else/endif at same indent level
                while i < len(lines):
                    sub_indent, sub_line, sub_line_num = lines[i]
                    if sub_indent < indent:
                        break

                    sub_parts = [p.strip() for p in sub_line.split(',')]
                    sub_cmd = sub_parts[0].lower()

                    if sub_cmd == 'elseif':
                        sub_cond = ','.join(sub_parts[1:]).strip()
                        b, ni = self._parse_block(lines, i + 1, sub_indent + 1)
                        branches.append((sub_cond, b, sub_line_num))
                        i = ni

                    elif sub_cmd == 'else':
                        b, ni = self._parse_block(lines, i + 1, sub_indent + 1)
                        branches.append(('else', b, sub_line_num))
                        i = ni

                    elif sub_cmd == 'endif':
                        i += 1
                        break
                    else:
                        break

                actions.append(('IF', branches, line_num))

            # END IF marker
            elif cmd == 'endif':
                return actions, i + 1

            # FUNCTION definition
            elif cmd == 'function':
                func_name = parts[1] if len(parts) > 1 else None
                if not func_name:
                    raise SyntaxError(f"Function requires a name at line {line_num}")

                # Remove parentheses if present (e.g., "heal()" -> "heal")
                func_name = func_name.replace('()', '')

                # Parse function body
                func_body, new_i = self._parse_block(lines, i + 1, indent + 1)

                # Register function in context
                self.context.register_function(func_name, func_body)

                i = new_i

            # END FUNCTION marker
            elif cmd == 'endfunction':
                return actions, i + 1

            # BREAK command
            elif cmd == 'break':
                actions.append(('BREAK', line_num))
                i += 1

            # CONTINUE command
            elif cmd == 'continue':
                actions.append(('CONTINUE', line_num))
                i += 1

            # BREAKPOINT command (for debug mode)
            elif cmd == 'breakpoint':
                actions.append(('BREAKPOINT', line_num))
                i += 1

            # Function call (detect by presence of parentheses)
            elif '(' in line and ')' in line:
                func_name = line.split('(')[0].strip()
                # Check if function exists
                if self.context.get_function(func_name):
                    actions.append(('CALL_FUNCTION', func_name, line_num))
                    i += 1
                else:
                    # Not a function call, treat as regular action
                    actions.append((line, line_num))
                    i += 1

            # Regular action/command
            else:
                actions.append((line, line_num))
                i += 1

        return actions, i

    def validate_syntax(self, script):
        """
        Validate script syntax without executing

        Args:
            script: Script text to validate

        Returns:
            Tuple of (is_valid, error_message)
        """
        try:
            self.parse(script)
            return (True, "Syntax OK")
        except SyntaxError as e:
            return (False, str(e))
        except Exception as e:
            return (False, f"Validation error: {e}")
