import tkinter as tk

from screens.screen_list import ScreenList
import screens.screen_manager as screen_manager

from screens.starting_screen import StartingScreen
from screens.main_menu import MainMenu
from screens.ca_1d_prep_screen import CA1D_PrepScreen
from screens.ca_1d_sim_screen import CA1D_SimScreen
from screens.ca_2d_prep_screen import CA2D_PrepScreen
from screens.ca_2d_sim_screen import CA2D_SimScreen
from screens.ca_2d_4_prep_screen import CA2D_4_PrepScreen
from screens.ca_2d_4_sim_screen import CA2D_4_SimScreen

# setup main window
root = tk.Tk()
root.title("Cellular Automa in 1D and 2D")
root.geometry("1000x500")
root.resizable(False, False)
root.configure(bg = "#8D8A8A")

# instantiate screens
starting_screen = StartingScreen(root)
main_menu = MainMenu(root)
ca_1d_prep_screen = CA1D_PrepScreen(root)
ca_1d_sim_screen = CA1D_SimScreen(root)
ca_2d_prep_screen = CA2D_PrepScreen(root)
ca_2d_sim_screen = CA2D_SimScreen(root)
ca_2d_4_prep_screen = CA2D_4_PrepScreen(root)
ca_2d_4_sim_screen = CA2D_4_SimScreen(root)

# register screens to the screenmanager
screen_manager.register(ScreenList.StartingScreen, starting_screen)
screen_manager.register(ScreenList.MainMenu, main_menu)
screen_manager.register(ScreenList.CA1D_Preparation, ca_1d_prep_screen)
screen_manager.register(ScreenList.CA1D_Simulation, ca_1d_sim_screen)
screen_manager.register(ScreenList.CA2D_Preparation, ca_2d_prep_screen)
screen_manager.register(ScreenList.CA2D_Simulation, ca_2d_sim_screen)
screen_manager.register(ScreenList.CA2D_4_Preparation, ca_2d_4_prep_screen)
screen_manager.register(ScreenList.CA2D_4_Simulation, ca_2d_4_sim_screen)

# run the application from starting screen
screen_manager.execute(ScreenList.StartingScreen, None)

root.mainloop()