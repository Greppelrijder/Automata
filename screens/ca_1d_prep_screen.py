import tkinter as tk
import sys
from .screen_list import ScreenList
from .screen_manager import execute
from .screen import Screen

sys.path.append("..")
from models.boundry_conditions import BoundryConditions

class CA1D_PrepScreen(Screen):
    
    def __init__(self, root: tk.Tk) -> None:
        super().__init__(root)

        # creating widgets
        self.header = tk.Label(self.canvas, text="Creating 1D CA")
        self.go_back_button = tk.Button(self.canvas, text="back", command= lambda: execute(ScreenList.MainMenu, None))

        self.size_slider = tk.Scale(self.canvas, from_ = 1, to = 21, orient="horizontal")

        self.ruleset = tk.StringVar(self.canvas)
        self.ruleset_entry = tk.Entry(self.canvas, textvariable=self.ruleset)
        self.invalid_ruleset_warning = tk.Label(self.canvas, fg="red", text="Ruleset must consist of 8 characters")

        self.boundry_condition_choice = tk.StringVar(self.canvas, value=BoundryConditions.Dirichlet0.name)
        self.boundry_conditions_dropdown = tk.OptionMenu(self.canvas, self.boundry_condition_choice, *BoundryConditions._member_names_)

        self.ca_name = tk.StringVar(self.canvas)
        self.ca_name_entry = tk.Entry(self.canvas, textvariable=self.ca_name)
        self.invalid_name_warning = tk.Label(self.canvas, fg="red", text="Name must be non-empty")

        self.create_button = tk.Button(self.canvas, text="Create", command = self.on_create)

        # we'll store callback id's so that we can cancel them later
        self.ruleset_validation_callback_id: str = ""
        self.ca_name_validation_callback_id: str = ""

    def run(self, args) -> None:
        
        self.canvas.place(x = 0, y = 0, width = 800, height = 400)
        self.apply_presets(args)
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
        
    def apply_presets(self, args) -> None:
        try: # use presets that were passed through args
            size_preset = int(args[0])
            ruleset_preset = str(args[1])
            assert isinstance(boundry_conditions_preset := args[2], BoundryConditions)
            name_preset: str = str(args[3])
        except (TypeError, IndexError, ValueError, AssertionError): # no presets passed -> use default
            size_preset = "9"
            ruleset_preset = "00011110"
            boundry_conditions_preset = BoundryConditions.Dirichlet0
            name_preset = "New"  
        self.size_slider.set(size_preset)
        self.ruleset.set(ruleset_preset)
        self.ca_name.set(name_preset)
        self.boundry_condition_choice.set(boundry_conditions_preset.name)

    def place_widgets(self) -> None:
        self.header.place(x=400, y=0)
        self.go_back_button.place(x=400, y=50)
        self.size_slider.place(x=400, y=75)
        self.ruleset_entry.place(x=400, y=125)
        self.boundry_conditions_dropdown.place(x=400, y=150)
        self.ca_name_entry.place(x=400, y=200)
        self.create_button.place(x=400, y=225)

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
    def on_create(self) -> None:
        if not (self.validate_name() and self.validate_ruleset()):
            return
        size = int(self.size_slider.get())
        ruleset_value = self.ruleset.get()
        boundry_conditions = BoundryConditions[self.boundry_condition_choice.get()]
        ca_name_value = self.ca_name.get()
        execute(ScreenList.CA1D_Simulation, (size, ruleset_value, boundry_conditions, ca_name_value))