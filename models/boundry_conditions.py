from enum import Enum

class BoundryConditions(Enum):
    """
    A list of approaches to handle edge cases (literally) when evolving a Grid.
    A boundry condition tells you what should happen when a particular cell's alleged neighbour does not exist (in a specific direction)
    * Dirichlet0: A constant cell with state 0 is used (this cell is not part of the Grid)
    * Dirichlet1: A constant cell with state 1 is used (this cell is not part of the Grid)
    * Periodic: The Grid is 'wrapped around', so that the cell on the other side of the grid is used
    * Neumann: A cell with the same state as the border cell is used (this cell is not part of the Grid)
    """
    Dirichlet0 = 0
    Dirichlet1 = 1
    Periodic = 2
    Neumann  = 3