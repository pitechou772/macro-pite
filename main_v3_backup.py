import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
from pynput.keyboard import Controller as KController, Key
from pynput.mouse import Controller as MController, Button
import threading
import time
import datetime
import ast
import operator

# ============================
# Safe Expression Evaluation
# Supports arithmetic, comparisons and boolean ops
# ============================

OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod,
    ast.USub: operator.neg
}
CMP_OPS = {
    ast.Eq: operator.eq,
    ast.NotEq: operator.ne,
    ast.Lt: operator.lt,
    ast.LtE: operator.le,
    ast.Gt: operator.gt,
    ast.GtE: operator.ge
}
BOOL_OPS = {
    ast.And: all,
    ast.Or: any
}


def safe_eval_expr(expr, variables=None):
    """
    Évalue une expression (arithmétique / logique) en toute sécurité.
    Supporte +, -, *, /, %, comparaisons, et, ou, not, et variables ($x).
    """
    variables = variables or {}
    expr = expr.strip()
    # Remplace les variables simples par des identifiants temporaires (pour parsing)
    # On remplace $var par var__val0 puis on injecte dans un env lors de l'évaluation
    env = {}
    idx = 0
    for k, v in variables.items():
        placeholder = f"_v{idx}"
        expr = expr.replace(k, placeholder)
        env[placeholder] = v
        idx += 1

    try:
        tree = ast.parse(expr, mode='eval')
        return _eval_ast(tree.body, env)
    except Exception as e:
        raise ValueError(f"Expression invalide : {expr} -> {e}")


def _eval_ast(node, env=None):
    env = env or {}
    if isinstance(node, ast.Constant):
        return node.value
    if isinstance(node, ast.Num):  # compat
        return node.n
    if isinstance(node, ast.Name):
        # récupère depuis env si présent
        return env.get(node.id, 0)
    if isinstance(node, ast.BinOp):
        if type(node.op) in OPS:
            return OPS[type(node.op)](_eval_ast(node.left, env), _eval_ast(node.right, env))
    if isinstance(node, ast.UnaryOp):
        if isinstance(node.op, ast.Not):
            return not _eval_ast(node.operand, env)
        if type(node.op) in OPS:
            return OPS[type(node.op)](_eval_ast(node.operand, env))
    if isinstance(node, ast.Compare):
        left = _eval_ast(node.left, env)
        result = True
        for op, comparator in zip(node.ops, node.comparators):
            if type(op) in CMP_OPS:
                right = _eval_ast(comparator, env)
                result = CMP_OPS[type(op)](left, right)
                left = right
            else:
                raise ValueError("Comparaison non supportée")
        return result
    if isinstance(node, ast.BoolOp):
        vals = [_eval_ast(v, env) for v in node.values]
        if type(node.op) in BOOL_OPS:
            func = BOOL_OPS[type(node.op)]
            # and -> all, or -> any ; on considère les valeurs truthy
            return func([bool(v) for v in vals])
    raise ValueError("Opération non supportée dans expression")


# ============================
# Parsing & Script Handling (extended)
# - Now returns actions (which can be strings or tuples for control structures)
# - Supports: if / elseif / else / endif ; while / endwhile ; loop / endloop ; break / continue
# ============================


