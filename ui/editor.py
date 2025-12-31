"""
Code Editor Module (PyQt5/QScintilla version)
Professional code editor with syntax highlighting, auto-completion, code folding, and debugging features
"""
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QCheckBox, QLabel, QShortcut
from PyQt5.QtGui import QColor, QFont, QKeySequence
from PyQt5.QtCore import Qt
from PyQt5.Qsci import QsciScintilla

from .lexer import MacroDSLLexer
from .autocomplete import MacroAutoComplete


class MacroEditor(QsciScintilla):
    """Professional code editor based on QScintilla"""

    # Marker constants
    MARKER_BREAKPOINT = 1
    MARKER_DEBUG_LINE = 2

    def __init__(self, parent=None, parser=None):
        """
        Initialize code editor

        Args:
            parent: Parent widget
            parser: ScriptParser instance for validation (optional)
        """
        super().__init__(parent)

        self.breakpoints = set()  # Set of line numbers with breakpoints
        self.current_line = None  # Currently highlighted line (debug mode)
        self.search_dialog = None

        # Setup editor components
        self._setup_editor()
        self._setup_margins()
        self._setup_lexer()
        self._setup_folding()
        self._setup_autocompletion()
        self._setup_shortcuts()

        # Setup validator if parser provided
        if parser:
            from engine.validator import MacroValidator
            self.validator = MacroValidator(self, parser)

    def _setup_editor(self):
        """Configure basic editor properties"""
        # Font configuration
        font = QFont("Consolas", 10)
        self.setFont(font)
        self.setMarginsFont(font)

        # Tab configuration
        self.setTabWidth(4)
        self.setIndentationsUseTabs(False)
        self.setAutoIndent(True)

        # Caret configuration
        self.setCaretLineVisible(True)
        self.setCaretLineBackgroundColor(QColor("#E8F2FF"))
        self.setCaretForegroundColor(QColor("#000000"))

        # Selection colors
        self.setSelectionBackgroundColor(QColor("#A6D2FF"))
        self.setSelectionForegroundColor(QColor("#000000"))

        # Brace matching
        self.setBraceMatching(QsciScintilla.SloppyBraceMatch)
        self.setMatchedBraceBackgroundColor(QColor("#B4EEB4"))
        self.setMatchedBraceForegroundColor(QColor("#000000"))

        # Whitespace visibility
        self.setWhitespaceVisibility(QsciScintilla.WsInvisible)

        # Edge mode (optional line length indicator)
        self.setEdgeMode(QsciScintilla.EdgeNone)

        # Enable undo/redo
        self.setUtf8(True)

    def _setup_margins(self):
        """Configure line numbers and breakpoint margins"""
        # Margin 0: Line numbers
        self.setMarginType(0, QsciScintilla.NumberMargin)
        self.setMarginWidth(0, "0000")
        self.setMarginsForegroundColor(QColor("#666666"))
        self.setMarginsBackgroundColor(QColor("#F0F0F0"))

        # Margin 1: Breakpoint/debug margin
        self.setMarginType(1, QsciScintilla.SymbolMargin)
        self.setMarginWidth(1, 20)
        self.setMarginSensitivity(1, True)
        self.setMarginMarkerMask(1, (1 << self.MARKER_BREAKPOINT) | (1 << self.MARKER_DEBUG_LINE))

        # Connect margin click
        self.marginClicked.connect(self._on_margin_clicked)

        # Define breakpoint marker (red circle)
        self.markerDefine(QsciScintilla.Circle, self.MARKER_BREAKPOINT)
        self.setMarkerBackgroundColor(QColor("#FF0000"), self.MARKER_BREAKPOINT)
        self.setMarkerForegroundColor(QColor("#FFFFFF"), self.MARKER_BREAKPOINT)

        # Define debug line marker (yellow arrow)
        self.markerDefine(QsciScintilla.RightArrow, self.MARKER_DEBUG_LINE)
        self.setMarkerBackgroundColor(QColor("#FFFF00"), self.MARKER_DEBUG_LINE)
        self.setMarkerForegroundColor(QColor("#000000"), self.MARKER_DEBUG_LINE)

    def _setup_lexer(self):
        """Attach custom lexer for syntax highlighting"""
        self.lexer = MacroDSLLexer(self)
        self.setLexer(self.lexer)

    def _setup_folding(self):
        """Enable code folding"""
        self.setFolding(QsciScintilla.BoxedTreeFoldStyle)
        self.setFoldMarginColors(QColor("#F0F0F0"), QColor("#F0F0F0"))

    def _setup_autocompletion(self):
        """Configure auto-completion"""
        self.autocomplete = MacroAutoComplete(self.lexer)

        # Configure behavior
        self.setAutoCompletionSource(QsciScintilla.AcsAPIs)
        self.setAutoCompletionThreshold(1)  # Show after 1 character
        self.setAutoCompletionCaseSensitivity(False)
        self.setAutoCompletionReplaceWord(True)

        # Call tips for functions
        self.setCallTipsStyle(QsciScintilla.CallTipsContext)
        self.setCallTipsVisible(0)

    def _setup_shortcuts(self):
        """Setup keyboard shortcuts"""
        # Ctrl+F for search
        search_shortcut = QShortcut(QKeySequence("Ctrl+F"), self)
        search_shortcut.activated.connect(self.show_search_dialog)

        # Ctrl+H for replace
        replace_shortcut = QShortcut(QKeySequence("Ctrl+H"), self)
        replace_shortcut.activated.connect(self.show_search_dialog)

    def _on_margin_clicked(self, margin, line, modifiers):
        """Handle margin clicks for breakpoints"""
        if margin == 1:  # Breakpoint margin
            self.toggle_breakpoint(line + 1)  # Convert to 1-indexed

    # Breakpoint management
    def toggle_breakpoint(self, line_number):
        """
        Toggle breakpoint at line

        Args:
            line_number: Line number (1-indexed)
        """
        if line_number in self.breakpoints:
            self.breakpoints.remove(line_number)
            self.markerDelete(line_number - 1, self.MARKER_BREAKPOINT)
        else:
            self.breakpoints.add(line_number)
            self.markerAdd(line_number - 1, self.MARKER_BREAKPOINT)

    def clear_breakpoints(self):
        """Clear all breakpoints"""
        self.breakpoints.clear()
        self.markerDeleteAll(self.MARKER_BREAKPOINT)

    def get_breakpoints(self):
        """
        Get all breakpoints

        Returns:
            Set of line numbers with breakpoints (1-indexed)
        """
        return self.breakpoints.copy()

    # Debug line highlighting
    def highlight_line(self, line_number):
        """
        Highlight a line (for debug mode)

        Args:
            line_number: Line number to highlight (1-indexed), or None to clear
        """
        # Clear previous debug markers
        self.markerDeleteAll(self.MARKER_DEBUG_LINE)

        if line_number:
            self.current_line = line_number
            # Add debug marker (0-indexed)
            self.markerAdd(line_number - 1, self.MARKER_DEBUG_LINE)
            # Scroll to line
            self.ensureLineVisible(line_number - 1)
        else:
            self.current_line = None

    def clear_highlight(self):
        """Clear line highlighting"""
        self.highlight_line(None)

    # Content management
    def get_content(self):
        """
        Get editor content

        Returns:
            Editor text as string
        """
        return self.text()

    def set_content(self, text):
        """
        Set editor content

        Args:
            text: Text to set
        """
        self.setText(text)

    # Search and Replace
    def show_search_dialog(self):
        """Show search/replace dialog"""
        if not self.search_dialog:
            self.search_dialog = SearchDialog(self, self.parent())
        self.search_dialog.show()
        self.search_dialog.find_input.setFocus()
        self.search_dialog.find_input.selectAll()


