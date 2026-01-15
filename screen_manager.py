import tkinter as tk

from typing import Callable
from screens import Screen

class ScreenNameDuplicateError(Exception):
    
    def __init__(self, message) -> None:
        self.message = message
        super().__init__(self.message)

class ScreenNotFoundError(Exception):
    
    def __init__(self, message) -> None:
        self.message = message
        super().__init__(self.message)


screens: dict[Screen, Callable[[tk.Tk, object], None]] = {}

def register(name: Screen, screen: Callable[[tk.Tk, object], None]) -> None:
    if name in screens.keys():
        raise ScreenNameDuplicateError(f"Cannot register screen because name '{name}' is already taken")
    screens[name] = screen

def deregister(name: Screen) -> bool:
    try:
        del screens[name]
        return True
    except KeyError:
        return False
    
def run(screen_name: Screen, root: tk.Tk, args: object) -> None:
    try:
        screen = screens[screen_name]
        screen(root, args)
    except KeyError:
        raise ScreenNotFoundError(f"Cannot run screen with name '{screen_name}', because it is not registered")