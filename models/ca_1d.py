from copy import deepcopy

from .boundry_conditions import BoundryConditions
from .cell import Cell
from .grid import Grid, InvalidStateError, CANotInitializedError

class CA_1D(Grid):
    """
    A 1-dimensional CA consists of a single line of cells. Each cell is connected to (itself and) the cell to its left and to its right. Each cell can be in one of two states: alive (1) or dead (0).
    """
    neighbour_directions: list[int] = [-1, 0, 1] # in order

    def __init__(self, cells: int, rules: str, boundry_conditions: BoundryConditions):
        """
        Create a Grid with 2 states and 2 neighbours per cell.
        See Grid.__init__ for details on the parameters and potential errors.

        Neighbours are being assigned immediately, so that they need not be recalculated later
        """

        super().__init__(cells, states=2, neighbours = 2, rules=rules, boundry_conditions=boundry_conditions)

        self.cells: list[Cell] = [Cell() for _ in range(cells)]

        # assigning neighbours
        for position, cell in enumerate(self.cells):
            self.assign_neighbours(cell, position)

    def assign_neighbours(self, cell: Cell, position: int) -> None:
        """
        Find and connect all neighbours for the cell in the given position
        """
        for dir in self.neighbour_directions:
            neighbour = self.apply_boundry_rules(position + dir)
            cell.add_to_neighbourhood(neighbour)

    def apply_boundry_rules(self, target_index: int) -> Cell:
        """
        Find the cell in the given position.
        Boundry conditions are applied if the position falls outside the grid
        """

        if 0 <= target_index < self.amount_of_cells: # inside the grid
            return self.cells[target_index]
        
        # outside the grid
        match self.boundry_conditions:
            case BoundryConditions.Periodic:
                return self.cells[target_index % self.amount_of_cells]
            case BoundryConditions.Dirichlet0:
                return Cell(0)
            case BoundryConditions.Dirichlet1:
                return Cell(1)
            case BoundryConditions.Neumann:
                return self.cells[0] if target_index < 0 else self.cells[-1]
    
    def configure_initial_state(self, initial_state: list[int]) -> None:
        """
        We only expand the base class functionality by adding a parameter check

        Errors:
        * InvalidStateError: this error occurs when initial state contains integers other than 0 or 1
        """
                
        if not all(s in range(0, self.amount_of_states) for s in initial_state):
            raise InvalidStateError(f"Cannot set this CA's state to '{initial_state}'; the only allowed cell states are: {[range(0, self.amount_of_states)]}")
        super().configure_initial_state(initial_state)

    def reset(self) -> None:
        """
        We expand the base class functionality by setting each cell's state to 0
        """
        for cell in self.cells:
            cell.state = 0
        super().reset()

    def get_state(self, index: None | int = None) -> list[int]:
        # we override the base method so that we can give a more precise return type
        return super().get_state(index)
        
    def determine_next_state(self) -> list[int]:
        """
        Finds the states of each cell's neighbours and uses the ruleset to determine the appropriate next state for that particular cell 
        """
        result: list[int] = []
        for cell in self.cells:
            neighbourhood: list[Cell] = cell.get_neighbourhood()
            neighbourhood_code = self.convert_to_neighbourhood_code(neighbourhood)
            index: int = 7 - int(neighbourhood_code, 2) # e.g '111' has index 0; '000' has index 7 within the ruleset
            new_state: int = int(self.ruleset[index])
            result.append(new_state)

        return result
    
    def set_state(self, state: list[int]) -> None:
        """
        Assigns each cell the corresponding cell_state in 'state'
        """
        for cell, cell_state in zip(self.cells, state):
            cell.state = cell_state