import tkinter as tk
from .screen_list import ScreenList
from .screen_manager import execute
from .screen import Screen


class StartingScreen(Screen):

    def __init__(self, root: tk.Tk) -> None:
        super().__init__(root)

        self.header: tk.Label = tk.Label(self.canvas, text="Cellular automata")
        self.main_menu_button: tk.Button = tk.Button(self.canvas, text="Main menu", command= lambda : execute(ScreenList.MainMenu, None))


    def run(self, args) -> None:
        self.canvas.place(x = 0, y = 0, width = 800, height = 400)
        self.header.place(x=400, y=0)
        self.main_menu_button.place(x=400, y=50)