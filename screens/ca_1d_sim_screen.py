import sys
import tkinter as tk


from .screen import Screen
from .screen_manager import execute

sys.path.append("..")
from models.ca_1d import CA_1D
from models.boundry_conditions import BoundryConditions


def run(root: tk.Misc, args: object) -> None:

    # checking args
    error_message = f"For ca_1d_sim_screen, the 'args' parameter must be of type tuple[int, str, BoundryConditions, str] (got {type(args)})"
    if not isinstance(args, tuple):
        raise ValueError(error_message)
    
    try:
        grid_size = int(args[0])
        ruleset = str(args[1])
        assert isinstance(boundry_conditions := args[2], BoundryConditions)
        name = str(args[3])
    except (IndexError, ValueError, AssertionError):
        print(type(args[2]))
        raise ValueError(error_message)

    # setting up CA
    ca = CA_1D(grid_size, ruleset, boundry_conditions)

    # creating widgets
    canvas = tk.Canvas(root)
    canvas.place(x = 0, y = 0, width = 800, height = 400)

    header = tk.Label(canvas, text=f"Simulating 1D CA '{name}'")
    size_label = tk.Label(canvas, text=f"Size: {grid_size}")
    ruleset_label = tk.Label(canvas, text=f"Rules: {ruleset}")
    boundry_conditions_label = tk.Label(canvas, text=f"Boundry conditions: {boundry_conditions.name}")
    go_back_button = tk.Button(canvas, text="back", command= lambda: execute(Screen.CA_1D_preparation, (
        grid_size, 
        ruleset, 
        boundry_conditions, 
        name
        )))
    
    starting_state = tk.StringVar(value= "0" * grid_size)
    starting_state_entry = tk.Entry(canvas, textvariable=starting_state)
    confirm_starting_state_button = tk.Button(canvas, text="confirm", command = lambda: on_confirm_starting_state()) 
    invalid_starting_state_warning = tk.Label(canvas, fg="red", text=f"Starting state must consist of {grid_size} characters")

    ca_display = tk.Label(canvas)
    next_state_button = tk.Button(canvas, text="next", command = lambda: on_next_state())
    prev_state_button = tk.Button(canvas, text="previous", command = lambda: on_prev_state())
    reset_button = tk.Button(canvas, text="reset", command = lambda: on_reset())

    # configuring widgets
    next_state_button.config(state="disabled")
    prev_state_button.config(state="disabled")

    # placing widgets
    header.place(x=400, y=0)
    size_label.place(x=400, y=50)
    ruleset_label.place(x=400, y=75)
    boundry_conditions_label.place(x=400, y=100)
    starting_state_entry.place(x=400,y=200)
    confirm_starting_state_button.place(x=400, y=250)
    next_state_button.place(x=400, y=275)
    prev_state_button.place(x=450, y=275)
    reset_button.place(x=400, y=375)
    go_back_button.place(x=20, y=20)

    # automatic warnings on invalid input
    def validate_starting_state() -> bool:
        starting_state_value = starting_state.get()
        if len(starting_state_value) != grid_size:
            invalid_starting_state_warning.config(text=f"Starting state must consist of {grid_size} characters")
            invalid_starting_state_warning.place(x=400, y=225)
            return False
        elif not all(char in ["0", "1"] for char in starting_state_value):
            invalid_starting_state_warning.config(text=f"Starting state must consist of only 1's & 0's")
            invalid_starting_state_warning.place(x=400, y=225)
            return False
        else:
            invalid_starting_state_warning.place_forget()
            return True
    starting_state.trace_add("write", callback = lambda *args: validate_starting_state())

    # commands
    def on_confirm_starting_state() -> None:

        if not validate_starting_state():
            return
        
        ca.configure_initial_state([int(char) for char in starting_state_entry.get()])
        ca_display.config(text=starting_state_entry.get())

        entry_x, entry_y = starting_state_entry.winfo_x(), starting_state_entry.winfo_y()    

        starting_state_entry.place_forget()
        ca_display.place(x=entry_x, y=entry_y)
        
        confirm_starting_state_button.config(state="disabled")
        next_state_button.config(state="normal")
        prev_state_button.config(state="normal")

    def on_next_state() -> None:
        ca.evolve()
        ca_display.config(text=ca.get_state_string())

    def on_prev_state() -> None:
        try:
            ca.devolve()
            ca_display.config(text=ca.get_state_string())
        except IndexError:
            pass

    def on_reset() -> None:
        try: # set starting state to CA's starting state
            starting_state.set(ca.get_state_string(index = 0)) 
        except IndexError: # CA was not yet initialized
            starting_state.set("0" * grid_size)

        ca.reset()

        ca_display.place_forget()
        starting_state_entry.place(x=400,y=200)
        confirm_starting_state_button.config(state="normal")
        next_state_button.config(state="disabled")
        prev_state_button.config(state="disabled")