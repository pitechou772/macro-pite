"""
Macro Builder v4.0 - Professional IDE
Entry point for the application

This is a modular macro builder with DSL language support,
featuring advanced syntax highlighting, auto-completion, code folding,
error detection, debug mode, and recording.
"""

import sys
from PyQt5.QtWidgets import QApplication
from ui.window import MacroBuilderWindow


def main():
    """Launch Macro Builder"""
    app = QApplication(sys.argv)

    # Set application info
    app.setApplicationName("Macro Builder")
    app.setApplicationVersion("4.0")
    app.setOrganizationName("Macro Builder")

    # Create and show main window
    window = MacroBuilderWindow()
    window.show()

    # Run application
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
