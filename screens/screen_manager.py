import tkinter as tk

from typing import Callable
from screens.screen import Screen

class ScreenNameDuplicateError(Exception):
    
    def __init__(self, message) -> None:
        self.message = message
        super().__init__(self.message)

class ScreenNotFoundError(Exception):
    
    def __init__(self, message) -> None:
        self.message = message
        super().__init__(self.message)

class RootNotFoundError(Exception):
    
    def __init__(self, message) -> None:
        self.message = message
        super().__init__(self.message)


screens: dict[Screen, Callable[[tk.Misc, object], None]] = {}
root: tk.Misc | None = None


def register(name: Screen, screen: Callable[[tk.Misc, object], None]) -> None:
    if name in screens.keys():
        raise ScreenNameDuplicateError(f"Cannot register screen because name '{name}' is already taken")
    screens[name] = screen

def deregister(name: Screen) -> bool:
    try:
        del screens[name]
        return True
    except KeyError:
        return False
    
def execute(screen_name: Screen, args: object) -> None:

    if root is None:
        raise RootNotFoundError(f"Cannot execute screens before root is configured")
    try:
        screen = screens[screen_name]
    except KeyError:
        raise ScreenNotFoundError(f"Cannot run screen with name '{screen_name}', because it is not registered")
    
    #cleanup the window first
    for element in root.winfo_children():
        element.destroy()
        
    screen(root, args)