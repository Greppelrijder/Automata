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
    starting_state_entry = tk.Entry(canvas)
    ca_display = tk.Label(canvas)
    confirm_starting_state_button = tk.Button(canvas, text="confirm", command = lambda: on_confirm_starting_state())
    next_state_button = tk.Button(canvas, text="next", command = lambda: on_next_state())
    prev_state_button = tk.Button(canvas, text="previous", command = lambda: on_prev_state())

    # configuring widgets
    starting_state_entry.insert(0, "0" * grid_size)
    next_state_button.config(state="disabled")
    prev_state_button.config(state="disabled")

    # placing widgets
    header.place(x=400, y=0)
    size_label.place(x=400, y=50)
    ruleset_label.place(x=400, y=75)
    boundry_conditions_label.place(x=400, y=100)
    starting_state_entry.place(x=400,y=200)
    confirm_starting_state_button.place(x=400, y=225)
    next_state_button.place(x=400, y=250)
    prev_state_button.place(x=450, y=250)
    go_back_button.place(x=400, y=350)


    # commands
    def on_confirm_starting_state() -> None:

        ca.configure_initial_state([int(char) for char in starting_state_entry.get()])
        ca_display.config(text=starting_state_entry.get())

        entry_x, entry_y = starting_state_entry.winfo_x(), starting_state_entry.winfo_y()    

        starting_state_entry.destroy()
        ca_display.place(x=entry_x, y=entry_y)
        
        confirm_starting_state_button.config(state="disabled")
        next_state_button.config(state="normal")
        prev_state_button.config(state="normal")

    def on_next_state() -> None:
        ca.evolve()
        ca_display.config(text="".join(str(s) for s in ca.get_states()))

    def on_prev_state() -> None:
        print("test")
        ca.devolve()
        ca_display.config(text="".join(str(s) for s in ca.get_states()))