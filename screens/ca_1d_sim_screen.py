import tkinter as tk
from .screen import Screen
from .screen_manager import execute


def run(root: tk.Tk, args: object) -> None:

    if not isinstance(args, tuple):
        raise ValueError(f"For ca_1d_sim_screen, the 'args' parameter must be of type tuple[int, str, str, str] (got {type(args)})")
    
    try:
        grid_size = int(args[0])
        ruleset = str(args[1])
        boundry_conditions = str(args[2])
        name = str(args[3])
    except (IndexError, ValueError):
        raise ValueError(f"For ca_1d_sim_screen, the 'args' parameter must be of type tuple[int, str, str, str] (got {type(args)})")

    canvas = tk.Canvas(root)
    canvas.place(x = 0, y = 0, width = 800, height = 400)

    header = tk.Label(canvas, text=f"Simulating 1D CA '{name}'")
    size_label = tk.Label(canvas, text=f"Size: {grid_size}")
    ruleset_label = tk.Label(canvas, text=f"Rules: {ruleset}")
    boundry_conditions_label = tk.Label(canvas, text=f"Boundry conditions: {boundry_conditions}")
    go_back_button = tk.Button(canvas, text="back", command= lambda: execute(Screen.CA_1D_preparation, root, (
        grid_size, 
        ruleset, 
        boundry_conditions, 
        name
        )))


    header.place(x=400, y=0)
    size_label.place(x=400, y=50)
    ruleset_label.place(x=400, y=75)
    boundry_conditions_label.place(x=400, y=100)
    go_back_button.place(x=400, y=150)