def parse_script(script):
    raw_lines = script.splitlines()
    lines = []
    variables = {}

    for raw in raw_lines:
        if not raw.strip() or raw.strip().startswith('#'):
            continue
        indent = len(raw) - len(raw.lstrip(' '))
        line = raw.strip()

        # Gestion des variables avec calcul
        if line.startswith('$') and '=' in line:
            name, expr = line.split('=', 1)
            name = name.strip()
            expr = expr.strip()
            
            # Détection spéciale pour input: $var = input,"message"
            if expr.strip().startswith('input,'):
                # C'est une commande input, on la traite comme une action spéciale
                input_parts = expr.split(',', 1)
                if len(input_parts) > 1:
                    prompt = input_parts[1].strip().strip('"')
                    # On ajoute une action spéciale input_var
                    action_line = f"input_var,{name},{prompt}"
                    lines.append((indent, action_line))

                continue
            
            # Évaluer expression avec variables connues
            try:
                variables[name] = safe_eval_expr(expr, variables)
            except Exception:
                # si échec, garder la chaîne
                variables[name] = expr
            continue

        lines.append((indent, line))

    def parse_block(start, base_indent):
        actions = []
        i = start
        while i < len(lines):
            indent, line = lines[i]
            if indent < base_indent:
                break
            parts = [p.strip() for p in line.split(',')]
            cmd = parts[0].lower()

            if cmd == 'loop':
                loop_count = parts[1] if len(parts) > 1 else '1'
                infinite = loop_count.lower() == 'infinite'
                try:
                    count = float(loop_count) if not infinite else float('inf')
                except:
                    raise SyntaxError(f"Invalid loop count at line {i+1}: '{line}'")
                block, new_i = parse_block(i+1, indent+1)
                # create loop action
                actions.append(('LOOP', count, block))
                i = new_i

            elif cmd in ['endloop', 'next']:
                return actions, i+1

            elif cmd == 'while':
                cond = ','.join(parts[1:]).strip()
                if not cond:
                    raise SyntaxError(f"While requires a condition at line {i+1}")
                block, new_i = parse_block(i+1, indent+1)
                actions.append(('WHILE', cond, block))
                i = new_i

            elif cmd == 'endwhile':
                return actions, i+1

            elif cmd == 'if':
                # collect branches until endif
                branches = []  # list of (cond_str or 'else', block)
                cond = ','.join(parts[1:]).strip()
                if not cond:
                    raise SyntaxError(f"If requires a condition at line {i+1}")
                # parse first block
                block, new_i = parse_block(i+1, indent+1)
                branches.append((cond, block))
                i = new_i
                # look for elseif / else / endif at same indent
                while i < len(lines):
                    sub_indent, sub_line = lines[i]
                    if sub_indent < indent:
                        break
                    sub_parts = [p.strip() for p in sub_line.split(',')]
                    sub_cmd = sub_parts[0].lower()
                    if sub_cmd == 'elseif':
                        sub_cond = ','.join(sub_parts[1:]).strip()
                        b, ni = parse_block(i+1, sub_indent+1)
                        branches.append((sub_cond, b))
                        i = ni
                    elif sub_cmd == 'else':
                        b, ni = parse_block(i+1, sub_indent+1)
                        branches.append(('else', b))
                        i = ni
                    elif sub_cmd == 'endif':
                        i += 1
                        break
                    else:
                        # unexpected line (probably end of branch)
                        break
                actions.append(('IF', branches))

            elif cmd == 'endif':
                return actions, i+1

            elif cmd == 'break':
                actions.append('BREAK')
                i += 1

            elif cmd == 'continue':
                actions.append('CONTINUE')
                i += 1

            else:
                # action simple (ne pas remplacer les variables maintenant ; on le fera au runtime)
                actions.append(line)
                i += 1
        return actions, i

    expanded, _ = parse_block(0, 0)
    return expanded, variables


def replace_vars_runtime(line, vars_dict=None, loop_vars=None, system_vars=None):
    """
    Remplace les variables dans la ligne au moment de l'exécution.
    - vars_dict : variables définies lors du parsing
    - loop_vars : variables de boucle (ex: $i)
    - system_vars : variables système (ex: $mouse_x)
    """
    vars_dict = vars_dict or {}
    loop_vars = loop_vars or {}
    system_vars = system_vars or {}
    all_vars = {}
    all_vars.update(vars_dict)
    all_vars.update(loop_vars)
    all_vars.update(system_vars)
    # Remplacer par valeur str
    for k, v in all_vars.items():
        line = line.replace(k, str(v))
    return line


# ============================
# Macro Engine (extended)
# - execute actions which can be nested structures
# - supports while, loop, if, break, continue
# - resolves variables at runtime including system vars
# ============================

