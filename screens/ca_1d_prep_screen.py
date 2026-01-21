import tkinter as tk
import tkinter.colorchooser
import sys
from .screen_list import ScreenList
from .screen_manager import execute
from .screen import Screen
from .ca_1d_sim_screen import CA1D_SimOptions

sys.path.append("..")
from models.boundry_conditions import BoundryConditions

class CA1D_PrepScreen(Screen):
    
    def __init__(self, root: tk.Tk) -> None:
        super().__init__(root)

        # creating widgets
        self.header = tk.Label(self.frame, text="Creating 1D CA")
        self.go_back_button = tk.Button(self.frame, text="back", command= lambda: execute(ScreenList.MainMenu, None))

        self.size_slider = tk.Scale(self.frame, from_ = 1, to = 21, orient="horizontal")

        self.ruleset = tk.StringVar(self.frame)
        self.ruleset_entry = tk.Entry(self.frame, textvariable=self.ruleset)
        self.invalid_ruleset_warning = tk.Label(self.frame, fg="red", text="Ruleset must consist of 8 characters")

        self.boundry_condition_choice = tk.StringVar(self.frame, value=BoundryConditions.Dirichlet0.name)
        self.boundry_conditions_dropdown = tk.OptionMenu(self.frame, self.boundry_condition_choice, *BoundryConditions._member_names_)

        self.ca_name = tk.StringVar(self.frame)
        self.ca_name_entry = tk.Entry(self.frame, textvariable=self.ca_name)
        self.invalid_name_warning = tk.Label(self.frame, fg="red", text="Name must be non-empty")
        
        self.alive_cell_color_label= tk.Label(self.frame, text="pick alive cell color", width=30)
        self.alive_cell_color_button = tk.Button(self.frame, width=30, command = self.on_choose_alive_cell_color)

        self.dead_cell_color_label= tk.Label(self.frame, text="pick dead cell color", width=30)
        self.dead_cell_color_button = tk.Button(self.frame, width=30, command = self.on_choose_dead_cell_color)

        self.create_button = tk.Button(self.frame, text="Create", command = self.on_create)

        # we'll store callback id's so that we can cancel them later
        self.ruleset_validation_callback_id: str = ""
        self.ca_name_validation_callback_id: str = ""

    def run(self, args) -> None:
        
        self.frame.place(x = 0, y = 0)
        self.parse_args(args)
        self.place_widgets()
        self.configure_input_warnings()

    def cleanup(self) -> None:
        # forget callbacks
        try: self.ca_name.trace_remove("write", self.ca_name_validation_callback_id)
        except (ValueError, tk.TclError): pass
        try: self.ruleset.trace_remove("write", self.ruleset_validation_callback_id)    
        except (ValueError, tk.TclError): pass

        self.invalid_name_warning.place_forget()
        super().cleanup()
        
    def parse_args(self, args) -> None:
        if isinstance(args, CA1D_SimOptions): # use presets that were passed through args
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
        self.header.place(x=400, y=0)
        self.go_back_button.place(x=400, y=50)
        self.size_slider.place(x=400, y=75)
        self.ruleset_entry.place(x=400, y=125)
        self.boundry_conditions_dropdown.place(x=400, y=150)
        self.ca_name_entry.place(x=400, y=200)
        self.alive_cell_color_label.place(x=400, y=230)
        self.alive_cell_color_button.place(x=400, y=255)
        self.dead_cell_color_label.place(x=400, y=295)
        self.dead_cell_color_button.place(x=400, y=320)
        self.create_button.place(x=400, y=360)

    def configure_input_warnings(self) -> None:
        self.ca_name_validation_callback_id = self.ca_name.trace_add("write", callback= lambda *args: self.validate_name())
        self.ruleset_validation_callback_id = self.ruleset.trace_add("write", callback= lambda *args: self.validate_ruleset())

    # input validations
    def validate_name(self) -> bool:
        if len(self.ca_name.get()) == 0:
            self.invalid_name_warning.place(x=400, y=250)
            return False
        else:
            self.invalid_name_warning.place_forget()
            return True
        
    def validate_ruleset(self) -> bool:
        ruleset_value = self.ruleset.get()
        if len(ruleset_value) != 8:
            self.invalid_ruleset_warning.config(text="Ruleset must consist of 8 characters")
            self.invalid_ruleset_warning.place(x=400, y=250)
            return False
        elif not all(char in ["0", "1"] for char in ruleset_value):
            self.invalid_ruleset_warning.config(text="Ruleset must consist of only 1's & 0's")
            self.invalid_ruleset_warning.place(x=400, y=250)
            return False
        else:
            self.invalid_ruleset_warning.place_forget()
            return True
    
    # buttons
    def on_choose_alive_cell_color(self) -> None:
        choice_hex = tkinter.colorchooser.askcolor()[1]
        if choice_hex is not None:
            self.alive_cell_color_button.config(bg=choice_hex)

    def on_choose_dead_cell_color(self) -> None:
        choice_hex = tkinter.colorchooser.askcolor()[1]
        if choice_hex is not None:
            self.dead_cell_color_button.config(bg=choice_hex)

    def on_create(self) -> None:
        if not (self.validate_name() and self.validate_ruleset()):
            return
        size = int(self.size_slider.get())
        ruleset_value = self.ruleset.get()
        boundry_conditions = BoundryConditions[self.boundry_condition_choice.get()] # convert option name to enum
        ca_name_value = self.ca_name.get()
        alive_cell_color = self.alive_cell_color_button["background"]
        dead_cell_color = self.dead_cell_color_button["background"]
        sim_options = CA1D_SimOptions(size, ruleset_value, boundry_conditions, ca_name_value, alive_cell_color, dead_cell_color)
        execute(ScreenList.CA1D_Simulation, sim_options)