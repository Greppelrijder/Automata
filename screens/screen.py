from abc import ABC, abstractmethod
import tkinter as tk

class Screen(ABC):
    """
    The Screen class provides an abstract layer for all screens
    """
    def __init__(self, root: tk.Tk):
        """
        Each screen will draw onto its own frame that is then placed onto 'root'. The advantage of this approach is that clearing a screen becomes easier.
        """
        self.root = root
        self.frame = tk.Frame(root, width=1000, height=500, bg="#8D8A8A")

    @abstractmethod
    def run(self, args) -> None:
        """
        All specific screen functionality goes here (creating and placing widgets, setting up triggers, etc.).
        Additional information can be passed through 'args'. Some screens might need this information to run (e.g. what CA are we drawing?). We intentionally omitted type annotations for the 'args' parameter, so that each Screen can decide what type of input is needed / allowed.
        """
        self.frame.place(x = 0, y = 0)

    def cleanup(self) -> None:
        """
        Cleans up the Screen by simply un-placing its frame (which contains all its widgets). This method may be expanded by child classes, if an additional cleanup routine is needed when exiting said screen. For example: triggers may need to be unregistered. The screen manager can make use of this method to ensure proper cleanup when switching between screens.
        """
        self.frame.place_forget()