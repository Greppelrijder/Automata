from abc import ABC, abstractmethod
import tkinter as tk

class Screen(ABC):

    def __init__(self, root: tk.Tk):
        self.root = root
        self.frame = tk.Frame(root, width=1000, height=500)

    @abstractmethod
    def run(self, args) -> None:
        pass

    def cleanup(self) -> None:
        self.frame.place_forget()