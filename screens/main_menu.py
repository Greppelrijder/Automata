import tkinter as tk
from .screen_list import ScreenList
from .screen_manager import execute
from .screen import Screen

class MainMenu(Screen):

    def __init__(self, root: tk.Tk):
        super().__init__(root)

        self.header: tk.Label = tk.Label(self.canvas, text="Main menu")
        self.go_back_button: tk.Button = tk.Button(self.canvas, text="back", command= lambda: execute(ScreenList.StartingScreen, None))
        self.ca_1d_button: tk.Button = tk.Button(self.canvas, text="1D", command = lambda: execute(ScreenList.CA1D_Preparation, None))
        self.ca_2d_button: tk.Button = tk.Button(self.canvas, text="2D", command= lambda: execute(ScreenList.CA2D_Preparation, None))

    def run(self, args) -> None:
        self.canvas.place(x = 0, y = 0, width = 800, height = 400)
        self.header.place(x=400, y=0)
        self.go_back_button.place(x=400, y=50)
        self.ca_1d_button.place(x=400, y=75)
        self.ca_2d_button.place(x=400, y=100)

