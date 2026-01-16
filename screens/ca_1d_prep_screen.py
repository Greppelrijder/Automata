import tkinter as tk
import sys
from .screen import Screen
from .screen_manager import execute

sys.path.append("..")
from models.boundry_conditions import BoundryConditions



def run(root: tk.Misc, args) -> None:

    canvas = tk.Canvas(root)
    canvas.place(x = 0, y = 0, width = 800, height = 400)

    # creating widgets
    header = tk.Label(canvas, text="Creating 1D CA")
    go_back_button = tk.Button(canvas, text="back", command= lambda: execute(Screen.Main_menu, None))
    size_entry = tk.Entry(canvas)
    ruleset_entry = tk.Entry(canvas)

    opt = tk.StringVar(value=BoundryConditions.Dirichlet0.name)
    boundry_conditions_dropdown = tk.OptionMenu(canvas, opt, *BoundryConditions._member_names_)

    name_entry = tk.Entry(canvas)
    create_button = tk.Button(canvas, text="Create", command = lambda: execute(Screen.CA_1D_simulation, (
        int(size_entry.get()),
        ruleset_entry.get(),
        BoundryConditions[opt.get()],
        name_entry.get()
        )))

    # widget presets
    try: # use presets that were passed through args
        size_preset = str(int(args[0]))
        ruleset_preset = str(args[1])
        assert isinstance(boundry_conditions_preset := args[2], BoundryConditions)
        name_preset: str = str(args[3])
    except (TypeError, IndexError, ValueError, AssertionError): # no presets passed -> use default
        size_preset = "9"
        ruleset_preset = "00011110"
        boundry_conditions_preset = BoundryConditions.Dirichlet0
        name_preset = "New"  
    size_entry.insert(0, size_preset)
    ruleset_entry.insert(0, ruleset_preset)
    name_entry.insert(0, name_preset)
    opt.set(boundry_conditions_preset.name)

    # placing widgets
    header.place(x=400, y=0)
    go_back_button.place(x=400, y=50)
    size_entry.place(x=400, y=100)
    ruleset_entry.place(x=400, y=125)
    boundry_conditions_dropdown.place(x=400, y=150)
    name_entry.place(x=400, y=200)
    create_button.place(x=400, y=225)