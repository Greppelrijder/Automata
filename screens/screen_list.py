from enum import Enum

class ScreenList(Enum):
    """
    These values are used as keys by the screen manager to keep track of all the different screens. This enum replaces string keys which are prone to typo's and harder to rename or expand. In this way, other classes can refer to Screens in a universal way.
    """
    
    StartingScreen = 0
    MainMenu = 1
    CA1D_Preparation = 2
    CA1D_Simulation = 3
    CA2D_Preparation = 4
    CA2D_Simulation = 5
    CA2D_4_Preparation = 6
    CA2D_4_Simulation = 7