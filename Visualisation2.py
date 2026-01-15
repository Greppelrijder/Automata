import tkinter as tk
from tkinter import ttk

from models.ca_1d import CA_1D
from models.boundry_conditions import BoundryConditions

from screens import Screen
import screen_manager

import starting_screen
import main_menu

root = tk.Tk()
root.title("Cellular Automa in 1D and 2D")
root.geometry("1000x500")
root.resizable(False, False)

test: CA_1D = CA_1D(10, "11111111", BoundryConditions.Dirichlet0)

screen_manager.register(Screen.Starting_screen, starting_screen.run)
screen_manager.register(Screen.Main_menu, main_menu.run)

screen_manager.run(Screen.Starting_screen, root, None)

root.mainloop()