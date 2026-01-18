from .screen_list import ScreenList
from .screen import Screen

class ScreenNameDuplicateError(Exception):
    
    def __init__(self, message) -> None:
        self.message = message
        super().__init__(self.message)

class ScreenNotFoundError(Exception):
    
    def __init__(self, message) -> None:
        self.message = message
        super().__init__(self.message)


screens: dict[ScreenList, Screen] = {}
current_screen: None | Screen = None

def register(screen_name: ScreenList, screen: Screen) -> None:
    if screen_name in screens.keys():
        raise ScreenNameDuplicateError(f"Cannot register screen because name '{screen_name}' is already taken")
    else:
        screens[screen_name] = screen

def deregister(screen_name: ScreenList) -> None:
    if screen_name in screens.keys():
        del screens[screen_name]
    else:
        raise ScreenNotFoundError(f"Cannot deregister screen because '{screen_name}' was not found")
    
def execute(screen_name: ScreenList, args: object) -> None:
    try:
        target = screens[screen_name]
    except IndexError:
        raise ScreenNotFoundError(f"Cannot execute screen '{screen_name}' because it was not found")
    
    for screen in screens.values():
        screen.cleanup()
    target.run(args)