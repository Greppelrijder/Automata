import sys
import tkinter as tk
from .grid_ca_sim_screen import GridCA_SimScreen
from .screen_list import ScreenList

sys.path.append("..")
from models.ca_2d import CA_2D


class CA2D_SimScreen(GridCA_SimScreen):

    
    @property
    def PREP_SCREEN(self) -> ScreenList:
        return ScreenList.CA2D_Preparation

    def __init__(self, root: tk.Tk) -> None:
        super().__init__(root)


    def setup_ca(self) -> None:
        self.ca: CA_2D = CA_2D(self.grid_size**2, self.ruleset, self.boundry_conditions)

        ca_canvas_width: float = self.CA_REL_CANVAS_WIDTH * self.frame["width"]
        self.ca_cell_width = ca_canvas_width / self.grid_size

        self.ca_canvas.place(relx=0.5, rely=0.65, anchor="center", width=ca_canvas_width, height=ca_canvas_width)
        super().setup_ca()

    def configure_widgets(self) -> None:
        super().configure_widgets()
        self.header.config(text=f"Simulating 2D CA '{self.ca_name}'")

        if self.ruleset == "00000000000000000000000000000000000000000000000100000000000000010000000000000001000000000000000100000001000101110000000100010110000000000000000100000000000000010000000100010111000000010001011000000001000101110000000100010110000101110111111000010110011010000000000000000001000000000000000100000001000101110000000100010110000000010001011100000001000101100001011101111110000101100110100000000001000101110000000100010110000101110111111000010110011010000001011101111110000101100110100001111110111010000110100010000000":
            self.ruleset_label.config(text="Rules: Conway's game of life")
        else:
            # we don't display the entire ruleset; it's too large
            self.ruleset_label.config(text=f"Rules: {self.ruleset[0:5]}...{self.ruleset[-5:]}") 

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
        index_row: int = int(args.x // self.ca_cell_width) # which row was clicked
        index_column: int = int(args.y // self.ca_cell_width) # which column was clicked
        self.ca_starting_state[index_row][index_column] = 1 - self.ca_starting_state[index_row][index_column] # flip cell's state
        self.draw_cell((index_row, index_column), self.ca_starting_state[index_row][index_column])

    # draw the CA    
    def draw_cell(self, position: tuple[int, int], state: int = 0):
        index_row, index_column = position
        top_left = (index_row*self.ca_cell_width, index_column*self.ca_cell_width)
        bottom_right = ((index_row+1)*self.ca_cell_width, (index_column + 1)*self.ca_cell_width)
        fill_color = self.alive_cell_color if state == 1 else self.dead_cell_color
        self.ca_canvas.create_rectangle(top_left, bottom_right, fill=fill_color, outline="black")

    def draw_ca(self):
        for row_number, row in enumerate(self.ca.get_state()):
            for column_number, cell_state in enumerate(row):
                self.draw_cell((row_number, column_number), cell_state)

    def clear_canvas(self) -> None:
        self.ca_starting_state: list[list[int]] = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                self.draw_cell((i, j), state=0)