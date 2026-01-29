import tkinter as tk
import tkinter.font as tkFont
from typing import Any
from abc import ABC, abstractmethod

from .screen import Screen
from .screen_manager import execute
from .screen_list import ScreenList
from .grid_ca_sim_options import GridCA_SimOptions


class GridCA_SimScreen(Screen, ABC):

    """
    This class provides another abstract screen layer, capturing the functionality that is shared between all grid-based CA simulation screens (regardless of dimension or neighbour count). Any grid-based CA simulation screen features:
    * A button that brings the user back to the preparation screen
    * A canvas that displays the CA; canvas is clickable to allow the user to choose a starting state
    * A confirm button to fix the starting state
    * One button to evolve the CA to its next state; one to go back to the previous state
    * A reset button to allow the user to modify the starting state and restart the CA
    * A button to let the CA evolve automatically (or stop it), as well as a slider to determine the interval between consecutive evolves

    Each individual simulation screen can decide on its own design and specific implementations
    """

    CA_REL_CANVAS_WIDTH = 0.3

    def __init__(self, root):
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
        super().run(args)
        self.parse_args(args)
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
            self.clear_canvas()

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

    def loop_evolve(self, interval_milliseconds: int) -> None:
        """
        Evolves the CA (by calling 'on_next_state') and schedules another call to this function after 'inteval_milliseconds' milliseconds (creating a loop). The id of the scheduled call is stored so that it can be cancelled later (breaking the loop).
        """
        self.on_next_state()
        self.loop_evolve_id = self.frame.after(interval_milliseconds, self.loop_evolve, interval_milliseconds)

    def parse_args(self, args: GridCA_SimOptions) -> None:
        """
        Stores the information in 'args'
        """
        self.grid_size = args.size
        self.ruleset = args.ruleset
        self.boundry_conditions = args.boundry_conditions
        self.ca_name = args.name
        self.alive_cell_color = args.alive_cell_color
        self.dead_cell_color = args.dead_cell_color

    def configure_widgets(self) -> None:
        """
        Ensuring the right widgets are enabled & displaying correctly
        """
        custom_font1 = tkFont.Font(family="Arial", size=25)
        custom_font2 = tkFont.Font(family="Arial", size=15)

        self.header.config(text=f"Simulating Grid CA '{self.ca_name}'", font=custom_font1, background="#8D8A8A")
        self.size_label.config(text=f"Size: {self.grid_size}", font=custom_font2, background="#8D8A8A")
        self.ruleset_label.config(text=f"Rules: {self.ruleset} (Rule: {int(self.ruleset,2)})", font=custom_font2, background="#8D8A8A")
        self.boundry_conditions_label.config(text=f"Boundry conditions: {self.boundry_conditions.name}", font=custom_font2, background="#8D8A8A")
        
        
        self.go_back_button.config(font=custom_font1, border=5, background="#2DE840", activebackground="#178122", fg="#202020", activeforeground="#202020", anchor="center",
                                    command= lambda: execute(self.PREP_SCREEN, GridCA_SimOptions(
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
    
    @property
    @abstractmethod
    def PREP_SCREEN(self) -> ScreenList:
        """
        Allows each specific simulation screen to define its corresponding preparation screen
        """
        pass

    @abstractmethod
    def setup_ca(self) -> None:
        """
        Each simulation screen constructs its own CA here, self.ca must be set during that process. Important: this base method has partial implementation which must be called at the END of an implemented version. (super().setup_ca() must be at the END)
        """
        self.ca: Any
        self.clear_canvas()
        self.ca_canvas_click_callback_id = self.ca_canvas.bind("<Button-1>", self.on_ca_canvas_clicked)
        pass

    @abstractmethod
    def place_widgets(self) -> None:
        """
        Designing goes here
        """
        pass

    @abstractmethod
    def draw_cell(self, position, state: int = 0):
        """
        Draws a square onto the canvas in the position determined by 'index', that has the color matching 'state' (dead/0 or alive/1).
        The cell is assumed to be dead if any other value than 0 or 1 is passed through 'state'.
        """
        pass

    @abstractmethod
    def draw_ca(self):
        """
        Draws all cells (see draw_cell) associated with this screen's CA
        """
        pass

    @abstractmethod
    def clear_canvas(self) -> None:
        """
        The canvas is cleared up so that all cells are dead
        """
        pass

    @abstractmethod
    def on_ca_canvas_clicked(self, args: tk.Event) -> None:
        """
        Calculates which cell was clicked, flips the state of that cell (dead <-> alive) and redraws it accordingly
        """
        pass