class SearchDialog(QDialog):
    """Search and Replace dialog with regex support"""

    def __init__(self, editor, parent=None):
        super().__init__(parent)
        self.editor = editor
        self.setWindowTitle("Find and Replace")
        self.setMinimumWidth(450)
        self._setup_ui()

    def _setup_ui(self):
        """Setup dialog UI"""
        layout = QVBoxLayout()

        # Find field
        find_layout = QHBoxLayout()
        find_layout.addWidget(QLabel("Find:"))
        self.find_input = QLineEdit()
        self.find_input.setPlaceholderText("Enter search text...")
        self.find_input.returnPressed.connect(self._find_next)
        find_layout.addWidget(self.find_input)
        layout.addLayout(find_layout)

        # Replace field
        replace_layout = QHBoxLayout()
        replace_layout.addWidget(QLabel("Replace:"))
        self.replace_input = QLineEdit()
        self.replace_input.setPlaceholderText("Enter replacement text...")
        self.replace_input.returnPressed.connect(self._replace)
        replace_layout.addWidget(self.replace_input)
        layout.addLayout(replace_layout)

        # Options
        options_layout = QHBoxLayout()
        self.case_sensitive = QCheckBox("Case sensitive")
        self.whole_word = QCheckBox("Whole word")
        self.regex = QCheckBox("Regular expression")
        options_layout.addWidget(self.case_sensitive)
        options_layout.addWidget(self.whole_word)
        options_layout.addWidget(self.regex)
        options_layout.addStretch()
        layout.addLayout(options_layout)

        # Buttons
        button_layout = QHBoxLayout()
        self.find_next_btn = QPushButton("Find Next")
        self.find_prev_btn = QPushButton("Find Previous")
        self.replace_btn = QPushButton("Replace")
        self.replace_all_btn = QPushButton("Replace All")
        self.close_btn = QPushButton("Close")

        self.find_next_btn.clicked.connect(self._find_next)
        self.find_prev_btn.clicked.connect(self._find_previous)
        self.replace_btn.clicked.connect(self._replace)
        self.replace_all_btn.clicked.connect(self._replace_all)
        self.close_btn.clicked.connect(self.close)

        button_layout.addWidget(self.find_next_btn)
        button_layout.addWidget(self.find_prev_btn)
        button_layout.addWidget(self.replace_btn)
        button_layout.addWidget(self.replace_all_btn)
        button_layout.addStretch()
        button_layout.addWidget(self.close_btn)
        layout.addLayout(button_layout)

        # Status label
        self.status_label = QLabel("")
        self.status_label.setStyleSheet("color: #666666; font-style: italic;")
        layout.addWidget(self.status_label)

        self.setLayout(layout)

    def _find_next(self):
        """Find next occurrence"""
        self._find(forward=True)

    def _find_previous(self):
        """Find previous occurrence"""
        self._find(forward=False)

    def _find(self, forward=True):
        """
        Find text in editor

        Args:
            forward: Search direction
        """
        search_text = self.find_input.text()
        if not search_text:
            self.status_label.setText("Enter search text")
            return

        # QScintilla search flags
        found = self.editor.findFirst(
            search_text,
            self.regex.isChecked(),
            self.case_sensitive.isChecked(),
            self.whole_word.isChecked(),
            True,  # Wrap search
            forward=forward
        )

        if found:
            self.status_label.setText("")
        else:
            self.status_label.setText(f"'{search_text}' not found")

    def _replace(self):
        """Replace current selection"""
        if self.editor.hasSelectedText():
            self.editor.replace(self.replace_input.text())
            self._find_next()
            self.status_label.setText("Replaced")
        else:
            self.status_label.setText("No selection to replace")

    def _replace_all(self):
        """Replace all occurrences"""
        search_text = self.find_input.text()
        replace_text = self.replace_input.text()

        if not search_text:
            self.status_label.setText("Enter search text")
            return

        # Start from beginning
        self.editor.setCursorPosition(0, 0)

        count = 0
        while self.editor.findFirst(
            search_text,
            self.regex.isChecked(),
            self.case_sensitive.isChecked(),
            self.whole_word.isChecked(),
            False,  # Don't wrap for replace all
            forward=True
        ):
            self.editor.replace(replace_text)
            count += 1

        self.status_label.setText(f"Replaced {count} occurrence(s)")
