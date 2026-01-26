from .screen_list import ScreenList
from .screen import Screen

class ScreenNameDuplicateError(Exception):
    """
    This error occurs when an attempt is made to register a screen under a name that has already been taken. Note that the screen names are defined by the 'ScreenList' enum.
    """
    def __init__(self, message) -> None:
        self.message = message
        super().__init__(self.message)

class ScreenNotFoundError(Exception):
    """
    This error occurs when a non-existing Screen is referenced. Note that the screen names are defined by the 'ScreenList' enum
    """
    
    def __init__(self, message) -> None:
        self.message = message
        super().__init__(self.message)

"""
This screen manager file acts as a 'static class'. It is responsible for keeping track of and running all Screens.
"""


screens: dict[ScreenList, Screen] = {}
info: dict[str, Screen | None] = {"current": None}

def register(screen_name: ScreenList, screen: Screen) -> None:
    """
    Link 'screen' to 'screen_name' for later access

    Errors:
    * ScreenNameDuplicateError: this error will be raised if 'screen_name' already has a Screen associated with it
    """

    if screen_name in screens.keys():
        raise ScreenNameDuplicateError(f"Cannot register screen because name '{screen_name}' is already taken")
    else:
        screens[screen_name] = screen

def deregister(screen_name: ScreenList) -> None:
    """
    Forget the Screen associated with 'screen_name'

    Errors:
    * ScreenNotFoundError: this error occurs when 'screen_name' does not have any Screen associated with it

    """
    if screen_name in screens.keys():
        del screens[screen_name]
    else:
        raise ScreenNotFoundError(f"Cannot deregister screen because '{screen_name}' was not found")
    
def execute(screen_name: ScreenList, args) -> None:
    """
    Run the Screen that is associated with 'screen_name', passing 'args'. The Screen that is currently running (if any) will be cleaned up beforehand.

    Errors:
    * ScreenNotFoundError: this error occurs when 'screen_name' does not have any Screen associated with it
    """
    try:
        target = screens[screen_name]
    except IndexError:
        raise ScreenNotFoundError(f"Cannot execute screen '{screen_name}' because it was not found")
    
    if (current := info["current"]) is not None:
        current.cleanup()
    info["current"] = target
    target.run(args)