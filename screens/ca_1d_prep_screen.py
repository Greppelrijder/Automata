import tkinter as tk
from .screen import Screen
from .screen_manager import execute


def run(root: tk.Tk, args) -> None:

    canvas = tk.Canvas(root)
    canvas.place(x = 0, y = 0, width = 800, height = 400)

    # creating widgets
    header = tk.Label(canvas, text="Creating 1D CA")
    go_back_button = tk.Button(canvas, text="back", command= lambda: execute(Screen.Main_menu, root, None))
    size_entry = tk.Entry(canvas)
    ruleset_entry = tk.Entry(canvas)
    boundry_conditions_entry = tk.Entry(canvas)
    name_entry = tk.Entry(canvas)
    create_button = tk.Button(canvas, text="Create", command = lambda: execute(Screen.CA_1D_simulation, root, (
        int(size_entry.get()),
        ruleset_entry.get(),
        boundry_conditions_entry.get(),
        name_entry.get()
        )))

    # widget presets
    try: # use presets that were passed through args
        size_preset = str(int(args[0]))
        ruleset_preset = str(args[1])
        boundry_conditions_preset = str(args[2])
        name_preset: str = str(args[3])
    except (TypeError, IndexError, ValueError): # no presets passed -> use default
        size_preset = "9"
        ruleset_preset = "00011110"
        boundry_conditions_preset = "Dirichlet0"
        name_preset = "New"  
    size_entry.insert(0, size_preset)
    ruleset_entry.insert(0, ruleset_preset)
    boundry_conditions_entry.insert(0, boundry_conditions_preset)
    name_entry.insert(0, name_preset)

    # placing widgets
    header.place(x=400, y=0)
    go_back_button.place(x=400, y=50)
    size_entry.place(x=400, y=100)
    ruleset_entry.place(x=400, y=125)
    boundry_conditions_entry.place(x=400, y=150)
    name_entry.place(x=400, y=200)
    create_button.place(x=400, y=225)