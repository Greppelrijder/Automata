import tkinter as tk
import tkinter.font as tkFont

from .screen_list import ScreenList
from .screen_manager import execute
from .screen import Screen




class StartingScreen(Screen):

    def __init__(self, root: tk.Tk) -> None:
        super().__init__(root)

        # Define a custom font
        custom_font = tkFont.Font(family="Arial", size=25)


        self.header: tk.Label = tk.Label(self.canvas, text="Cellular automata", font=custom_font, padx=30, pady=50, justify="center", background="#8D8A8A")
        self.main_menu_button: tk.Button = tk.Button(self.canvas, border=5,background="#2DE840", activebackground="#178122", 
                                                     text="Main menu",fg="#202020", activeforeground="#202020", font=50, anchor="center", 
                                                     command= lambda : execute(ScreenList.MainMenu, None))

    def run(self, args) -> None:
        self.canvas.place(x = 0, y = 0, width = 800, height = 400)
        self.header.place(x=300, y=20)
        self.main_menu_button.place(x=400, y=200)

# gif = "Gospers_glider_gun.gif"
# img = Image.open(gif)

# frames = img.n_frames  # number of frames

# photoimage_objects = []
# for i in range(frames):
#     obj = tk.PhotoImage(file=gif, format=f"gif -index {i}")
#     photoimage_objects.append(obj)


# def animation(current_frame=0):
#     global loop
#     image = photoimage_objects[current_frame]

#     gif_label.configure(image=image)
#     current_frame = (current_frame + 1) % frames

#     if current_frame == frames:
#         current_frame = 0

#     loop = root.after(50, lambda: animation(current_frame))

# gif_label = tk.Label(root, image="")
# gif_label.pack()

# start = tk.Button(root, text="Start", command=lambda: animation(current_frame=0))
# start.pack()