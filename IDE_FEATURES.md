# Macro Builder v4.0 - Professional IDE

## 🎉 What's New

Your macro builder has been transformed into a professional IDE with advanced features comparable to VSCode, PyCharm, and other modern code editors!

## ✨ New Features

### 1. Advanced Syntax Highlighting
Beautiful color-coded syntax for better readability:

- **Keywords** (`press`, `click`, `loop`, `if`, etc.) → **Blue & Bold**
- **User Variables** (`$counter`, `$myvar`) → **Teal**
- **System Variables** (`$mouse_x`, `$mouse_y`, `@speed`) → **Orange & Bold**
- **Strings** (`"text"`, `'message'`) → **Red**
- **Numbers** (`123`, `4.5`) → **Green**
- **Comments** (`# comment`) → **Green & Italic**
- **Functions** (`my_function()`) → **Gold/Brown**
- **Operators** (`+`, `-`, `=`, `<`, `>`) → **Black**

### 2. Intelligent Auto-Completion
Type-ahead suggestions as you code:

- **Command suggestions**: Start typing `pr` → suggests `press,key`
- **Parameter hints**: See command signatures like `click,x,y,button`
- **System variables**: Auto-suggest `$mouse_x`, `$screen_width`, etc.
- **User functions**: Automatically suggests your defined functions
- **Triggers after 1 character** for instant feedback

**How to use**: Just start typing! Press `Tab` or `Enter` to accept a suggestion.

### 3. Code Folding
Collapse and expand code blocks for better organization:

- Fold `loop...endloop` blocks
- Fold `if...endif` conditionals
- Fold `function...endfunction` definitions
- Click the **arrows** in the margin to fold/unfold

### 4. Real-Time Error Highlighting
Catch errors before running:

- **Red squiggly underlines** for syntax errors
- **Error annotations** with helpful messages
- **Live validation** as you type (500ms debounce)
- Uses your existing parser for accuracy

### 5. Advanced Search & Replace
Powerful text search with regex support:

- **Keyboard shortcuts**:
  - `Ctrl+F` → Open find dialog
  - `Ctrl+H` → Open replace dialog
- **Features**:
  - Find next/previous
  - Replace one or replace all
  - Case-sensitive search
  - Whole word matching
  - **Regular expression** support
  - Search wrapping

### 6. Professional Editor Features
Everything you expect from a modern IDE:

- **Line numbers** with clickable margins
- **Breakpoint markers** (red circles)
- **Debug line highlighting** (yellow arrow)
- **Brace matching** (highlights matching parentheses)
- **Current line highlighting** (light blue background)
- **Auto-indentation**
- **Undo/Redo** support
- **Smooth scrolling**

## 🚀 How to Use

### Starting the IDE

```bash
cd C:\dev\map\macro-pite-main
python main.py
```

### Testing Features

1. Open the test file to see syntax highlighting:
   - File → Ouvrir → `test_ide_features.txt`

2. Try auto-completion:
   - Type `pr` and wait for suggestions
   - Type `$` to see variable suggestions
   - Type `loop,` to see loop syntax

3. Test code folding:
   - Look for **▼** arrows next to `loop`, `if`, `function`
   - Click to collapse/expand blocks

4. Try search & replace:
   - Press `Ctrl+F` to find text
   - Press `Ctrl+H` to replace text
   - Enable "Regular expression" for advanced patterns

5. Debug with breakpoints:
   - Click the **margin** (left of line numbers) to add breakpoint
   - Press `F8` to enable debug mode
   - Press `F5` to run the macro
   - It will pause at breakpoints

### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+N` | New file |
| `Ctrl+O` | Open file |
| `Ctrl+S` | Save file |
| `Ctrl+F` | Find |
| `Ctrl+H` | Replace |
| `F5` | Run macro |
| `F7` | Validate syntax |
| `F8` | Toggle debug mode |
| `F9` | Toggle breakpoint |
| `F10` | Step next (debug) |
| `Ctrl+Z` | Undo |
| `Ctrl+Y` | Redo |

## 📁 File Structure

```
macro-pite-main/
├── ui/
│   ├── editor.py          # NEW: QScintilla professional editor
│   ├── lexer.py           # NEW: Custom syntax highlighting
│   ├── autocomplete.py    # NEW: Auto-completion system
│   ├── window.py          # UPDATED: PyQt5 main window
│   └── controls.py        # UPDATED: PyQt5 control panel
├── engine/
│   ├── validator.py       # NEW: Real-time error detection
│   ├── parser.py          # (unchanged)
│   ├── executor.py        # (unchanged)
│   └── context.py         # (unchanged)
├── main.py                # UPDATED: PyQt5 entry point
└── test_ide_features.txt  # NEW: Test file showcasing features
```

## 🎨 Color Scheme

The IDE uses a VSCode-inspired color scheme:

- **Background**: White
- **Current line**: Light blue (`#E8F2FF`)
- **Selection**: Blue (`#A6D2FF`)
- **Line numbers**: Gray background (`#F0F0F0`)
- **Margins**: Light gray
- **Console**: Dark theme (black background, green text)

## 🔧 Technical Details

### Dependencies
- **PyQt5** (v5.15.11) - Modern GUI framework
- **QScintilla** (v2.14.1) - Professional code editor component
- **pynput** (v1.8.1) - Keyboard/mouse control (existing)

### What Was Changed
- ✅ Migrated from **Tkinter** to **PyQt5**
- ✅ Replaced basic text widget with **QScintilla** editor
- ✅ Added custom **lexer** for syntax highlighting
- ✅ Integrated **auto-completion** API
- ✅ Real-time **validation** with error indicators
- ✅ Advanced **search/replace** dialog
- ✅ **All existing features preserved**:
  - Breakpoints and debug mode
  - Macro recording
  - JSON import/export
  - Speed and iteration controls
  - Console output
  - Variable inspector

### Backward Compatibility
Your old Tkinter files have been backed up:
- `ui/editor.py.tkinter.bak`
- `ui/window.py.tkinter.bak`
- `ui/controls.py.tkinter.bak`
- `main.py.tkinter.bak`

## 💡 Tips & Tricks

1. **Maximize productivity**: Use code folding to focus on specific sections
2. **Quick navigation**: Press `Ctrl+F` and use regex to find complex patterns
3. **Error prevention**: Watch for red squiggles before running
4. **Learn shortcuts**: Right-click for context menu options
5. **Customize speed**: Use the slider for precise control
6. **Debug efficiently**: Set breakpoints on critical lines

## 🐛 Known Limitations

- Code folding works best with properly indented code
- Auto-completion triggers after 1 character (can feel aggressive)
- Error highlighting has 500ms delay (by design to avoid lag)

## 🎯 Next Steps

Try these to explore the IDE:

1. Open `test_ide_features.txt` to see all syntax highlighting
2. Create a new macro and test auto-completion
3. Try folding all loop blocks
4. Search for `$` using regex to find all variables
5. Set breakpoints and debug your macro

---

**Enjoy your new professional IDE! 🚀**

For questions or issues, check the plan file at:
`C:\Users\Axel\.claude\plans\generic-yawning-wilkinson.md`
