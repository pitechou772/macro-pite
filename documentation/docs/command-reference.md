# Macro Builder DSL – Command Reference

This page lists the most important commands of the Macro Builder scripting language (DSL) with **simple explanations** and **color‑friendly examples**.

> Tip: open this file in the IDE to see full syntax highlighting.

---

## 1. Variables

### 1.1 User variables

Variables start with `$`.

```text
$Name = "Axel"
$Count = 3
$Speed = 1.5
```

Supported types:

- numbers: `1`, `2.5`
- strings: `"hello"`
- booleans (via expressions): `true`, `false`

You can update variables:

```text
$Score += 10
$HP -= 1
```

### 1.2 Special / system variables

Some variables are provided automatically by the engine:

- `$i` – loop index (starts at 0)
- `$mouse_x`, `$mouse_y` – current mouse position
- `$screen_width`, `$screen_height` – screen size
- `$timestamp` – current timestamp
- `$random` – random value
- `@speed` – global speed multiplier
- `@iterations` – number of iterations set in the UI

Example:

```text
loop,5
    echo, Loop $i at position $mouse_x / $mouse_y
    wait,0.5
endloop
```

### 1.3 User input

Ask the user for a value (thread‑safe dialog):

```text
$Name = input,"Enter your name"
$Times = input,"How many times?"
```

---

## 2. Flow control

### 2.1 Loops

Simple loop with a fixed count:

```text
loop,5
    echo, Loop $i
    wait,0.5
endloop
```

Infinite loop (⚠ always use a `wait` inside):

```text
loop,infinite
    echo, Running forever
    wait,1
endloop
```

### 2.2 While loop

```text
$HP = 3

while,$HP > 0
    echo, HP = $HP
    wait,1
    $HP -= 1
endwhile
```

### 2.3 Conditions

Basic `if`:

```text
if,$HP > 50
    echo, High HP
endif
```

If / else:

```text
if,$mouse_x > $screen_width / 2
    echo, Mouse on the right side
else
    echo, Mouse on the left side
endif
```

If / elseif / else:

```text
if,$HP > 70
    echo, HP high
elseif,$HP > 30
    echo, HP medium
else
    echo, HP low
endif
```

You can use logical operators: `and`, `or`, `not`.

Example:

```text
if,$HP > 0 and $Mana > 10
    echo, Can cast spell
endif
```

### 2.4 Break / continue

```text
loop,10
    if,$i == 5
        break
    endif
    if,$i % 2 == 0
        continue
    endif
    echo, i = $i
endloop
```

---

## 3. Keyboard commands

### 3.1 Press a key

```text
press,a,0.1          # Press key "a" for 0.1s
press,ctrl+c,0.05    # Press CTRL+C
hotkey,alt+tab       # ALT+TAB shortcut
```

### 3.2 Type text

```text
type,Hello world!
```

You can mix variables:

```text
$Name = "Axel"
type,Hello $Name
```

---

## 4. Mouse commands

### 4.1 Simple clicks

Short aliases:

```text
lmc              # Left mouse click
rmc              # Right mouse click
mmc              # Middle mouse click
```

### 4.2 Click at position

```text
click,100,200,left
click,500,400,right
```

### 4.3 Move and drag

```text
move,400,300
wait,0.2
lmc

# Drag from (100,100) to (400,400)
drag,100,100,400,400
```

### 4.4 Scroll

```text
scroll,up,3
scroll,down,10
```

---

## 5. Timing and control commands

### 5.1 Wait

```text
wait,1       # wait 1 second
wait,0.25    # wait 0.25 second
```

### 5.2 Echo (log to console)

```text
echo, Starting macro
loop,3
    echo, Loop $i
    wait,1
endloop
echo, Done
```

### 5.3 Breakpoints and debug

```text
breakpoint
```

When the executor hits `breakpoint`, execution pauses in **debug mode**. You can also:

- set/remove breakpoints by clicking in the margin
- use **F8** to toggle debug mode
- use **F10** to step

---

## 6. Pixel / color checks

> Requires Pillow (`PIL`) installed. Used internally by the engine.

Check if a pixel has a specific color:

```text
if,pixel,100,200,#FF0000
    echo, Pixel is red
endif
```

You can combine with loops or waits to build “wait until screen is ready” logic.

---

## 7. Functions

### 7.1 Define a function

```text
function heal()
    press,h,0.1
    wait,0.2
endfunction
```

### 7.2 Call a function

```text
heal()
```

Functions:

- have **no return value**
- can read and modify global variables

Example:

```text
$Times = 3

function buff()
    echo, Casting buff $i
    press,f1,0.1
    wait,1
endfunction

loop,$Times
    buff()
endloop
```

---

## 8. Example full script

```text
# Ask user
$Name = input,"Your name?"
$Loops = input,"How many loops?"

# Greet
echo, Hello $Name

# Main loop
loop,$Loops
    echo, Loop $i for $Name
    type,Hello from Macro Builder
    wait,1
endloop

echo, Finished!
```

---

If you want even more detail (all internal rules and architecture), check the **full technical spec** in `README.md`.
