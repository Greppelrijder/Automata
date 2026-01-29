import tkinter as tk
import sys
from .screen_list import ScreenList
from .grid_ca_prep_screen import GridCA_PrepScreen
from .grid_ca_prep_screen import GridCA_SimOptions

# this feels a bit hacky but for the scale of this project, it should be fine
sys.path.append("..")
from models.boundry_conditions import BoundryConditions


class CA1D_PrepScreen(GridCA_PrepScreen):
    """
    For this preparation screen the CA's amount of neighbours is eight.
    Other functionality is described inside the base class
    """
    @property
    def SIM_SCREEN(self) -> ScreenList:
        return ScreenList.CA1D_Simulation

    def __init__(self, root: tk.Tk) -> None:
        super().__init__(root)
        self.header.config(text="Creating 1D CA")
        self.invalid_ruleset_warning.config(text="Ruleset must consist of eight characters")

    def parse_args(self, args) -> None:
        if isinstance(args, GridCA_SimOptions): # use presets that were passed through args
            size_preset = args.size
            ruleset_preset = args.ruleset
            boundry_conditions_preset = args.boundry_conditions
            name_preset = args.name
            alive_cell_color_preset = args.alive_cell_color
            dead_cell_color_preset = args.dead_cell_color
        else: # no presets passed -> use default
            size_preset = "9"
            ruleset_preset = "00011110"
            boundry_conditions_preset = BoundryConditions.Dirichlet0
            name_preset = "New"  
            alive_cell_color_preset = "#000000"
            dead_cell_color_preset = "#FFFFFF"
    
        self.size_slider.set(size_preset)
        self.ruleset.set(ruleset_preset)
        self.ca_name.set(name_preset)
        self.boundry_condition_choice.set(boundry_conditions_preset.name)
        self.alive_cell_color_button.config(bg=alive_cell_color_preset)
        self.dead_cell_color_button.config(bg=dead_cell_color_preset)

    def place_widgets(self) -> None:
        """
        Puts most widgets on the screen. Input warnings are excluded.
        """

        self.header.place(relx=0.5, rely=0.1, anchor="center")
        self.go_back_button.place(relx=0.01, rely=0.01)

        self.slider_label.place(relx=0.1, rely=0.2)
        self.size_slider.place(relx=0.1, rely=0.27)

        self.ruleset_label.place(relx=0.5, rely=0.2)
        self.ruleset_entry.place(relx=0.5, rely=0.3, relwidth=0.2)

        self.boundry_condition_choice_label.place(relx=0.25, rely=0.2)
        self.boundry_conditions_dropdown.place(relx=0.25, rely=0.28)

        self.ca_name_label.place(relx=0.7, rely=0.2)
        self.ca_name_entry.place(relx=0.7, rely=0.3, relwidth=0.2)

        self.alive_cell_color_label.place(relx=0.3, rely=0.55)
        self.alive_cell_color_button.place(relx=0.3, rely=0.65, relwidth=0.2)
        self.dead_cell_color_label.place(relx=0.5, rely=0.55)
        self.dead_cell_color_button.place(relx=0.5, rely=0.65, relwidth=0.2)
        self.create_button.place(relx=0.5, rely=0.85, anchor="center")

    # input validations
    def validate_name(self) -> bool:
        """
        If the name that the user has input so far is non-empty and contains at most MAX_NAME_LENGTH characters, the input warning (if present) is removed and True is returned; otherwise, the input warning is placed and False is returned.
        """
        if len(self.ca_name.get()) == 0 or len(self.ca_name.get()) > self.MAX_NAME_LENGTH:
            self.invalid_name_warning.place(relx=0.5, rely=0.45)
            return False
        else:
            self.invalid_name_warning.place_forget()
            return True
        
    def validate_ruleset(self) -> bool:
        """
        If the ruleset that the user has input so far consists of eight characters and contains only 1's and 0's, the input warning (if present) is removed and True is returned; otherwise, the input warning is placed (with the relevant message) and False is returned.
        """
        ruleset_value = self.ruleset.get()
        if len(ruleset_value) != 8:
            self.invalid_ruleset_warning.config(text="Ruleset must consist of 8 characters")
            self.invalid_ruleset_warning.place(relx=0.5, rely=0.4)
            return False
        elif not all(char in ["0", "1"] for char in ruleset_value):
            self.invalid_ruleset_warning.config(text="Ruleset must consist of only 1's & 0's")
            self.invalid_ruleset_warning.place(relx=0.5, rely=0.4)
            return False
        else:
            self.invalid_ruleset_warning.place_forget()
            return True