from copy import deepcopy
from .boundry_conditions import BoundryConditions
from .grid import Grid, InvalidStateError
from .cell import Cell
from .grid import CANotInitializedError
import math

class CA_2D_4(Grid):

    neighbour_directions: list[tuple[int, int]] = [
                 (-1, 0),
        (0, -1), (0, 0), (0, 1),
                 (1, 0)
    ]

    def __init__(self, cells: int, rules: str, boundry_conditions: BoundryConditions):
        super().__init__(cells, states=2, neighbours = 4, rules=rules, boundry_conditions=boundry_conditions)

        # the grid will contain *at least* as many cells as specified
        # if necessary, we will add more cells to reach a perfect square
        self.side_length: int = math.ceil(math.sqrt(cells))
        self.amount_of_cells = self.side_length ** 2

        # we'll use lists to keep our data
        self.cells: list[list[Cell]] = []
        for _ in range(self.side_length):
            self.cells.append([Cell() for _ in range(self.side_length)])

        for row_number, row in enumerate(self.cells):
            for column_number, cell in enumerate(row):
                self.assign_neighbours(cell, row_number, column_number)


    def assign_neighbours(self, cell: Cell, row_number: int, column_number: int) -> None:
        for dir in self.neighbour_directions:
            neighbour: Cell = self.apply_boundry_rules(row_number + dir[0], column_number + dir[1])
            cell.add_to_neighbourhood(neighbour)


    def apply_boundry_rules(self, target_row: int, target_column: int) -> Cell:

        # check if boundry rules are unnecessary
        if (0 <= target_row < self.side_length) and (0 <= target_column < self.side_length):
            return self.cells[target_row][target_column]
        
        # from this point on, assume at least one of the coords is unreachable
        match self.boundry_conditions:
            case BoundryConditions.Periodic:
                return self.cells[target_row % self.side_length][target_column % self.side_length]
            case BoundryConditions.Dirichlet0:
                return Cell(0)
            case BoundryConditions.Dirichlet1:
                return Cell(1)
            case BoundryConditions.Neumann:
                result_row: int = CA_2D_4.fit_in_range(target_row, 0, self.side_length)
                result_column: int = CA_2D_4.fit_in_range(target_column, 0, self.side_length)
                return self.cells[result_row][result_column]

    @staticmethod
    def fit_in_range(value: int, lower_bound: int, upper_bound: int) -> int:
        """
        returns the value itself if it is between lower_bound (inclusive) and upper_bound (exclusive).
        If value is less than minimum, minimum is returned.
        If value is greater than or equal to maximum, (maximum - 1) is returned.
        """
        return max(min(upper_bound - 1, value), lower_bound)
            
    def evolve(self) -> None:

        # setup for history
        if self.current_state_index == None:
            raise CANotInitializedError("Cannot evolve CA because it has no starting state")
        if self.current_state_index < (len(self.history) - 1): # next state has already been calculated
            self.goto_state(self.current_state_index + 1)
            return
        
        # first, we figure out what al new states should be
        result: list[list[int]] = []
        for row in self.cells:
            new_row: list[int] = []
            for cell in row:
                neighbourhood: list[Cell] = cell.get_neighbourhood()
                neighbourhood_code = self.convert_to_neighbourhood_code(neighbourhood)
                index: int = 31 - int(neighbourhood_code, 2) # e.g '11111' has index 0; '00000' has index 31 within the ruleset
                new_state: int = int(self.ruleset[index])
                new_row.append(new_state)
            result.append(new_row)

        # finally, we update all cells with their new state
        for row, new_row_values in zip(self.cells, result):
            for cell, new_value in zip(row, new_row_values):
                cell.state = new_value

        # record state
        self.history.append(deepcopy(result))
        self.current_state_index += 1

    def configure_initial_state(self, states: list[list[int]]) -> None:

        for row in states:
            if not all(s in range(0, self.amount_of_states) for s in row):
                raise InvalidStateError(f"Cannot configure initial state '{states}'; the only allowed states are: {[range(0, self.amount_of_states)]}")
        
        for row, new_row_states in zip(self.cells, states):
            for cell, new_state in zip(row, new_row_states):
                cell.state = new_state

        self.history = []
        self.history.append(states)
        self.current_state_index = 0

    def get_states(self) -> list[list[int]]:
        return [[c.state for c in row] for row in self.cells]
    
    def goto_state(self, index: int) -> None:
        try:
            target_state = self.history[index]
        except IndexError:
            raise IndexError(f"Cannot go to state {index} for this CA, because it does not exist")
        
        self.current_state_index = index
        for row, new_row_values in zip(self.cells, target_state):
            for cell, state in zip(row, new_row_values):
                cell.state = state
        
    def devolve(self) -> None:
        if self.current_state_index is None or self.current_state_index == 0:
            raise IndexError(f"Cannot devolve CA because there is no previous state")
        else:
            self.goto_state(self.current_state_index - 1)

    def reset(self) -> None:
        for row in self.cells:
            for cell in row:
                cell.state = 0
        self.history = []
        self.current_state_index = None