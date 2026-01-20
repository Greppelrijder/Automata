from abc import ABC, abstractmethod
import tkinter as tk

class Screen(ABC):

    def __init__(self, root: tk.Tk):
        self.root = root
        self.canvas = tk.Canvas(root, background="#8D8A8A")

    @abstractmethod
    def run(self, args) -> None:
        pass

    def cleanup(self) -> None:
        self.canvas.place_forget()