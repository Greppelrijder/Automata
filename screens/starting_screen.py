import tkinter as tk
from .screen import Screen
from .screen_manager import execute


def run(root: tk.Tk, args: object) -> None:
    canvas = tk.Canvas(root)
    canvas.place(x = 0, y = 0, width = 800, height = 400)

    header: tk.Label = tk.Label(canvas, text="Cellular automata")
    main_menu_button: tk.Button = tk.Button(canvas, text="Main menu", command= lambda : execute(Screen.Main_menu, root, None))

    header.place(x=400, y=0)
    main_menu_button.place(x=400, y=50)