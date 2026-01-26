import tkinter as tk
import tkinter.font as tkFont

from .screen_list import ScreenList
from .screen_manager import execute
from .screen import Screen




class StartingScreen(Screen):
    """
    The starting screen features:
    * A button that brings the user to the main menu  
    """
    def __init__(self, root: tk.Tk) -> None:
        super().__init__(root)

        # Define a custom font
        custom_font = tkFont.Font(family="Arial", size=25)


        self.header: tk.Label = tk.Label(self.frame, text="Cellular automata", font=custom_font, padx=30, pady=50, justify="center", background="#8D8A8A")
        self.main_menu_button = tk.Button(self.frame, border=5,background="#2DE840", activebackground="#178122", 
                                                     text="Main menu",fg="#202020", activeforeground="#202020", font=custom_font, 
                                                     justify="center",
                                                     command= lambda : execute(ScreenList.MainMenu, None))

    def run(self, args) -> None:
        """
        For this Screen, the 'args' parameter is unused
        """
        self.frame.place(x = 0, y = 0)
        self.header.place(relx=0.5, rely=0.15, anchor="center")
        self.main_menu_button.place(relx=0.5, rely=0.5, anchor="center")