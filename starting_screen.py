import tkinter as tk
from screens import Screen
import screen_manager


def run(root: tk.Tk, args: object) -> None:
    canvas = tk.Canvas(root)
    canvas.place(x = 0, y = 0, width = 800, height = 400)

    header: tk.Label = tk.Label(root, text="Cellular automata")
    main_menu_button: tk.Button = tk.Button(root, text="Main menu", command= lambda : screen_manager.run(Screen.Main_menu, root, None))

    header.place(x=400, y=0)
    main_menu_button.place(x=400, y=50)