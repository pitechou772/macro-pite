"""
Real-Time Syntax Validator
Provides live error highlighting in the editor
"""
from PyQt5.QtCore import QObject, QTimer
from PyQt5.Qsci import QsciScintilla
from PyQt5.QtGui import QColor


class MacroValidator(QObject):
    """Real-time syntax validator using existing parser"""

    ERROR_INDICATOR = 0

    def __init__(self, editor, parser):
        """
        Initialize validator

        Args:
            editor: QScintilla editor instance
            parser: ScriptParser instance
        """
        super().__init__()
        self.editor = editor
        self.parser = parser

        # Debounce timer for validation
        self.validation_timer = QTimer()
        self.validation_timer.setSingleShot(True)
        self.validation_timer.timeout.connect(self._validate)

        # Define error indicator (red squiggly underline)
        self.editor.indicatorDefine(QsciScintilla.SquiggleIndicator, self.ERROR_INDICATOR)
        self.editor.setIndicatorForegroundColor(QColor("#FF0000"), self.ERROR_INDICATOR)

        # Connect to text changes
        self.editor.textChanged.connect(self._on_text_changed)

    def _on_text_changed(self):
        """Debounce validation on text change"""
        self.validation_timer.stop()
        self.validation_timer.start(500)  # Validate after 500ms of no typing

    def _validate(self):
        """Run validation using existing parser"""
        # Clear previous error indicators
        self.editor.clearIndicatorRange(
            0, 0,
            self.editor.lines(),
            self.editor.lineLength(self.editor.lines() - 1) if self.editor.lines() > 0 else 0,
            self.ERROR_INDICATOR
        )

        # Clear annotations
        self.editor.clearAnnotations()

        # Get current text
        code = self.editor.text()

        if not code.strip():
            return  # Don't validate empty code

        try:
            # Use existing parser to validate
            is_valid, message = self.parser.validate_syntax(code)

            if not is_valid:
                # Try to extract line number from error message
                self._highlight_error_from_message(message)

        except SyntaxError as e:
            # Highlight error location if available
            if hasattr(e, 'lineno') and e.lineno:
                self._highlight_error_line(e.lineno, str(e))

        except Exception:
            # Silently ignore other exceptions during validation
            pass

    def _highlight_error_from_message(self, message):
        """
        Extract line number from error message and highlight

        Args:
            message: Error message string
        """
        # Try to extract line number from common error message patterns
        import re
        match = re.search(r'line (\d+)', message, re.IGNORECASE)

        if match:
            line_num = int(match.group(1))
            self._highlight_error_line(line_num, message)
        else:
            # If no line number found, highlight first line
            self._highlight_error_line(1, message)

    def _highlight_error_line(self, line_num, error_msg):
        """
        Highlight a specific line with error

        Args:
            line_num: Line number (1-indexed)
            error_msg: Error message to display
        """
        # Convert to 0-indexed
        line = line_num - 1

        # Ensure line is valid
        if line < 0:
            line = 0
        if line >= self.editor.lines():
            line = self.editor.lines() - 1

        # Get line length
        line_length = self.editor.lineLength(line)

        if line_length > 0:
            # Highlight the entire line
            self.editor.fillIndicatorRange(
                line, 0,
                line, line_length,
                self.ERROR_INDICATOR
            )

            # Add annotation with error message
            self.editor.annotate(line, error_msg, self.editor.annotationDisplay())
            self.editor.setAnnotationDisplay(QsciScintilla.AnnotationBoxed)

    def disable(self):
        """Disable validation (useful during macro execution)"""
        self.validation_timer.stop()
        self.editor.textChanged.disconnect(self._on_text_changed)

    def enable(self):
        """Re-enable validation"""
        self.editor.textChanged.connect(self._on_text_changed)
