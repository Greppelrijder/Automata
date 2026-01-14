import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Cellular Automa in 1D and 2D")
root.geometry("1000x500")
root.resizable(0, 0)

canvas = tk.Canvas(root)
canvas.place(x = 0, y = 0, width = 800, height = 400)

#functions: We implement the functions that the buttons use right here
def vooruit():
    pass


#We implement the buttons placement overhere
tekstvr = tk.StringVar()
Avooruit = ttk.Entry(root, textvariable = tekstvr)
Avooruit.place(x = 205, y = 440, width = 50, height = 40)
fd = tk.Button(root, text = "Forward", command = lambda : vooruit())
fd.place(x = 255, y = 460, width = 100, height = 20)


root.mainloop()