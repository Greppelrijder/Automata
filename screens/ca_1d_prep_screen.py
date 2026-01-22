import tkinter as tk
import tkinter.font as tkFont
import tkinter.colorchooser
import sys
from .screen_list import ScreenList
from .screen_manager import execute
from .screen import Screen
from .ca_1d_sim_screen import CA1D_SimOptions

sys.path.append("..")
from models.boundry_conditions import BoundryConditions

class CA1D_PrepScreen(Screen):
    
    MAX_NAME_LENGTH = 15

    def __init__(self, root: tk.Tk) -> None:
        super().__init__(root)

        # create costum font
        custom_font = tkFont.Font(family="Arial", size=25)
        custom_font2 = tkFont.Font(family="Arial", size=15)
        custom_font3 = tkFont.Font(family="Arial", size=10)

        # creating widgets
        self.header = tk.Label(self.frame, text="Creating 1D CA", font=custom_font, justify="center", background="#8D8A8A")
        self.go_back_button = tk.Button(self.frame, text="back", border=5,background="#2DE840", activebackground="#178122", 
                                            fg="#202020", activeforeground="#202020", font=custom_font, anchor="center",
                                            command= lambda: execute(ScreenList.MainMenu, None))

        self.slider_label = tk.Label(self.frame, text="Amount of cells", font=custom_font2, justify="center", background="#8D8A8A")
        self.size_slider = tk.Scale(self.frame, from_ = 1, to = 21, orient="horizontal", background="#2DE840", activebackground="#0C0D0C", 
                                            fg="#202020", font=custom_font2, troughcolor="#2DE840", highlightbackground="#8D8A8A", border=3)

        self.ruleset_label = tk.Label(self.frame, text="Enter ruleset", font=custom_font2, justify="center", background="#8D8A8A")
        self.ruleset = tk.StringVar(self.frame)
        self.ruleset_entry = tk.Entry(self.frame, textvariable=self.ruleset, border=5,background="#2DE840", 
                                            fg="#202020", font=custom_font2)
        self.invalid_ruleset_warning = tk.Label(self.frame, fg="#880000", text="Ruleset must consist of 8 characters", font=custom_font3, justify="center", background="#8D8A8A")

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
        self.invalid_ruleset_warning.place_forget()
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
        self.header.place(relx=0.4, rely=0.01)
        self.go_back_button.place(relx=0.01, rely=0.01)

        self.slider_label.place(relx=0.1, rely=0.2)
        self.size_slider.place(relx=0.1, rely=0.27)

        self.ruleset_label.place(relx=0.5, rely=0.2)
        self.ruleset_entry.place(relx=0.5, rely=0.3, width=200)

        self.boundry_condition_choice_label.place(relx=0.25, rely=0.2)
        self.boundry_conditions_dropdown.place(relx=0.25, rely=0.28)

        self.ca_name_label.place(relx=0.7, rely=0.2)
        self.ca_name_entry.place(relx=0.7, rely=0.3, width=200)

        self.alive_cell_color_label.place(relx=0.3, rely=0.55)
        self.alive_cell_color_button.place(relx=0.3, rely=0.65)
        self.dead_cell_color_label.place(relx=0.5, rely=0.55)
        self.dead_cell_color_button.place(relx=0.5, rely=0.65)
        self.create_button.place(relx=0.5, rely=0.8)

    def configure_input_warnings(self) -> None:
        self.ca_name_validation_callback_id = self.ca_name.trace_add("write", callback= lambda *args: self.validate_name())
        self.ruleset_validation_callback_id = self.ruleset.trace_add("write", callback= lambda *args: self.validate_ruleset())

    # input validations
    def validate_name(self) -> bool:
        if len(self.ca_name.get()) == 0 or len(self.ca_name.get()) > 15:
            self.invalid_name_warning.place(relx=0.5, rely=0.45)
            return False
        else:
            self.invalid_name_warning.place_forget()
            return True
        
    def validate_ruleset(self) -> bool:
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