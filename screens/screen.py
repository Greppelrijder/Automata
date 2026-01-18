from abc import ABC, abstractmethod
import tkinter as tk

class Screen(ABC):

    def __init__(self, root: tk.Tk):
        self.root = root
        self.canvas = tk.Canvas(root)

    @abstractmethod
    def run(self, args) -> None:
        pass

    def cleanup(self) -> None:
        self.canvas.place_forget()