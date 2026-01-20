import tkinter as tk
import tkinter.font as tkFont
from .screen_list import ScreenList
from .screen_manager import execute
from .screen import Screen

class MainMenu(Screen):

    def __init__(self, root: tk.Tk):
        super().__init__(root)

        custom_font = tkFont.Font(family="Arial", size=25)

        self.header: tk.Label = tk.Label(self.canvas, text="Main menu", font=custom_font, padx=30, pady=50, justify="center", background="#8D8A8A")
        self.go_back_button: tk.Button = tk.Button(self.canvas, text="back", border=5,background="#2DE840", activebackground="#178122", 
                                                     fg="#202020", activeforeground="#202020", font=50, anchor="center", 
                                                     command= lambda: execute(ScreenList.StartingScreen, None))
        self.ca_1d_button: tk.Button = tk.Button(self.canvas, text="1D", border=5,background="#2DE840", activebackground="#178122", 
                                                     fg="#202020", activeforeground="#202020", font=50, anchor="center",
                                                     command = lambda: execute(ScreenList.CA1D_Preparation, None))
        self.ca_2d_button: tk.Button = tk.Button(self.canvas, text="2D", border=5,background="#2DE840", activebackground="#178122", 
                                                     fg="#202020", activeforeground="#202020", font=50, anchor="center",
                                                     command= lambda: execute(ScreenList.CA2D_Preparation, None))


    def run(self, args) -> None:
        self.canvas.place(x = 0, y = 0, width = 800, height = 400)
        self.header.place(x=350, y=10)
        self.go_back_button.place(x=450, y=200)
        self.ca_1d_button.place(x=300, y=200)
        self.ca_2d_button.place(x=600, y=200)

