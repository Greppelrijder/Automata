import tkinter as tk
from screen import Screen
import screen_manager


def run(root: tk.Tk, args: object) -> None:
    canvas = tk.Canvas(root)
    canvas.place(x = 0, y = 0, width = 800, height = 400)

    header: tk.Label = tk.Label(root, text="Main menu")
    back_button: tk.Button = tk.Button(root, text="back", command= lambda : screen_manager.run(Screen.Starting_screen, root, None))

    header.place(x=400, y=0)
    back_button.place(x=400, y=50)
