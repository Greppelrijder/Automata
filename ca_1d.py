from boundry_conditions import BoundryConditions
from grid import Grid

class CA_1D(Grid):

    def __init__(self, cells: int, rules: str, boundry_conditions: BoundryConditions):
        super().__init__(cells, states=2, neighbours = 2, rules=rules, boundry_conditions=boundry_conditions)
        

        # grid construction goes here; a cell's neighbours should be assigned immediately
        # the 'grid' wil be an array of cells, where each cell has neighbourhood: the cell to its left, itself, the cell to its right, in that order
        raise NotImplemented

    def evolve(self) -> int:
        # we create a new array that will contain each cell's new state
        # for each cell, we find its neighbourhood code using the dedicated method from the super class. We then apply the ruleset to determine a cell's new state
        # finally, we update all cells with their new state
        raise NotImplemented