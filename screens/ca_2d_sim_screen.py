import sys
import tkinter as tk
import tkinter.colorchooser
import tkinter.font as tkFont
import math

from .screen_list import ScreenList
from .screen_manager import execute
from .screen import Screen

sys.path.append("..")
from models.ca_2d import CA_2D
from models.boundry_conditions import BoundryConditions


class CA2D_SimOptions:

    def __init__(self, size: int, ruleset: str, boundry_conditions: BoundryConditions, name: str, alive_cell_color: str, dead_cell_color: str):
        self.size = size
        self.ruleset = ruleset
        self.boundry_conditions = boundry_conditions
        self.name = name
        self.alive_cell_color = alive_cell_color
        self.dead_cell_color = dead_cell_color

class CA2D_SimScreen(Screen):
        
    CA_CANVAS_WIDTH = 250


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

        self.auto_evolve_button_text = tk.StringVar(self.frame)
        self.auto_evolve_button = tk.Button(self.frame, textvariable=self.auto_evolve_button_text, command = self.on_auto_evolve_pressed)
        self.auto_evolve_interval_slider = tk.Scale(self.frame, from_ = 100, to = 5000, resolution=100, orient="horizontal")

        # we'll store callback id's so that we can cancel them later
        self.loop_evolve_id: str = ""

    def run(self, args) -> None:
        
        self.parse_args(args)

        self.frame.place(x = 0, y = 0)

        self.setup_ca()
        self.configure_widgets()
        self.place_widgets()

    def cleanup(self) -> None:
        # forget callbacks (if any)
        try: self.frame.after_cancel(self.loop_evolve_id)
        except (ValueError, tk.TclError): pass

        self.ca_canvas.place_forget()
        super().cleanup()

    def parse_args(self, args) -> None:
        if not isinstance(args, CA2D_SimOptions):
            raise ValueError(f"For ca_2d_sim_screen, the 'args' parameter must be of type CA2D_SimScreenArgs (got {type(args)})")
        
        self.grid_size = args.size**2
        self.ruleset = args.ruleset
        self.boundry_conditions = args.boundry_conditions
        self.ca_name = args.name
        self.alive_cell_color = args.alive_cell_color
        self.dead_cell_color = args.dead_cell_color

    def setup_ca(self) -> None:

        self.ca = CA_2D(self.grid_size, self.ruleset, self.boundry_conditions)

        self.ca_cell_width = self.CA_CANVAS_WIDTH / int(math.sqrt(self.grid_size))
        self.ca_starting_state: list[list[int]] = [[0 for _ in range(int(math.sqrt(self.grid_size)))] for _ in range(int(math.sqrt(self.grid_size)))]

        self.ca_canvas.place(relx=0.5, rely=0.65, anchor="center", width=self.CA_CANVAS_WIDTH, height=self.CA_CANVAS_WIDTH)
        for i in range(int(math.sqrt(self.grid_size))):
            for j in range(int(math.sqrt(self.grid_size))):
                self.draw_cell(i, j, state=0)
            
        self.ca_canvas_click_callback_id = self.ca_canvas.bind("<Button-1>", self.on_ca_canvas_clicked)

    def configure_widgets(self) -> None:

        # create costum font
        custom_font1 = tkFont.Font(family="Arial", size=25)
        custom_font2 = tkFont.Font(family="Arial", size=15)

        self.header.config(text=f"Simulating 2D CA '{self.ca_name}'", font=custom_font1, background="#8D8A8A")
        self.size_label.config(text=f"Size: {self.grid_size}", font=custom_font2, background="#8D8A8A")
        if self.ruleset == "00000000000000000000000000000000000000000000000100000000000000010000000000000001000000000000000100000001000101110000000100010110000000000000000100000000000000010000000100010111000000010001011000000001000101110000000100010110000101110111111000010110011010000000000000000001000000000000000100000001000101110000000100010110000000010001011100000001000101100001011101111110000101100110100000000001000101110000000100010110000101110111111000010110011010000001011101111110000101100110100001111110111010000110100010000000":
            self.ruleset_label.config(text="Rules: Conway's game of life", font=custom_font2, background="#8D8A8A")
        else:
            self.ruleset_label.config(text=f"Rules: {self.ruleset[0]}{self.ruleset[1]}{self.ruleset[2]}{self.ruleset[3]}{self.ruleset[4]}...{self.ruleset[-5]}{self.ruleset[-4]}{self.ruleset[-3]}{self.ruleset[-2]}{self.ruleset[-1]}",
                                       font=custom_font2, background="#8D8A8A")
        self.boundry_conditions_label.config(text=f"Boundry conditions: {self.boundry_conditions.name}", font=custom_font2, background="#8D8A8A")
        
        
        self.go_back_button.config(font=custom_font1, border=5, background="#2DE840", activebackground="#178122", fg="#202020", activeforeground="#202020", anchor="center",
                                    command= lambda: execute(ScreenList.CA2D_Preparation, CA2D_SimOptions(
            int(math.sqrt(self.grid_size)),
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
        self.reset_button.config(state="disabled", border=5,background="#2DE840", activebackground="#178122", 
                                            fg="#202020", activeforeground="#202020", font=custom_font1, anchor="center")

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
    def on_ca_canvas_clicked(self, args) -> None: # : tk.Event[tk.Canvas]           HIER NOG NAAR KIJKEN
        index_row: int = int(args.x // self.ca_cell_width) # which row was clicked
        index_column: int = int(args.y // self.ca_cell_width) # which column was clicked
        self.ca_starting_state[index_row][index_column] = 1 - self.ca_starting_state[index_row][index_column] # flip cell's state
        self.draw_cell(index_row, index_column, self.ca_starting_state[index_row][index_column])

    def on_confirm_starting_state(self) -> None:
        self.ca_canvas.unbind("<Button-1>", self.ca_canvas_click_callback_id)
        self.ca.configure_initial_state(self.ca_starting_state)
        self.confirm_starting_state_button.config(state="disabled")
        self.next_state_button.config(state="normal")
        self.prev_state_button.config(state="normal")
        self.auto_evolve_button.config(state="normal")
        self.auto_evolve_interval_slider.config(state="normal")
        self.reset_button.config(state="normal") 

    def on_next_state(self) -> None:
        self.ca.evolve()
        self.draw_ca()

    def on_prev_state(self) -> None:
        try:
            self.ca.devolve()
        except IndexError:
            pass
        self.draw_ca()

    def on_reset(self) -> None:

        try: # use ca's starting state
            self.ca.goto_state(0)
            self.draw_ca()
            self.ca_starting_state = self.ca.get_state()
        except IndexError: # no starting state -> default to 0's
            for i in range(int(math.sqrt(self.grid_size))):
                for j in range(int(math.sqrt(self.grid_size))):
                    self.draw_cell(i, j, state=0)
            self.ca_starting_state = [[0 for _ in range(int(math.sqrt(self.grid_size)))] for _ in range(int(math.sqrt(self.grid_size)))]

        self.ca.reset()

        self.confirm_starting_state_button.config(state="normal")
        self.next_state_button.config(state="disabled")
        self.prev_state_button.config(state="disabled")
        self.auto_evolve_button.config(state="disabled")
        self.auto_evolve_interval_slider.config(state="disabled")
        self.ca_canvas_click_callback_id = self.ca_canvas.bind("<Button-1>", self.on_ca_canvas_clicked)

    def on_auto_evolve_pressed(self) -> None:
        
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
        self.on_next_state()
        self.loop_evolve_id = self.frame.after(interval_milliseconds, self.loop_evolve, interval_milliseconds)

    
    def draw_cell(self, index_row: int, index_column, state: int = 0):
        top_left = (index_row*self.ca_cell_width, index_column*self.ca_cell_width)
        bottom_right = ((index_row+1)*self.ca_cell_width, (index_column + 1)*self.ca_cell_width)
        fill_color = self.alive_cell_color if state == 1 else self.dead_cell_color
        self.ca_canvas.create_rectangle(top_left, bottom_right, fill=fill_color, outline="black")

    def draw_ca(self):
        for row_number, row in enumerate(self.ca.get_state()):
            for column_number, cell_state in enumerate(row):
                self.draw_cell(row_number, column_number, cell_state)