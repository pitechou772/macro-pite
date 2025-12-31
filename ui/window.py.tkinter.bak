"""
Main Window Module
Orchestrates the entire application - UI, engine, and interactions
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
import threading

from ui.editor import CodeEditor
from ui.controls import ControlPanel
from engine.context import ExecutionContext
from engine.parser import ScriptParser
from engine.executor import MacroExecutor
from engine.recorder import ActionRecorder
from utils.file_io import FileManager


class MacroBuilderWindow(tk.Tk):
    """Main application window"""

    def __init__(self):
        """Initialize main window"""
        super().__init__()

        self.title("Macro Builder v4.0")
        self.geometry("1000x800")

        # File state
        self.current_file = None
        self.file_manager = FileManager()

        # Engine components
        self.context = ExecutionContext()
        self.parser = ScriptParser(self.context)
        self.executor = MacroExecutor(self.context, gui_callback=self)
        self.recorder = ActionRecorder()

        # Debug state
        self.debug_mode = False
        self.recording = False

        # Build UI
        self._build_ui()

    def _build_ui(self):
        """Build main UI"""
        # Menu bar
        self._build_menu()

        # Editor
        self.editor = CodeEditor(self)
        self.editor.pack(fill='both', expand=True, padx=10, pady=5)

        # Controls
        callbacks = {
            'execute': self.start_macro,
            'pause': self.pause_macro,
            'stop': self.stop_macro,
            'step_next': self.step_next,
            'toggle_breakpoint': self.toggle_breakpoint,
            'clear_breakpoints': self.clear_breakpoints
        }
        self.controls = ControlPanel(self, callbacks)
        self.controls.pack(fill='both', expand=False, padx=10, pady=5)

    def _build_menu(self):
        """Build menu bar"""
        menubar = tk.Menu(self)

        # File menu
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Nouveau", command=self.new_file, accelerator="Ctrl+N")
        filemenu.add_command(label="Ouvrir", command=self.load_file, accelerator="Ctrl+O")
        filemenu.add_command(label="Enregistrer", command=self.save_file, accelerator="Ctrl+S")
        filemenu.add_command(label="Enregistrer sous...", command=self.save_file_as)
        filemenu.add_separator()
        filemenu.add_command(label="Ouvrir JSON", command=self.load_json)
        filemenu.add_command(label="Enregistrer JSON", command=self.save_json)
        filemenu.add_separator()
        filemenu.add_command(label="Quitter", command=self.quit)
        menubar.add_cascade(label="Fichier", menu=filemenu)

        # Edit menu
        editmenu = tk.Menu(menubar, tearoff=0)
        editmenu.add_command(label="Valider Syntaxe", command=self.validate_syntax, accelerator="F7")
        menubar.add_cascade(label="Édition", menu=editmenu)

        # Debug menu
        debugmenu = tk.Menu(menubar, tearoff=0)
        debugmenu.add_command(label="Mode Debug", command=self.toggle_debug_mode, accelerator="F8")
        debugmenu.add_separator()
        debugmenu.add_command(label="Toggle Breakpoint", command=self.toggle_breakpoint, accelerator="F9")
        debugmenu.add_command(label="Clear Breakpoints", command=self.clear_breakpoints)
        debugmenu.add_separator()
        debugmenu.add_command(label="Step Next", command=self.step_next, accelerator="F10")
        menubar.add_cascade(label="Debug", menu=debugmenu)

        # Record menu
        recordmenu = tk.Menu(menubar, tearoff=0)
        recordmenu.add_command(label="Start Recording", command=self.start_recording)
        recordmenu.add_command(label="Stop Recording", command=self.stop_recording)
        menubar.add_cascade(label="Record", menu=recordmenu)

        # Help menu
        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="À propos", command=self.show_about)
        menubar.add_cascade(label="Aide", menu=helpmenu)

        self.config(menu=menubar)

        # Keyboard shortcuts
        self.bind('<Control-n>', lambda e: self.new_file())
        self.bind('<Control-o>', lambda e: self.load_file())
        self.bind('<Control-s>', lambda e: self.save_file())
        self.bind('<F5>', lambda e: self.start_macro())
        self.bind('<F7>', lambda e: self.validate_syntax())
        self.bind('<F8>', lambda e: self.toggle_debug_mode())
        self.bind('<F9>', lambda e: self.toggle_breakpoint())
        self.bind('<F10>', lambda e: self.step_next())

    # File operations
    def new_file(self):
        """Create new file"""
        if messagebox.askyesno("Nouveau fichier", "Créer un nouveau fichier ?"):
            self.editor.set_content("")
            self.current_file = None
            self.title("Macro Builder v4.0 - Nouveau")

    def load_file(self):
        """Load a text file"""
        path = filedialog.askopenfilename(
            title="Ouvrir un fichier",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if path:
            try:
                script, speed, iterations, metadata = self.file_manager.load_file(path)
                self.editor.set_content(script)
                self.controls.speed_var.set(speed)
                self.controls.iterations_var.set(iterations)
                self.current_file = path
                self.title(f"Macro Builder v4.0 - {path}")
                self.controls.log(f"Fichier chargé: {path}")
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible de charger le fichier:\n{e}")

    def save_file(self):
        """Save current file"""
        if self.current_file:
            try:
                content = self.editor.get_content()
                self.file_manager.save_text(self.current_file, content)
                self.controls.log(f"Fichier enregistré: {self.current_file}")
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible d'enregistrer:\n{e}")
        else:
            self.save_file_as()

    def save_file_as(self):
        """Save file as"""
        path = filedialog.asksaveasfilename(
            title="Enregistrer sous",
            defaultextension='.txt',
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if path:
            try:
                content = self.editor.get_content()
                self.file_manager.save_text(path, content)
                self.current_file = path
                self.title(f"Macro Builder v4.0 - {path}")
                self.controls.log(f"Fichier enregistré: {path}")
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible d'enregistrer:\n{e}")

    def load_json(self):
        """Load JSON macro file"""
        path = filedialog.askopenfilename(
            title="Ouvrir JSON",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if path:
            try:
                data = self.file_manager.load_json(path)
                self.editor.set_content(data['script'])
                self.controls.speed_var.set(data.get('speed', 1.0))
                self.controls.iterations_var.set(data.get('metadata', {}).get('iterations', 1))
                self.current_file = path
                self.title(f"Macro Builder v4.0 - {path}")
                self.controls.log(f"JSON chargé: {path} (v{data['version']})")
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible de charger JSON:\n{e}")

    def save_json(self):
        """Save as JSON macro file"""
        path = filedialog.asksaveasfilename(
            title="Enregistrer JSON",
            defaultextension='.json',
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if path:
            try:
                script = self.editor.get_content()
                speed = self.controls.get_speed()
                iterations = self.controls.get_iterations()
                self.file_manager.save_json(path, script, speed, iterations)
                self.controls.log(f"JSON enregistré: {path}")
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible d'enregistrer JSON:\n{e}")

    # Execution
    def validate_syntax(self):
        """Validate script syntax"""
        script = self.editor.get_content()
        is_valid, message = self.parser.validate_syntax(script)

        if is_valid:
            messagebox.showinfo("Validation", "Syntaxe OK ✓")
        else:
            messagebox.showerror("Erreur de syntaxe", message)

    def start_macro(self):
        """Start macro execution"""
        script = self.editor.get_content()

        # Clear previous context
        self.context = ExecutionContext()
        self.parser = ScriptParser(self.context)
        self.executor = MacroExecutor(self.context, gui_callback=self)

        # Apply debug settings
        if self.debug_mode:
            self.executor.enable_debug_mode(True)
            for line_num in self.editor.get_breakpoints():
                self.executor.add_breakpoint(line_num)

        # Parse script
        try:
            actions = self.parser.parse(script)
        except SyntaxError as e:
            messagebox.showerror("Erreur", str(e))
            return

        # Clear console
        self.controls.clear_console()

        # Reset executor state
        self.executor.stop_event.clear()
        self.executor.pause_event.clear()

        # Get speed and iterations
        speed = self.controls.get_speed()
        iterations = self.controls.get_iterations()

        # Set @iterations special variable
        self.context.set_special_var('@iterations', iterations)

        # Execute in thread
        def run_macro():
            for i in range(iterations):
                if self.executor.stop_event.is_set():
                    break
                if iterations > 1:
                    self.controls.log(f"=== Itération {i+1}/{iterations} ===")
                self.executor.execute(actions, speed, self.controls.log)

        threading.Thread(target=run_macro, daemon=True).start()

    def stop_macro(self):
        """Stop macro execution"""
        self.executor.stop()
        self.controls.log("⏹ Arrêt demandé")

    def pause_macro(self):
        """Pause/resume macro execution"""
        if not self.executor.pause_event.is_set():
            self.executor.pause()
            self.controls.log("⏸ Pause")
            self.controls.btn_pause.config(text="▶ Reprendre")
        else:
            self.executor.resume()
            self.controls.log("▶ Reprise")
            self.controls.btn_pause.config(text="⏸ Pause")

    # Debug
    def toggle_debug_mode(self):
        """Toggle debug mode"""
        self.debug_mode = not self.debug_mode
        self.controls.show_debug_panel(self.debug_mode)

        if self.debug_mode:
            self.controls.log("[DEBUG] Mode debug activé")
        else:
            self.controls.log("[DEBUG] Mode debug désactivé")
            self.editor.clear_highlight()

    def toggle_breakpoint(self):
        """Toggle breakpoint at current line"""
        # Get current line from text widget
        current = self.editor.text_widget.index('insert')
        line_num = int(current.split('.')[0])

        self.editor.toggle_breakpoint(line_num)

        if line_num in self.editor.get_breakpoints():
            self.controls.log(f"[DEBUG] Breakpoint ajouté à la ligne {line_num}")
        else:
            self.controls.log(f"[DEBUG] Breakpoint retiré de la ligne {line_num}")

    def clear_breakpoints(self):
        """Clear all breakpoints"""
        self.editor.clear_breakpoints()
        self.executor.clear_breakpoints()
        self.controls.log("[DEBUG] Tous les breakpoints effacés")

    def step_next(self):
        """Step to next instruction in debug mode"""
        if self.debug_mode:
            self.executor.step_next()

    def on_breakpoint_hit(self, line_num, variables):
        """Callback when breakpoint is hit"""
        self.editor.highlight_line(line_num)
        self.controls.update_variables(variables)
        self.controls.log(f"[DEBUG] Breakpoint atteint à la ligne {line_num}")

    # Recording
    def start_recording(self):
        """Start recording actions"""
        if not self.recording:
            self.recorder.start_recording()
            self.recording = True
            self.controls.log("[RECORD] Enregistrement démarré")
            messagebox.showinfo("Enregistrement", "Enregistrement démarré. Effectuez vos actions puis arrêtez l'enregistrement.")

    def stop_recording(self):
        """Stop recording and insert script"""
        if self.recording:
            self.recorder.stop_recording()
            self.recording = False

            # Generate script
            script = self.recorder.generate_script()

            # Insert into editor
            self.editor.set_content(script)

            self.controls.log(f"[RECORD] Enregistrement arrêté - {len(self.recorder.actions)} actions")
            messagebox.showinfo("Enregistrement", f"Script généré avec {len(self.recorder.actions)} actions")

    # Callbacks
    def ask_input(self, prompt):
        """Thread-safe input dialog"""
        result = [None]

        def do_ask():
            try:
                val = simpledialog.askstring("Saisie", prompt, parent=self)
                result[0] = val if val is not None else ""
            except Exception as e:
                self.controls.log(f"[ERREUR INPUT] {e}")
                result[0] = ""

        # Execute in main thread
        self.after(0, do_ask)

        # Wait for result
        import time
        timeout = 0
        while result[0] is None and timeout < 300:
            self.update()
            time.sleep(0.1)
            timeout += 1

        return result[0] if result[0] is not None else ""

    # Misc
    def show_about(self):
        """Show about dialog"""
        messagebox.showinfo(
            "À propos",
            "Macro Builder v4.0\n\n"
            "Application de création de macros clavier/souris\n"
            "avec langage DSL intégré.\n\n"
            "Fonctionnalités v4:\n"
            "• Éditeur avec numéros de ligne\n"
            "• Support des fonctions\n"
            "• Mode debug avec breakpoints\n"
            "• Enregistrement d'actions\n"
            "• Import/Export JSON"
        )
