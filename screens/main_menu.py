import tkinter as tk
import tkinter.font as tkFont
from .screen_list import ScreenList
from .screen_manager import execute
from .screen import Screen

class MainMenu(Screen):

    def __init__(self, root: tk.Tk):
        super().__init__(root)

        custom_font = tkFont.Font(family="Arial", size=25)

        self.header: tk.Label = tk.Label(self.frame, text="Main menu", font=custom_font, padx=30, pady=50, justify="center", background="#8D8A8A")
        self.go_back_button: tk.Button = tk.Button(self.frame, text="back", border=5,background="#2DE840", activebackground="#178122", 
                                                     fg="#202020", activeforeground="#202020", font=custom_font, justify="center", 
                                                     command= lambda: execute(ScreenList.StartingScreen, None))
        self.ca_1d_button: tk.Button = tk.Button(self.frame, text="1D", border=5,background="#2DE840", activebackground="#178122", 
                                                     fg="#202020", activeforeground="#202020", font=custom_font, justify="center",
                                                     command = lambda: execute(ScreenList.CA1D_Preparation, None))
        self.ca_2d_button: tk.Button = tk.Button(self.frame, text="2D", border=5,background="#2DE840", activebackground="#178122", 
                                                     fg="#202020", activeforeground="#202020", font=custom_font, justify="center",
                                                     command= lambda: execute(ScreenList.CA2D_Preparation, None))
        self.ca_2d_4_button: tk.Button = tk.Button(self.frame, text="2D with 4 neighbours", border=5,background="#2DE840", activebackground="#178122", 
                                                     fg="#202020", activeforeground="#202020", font=custom_font, justify="center",
                                                     command= lambda: execute(ScreenList.CA2D_4_Preparation, None))


    def run(self, args) -> None:
        self.frame.place(x = 0, y = 0)
        self.header.place(relx=0.5, rely=0.15, anchor="center")
        self.go_back_button.place(relx=0.01, rely=0.01, anchor="nw")
        self.ca_1d_button.place(relx=1/3, rely=0.55, anchor="center")
        self.ca_2d_button.place(relx=2/3, rely=0.55, anchor="center")
        self.ca_2d_4_button.place(relx=0.5, rely=0.8, anchor="center")