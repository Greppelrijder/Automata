import tkinter as tk
from .screen import Screen
from .screen_manager import execute


def run(root: tk.Tk, args: object) -> None:
    canvas = tk.Canvas(root)
    canvas.place(x = 0, y = 0, width = 800, height = 400)

    header: tk.Label = tk.Label(root, text="Main menu")
    back_button: tk.Button = tk.Button(root, text="back", command= lambda: execute(Screen.Starting_screen, root, None))
    ca_1d_button: tk.Button = tk.Button(root, text="1D", command = lambda: execute(Screen.CA_1D_preparation, root, None))
    ca_2d_button: tk.Button = tk.Button(root, text="2D", command= lambda: execute(Screen.CA_2D_preparation, root, None))


    header.place(x=400, y=0)
    back_button.place(x=400, y=50)
    ca_1d_button.place(x=400, y=75)
    ca_2d_button.place(x=400, y=100)
