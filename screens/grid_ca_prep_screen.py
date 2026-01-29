import tkinter as tk
import tkinter.font as tkFont
import tkinter.colorchooser
import sys

from abc import ABC, abstractmethod
from .screen import Screen
from .screen_list import ScreenList
from .screen_manager import execute
from .grid_ca_sim_options import GridCA_SimOptions

sys.path.append("..")
from models.boundry_conditions import BoundryConditions


class GridCA_PrepScreen(Screen, ABC):
    """
    The Grid-CA preparation screen provides another abstract screen layer, capturing the functionality that is shared between all grid-based CA preparation screens (regardless of dimension or neighbour count). Any grid-based CA preparation screen features:
    * A button that brings the user back to the main menu
    * A slider to set the CA's size
    * An entry to set the CA's ruleset
    * A dropdown to pick boundry conditions
    * An entry to choose the CA's name
    * Colorpickers to set the color of dead and alive cells
    * A button that submits the presets and takes the user to the simulation screen
    * Automatic warnings that show on invalid input

    Each individual preparation screen can decide on its own design and specific implementations
    """

    MAX_NAME_LENGTH = 15

    def __init__(self, root: tk.Tk):

        custom_font = tkFont.Font(family="Arial", size=25)
        custom_font2 = tkFont.Font(family="Arial", size=15)
        custom_font3 = tkFont.Font(family="Arial", size=10)

        super().__init__(root)

        # creating widgets
        self.header = tk.Label(self.frame, text="Creating Grid CA", font=custom_font, justify="center", background="#8D8A8A")
        self.go_back_button = tk.Button(self.frame, text="back", border=5,background="#2DE840", activebackground="#178122", 
                                            fg="#202020", activeforeground="#202020", font=custom_font, anchor="center",
                                            command= lambda: execute(ScreenList.MainMenu, None))

        self.slider_label = tk.Label(self.frame, text="Amount of cells", font=custom_font2, justify="center", background="#8D8A8A")
        self.size_slider = tk.Scale(self.frame, from_ = 3, to = 21, orient="horizontal", background="#2DE840", activebackground="#0C0D0C", 
                                            fg="#202020", font=custom_font2, troughcolor="#2DE840", highlightbackground="#8D8A8A", border=3)

        self.ruleset_label = tk.Label(self.frame, text="Enter ruleset", font=custom_font2, justify="center", background="#8D8A8A")
        self.ruleset = tk.StringVar(self.frame)
        self.ruleset_entry = tk.Entry(self.frame, textvariable=self.ruleset, border=5,background="#2DE840", 
                                            fg="#202020", font=custom_font2)
        self.invalid_ruleset_warning = tk.Label(self.frame, fg="#880000", text="Ruleset does not contain the correct amount of characters", font=custom_font3, justify="center", background="#8D8A8A")

        self.boundry_condition_choice_label = tk.Label(self.frame, text="Choose boundry conditions", font=custom_font2, justify="center", background="#8D8A8A")
        self.boundry_condition_choice = tk.StringVar(self.frame, value=BoundryConditions.Dirichlet0.name)
        self.boundry_conditions_dropdown = tk.OptionMenu(self.frame, self.boundry_condition_choice, *BoundryConditions._member_names_)
        self.boundry_conditions_dropdown.config(font=custom_font2, background="#2DE840", activebackground="#2DE840",
                                            fg="#202020", highlightbackground="#8D8A8A", border=5)

        self.ca_name_label = tk.Label(self.frame, text="Enter name", font=custom_font2, justify="center", background="#8D8A8A")
        self.ca_name = tk.StringVar(self.frame)
        self.ca_name_entry = tk.Entry(self.frame, textvariable=self.ca_name, border=5,background="#2DE840", 
                                            fg="#202020", font=custom_font2)
        self.invalid_name_warning = tk.Label(self.frame, fg="#880000", text=f"Name must be non-empty and may not contain more than {self.MAX_NAME_LENGTH} characters", font=custom_font3, justify="center", background="#8D8A8A")

        self.alive_cell_color_label= tk.Label(self.frame, text="pick alive cell color", font=custom_font2, justify="left", background="#8D8A8A")
        self.alive_cell_color_button = tk.Button(self.frame, width=30, command = self.on_choose_alive_cell_color)

        self.dead_cell_color_label= tk.Label(self.frame, text="pick dead cell color", font=custom_font2, justify="left", background="#8D8A8A")
        self.dead_cell_color_button = tk.Button(self.frame, width=30, command = self.on_choose_dead_cell_color)

        self.create_button = tk.Button(self.frame, text="Create",  border=5,background="#2DE840", activebackground="#178122", 
                                            fg="#202020", activeforeground="#202020", font=custom_font, anchor="center",
                                            command = self.on_create)

        # we'll store callback id's so that we can cancel them later
        self.ruleset_validation_callback_id: str = ""
        self.ca_name_validation_callback_id: str = ""

    def run(self, args) -> None:
        """
        For this screen, 'args' is optional. The parameter *can* be read to set default values (type must be GridCA_SimOptions). This behaviour is mainly used when returning to this screen from the simulation screen. The presets of the CA that was being simulated are copied.
        """
        super().run(args)
        self.parse_args(args)
        self.place_widgets()
        self.configure_input_warnings()


    def cleanup(self) -> None:
        """
        Un-links automatic input checks from the inputvariables that they were associated with (if any). Removes warnings (if any).
        """

        # forget callbacks
        try: self.ca_name.trace_remove("write", self.ca_name_validation_callback_id)
        except (ValueError, tk.TclError): pass
        try: self.ruleset.trace_remove("write", self.ruleset_validation_callback_id)    
        except (ValueError, tk.TclError): pass

        self.invalid_name_warning.place_forget()
        self.invalid_ruleset_warning.place_forget()
        super().cleanup()

    def configure_input_warnings(self) -> None:
        """
        Links input checks to the corresponding input variable. Whenever the variable in question is changed, a check is made to determine whether or not a warning should be displayed.  
        """
        self.ca_name_validation_callback_id = self.ca_name.trace_add("write", callback= lambda *args: self.validate_name())
        self.ruleset_validation_callback_id = self.ruleset.trace_add("write", callback= lambda *args: self.validate_ruleset())

    # buttons
    def on_choose_alive_cell_color(self) -> None:
        """
        Prompts the user with a colorpicker and sets the color of the corresponding button to the chosen color (if any)
        """
        choice_hex = tkinter.colorchooser.askcolor()[1]
        if choice_hex is not None:
            self.alive_cell_color_button.config(bg=choice_hex)

    def on_choose_dead_cell_color(self) -> None:
        """
        Prompts the user with a colorpicker and sets the color of the corresponding button to the chosen color (if any)
        """
        choice_hex = tkinter.colorchooser.askcolor()[1]
        if choice_hex is not None:
            self.dead_cell_color_button.config(bg=choice_hex)

    def on_create(self) -> None:
        """
        First a check is made to ensure that all input is valid. If so, all input values are passed on to the simulation screen and that screen runs.
        """
        if not (self.validate_name() and self.validate_ruleset()):
            return
        size = int(self.size_slider.get())
        ruleset_value = self.ruleset.get()
        boundry_conditions = BoundryConditions[self.boundry_condition_choice.get()] # convert option name to enum
        ca_name_value = self.ca_name.get()
        alive_cell_color = self.alive_cell_color_button["background"]
        dead_cell_color = self.dead_cell_color_button["background"]
        sim_options = GridCA_SimOptions(size, ruleset_value, boundry_conditions, ca_name_value, alive_cell_color, dead_cell_color)
        execute(self.SIM_SCREEN, sim_options)

    @property
    @abstractmethod
    def SIM_SCREEN(self) -> ScreenList:
        """
        Allows each specific preparation screen to define its corresponding simulation screen
        """
        pass
    
    @abstractmethod
    def parse_args(self, args) -> None:
        """
        This method determines what presets should be used for input widgets (e.g. the size slider). If the 'args' parameter is of type GridCA_SimOptions, then it will determine what presets to use (e.g. set size slider to 15). Default values are used otherwise (e.g. size slider defaults to 9).
        """
        pass

    @abstractmethod
    def place_widgets(self) -> None:
        """
        Each child class can decide how to design its screen
        """
        pass

    @abstractmethod
    def validate_name(self) -> bool:
        """
        Each child class should decide when names are valid and what should happen if they are not
        """
        pass

    @abstractmethod
    def validate_ruleset(self) -> bool:
        """
        Each child class should decide when rulesets are valid and what should happen if they are not
        """
        pass