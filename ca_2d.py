from boundry_conditions import BoundryConditions
from grid import Grid

class CA_2D(Grid):

    def __init__(self, cells: int, rules: str, boundry_conditions: BoundryConditions):
        super().__init__(cells, states=2, neighbours = 8, rules=rules, boundry_conditions=boundry_conditions)

            
        # grid construction goes here; a cell's neighbours should be assigned immediately
        # the 'grid' wil be a 2d-array of cells, where each cell has the 3x3 area around itself as its neighbourhood. We'll read left to right, top to bottom
        raise NotImplemented

    def evolve(self) -> None:
        # we create a new 2d-array that will contain each cell's new state
        # for each cell, we find its neighbourhood code using the dedicated method from the super class. We then apply the ruleset to determine a cell's new state
        # finally, we update all cells with their new state
        raise NotImplemented