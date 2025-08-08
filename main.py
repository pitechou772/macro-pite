import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pynput.keyboard import Controller as KController, Key
from pynput.mouse import Controller as MController, Button
import threading
import time

# --- Parsing with indentation-based loops ---
def parse_script(script):
    """
    Parse le script macro avec support pour boucles nommées :
    loop,count,"nom"
        ...actions...
    endloop,"nom"
    """
    raw_lines = script.splitlines()
    lines = []
    for raw in raw_lines:
        if not raw.strip() or raw.strip().startswith('#'): continue
        indent = len(raw) - len(raw.lstrip(' '))
        lines.append((indent, raw.strip()))

    def parse_block(start, base_indent):
        actions = []
        i = start
        while i < len(lines):
            indent, line = lines[i]
            if indent < base_indent:
                break
            parts = [p.strip() for p in line.split(',')]
            cmd = parts[0]
            if cmd == 'loop':
                # loop,count,"nom" ou loop,count
                try:
                    count = int(parts[1])
                except Exception:
                    raise SyntaxError(f"Invalid loop count at line {i+1}: '{line}'")
                loop_name = parts[2].strip('"') if len(parts) > 2 else None
                # Chercher la fin de boucle correspondante
                j = i + 1
                while j < len(lines):
                    sub_indent, sub_line = lines[j]
                    sub_parts = [p.strip() for p in sub_line.split(',')]
                    if sub_parts[0] == 'endloop':
                        end_name = sub_parts[1].strip('"') if len(sub_parts) > 1 else None
                        if loop_name == end_name:
                            break
                    j += 1
                # Parser le bloc entre loop et endloop
                block, _ = parse_block(i+1, indent+1)
                for _ in range(count):
                    actions.extend(block)
                i = j + 1  # Sauter après endloop
            elif cmd == 'endloop':
                # Fin de boucle nommée
                return actions, i+1
            elif cmd == 'next':
                # Support backward compatibility
                return actions, i+1
            else:
                actions.append(line)
                i += 1
        return actions, i

    expanded, _ = parse_block(0, 0)
    return expanded

class MacroEngine:
    def __init__(self):
        self.kb = KController()
        self.ms = MController()
        self.stop_event = threading.Event()

    def execute(self, actions, speed=1.0):
        for action in actions:
            if self.stop_event.is_set():
                break
            parts = action.split(',', 2)
            cmd = parts[0]
            try:
                if cmd == 'press':
                    keys_str, dur_str = parts[1], parts[2]
                    duration = float(dur_str) / speed
                    keys = [k.strip() for k in keys_str.split('+')]
                    key_objs = [getattr(Key, k, k) for k in keys]
                    for k in key_objs: self.kb.press(k)
                    time.sleep(duration)
                    for k in reversed(key_objs): self.kb.release(k)
                elif cmd == 'type':
                    text = parts[1]
                    for char in text:
                        # Simule chaque touche comme un press/release
                        self.kb.press(char)
                        time.sleep(0.03 / speed)
                        self.kb.release(char)
                        time.sleep(0.03 / speed)
                elif cmd == 'wait':
                    time.sleep(float(parts[1]) / speed)
                elif cmd == 'lmc':
                    self._click(Button.left)
                elif cmd == 'rmc':
                    self._click(Button.right)
                elif cmd == 'on':
                    btn = Button.left if parts[1].strip().lower() in ['lmc', 'left'] else Button.right
                    self.ms.press(btn)
                elif cmd == 'off':
                    btn = Button.left if parts[1].strip().lower() in ['lmc', 'left'] else Button.right
                    self.ms.release(btn)
            except Exception as e:
                print(f"Erreur '{action}': {e}")
            time.sleep(0.1 / speed)
        return not self.stop_event.is_set()

    def _click(self, button):
        self.ms.press(button)
        time.sleep(0.05)
        self.ms.release(button)

    def stop(self):
        self.stop_event.set()

class MacroGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Macro Builder v2.1")
        self.geometry("700x600")
        self.engine = MacroEngine()
        self._build_ui()

    def _build_ui(self):
        menubar = tk.Menu(self)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Ouvrir...", command=self.load_file)
        filemenu.add_command(label="Enregistrer...", command=self.save_file)
        menubar.add_cascade(label="Fichier", menu=filemenu)
        self.config(menu=menubar)

        ttk.Label(self, text="Définition de la macro :").pack(anchor='w', padx=10, pady=(10,0))
        self.text = tk.Text(self, height=18)
        self.text.pack(fill='both', expand=True, padx=10)

        # Console d'évolution
        ttk.Label(self, text="Console d'exécution :").pack(anchor='w', padx=10, pady=(5,0))
        self.console = tk.Text(self, height=7, state='disabled', bg='#222', fg='#0f0', font=('Consolas', 10))
        self.console.pack(fill='x', padx=10, pady=(0,5))

        ctrl = ttk.Frame(self)
        ctrl.pack(fill='x', pady=5)
        ttk.Label(ctrl, text="Vitesse :").pack(side='left', padx=5)
        self.speed = tk.DoubleVar(value=1.0)
        ttk.Scale(ctrl, from_=0.1, to=5.0, variable=self.speed, orient='horizontal').pack(side='left', fill='x', expand=True)
        ttk.Button(ctrl, text="Exécuter", command=self.start_macro).pack(side='right', padx=5)
        ttk.Button(ctrl, text="Arrêter", command=self.stop_macro).pack(side='right')

    def log_console(self, msg):
        self.console.config(state='normal')
        self.console.insert('end', msg + '\n')
        self.console.see('end')
        self.console.config(state='disabled')

    def load_file(self):
        path = filedialog.askopenfilename(filetypes=[('Text files','*.txt')])
        if path:
            with open(path, 'r', encoding='utf-8') as f:
                self.text.delete('1.0','end')
                self.text.insert('1.0', f.read())

    def save_file(self):
        path = filedialog.asksaveasfilename(defaultextension='.txt', filetypes=[('Text files','*.txt')])
        if path:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(self.text.get('1.0','end'))

    def start_macro(self):
        script = self.text.get('1.0','end')
        try:
            actions = parse_script(script)
        except SyntaxError as e:
            messagebox.showerror("Erreur de syntaxe", str(e))
            return
        self.engine.stop_event.clear()
        self.console.config(state='normal')
        self.console.delete('1.0', 'end')
        self.console.config(state='disabled')
        threading.Thread(target=self._run, args=(actions,), daemon=True).start()

    def _run(self, actions):
        for idx, action in enumerate(actions, 1):
            self.log_console(f"[{idx}/{len(actions)}] {action}")
            ok = self.engine.execute([action], speed=self.speed.get())
            if self.engine.stop_event.is_set():
                self.log_console("⏹ Macro interrompue.")
                messagebox.showwarning("Arrêt", "Macro interrompue.")
                return
        self.log_console("✅ Macro exécutée !")
        messagebox.showinfo("Terminé", "Macro exécutée !")

    def stop_macro(self):
        self.engine.stop()

# Exemple de macro adaptée à ta syntaxe :
"""
loop,300
    wait,3
    on,lmc
    loop,27
        press,d+z,17
        press,z,2
        press,q+z,17
        press,z,2
    endloop
    off,lmc
    type,!warp garden
endloop
"""

if __name__ == '__main__':
    app = MacroGUI()
    app.mainloop()