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
    
    size_slider = tk.Scale(canvas, from_ = 1, to = 21, orient="horizontal")

    ruleset = tk.StringVar()
    ruleset_entry = tk.Entry(canvas, textvariable=ruleset)
    invalid_ruleset_warning = tk.Label(canvas, fg="red", text="Ruleset must consist of 8 characters")

    boundry_condition_choice = tk.StringVar(value=BoundryConditions.Dirichlet0.name)
    boundry_conditions_dropdown = tk.OptionMenu(canvas, boundry_condition_choice, *BoundryConditions._member_names_)

    name = tk.StringVar()
    name_entry = tk.Entry(canvas, textvariable=name)
    invalid_name_warning = tk.Label(canvas, fg="red", text="Name must be non-empty")
    
    create_button = tk.Button(canvas, text="Create", command = lambda: on_create())

    # widget presets
    try: # use presets that were passed through args
        size_preset = int(args[0])
        ruleset_preset = str(args[1])
        assert isinstance(boundry_conditions_preset := args[2], BoundryConditions)
        name_preset: str = str(args[3])
    except (TypeError, IndexError, ValueError, AssertionError): # no presets passed -> use default
        size_preset = "9"
        ruleset_preset = "00011110"
        boundry_conditions_preset = BoundryConditions.Dirichlet0
        name_preset = "New"  
    size_slider.set(size_preset)
    ruleset.set(ruleset_preset)
    name.set(name_preset)
    boundry_condition_choice.set(boundry_conditions_preset.name)

    # placing widgets
    header.place(x=400, y=0)
    go_back_button.place(x=400, y=50)
    size_slider.place(x=400, y=75)
    ruleset_entry.place(x=400, y=125)
    boundry_conditions_dropdown.place(x=400, y=150)
    name_entry.place(x=400, y=200)
    create_button.place(x=400, y=225)

    # automatic warnings on invalid input
    def validate_name() -> bool:
        if len(name.get()) == 0:
            invalid_name_warning.place(x=400, y=250)
            return False
        else:
            invalid_name_warning.place_forget()
            return True
        
    def validate_ruleset() -> bool:
        ruleset_value = ruleset.get()
        if len(ruleset_value) != 8:
            invalid_ruleset_warning.config(text="Ruleset must consist of 8 characters")
            invalid_ruleset_warning.place(x=400, y=250)
            return False
        elif not all(char in ["0", "1"] for char in ruleset_value):
            invalid_ruleset_warning.config(text="Ruleset must consist of only 1's & 0's")
            invalid_ruleset_warning.place(x=400, y=250)
            return False
        else:
            invalid_ruleset_warning.place_forget()
            return True

    ruleset.trace_add("write", callback = lambda *args: validate_ruleset())
    name.trace_add("write", callback= lambda *args: validate_name())

    # commands
    def on_create() -> None:
        if not (validate_name() and validate_ruleset()):
            return
        size = int(size_slider.get())
        ruleset_value = ruleset.get()
        boundry_conditions = BoundryConditions[boundry_condition_choice.get()]
        name_value = name.get()
        execute(Screen.CA_1D_simulation, (size, ruleset_value, boundry_conditions, name_value))