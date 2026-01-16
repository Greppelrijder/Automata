import tkinter as tk

from screens.screen import Screen
import screens.screen_manager as screen_manager

from screens import starting_screen, main_menu, ca_1d_prep_screen, ca_1d_sim_screen, ca_2d_prep_screen, ca_2d_sim_screen

root = tk.Tk()
root.title("Cellular Automa in 1D and 2D")
root.geometry("1000x500")
root.resizable(False, False)

screen_manager.root = root
screen_manager.register(Screen.Starting_screen, starting_screen.run)
screen_manager.register(Screen.Main_menu, main_menu.run)
screen_manager.register(Screen.CA_1D_preparation, ca_1d_prep_screen.run)
screen_manager.register(Screen.CA_1D_simulation, ca_1d_sim_screen.run)
screen_manager.register(Screen.CA_2D_preparation, ca_2d_prep_screen.run)
screen_manager.register(Screen.CA_2D_simulation, ca_2d_sim_screen.run)

screen_manager.execute(Screen.Starting_screen, None)

root.mainloop()