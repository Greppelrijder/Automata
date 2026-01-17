import tkinter as tk
from tkinter import ttk

from models.ca_1d import CA_1D
from models.boundry_conditions import BoundryConditions

root = tk.Tk()
root.title("Cellular Automa in 1D and 2D")
root.geometry("1000x500")
root.resizable(False, False)

canvas = tk.Canvas(root)
canvas.place(x = 0, y = 0, width = 800, height = 400)

#functions: We implement the functions that the buttons use right here
#instead of running these functions we can maybe immediatly call the other ones
started_1D: bool = False
state_label: tk.Label = tk.Label(canvas)
test_CA: CA_1D = CA_1D(9, "00011110", BoundryConditions.Dirichlet0)
test_CA.configure_initial_state([0, 0, 0, 0, 1, 0, 0, 0, 0])
def oneD():
    
    global started_1D
    #this code is very ugly, just for testing

    if not started_1D:
        state_label.config(text="".join(str(char) for char in test_CA.get_state()))
        state_label.pack()
        started_1D = True
    else:
        test_CA.evolve()
        print(test_CA.get_state())    
        state_label.config(text="".join(str(char) for char in test_CA.get_state()))


def twoD():
    pass

def startup():
    pass

def run_once():
    pass

def run_amount(run_amount):
    pass

#We implement the buttons placement overhere
#Maybe distinction between 1D and 2D?
#test
#1D
oneD_button = tk.Button(root, text = "1D", command = lambda : oneD())
oneD_button.place(x = 400, y = 425, width = 100, height = 50)

#2D
twoD_button = tk.Button(root, text = "2D", command = lambda : twoD())
twoD_button.place(x = 500, y = 425, width = 100, height = 50)

#startup
startup_button = tk.Button(root, text = "Plot CA", command = lambda : startup())
startup_button.place(x = 850, y = 230, width = 100, height = 50)

#run_once
run_once_button = tk.Button(root, text = "Evolve 1 time", command = lambda : run_once())
run_once_button.place(x = 850, y = 280, width = 100, height = 50)

#run_amount
run_amount_input = tk.IntVar()
amount_input = ttk.Entry(root, textvariable = run_amount_input)
amount_input.place(x = 850, y = 400, width = 100, height = 50)
run_amount_button = tk.Button(root, text = "Run n times", command = lambda : run_amount(run_amount_input))
run_amount_button.place(x = 850, y = 350, width = 100, height = 50)

root.mainloop()
