import sys
import tkinter as tk
import tkinter.font as tkFont

from .screen_list import ScreenList
from .screen_manager import execute
from .grid_ca_sim_screen import GridCA_SimScreen
from .grid_ca_prep_screen import GridCA_SimOptions

sys.path.append("..")
from models.ca_1d import CA_1D


class CA1D_SimScreen(GridCA_SimScreen):


    def __init__(self, root: tk.Tk) -> None:
        super().__init__(root)

    # steps for running screen
    def setup_ca(self) -> None:
        """
        Creates the 1D CA according to the information passed through 'args' (see parse_args) and configures the canvas to display said CA. The canvas starts empty (all cells are dead), but it can be clicked to modify this starting state.
        """

        ca_canvas_width: float = self.CA_REL_CANVAS_WIDTH * self.frame["width"]
        self.ca_cell_width: float = ca_canvas_width / self.grid_size
        self.ca_canvas.place(relx=0.5, rely=0.5, anchor="center", width=ca_canvas_width, height=self.ca_cell_width)
        
        self.ca: CA_1D = CA_1D(self.grid_size, self.ruleset, self.boundry_conditions)
        self.ca_starting_state: list[int] = [0 for _ in range(self.grid_size)]
        self.clear_canvas()

        self.ca_canvas_click_callback_id = self.ca_canvas.bind("<Button-1>", self.on_ca_canvas_clicked)

    def configure_widgets(self) -> None:
        """
        Ensures all widgets have the correct presets for the start of this screen. This includes the enabling and disabling of buttons.
        """
        # create custom font
        custom_font1 = tkFont.Font(family="Arial", size=25)
        custom_font2 = tkFont.Font(family="Arial", size=15)

        self.header.config(text=f"Simulating 1D CA '{self.ca_name}'", font=custom_font1, background="#8D8A8A")
        self.size_label.config(text=f"Size: {self.grid_size}", font=custom_font2, background="#8D8A8A")
        self.ruleset_label.config(text=f"Rules: {self.ruleset} (Rule: {int(self.ruleset,2)})", font=custom_font2, background="#8D8A8A")
        self.boundry_conditions_label.config(text=f"Boundry conditions: {self.boundry_conditions.name}", font=custom_font2, background="#8D8A8A")
        
        
        self.go_back_button.config(font=custom_font1, border=5, background="#2DE840", activebackground="#178122", fg="#202020", activeforeground="#202020", anchor="center",
                                    command= lambda: execute(ScreenList.CA1D_Preparation, GridCA_SimOptions(
            self.grid_size,
            self.ruleset,
            self.boundry_conditions,
            self.ca_name,
            self.alive_cell_color,
            self.dead_cell_color
        )))
        self.auto_evolve_button_text.set("auto")
        self.auto_evolve_interval_slider.set(1000)

        self.next_state_button.config(state="disabled", border=5,background="#2DE840", activebackground="#178122", 
                                            fg="#202020", activeforeground="#202020", font=custom_font2, anchor="center")
        self.prev_state_button.config(state="disabled", border=5,background="#2DE840", activebackground="#178122", 
                                            fg="#202020", activeforeground="#202020", font=custom_font2, anchor="center")
        self.auto_evolve_button.config(state="disabled", border=5,background="#2DE840", activebackground="#178122", 
                                            fg="#202020", activeforeground="#202020", font=custom_font2, anchor="center")
        self.auto_evolve_interval_slider.config(state="disabled", background="#2DE840", activebackground="#0C0D0C", 
                                            fg="#202020", font=custom_font2, troughcolor="#2DE840", highlightbackground="#8D8A8A", border=3)

        self.confirm_starting_state_button.config(state="normal", border=5,background="#2DE840", activebackground="#178122", 
                                            fg="#202020", activeforeground="#202020", font=custom_font1, anchor="center")
        self.reset_button.config(state="normal", border=5,background="#2DE840", activebackground="#178122", 
                                            fg="#202020", activeforeground="#202020", font=custom_font1, anchor="center")

    def place_widgets(self) -> None:
        """
        Places all widget onto the screen
        """
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
        """
        Calculates which cell was clicked, flips the state of that cell (dead <-> alive) and redraws it accordingly
        """
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
        for i in range(self.grid_size):
            self.draw_cell(i, state=0)
            self.ca_starting_state = [0 for _ in range(self.grid_size)]