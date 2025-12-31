# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Macro Builder v4.0** is a desktop automation application with a custom Domain-Specific Language (DSL) for creating keyboard and mouse macros. The project recently underwent a major upgrade from Tkinter to PyQt5 with QScintilla, transforming it into a professional IDE with syntax highlighting, auto-completion, code folding, and real-time error detection.

## Running the Application

```bash
python main.py
```

**Dependencies:**
```bash
pip install PyQt5 QScintilla pynput
```

## Testing Features

Use the provided test file to see IDE features in action:
```bash
# Open test_ide_features.txt in the IDE to see:
# - Syntax highlighting
# - Code folding
# - Auto-completion examples
```

## Architecture Overview

### Two-Tier System: UI Layer + Execution Engine

**UI Layer (PyQt5/QScintilla):**
- `ui/window.py` - Main application window and orchestration
- `ui/editor.py` - QScintilla-based code editor with IDE features
- `ui/controls.py` - Control panel with console, buttons, speed/iteration controls
- `ui/lexer.py` - Custom QsciLexerCustom for DSL syntax highlighting
- `ui/autocomplete.py` - QsciAPIs configuration for command suggestions

**Execution Engine (unchanged during IDE upgrade):**
- `engine/parser.py` - Parses DSL script into action tree (handles variables, loops, conditionals, functions)
- `engine/executor.py` - Executes actions in separate thread with pause/stop/debug support
- `engine/context.py` - Manages execution context (variables, functions, special vars)
- `engine/recorder.py` - Records user actions and generates DSL scripts
- `engine/validator.py` - Real-time syntax validation with debounced checking

**Command Execution:**
- `commands/keyboard.py` - Keyboard commands via pynput
- `commands/mouse.py` - Mouse commands via pynput
- `commands/control.py` - Control flow (wait, echo)

### Critical Architectural Patterns

#### 1. Parser → Executor Separation
The parser (`engine/parser.py`) builds an action tree in two passes:
- **First pass**: Extract variables and evaluate declarations
- **Second pass**: Build recursive action tree with `_parse_block()`

Actions are tuples like `('LOOP', count, block, line_num)` or `('IF', branches, line_num)`. The executor interprets these tuples at runtime.

#### 2. Thread Safety for GUI Updates
Macro execution runs in a daemon thread. GUI callbacks (like `on_breakpoint_hit()`) are invoked from the executor thread. PyQt5 handles cross-thread signals/slots automatically, but any direct GUI updates from macros should use thread-safe mechanisms.

#### 3. Breakpoint System (1-indexed vs 0-indexed)
- **User-facing (parser, UI)**: Line numbers are 1-indexed
- **QScintilla markers**: Internally 0-indexed
- **Conversion**: Always happens in `ui/editor.py` margin click handler

Example:
```python
# User clicks margin at line 5 (displayed)
def _on_margin_clicked(self, margin, line, modifiers):
    if margin == 1:
        self.toggle_breakpoint(line + 1)  # Convert to 1-indexed
```

#### 4. Custom Lexer Token Matching
`ui/lexer.py` uses **ordered regex patterns** - order matters! System variables must be matched before user variables:
```python
patterns = [
    (r'#.*$', STYLE_COMMENT),                    # Comments first
    (r'"(?:[^"\\]|\\.)*"', STYLE_STRING),        # Strings
    (system_vars_pattern, STYLE_SYSTEM_VAR),     # $mouse_x BEFORE...
    (r'\$\w+', STYLE_VARIABLE),                  # ...generic $variables
    (keywords_pattern, STYLE_KEYWORD),           # Keywords
]
```

#### 5. Validator Debouncing
`engine/validator.py` uses QTimer with 500ms delay to avoid validating on every keystroke. This prevents UI lag while typing.

## DSL Language Specifics

### Variable Resolution Timing
Variables are resolved at different times:
- **Declaration time** (`$var = 10`): Evaluated during parsing
- **Runtime** (loop counts, conditionals): Evaluated by executor using `safe_eval_expr()`

Example:
```python
$count = 5        # Evaluated at parse time
loop,$count       # $count resolved at parse time → becomes loop,5
if,$count > 3     # $count > 3 evaluated at runtime by executor
```

### Special Variables
- `$i` - Loop counter (set by executor during loop execution)
- `@speed` - Global speed multiplier (read from UI controls)
- `@iterations` - Iteration count (read from UI controls)
- `$mouse_x`, `$mouse_y`, `$screen_width`, `$screen_height` - System variables

