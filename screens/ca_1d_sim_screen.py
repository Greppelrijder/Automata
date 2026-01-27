import sys
import tkinter as tk
import tkinter.font as tkFont

from .screen_list import ScreenList
from .screen_manager import execute
from .screen import Screen

sys.path.append("..")
from models.ca_1d import CA_1D
from models.boundry_conditions import BoundryConditions


class CA1D_SimOptions:

    def __init__(self, size: int, ruleset: str, boundry_conditions: BoundryConditions, name: str, alive_cell_color: str, dead_cell_color: str):
        self.size = size
        self.ruleset = ruleset
        self.boundry_conditions = boundry_conditions
        self.name = name
        self.alive_cell_color = alive_cell_color
        self.dead_cell_color = dead_cell_color

class CA1D_SimScreen(Screen):

    """
    The 1d CA simulation screen features:
    * A button that brings the user back to the preparation screen
    * A canvas that displays the CA; canvas is clickable to allow the user to choose a starting state
    * A confirm button to fix the starting state
    * One button to evolve the CA to its next state; one to go back to the previous state
    * A reset button to allow the user to modify the starting state and restart the CA
    * A button to let the CA evolve automatically (or stop it), as well as a slider to determine the interval between consecutive evolves
    """

    CA_REL_CANVAS_WIDTH = 0.3

    def __init__(self, root: tk.Tk) -> None:
        super().__init__(root)

        self.header = tk.Label(self.frame)
        self.size_label = tk.Label(self.frame)
        self.ruleset_label = tk.Label(self.frame)
        self.boundry_conditions_label = tk.Label(self.frame)
        self.go_back_button = tk.Button(self.frame, text="back")

        self.ca_canvas = tk.Canvas(self.frame, bg="white")
        self.confirm_starting_state_button = tk.Button(self.frame, text="confirm", command = self.on_confirm_starting_state) 

        self.next_state_button = tk.Button(self.frame, text="next", command = self.on_next_state)
        self.prev_state_button = tk.Button(self.frame, text="previous", command = self.on_prev_state)
        self.reset_button = tk.Button(self.frame, text="reset", command = self.on_reset)

        self.auto_evolve_button_text = tk.StringVar(self.frame, value="auto")
        self.auto_evolve_button = tk.Button(self.frame, textvariable=self.auto_evolve_button_text, command = self.on_auto_evolve_pressed)
        self.auto_evolve_interval_slider = tk.Scale(self.frame, from_ = 100, to = 5000, resolution=100, orient="horizontal")

        # we'll store callback id's so that we can cancel them later
        self.loop_evolve_id: str = ""

    def run(self, args) -> None:
        """
        For this screen, 'args' is required. The parameter must be of type CA1D_SimOptions and is needed to create the correct 1D CA
        """
        self.parse_args(args)
        self.frame.place(x = 0, y = 0)
        self.setup_ca()
        self.configure_widgets()
        self.place_widgets()

    def cleanup(self) -> None:
        """
        Stops looping callbacks (if any)
        """
        # forget callbacks (if any)
        try: self.frame.after_cancel(self.loop_evolve_id)
        except (ValueError, tk.TclError): pass

        self.ca_canvas.place_forget()
        super().cleanup()

    def parse_args(self, args) -> None:
        """
        The type of 'args' must be CA1D_SimOptions

        Errors:
        * ValueError: this error will be raised if the type of 'args' is not CA1D_SimOptions
        """
        if not isinstance(args, CA1D_SimOptions):
            raise ValueError(f"For ca_1d_sim_screen, the 'args' parameter must be of type CA1D_SimScreenArgs (got {type(args)})")
        
        self.grid_size = args.size
        self.ruleset = args.ruleset
        self.boundry_conditions = args.boundry_conditions
        self.ca_name = args.name
        self.alive_cell_color = args.alive_cell_color
        self.dead_cell_color = args.dead_cell_color

    def setup_ca(self) -> None:
        """
        Creates the 1D CA according to the information passed through 'args' (see parse_args) and configures the canvas to display said CA. The canvas starts empty (all cells are dead), but it can be clicked to modify this starting state.
        """

        ca_canvas_width: float = self.CA_REL_CANVAS_WIDTH * self.frame["width"]
        self.ca_cell_width: float = ca_canvas_width / self.grid_size
        self.ca_canvas.place(relx=0.5, rely=0.5, anchor="center", width=ca_canvas_width, height=self.ca_cell_width)
        
        self.ca = CA_1D(self.grid_size, self.ruleset, self.boundry_conditions)
        self.ca_starting_state: list[int] = [0 for _ in range(self.grid_size)]
        for i in range(self.grid_size):
            self.draw_cell(i, state=0)

        self.ca_canvas_click_callback_id = self.ca_canvas.bind("<Button-1>", self.on_ca_canvas_clicked)

    def configure_widgets(self) -> None:
        """
        Ensures all widgets have the correct presets for the start of this screen. This includes the enabling and disabling of buttons.
        """
        # create costum font
        custom_font1 = tkFont.Font(family="Arial", size=25)
        custom_font2 = tkFont.Font(family="Arial", size=15)

        self.header.config(text=f"Simulating 1D CA '{self.ca_name}'", font=custom_font1, background="#8D8A8A")
        self.size_label.config(text=f"Size: {self.grid_size}", font=custom_font2, background="#8D8A8A")
        self.ruleset_label.config(text=f"Rules: {self.ruleset} (Rule: {int(self.ruleset,2)})", font=custom_font2, background="#8D8A8A")
        self.boundry_conditions_label.config(text=f"Boundry conditions: {self.boundry_conditions.name}", font=custom_font2, background="#8D8A8A")
        
        
        self.go_back_button.config(font=custom_font1, border=5, background="#2DE840", activebackground="#178122", fg="#202020", activeforeground="#202020", anchor="center",
                                    command= lambda: execute(ScreenList.CA1D_Preparation, CA1D_SimOptions(
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

    # buttons
    def on_confirm_starting_state(self) -> None:
        """
        Fixes the current starting state for the CA and allows the user to start evolving it
        """
        self.ca_canvas.unbind("<Button-1>", self.ca_canvas_click_callback_id)
        self.ca.configure_initial_state(self.ca_starting_state)
        self.confirm_starting_state_button.config(state="disabled")
        self.next_state_button.config(state="normal")
        self.prev_state_button.config(state="normal")
        self.auto_evolve_button.config(state="normal")
        self.auto_evolve_interval_slider.config(state="normal")
        self.reset_button.config(state="normal")

    def on_next_state(self) -> None:
        """
        Evolves the CA and redraws it accordingly
        """
        self.ca.evolve()
        self.draw_ca()

    def on_prev_state(self) -> None:
        """
        Sets the CA back to its previous state (if possible) and redraws it accordingly
        """
        try:
            self.ca.devolve()
        except IndexError:
            pass
        self.draw_ca()

    def on_reset(self) -> None:
        """
        Sets the CA back to its initial state and allows modification of the starting state. If the CA had no starting state yet, then the canvas is cleared (all cells are dead).

        After pressing this button, the user can no longer evolve the CA (until starting state is confirmed again).
        """
        try: # use ca's starting state
            self.ca.goto_state(0)
            self.draw_ca()
            self.ca_starting_state = self.ca.get_state()
        except IndexError: # no starting state -> default to 0's
            for i in range(self.grid_size):
                self.draw_cell(i, state=0)
            self.ca_starting_state = [0 for _ in range(self.grid_size)]

        self.ca.reset()

        self.confirm_starting_state_button.config(state="normal")
        self.next_state_button.config(state="disabled")
        self.prev_state_button.config(state="disabled")
        self.auto_evolve_button.config(state="disabled")
        self.ca_canvas_click_callback_id = self.ca_canvas.bind("<Button-1>", self.on_ca_canvas_clicked)

    def on_auto_evolve_pressed(self) -> None:
        """
        Turns auto-evolve on if was off and vice versa. While auto evolve is on, all other input widgets are disabled (except the 'back' button). When auto-evolve is turned off again, relevant buttons will be re-enabled. 

        While in auto-evolve mode, the CA is evolved repeatedly. The interval between consecutive evolves is determined by the value of the auto-evolve interval slider (which cannot be modified while auto-evolve mode is active).
        """
        if self.auto_evolve_button_text.get() == "auto":

            self.next_state_button.config(state="disabled")
            self.prev_state_button.config(state="disabled")
            self.reset_button.config(state="disabled")
            self.auto_evolve_interval_slider.config(state="disabled")
            self.auto_evolve_button_text.set("stop")
            self.loop_evolve(int(self.auto_evolve_interval_slider.get()))
        else:
            self.next_state_button.config(state="normal")
            self.prev_state_button.config(state="normal")
            self.reset_button.config(state="normal")
            self.auto_evolve_interval_slider.config(state="normal")
            self.auto_evolve_button_text.set("auto")
            try:
                self.frame.after_cancel(self.loop_evolve_id)
            except (tk.TclError, ValueError):
                pass

    # helper functions
    def loop_evolve(self, interval_milliseconds: int) -> None:
        """
        Evolves the CA (by calling 'on_next_state') and schedules another call to this function after 'inteval_milliseconds' milliseconds (creating a loop). The id of the scheduled call is stored so that it can be cancelled later (breaking the loop).
        """
        self.on_next_state()
        self.loop_evolve_id = self.frame.after(interval_milliseconds, self.loop_evolve, interval_milliseconds)

    
    def draw_cell(self, index: int, state: int = 0):
        """
        Draws a square onto the canvas in the position determined by 'index', that has the color matching 'state' (dead/0 or alive/1).
        The cell is assumed to be dead if any other value than 0 or 1 is passed through 'state'.
        """
        top_left = (index*self.ca_cell_width, 0)
        bottom_right = ((index+1)*self.ca_cell_width, self.ca_cell_width)
        fill_color = self.alive_cell_color if state == 1 else self.dead_cell_color
        self.ca_canvas.create_rectangle(top_left, bottom_right, fill=fill_color, outline="black")

    def draw_ca(self):
        """
        Draws all cells (see draw_cell) associated with this screen's CA
        """
        for index, cell_state in enumerate(self.ca.get_state()):
            self.draw_cell(index, cell_state)