class MacroEngine:
    def __init__(self, gui_callback=None):
        self.kb = KController()
        self.ms = MController()
        self.stop_event = threading.Event()
        self.pause_event = threading.Event()
        self._screen_size = None
        self.gui_callback = gui_callback  # Référence vers l'interface GUI

    def _get_system_vars(self):
        # retourne dict des variables système actuelles
        x, y = self.ms.position
        # obtient la taille d'écran (crée temporairement un root tkinter invisble)
        if not self._screen_size:
            try:
                root = tk.Tk()
                root.withdraw()
                w = root.winfo_screenwidth()
                h = root.winfo_screenheight()
                root.destroy()
            except Exception:
                w, h = 0, 0
            self._screen_size = (w, h)
        w, h = self._screen_size
        return {'$mouse_x': int(x), '$mouse_y': int(y), '$screen_width': int(w), '$screen_height': int(h)}

    def execute(self, actions, variables=None, speed=1.0, log_callback=None):
        variables = variables or {}
        try:
            self._execute_actions(actions, variables, {}, speed, log_callback)
            if log_callback:
                log_callback("✅ Macro terminée")
        except Exception as e:
            if log_callback:
                log_callback(f"[ERREUR GLOBALE] {e}")

    def _execute_actions(self, actions, variables, loop_vars, speed, log_callback):
        i = 0
        while i < len(actions):
            if self.stop_event.is_set():
                return
            while self.pause_event.is_set():
                time.sleep(0.1)

            act = actions[i]

            # Branch by action type
            if isinstance(act, tuple):
                typ = act[0]
                if typ == 'LOOP':
                    count, block = act[1], act[2]
                    # if infinite, run until stop_event
                    if count == float('inf'):
                        idx = 0
                        while not self.stop_event.is_set():
                            # update loop var
                            lv = dict(loop_vars)
                            lv['$i'] = str(idx)
                            res = self._execute_actions(block, variables, lv, speed, log_callback)
                            # handle break/continue signals via return values
                            if res == 'BREAK':
                                break
                            idx += 1
                    else:
                        for idx in range(int(count)):
                            if self.stop_event.is_set():
                                break
                            lv = dict(loop_vars)
                            lv['$i'] = str(idx)
                            res = self._execute_actions(block, variables, lv, speed, log_callback)
                            if res == 'BREAK':
                                break
                    i += 1
                    continue

                if typ == 'WHILE':
                    cond = act[1]
                    block = act[2]
                    loops = 0
                    while True:
                        if self.stop_event.is_set():
                            return
                        sys_vars = self._get_system_vars()
                        try:
                            cond_val = safe_eval_expr(replace_cond_vars(cond, variables, loop_vars, sys_vars), { })
                        except Exception as e:
                            if log_callback:
                                log_callback(f"[ERREUR] Condition WHILE invalide: {cond} -> {e}")
                            break
                        if not cond_val:
                            break
                        res = self._execute_actions(block, variables, loop_vars, speed, log_callback)
                        if res == 'BREAK':
                            break
                        loops += 1
                        # simple safety cap
                        if loops > 100000:
                            if log_callback:
                                log_callback("[ERREUR] Boucle WHILE trop longue, coupée")
                            break
                    i += 1
                    continue

                if typ == 'IF':
                    branches = act[1]
                    executed = False
                    for cond, block in branches:
                        if cond == 'else':
                            # execute else only if none executed
                            if not executed:
                                res = self._execute_actions(block, variables, loop_vars, speed, log_callback)
                                executed = True
                                break
                        else:
                            sys_vars = self._get_system_vars()
                            try:
                                cond_eval = safe_eval_expr(replace_cond_vars(cond, variables, loop_vars, sys_vars), {})
                            except Exception as e:
                                if log_callback:
                                    log_callback(f"[ERREUR] Condition IF invalide: {cond} -> {e}")
                                cond_eval = False
                            if cond_eval:
                                res = self._execute_actions(block, variables, loop_vars, speed, log_callback)
                                executed = True
                                break
                    i += 1
                    continue

            # simple string action
            if isinstance(act, str):
                # BREAK/CONTINUE signals
                if act == 'BREAK':
                    return 'BREAK'
                if act == 'CONTINUE':
                    return 'CONTINUE'



                # Substitute variables now
                sys_vars = self._get_system_vars()
                line = replace_vars_runtime(act, variables, loop_vars, sys_vars)
                if log_callback:
                    log_callback(f"{line}")
                parts = [p.strip() for p in line.split(',')]
                cmd = parts[0].lower()

                try:
                    if cmd == 'press':
                        keys_str, dur_str = parts[1], parts[2]
                        duration = float(dur_str) / speed
                        keys = [getattr(Key, k, k) for k in keys_str.split('+')]
                        for k in keys: self.kb.press(k)
                        time.sleep(duration)
                        for k in reversed(keys): self.kb.release(k)

                    elif cmd == 'hotkey':
                        keys = [getattr(Key, k, k) for k in parts[1].split('+')]
                        for k in keys: self.kb.press(k)
                        for k in reversed(keys): self.kb.release(k)

                    elif cmd == 'type':
                        text = parts[1]
                        for char in text:
                            self.kb.press(char)
                            self.kb.release(char)
                            time.sleep(0.03 / speed)

                    elif cmd == 'wait':
                        time.sleep(float(parts[1]) / speed)

                    elif cmd in ['lmc', 'rmc', 'mmc']:
                        btn = {'lmc': Button.left, 'rmc': Button.right, 'mmc': Button.middle}[cmd]
                        self._click(btn)

                    elif cmd == 'click':
                        x, y, btn = int(parts[1]), int(parts[2]), parts[3]
                        self.ms.position = (x, y)
                        self._click({'left': Button.left, 'right': Button.right, 'middle': Button.middle}[btn])

                    elif cmd == 'move':
                        self.ms.position = (int(parts[1]), int(parts[2]))

                    elif cmd == 'scroll':
                        direction, amount = parts[1], int(parts[2])
                        self.ms.scroll(0, amount if direction == 'up' else -amount)

                    elif cmd == 'on':
                        btn = Button.left if parts[1] in ['lmc', 'left'] else Button.right
                        self.ms.press(btn)

                    elif cmd == 'off':
                        btn = Button.left if parts[1] in ['lmc', 'left'] else Button.right
                        self.ms.release(btn)

                    elif cmd == 'echo':
                        if log_callback:
                            log_callback(f"[ECHO] {','.join(parts[1:])}")

                    elif cmd == 'input':
                        # syntax: input, "Message", $var
                        prompt = parts[1].strip('"')
                        dest = parts[2] if len(parts) > 2 else None
                        
                        # Utiliser la GUI pour la saisie thread-safe
                        if self.gui_callback:
                            val = self.gui_callback.ask_input(prompt)
                        else:
                            # Fallback : saisie console
                            val = input(f"{prompt}: ")
                        
                        if val is None:
                            val = ""
                        
                        if dest and dest.startswith('$'):
                            variables[dest] = val

                    elif cmd == 'input_var':
                        # syntax: input_var, $var, "Message"
                        var_name = parts[1].strip()
                        prompt = parts[2].strip().strip('"')
                        if log_callback:
                            log_callback(f"[INPUT] Demande: {prompt} pour variable {var_name}")
                        
                        # Utiliser la GUI pour la saisie thread-safe
                        if self.gui_callback:
                            val = self.gui_callback.ask_input(prompt)
                        else:
                            # Fallback : saisie console
                            val = input(f"{prompt}: ")
                        
                        if val is None:
                            val = ""
                        
                        if log_callback:
                            log_callback(f"[INPUT] Valeur reçue: {val}")
                        
                        if var_name.startswith('$'):
                            variables[var_name] = val
                            if log_callback:
                                log_callback(f"[INPUT] Variable {var_name} = {val}")

                    else:
                        if log_callback:
                            log_callback(f"[UNKNOWN CMD] {cmd}")

                except Exception as e:
                    if log_callback:
                        log_callback(f"[ERREUR] {line} → {e}")

                i += 1
                continue

            i += 1

    def _click(self, button):
        self.ms.press(button)
        time.sleep(0.05)
        self.ms.release(button)

    def stop(self):
        self.stop_event.set()

    def pause(self):
        self.pause_event.set()

    def resume(self):
        self.pause_event.clear()


