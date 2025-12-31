"""
Custom QScintilla Lexer for Macro DSL
Provides syntax highlighting for the macro language
"""
from PyQt5.Qsci import QsciLexerCustom, QsciScintilla
from PyQt5.QtGui import QColor, QFont
import re


class MacroDSLLexer(QsciLexerCustom):
    """Custom lexer for Macro DSL syntax highlighting"""

    # Style definitions
    STYLE_DEFAULT = 0
    STYLE_KEYWORD = 1
    STYLE_VARIABLE = 2
    STYLE_SYSTEM_VAR = 3
    STYLE_SETTING = 4
    STYLE_STRING = 5
    STYLE_NUMBER = 6
    STYLE_OPERATOR = 7
    STYLE_COMMENT = 8
    STYLE_FUNCTION = 9

    # DSL Keywords (macro commands)
    KEYWORDS = {
        'press', 'click', 'type', 'wait', 'loop', 'if', 'else', 'elseif',
        'endif', 'endloop', 'function', 'endfunction', 'call', 'while', 'endwhile',
        'goto', 'label', 'return', 'break', 'continue', 'breakpoint',
        'mousemove', 'scroll', 'keydown', 'keyup', 'lmc', 'rmc', 'mmc',
        'drag', 'hotkey', 'echo', 'input', 'next'
    }

    # System variables
    SYSTEM_VARS = {
        '$mouse_x', '$mouse_y', '$screen_width', '$screen_height',
        '$timestamp', '$random', '$i'
    }

    # Settings/decorators
    SETTINGS = {'@speed', '@iterations', '@delay', '@retry'}

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_styles()

    def _setup_styles(self):
        """Define colors and fonts for each style"""
        # Default text
        self.setColor(QColor("#000000"), self.STYLE_DEFAULT)
        self.setFont(QFont("Consolas", 10), self.STYLE_DEFAULT)

        # Keywords (press, click, type, etc.) - Blue/Bold
        self.setColor(QColor("#0000FF"), self.STYLE_KEYWORD)
        self.setFont(QFont("Consolas", 10, QFont.Bold), self.STYLE_KEYWORD)

        # User variables ($name) - Teal
        self.setColor(QColor("#008080"), self.STYLE_VARIABLE)
        self.setFont(QFont("Consolas", 10), self.STYLE_VARIABLE)

        # System variables ($mouse_x, etc.) - Orange/Bold
        self.setColor(QColor("#FF8000"), self.STYLE_SYSTEM_VAR)
        self.setFont(QFont("Consolas", 10, QFont.Bold), self.STYLE_SYSTEM_VAR)

        # Settings (@speed, etc.) - Brown/Red
        self.setColor(QColor("#A31515"), self.STYLE_SETTING)
        self.setFont(QFont("Consolas", 10), self.STYLE_SETTING)

        # Strings - Red
        self.setColor(QColor("#A31515"), self.STYLE_STRING)
        self.setFont(QFont("Consolas", 10), self.STYLE_STRING)

        # Numbers - Green
        self.setColor(QColor("#098658"), self.STYLE_NUMBER)
        self.setFont(QFont("Consolas", 10), self.STYLE_NUMBER)

        # Operators - Black
        self.setColor(QColor("#000000"), self.STYLE_OPERATOR)
        self.setFont(QFont("Consolas", 10), self.STYLE_OPERATOR)

        # Comments - Green/Italic
        self.setColor(QColor("#008000"), self.STYLE_COMMENT)
        self.setFont(QFont("Consolas", 10, QFont.StyleItalic), self.STYLE_COMMENT)

        # Functions - Gold/Brown
        self.setColor(QColor("#795E26"), self.STYLE_FUNCTION)
        self.setFont(QFont("Consolas", 10), self.STYLE_FUNCTION)

    def language(self):
        return "Macro DSL"

    def description(self, style):
        """Return description for each style"""
        descriptions = {
            self.STYLE_DEFAULT: "Default",
            self.STYLE_KEYWORD: "Keyword",
            self.STYLE_VARIABLE: "Variable",
            self.STYLE_SYSTEM_VAR: "System Variable",
            self.STYLE_SETTING: "Setting",
            self.STYLE_STRING: "String",
            self.STYLE_NUMBER: "Number",
            self.STYLE_OPERATOR: "Operator",
            self.STYLE_COMMENT: "Comment",
            self.STYLE_FUNCTION: "Function",
        }
        return descriptions.get(style, "")

    def styleText(self, start, end):
        """
        Main syntax highlighting method.
        Called automatically when text changes.
        """
        # Get the editor widget
        editor = self.editor()
        if editor is None:
            return

        # Get text from start to end
        text = editor.text()[start:end]

        # Reset styling
        self.startStyling(start)

        # Tokenize and style
        self._tokenize_and_style(text)

    def _tokenize_and_style(self, text):
        """Tokenize text and apply appropriate styles"""
        # Build keyword pattern
        keywords_pattern = r'\b(?:' + '|'.join(re.escape(kw) for kw in self.KEYWORDS) + r')\b'

        # Build system vars pattern
        system_vars_pattern = '|'.join(re.escape(var) for var in self.SYSTEM_VARS)

        # Build settings pattern
        settings_pattern = '|'.join(re.escape(setting) for setting in self.SETTINGS)

        # Token patterns (order matters!)
        patterns = [
            (r'#.*$', self.STYLE_COMMENT),                          # Comments
            (r'"(?:[^"\\]|\\.)*"', self.STYLE_STRING),              # Double-quoted strings
            (r"'(?:[^'\\]|\\.)*'", self.STYLE_STRING),              # Single-quoted strings
            (r'\b\d+\.?\d*\b', self.STYLE_NUMBER),                  # Numbers
            (settings_pattern, self.STYLE_SETTING),                 # Settings @speed
            (system_vars_pattern, self.STYLE_SYSTEM_VAR),           # System vars
            (r'\$\w+', self.STYLE_VARIABLE),                        # User variables
            (keywords_pattern, self.STYLE_KEYWORD),                 # Keywords
            (r'\w+(?=\s*\()', self.STYLE_FUNCTION),                 # Function calls
            (r'[+\-*/=<>!&|]', self.STYLE_OPERATOR),                # Operators
        ]

        # Combine patterns into single regex
        combined = '|'.join(f'({pattern})' for pattern, _ in patterns)
        regex = re.compile(combined, re.MULTILINE)

        # Track position
        pos = 0

        for match in regex.finditer(text):
            # Style any default text before this match
            if match.start() > pos:
                length = match.start() - pos
                self.setStyling(length, self.STYLE_DEFAULT)

            # Find which pattern matched
            for i, (pattern, style) in enumerate(patterns):
                if match.group(i + 1):
                    self.setStyling(len(match.group(0)), style)
                    break

            pos = match.end()

        # Style remaining text
        if pos < len(text):
            self.setStyling(len(text) - pos, self.STYLE_DEFAULT)