### Function Registration
Functions are registered in `ExecutionContext` during parsing:
```python
# Parser finds "function heal()"
self.context.register_function('heal', func_body)

# Later, "heal()" or "call,heal" triggers:
('CALL_FUNCTION', 'heal', line_num)
```

## File Backup Convention

During the PyQt5 migration, old Tkinter files were backed up with `.tkinter.bak` extension:
- `ui/editor.py.tkinter.bak`
- `ui/window.py.tkinter.bak`
- `ui/controls.py.tkinter.bak`
- `main.py.tkinter.bak`

These backups preserve the original Tkinter implementation if rollback is needed.

## Known Behavior & Edge Cases

### 1. Input Command Thread Safety
`ask_input()` in `ui/window.py` uses `QInputDialog` which must run on the main thread. The executor calls this from a background thread, so it returns immediately and may timeout.

### 2. Parser Line Number Tracking
The parser tracks line numbers through tuples: `(indent, line, line_num)`. This enables debug highlighting and error reporting. Always preserve `line_num` when creating action tuples.

### 3. QScintilla Margin Configuration
Margins are fixed:
- **Margin 0**: Line numbers (NumberMargin)
- **Margin 1**: Breakpoints and debug markers (SymbolMargin)
- **Margin 2+**: Available for future features (code folding indicators)

### 4. Validation vs Execution Parsers
There are effectively two parser instances:
- **Editor validator**: `engine/validator.py` creates parser for syntax checking
- **Execution**: `ui/window.py` creates fresh parser before running macro

This ensures validation doesn't pollute execution state.

## Common Development Scenarios

### Adding a New DSL Command

1. Add command handler to `commands/` (keyboard.py, mouse.py, or control.py)
2. Update parser to recognize command name (no changes needed if comma-separated)
3. Add to auto-completion in `ui/autocomplete.py`:
   ```python
   'newcommand,arg1,arg2': 'Description of command'
   ```
4. Add keyword to lexer in `ui/lexer.py` if it should be highlighted:
   ```python
   KEYWORDS = {'press', 'click', ..., 'newcommand'}
   ```

### Modifying Syntax Highlighting Colors

Edit `ui/lexer.py` in `_setup_styles()`:
```python
self.setColor(QColor("#0000FF"), self.STYLE_KEYWORD)  # Change color
self.setFont(QFont("Consolas", 10, QFont.Bold), self.STYLE_KEYWORD)  # Change font
```

### Debugging Parser Issues

The parser raises `SyntaxError` with line numbers. To debug:
1. Add logging in `engine/parser.py` → `_parse_block()`
2. Check action tree structure by printing `actions` before return
3. Validate action tuples match executor expectations in `engine/executor.py`

### Understanding Execution Flow

```
User clicks "Run" (F5)
    ↓
window.py: start_macro()
    ↓
parser.parse(script) → action tree
    ↓
executor.execute(actions, speed, log_callback)
    [runs in daemon thread]
    ↓
executor calls commands/keyboard.py, commands/mouse.py
    ↓
if breakpoint hit → window.on_breakpoint_hit() [cross-thread]
    ↓
editor highlights line, controls show variables
```

## Integration Points

### Adding New Auto-Completion Items
Modify `ui/autocomplete.py` → `_load_commands()` and call `api.prepare()` after changes.

### Customizing Error Messages
Update `engine/validator.py` → `_highlight_error_from_message()` to parse custom error formats.

### Extending Keyboard Shortcuts
Add to `ui/window.py` → `_build_menu()` using QKeySequence or raw strings like "F11".

## JSON File Format (v4.0)

```json
{
  "version": "4.0",
  "speed": 1.2,
  "script": "press,a\nwait,100",
  "metadata": {
    "created_at": "2025-01-01T12:00:00",
    "created_by": "Macro Builder v4.0",
    "iterations": 1
  }
}
```

Handled by `utils/file_io.py` → `FileManager` class.

## Security Considerations

- **No eval()**: Uses `ast` module via `utils/safe_eval.py` for expression evaluation
- **Thread termination**: Uses `Event` objects, not thread killing
- **Iteration limits**: Configurable to prevent infinite loops from freezing app
- **Stop button priority**: Always responsive via `threading.Event`

## UI/UX Conventions

- **French labels**: UI is in French ("Exécuter", "Vitesse", "Itérations")
- **Console colors**: Dark theme (black background, green text #00FF00)
- **Debug panel**: Hidden by default, shown with F8
- **Breakpoint visual**: Red circle in margin
- **Debug line visual**: Yellow arrow in margin
