import sys
import tkinter as tk

from .screen_list import ScreenList
from .screen_manager import execute
from .screen import Screen

sys.path.append("..")
from models.ca_1d import CA_1D
from models.boundry_conditions import BoundryConditions

class CA1D_SimScreen(Screen):


    def __init__(self, root: tk.Tk) -> None:
        super().__init__(root)

        self.header = tk.Label(self.canvas)
        self.size_label = tk.Label(self.canvas)
        self.ruleset_label = tk.Label(self.canvas)
        self.boundry_conditions_label = tk.Label(self.canvas)
        self.go_back_button = tk.Button(self.canvas, text="back")

        self.starting_state = tk.StringVar()
        self.starting_state_entry = tk.Entry(self.canvas, textvariable=self.starting_state)
        self.confirm_starting_state_button = tk.Button(self.canvas, text="confirm", command = self.on_confirm_starting_state) 
        self.invalid_starting_state_warning = tk.Label(self.canvas, fg="red")

        self.ca_display = tk.Label(self.canvas)

        self.next_state_button = tk.Button(self.canvas, text="next", command = self.on_next_state)
        self.prev_state_button = tk.Button(self.canvas, text="previous", command = self.on_prev_state)
        self.reset_button = tk.Button(self.canvas, text="reset", command = self.on_reset)

        self.auto_evolve_button_text = tk.StringVar(value="auto")
        self.auto_evolve_button = tk.Button(self.canvas, textvariable=self.auto_evolve_button_text, command = self.on_auto_evolve_pressed,
                                            state="disabled")

    def run(self, args) -> None:
        
        # checking args
        error_message = f"For ca_1d_sim_screen, the 'args' parameter must be of type tuple[int, str, BoundryConditions, str] (got {type(args)})"
        if not isinstance(args, tuple):
            raise ValueError(error_message)
        try:
            self.grid_size = int(args[0])
            self.ruleset = str(args[1])
            self.boundry_conditions = args[2]
            assert isinstance(self.boundry_conditions, BoundryConditions)
            self.ca_name = str(args[3])
        except (IndexError, ValueError, AssertionError):
            raise ValueError(error_message)

        self.canvas.place(x = 0, y = 0, width = 800, height = 400)
        self.ca = CA_1D(self.grid_size, self.ruleset, self.boundry_conditions)
        
        # configuring widgets
        self.header.config(text=f"Simulating 1D CA '{self.ca_name}'")
        self.size_label.config(text=f"Size: {self.grid_size}")
        self.ruleset_label.config(text=f"Rules: {self.ruleset}")
        self.boundry_conditions_label.config(text=f"Boundry conditions: {self.boundry_conditions.name}")
        self.go_back_button.config(command= lambda: execute(ScreenList.CA1D_Preparation, (
            self.grid_size, 
            self.ruleset, 
            self.boundry_conditions, 
            self.ca_name
            )))
        self.starting_state.set("0" * self.grid_size)
        self.next_state_button.config(state="disabled")
        self.prev_state_button.config(state="disabled")
        self.auto_evolve_button.config(state="disabled")

        # placing widgets
        self.header.place(x=400, y=0)
        self.size_label.place(x=400, y=50)
        self.ruleset_label.place(x=400, y=75)
        self.boundry_conditions_label.place(x=400, y=100)
        self.starting_state_entry.place(x=400,y=200)
        self.confirm_starting_state_button.place(x=400, y=250)
        self.next_state_button.place(x=400, y=275)
        self.prev_state_button.place(x=450, y=275)
        self.auto_evolve_button.place(x=400, y=300)
        self.reset_button.place(x=400, y=375)
        self.go_back_button.place(x=20, y=20)

        # automatic warnings on invalid input
        self.starting_state.trace_add("write", callback = lambda *args: self.validate_starting_state())


    def validate_starting_state(self) -> bool:
        starting_state_value = self.starting_state.get()
        if len(starting_state_value) != self.grid_size:
            self.invalid_starting_state_warning.config(text=f"Starting state must consist of {self.grid_size} characters")
            self.invalid_starting_state_warning.place(x=400, y=225)
            return False
        elif not all(char in ["0", "1"] for char in starting_state_value):
            self.invalid_starting_state_warning.config(text=f"Starting state must consist of only 1's & 0's")
            self.invalid_starting_state_warning.place(x=400, y=225)
            return False
        else:
            self.invalid_starting_state_warning.place_forget()
            return True
    

    # commands
    def on_confirm_starting_state(self) -> None:

        if not self.validate_starting_state():
            return
        
        self.ca.configure_initial_state([int(char) for char in self.starting_state_entry.get()])
        self.ca_display.config(text=self.starting_state_entry.get())

        # we'll replace the entry with a label, so we must remember the coords
        entry_x, entry_y = self.starting_state_entry.winfo_x(), self.starting_state_entry.winfo_y()    
        self.starting_state_entry.place_forget()
        
        self.ca_display.place(x=entry_x, y=entry_y)
        
        self.confirm_starting_state_button.config(state="disabled")
        self.next_state_button.config(state="normal")
        self.prev_state_button.config(state="normal")
        self.auto_evolve_button.config(state="normal")

    def on_next_state(self) -> None:
        self.ca.evolve()
        self.ca_display.config(text=self.ca.get_state_string())

    def on_prev_state(self) -> None:
        try:
            self.ca.devolve()
            self.ca_display.config(text=self.ca.get_state_string())
        except IndexError:
            pass

    def on_reset(self) -> None:
        try: # set starting state to CA's starting state
            self.starting_state.set(self.ca.get_state_string(index = 0)) 
        except IndexError: # CA was not yet initialized
            self.starting_state.set("0" * self.grid_size)

        self.ca.reset()

        # we'll replace the label with an entry, so we must remember the coords
        label_x, label_y = self.starting_state_entry.winfo_x(), self.starting_state_entry.winfo_y()   
        self.ca_display.place_forget()
        
        self.starting_state_entry.place(x=label_x, y=label_y)
        self.confirm_starting_state_button.config(state="normal")
        self.next_state_button.config(state="disabled")
        self.prev_state_button.config(state="disabled")

    def on_auto_evolve_pressed(self) -> None:
            
        if self.auto_evolve_button_text.get() == "auto":
            self.next_state_button.config(state="disabled")
            self.prev_state_button.config(state="disabled")
            self.reset_button.config(state="disabled")
            self.auto_evolve_button_text.set("stop")
        else:
            self.next_state_button.config(state="normal")
            self.prev_state_button.config(state="normal")
            self.reset_button.config(state="normal")
            self.auto_evolve_button_text.set("auto")

    def cleanup(self) -> None:
        self.confirm_starting_state_button.config(state="normal")
        self.reset_button.config(state="normal")
        self.ca_display.place_forget()
        super().cleanup()