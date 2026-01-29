import sys
import tkinter as tk
from .grid_ca_sim_screen import GridCA_SimScreen
from .screen_list import ScreenList

sys.path.append("..")
from models.ca_1d import CA_1D


class CA1D_SimScreen(GridCA_SimScreen):


    @property
    def PREP_SCREEN(self) -> ScreenList:
        return ScreenList.CA1D_Preparation
    
    def __init__(self, root: tk.Tk) -> None:
        super().__init__(root)

    # steps for running screen
    def setup_ca(self) -> None:
        """
        Creates the 1D CA according to the information passed through 'args' (see parse_args) and configures the canvas to display said CA. The canvas starts empty (all cells are dead), but it can be clicked to modify this starting state.
        """
        self.ca: CA_1D = CA_1D(self.grid_size, self.ruleset, self.boundry_conditions)

        ca_canvas_width: float = self.CA_REL_CANVAS_WIDTH * self.frame["width"]
        self.ca_cell_width: float = ca_canvas_width / self.grid_size
        self.ca_canvas.place(relx=0.5, rely=0.5, anchor="center", width=ca_canvas_width, height=self.ca_cell_width)
        super().setup_ca()

    def configure_widgets(self) -> None:
        super().configure_widgets()
        self.header.config(text=f"Simulating 1D CA '{self.ca_name}'")

    def place_widgets(self) -> None:
        self.header.place(relx=0.5, rely=0.1, anchor="center")
        self.size_label.place(relx=0.4, rely=0.15)
        self.ruleset_label.place(relx=0.4, rely=0.2)
        self.boundry_conditions_label.place(relx=0.4, rely=0.25)
        self.confirm_starting_state_button.place(relx=0.9, rely=0.6, anchor="center", relwidth=0.15)
        self.next_state_button.place(relx=0.1, rely=0.55)
        self.prev_state_button.place(relx=0.2, rely=0.55)
        self.auto_evolve_button.place(relx=0.1, rely=0.65)
        self.auto_evolve_interval_slider.place(relx=0.2, rely=0.65)
        self.reset_button.place(relx=0.9, rely=0.75, anchor="center", relwidth=0.15)
        self.go_back_button.place(relx=0.01, rely=0.01)

    # commands
    def on_ca_canvas_clicked(self, args: tk.Event) -> None:
        index: int = int(args.x // self.ca_cell_width) # which cell was clicked
        self.ca_starting_state[index] = 1 - self.ca_starting_state[index] # flip cell's state
        self.draw_cell(index, self.ca_starting_state[index])

    # draw the CA
    def draw_cell(self, position: int, state: int = 0):
        """
        Draws a square onto the canvas in the position determined by 'position', that has the color matching 'state' (dead/0 or alive/1).
        The cell is assumed to be dead if any other value than 0 or 1 is passed through 'state'.
        """
        top_left = (position*self.ca_cell_width, 0)
        bottom_right = ((position+1)*self.ca_cell_width, self.ca_cell_width)
        fill_color = self.alive_cell_color if state == 1 else self.dead_cell_color
        self.ca_canvas.create_rectangle(top_left, bottom_right, fill=fill_color, outline="black")

    def draw_ca(self):
        """
        Draws all cells (see draw_cell) associated with this screen's CA
        """
        for index, cell_state in enumerate(self.ca.get_state()):
            self.draw_cell(index, cell_state)

    def clear_canvas(self) -> None:
        self.ca_starting_state = [0 for _ in range(self.grid_size)]
        for i in range(self.grid_size):
            self.draw_cell(i, state=0)