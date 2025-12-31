"""
Code Editor Module
Text editor with line numbers, breakpoint support, and line highlighting for debug mode
"""
import tkinter as tk
from tkinter import ttk


class CodeEditor(tk.Frame):
    """Code editor with line numbers and debug features"""

    def __init__(self, parent, **kwargs):
        """
        Initialize code editor

        Args:
            parent: Parent widget
            **kwargs: Additional frame arguments
        """
        super().__init__(parent, **kwargs)

        self.breakpoints = set()  # Set of line numbers with breakpoints
        self.current_line = None  # Currently highlighted line (debug mode)

        self._build_ui()

    def _build_ui(self):
        """Build editor UI with line numbers"""
        # Create container frame
        container = tk.Frame(self)
        container.pack(fill='both', expand=True)

        # Line numbers widget
        self.line_numbers = tk.Text(
            container,
            width=4,
            padx=4,
            takefocus=0,
            border=0,
            background='#f0f0f0',
            foreground='#666',
            state='disabled',
            wrap='none',
            font=('Consolas', 10)
        )
        self.line_numbers.pack(side='left', fill='y')

        # Main text editor
        self.text_widget = tk.Text(
            container,
            wrap='none',
            undo=True,
            font=('Consolas', 10)
        )
        self.text_widget.pack(side='left', fill='both', expand=True)

        # Scrollbar
        scrollbar = ttk.Scrollbar(container, command=self._on_scroll)
        scrollbar.pack(side='right', fill='y')

        self.text_widget.config(yscrollcommand=scrollbar.set)

        # Bind events
        self.text_widget.bind('<<Modified>>', self._on_text_modified)
        self.text_widget.bind('<KeyRelease>', self._on_text_modified)
        self.text_widget.bind('<ButtonRelease-1>', self._on_text_modified)
        self.line_numbers.bind('<Button-1>', self._on_line_number_click)

        # Configure tags for highlighting
        self.text_widget.tag_config('current_line', background='#ffff99')  # Yellow for current line
        self.line_numbers.tag_config('breakpoint', background='#ff6b6b', foreground='white')  # Red for breakpoint
        self.line_numbers.tag_config('current_line', background='#ffff99')

        # Initial line numbers
        self.update_line_numbers()

    def _on_scroll(self, *args):
        """Handle scrollbar events"""
        self.text_widget.yview(*args)
        self.line_numbers.yview(*args)

    def _on_text_modified(self, event=None):
        """Handle text modifications"""
        # Clear modified flag
        self.text_widget.edit_modified(False)

        # Update line numbers
        self.update_line_numbers()

    def _on_line_number_click(self, event):
        """Handle click on line numbers (toggle breakpoint)"""
        # Get line number from click position
        index = self.line_numbers.index(f"@{event.x},{event.y}")
        line_num = int(index.split('.')[0])

        # Toggle breakpoint
        self.toggle_breakpoint(line_num)

    def update_line_numbers(self):
        """Update line number display"""
        # Get number of lines
        line_count = int(self.text_widget.index('end-1c').split('.')[0])

        # Build line number text
        line_numbers_text = '\n'.join(str(i) for i in range(1, line_count + 1))

        # Update line numbers widget
        self.line_numbers.config(state='normal')
        self.line_numbers.delete('1.0', 'end')
        self.line_numbers.insert('1.0', line_numbers_text)

        # Re-apply breakpoint tags
        for line_num in self.breakpoints:
            if line_num <= line_count:
                self.line_numbers.tag_add('breakpoint', f"{line_num}.0", f"{line_num}.end")

        # Re-apply current line tag
        if self.current_line and self.current_line <= line_count:
            self.line_numbers.tag_add('current_line', f"{self.current_line}.0", f"{self.current_line}.end")

        self.line_numbers.config(state='disabled')

        # Sync scrolling
        self.line_numbers.yview_moveto(self.text_widget.yview()[0])

    def get_content(self):
        """
        Get editor content

        Returns:
            Editor text as string
        """
        return self.text_widget.get('1.0', 'end-1c')

    def set_content(self, text):
        """
        Set editor content

        Args:
            text: Text to set
        """
        self.text_widget.delete('1.0', 'end')
        self.text_widget.insert('1.0', text)
        self.update_line_numbers()

    def highlight_line(self, line_number):
        """
        Highlight a line (for debug mode)

        Args:
            line_number: Line number to highlight
        """
        # Clear previous highlight
        self.text_widget.tag_remove('current_line', '1.0', 'end')

        # Highlight new line
        if line_number:
            self.current_line = line_number
            self.text_widget.tag_add('current_line', f"{line_number}.0", f"{line_number}.end+1c")

            # Scroll to line
            self.text_widget.see(f"{line_number}.0")

            # Update line numbers
            self.update_line_numbers()
        else:
            self.current_line = None

    def toggle_breakpoint(self, line_number):
        """
        Toggle breakpoint at line

        Args:
            line_number: Line number
        """
        if line_number in self.breakpoints:
            self.breakpoints.remove(line_number)
        else:
            self.breakpoints.add(line_number)

        self.update_line_numbers()

    def clear_breakpoints(self):
        """Clear all breakpoints"""
        self.breakpoints.clear()
        self.update_line_numbers()

    def get_breakpoints(self):
        """
        Get all breakpoints

        Returns:
            Set of line numbers with breakpoints
        """
        return self.breakpoints.copy()

    def clear_highlight(self):
        """Clear line highlighting"""
        self.highlight_line(None)