# ============================
# Helpers
# ============================

def replace_cond_vars(cond, vars_dict, loop_vars, system_vars):
    # Remplace les variables dans une condition avant d'envoyer à safe_eval_expr
    s = cond
    for k, v in (vars_dict or {}).items():
        s = s.replace(k, str(v))
    for k, v in (loop_vars or {}).items():
        s = s.replace(k, str(v))
    for k, v in (system_vars or {}).items():
        s = s.replace(k, str(v))
    # Remplace 'and'/'or'/'not' en opérateurs python compatibles
    s = s.replace(' and ', ' and ')
    s = s.replace(' or ', ' or ')
    s = s.replace(' not ', ' not ')
    return s


# ============================
# Interface (mise à jour minimale)
# - start_macro passe maintenant variables à engine.execute
# ============================

class MacroGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Macro Builder v3.0+ (extended)")
        self.geometry("900x700")
        self.engine = MacroEngine(gui_callback=self)
        self._build_ui()

    def _build_ui(self):
        menubar = tk.Menu(self)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Ouvrir", command=self.load_file)
        filemenu.add_command(label="Enregistrer", command=self.save_file)
        menubar.add_cascade(label="Fichier", menu=filemenu)

        runmenu = tk.Menu(menubar, tearoff=0)
        runmenu.add_command(label="Valider Syntaxe", command=self.validate_syntax)
        menubar.add_cascade(label="Édition", menu=runmenu)

        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="À propos", command=lambda: messagebox.showinfo("À propos", "Macro Builder v3.0+ (extended)"))
        menubar.add_cascade(label="Aide", menu=helpmenu)

        self.config(menu=menubar)

        ttk.Label(self, text="Script Macro :").pack(anchor='w', padx=10, pady=5)
        self.text = tk.Text(self, height=22)
        self.text.pack(fill='both', expand=True, padx=10)

        ttk.Label(self, text="Console :").pack(anchor='w', padx=10, pady=5)
        self.console = tk.Text(self, height=10, state='disabled', bg='#222', fg='#0f0', font=('Consolas', 10))
        self.console.pack(fill='x', padx=10)

        ctrl = ttk.Frame(self)
        ctrl.pack(fill='x', pady=5)
        ttk.Label(ctrl, text="Vitesse :").pack(side='left', padx=5)
        self.speed = tk.DoubleVar(value=1.0)
        ttk.Scale(ctrl, from_=0.1, to=5.0, variable=self.speed, orient='horizontal').pack(side='left', fill='x', expand=True)
        ttk.Button(ctrl, text="▶ Exécuter", command=self.start_macro).pack(side='right', padx=5)
        ttk.Button(ctrl, text="⏸ Pause", command=self.pause_macro).pack(side='right', padx=5)
        ttk.Button(ctrl, text="⏹ Arrêter", command=self.stop_macro).pack(side='right')

    def log_console(self, msg):
        self.console.config(state='normal')
        self.console.insert('end', f"[{datetime.datetime.now().strftime('%H:%M:%S')}] {msg}\n")
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

    def validate_syntax(self):
        try:
            parse_script(self.text.get('1.0', 'end'))
            messagebox.showinfo("Validation", "Syntaxe OK")
        except Exception as e:
            messagebox.showerror("Erreur syntaxe", str(e))

    def start_macro(self):
        try:
            actions, variables = parse_script(self.text.get('1.0', 'end'))
        except SyntaxError as e:
            messagebox.showerror("Erreur", str(e))
            return
        self.engine.stop_event.clear()
        self.console.config(state='normal')
        self.console.delete('1.0', 'end')
        self.console.config(state='disabled')
        threading.Thread(target=self.engine.execute, args=(actions, variables, self.speed.get(), self.log_console), daemon=True).start()

    def stop_macro(self):
        self.engine.stop()

    def pause_macro(self):
        if not self.engine.pause_event.is_set():
            self.engine.pause()
            self.log_console("⏸ Pause activée")
        else:
            self.engine.resume()
            self.log_console("▶ Reprise")

    def ask_input(self, prompt):
        """Méthode thread-safe pour demander une saisie utilisateur"""
        result = [None]
        
        def do_ask():
            try:
                val = simpledialog.askstring("Saisie", prompt, parent=self)
                result[0] = val if val is not None else ""
            except Exception as e:
                self.log_console(f"[ERREUR INPUT] {e}")
                result[0] = ""
        
        # Exécuter dans le thread principal
        self.after(0, do_ask)
        
        # Attendre le résultat avec une boucle d'attente
        import time
        timeout = 0
        while result[0] is None and timeout < 300:  # 30 secondes max
            self.update()
            time.sleep(0.1)
            timeout += 1
        
        return result[0] if result[0] is not None else ""


if __name__ == '__main__':
    app = MacroGUI()
    app.mainloop()
