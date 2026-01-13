from boundry_conditions import BoundryConditions
from grid import Grid
from cell import Cell
import math

class CA_2D(Grid):

    neighbour_directions: list[tuple[int, int]] = [
        (-1, 1), (0, 1), (1, 1),
        (-1, 0), (0, 0), (1, 0),
        (-1, -1), (0, -1), (1, -1)
    ]

    def __init__(self, cells: int, rules: str, boundry_conditions: BoundryConditions):
        super().__init__(cells, states=2, neighbours = 8, rules=rules, boundry_conditions=boundry_conditions)

        # the grid will contain *at least* as many cells as specified
        # if necessary, we will add more cells to reach a perfect square
        self.side_length: int = math.ceil(math.sqrt(cells))
        self.amount_of_cells = self.side_length ** 2

        # we'll use lists for now, then transition to arrays
        self.cells: list[list[Cell]] = []
        for _ in range(self.side_length):
            self.cells.append([Cell() for _ in range(self.side_length)])

        for column_number, column in enumerate(self.cells):
            for row_number, cell in enumerate(column):
                self.assign_neighbours(cell, column_number, row_number)


    def assign_neighbours(self, cell: Cell, column_number: int, row_number: int) -> None:
        for dir in self.neighbour_directions:
            neighbour: Cell = self.apply_boundry_rules(column_number + dir[0], row_number + dir[1])
            cell.add_to_neighbourhood(neighbour)

    def apply_boundry_rules(self, target_x: int, target_y: int) -> Cell:

        # check if boundry rules are unnecessary
        if (0 <= target_x < self.side_length) and (0 <= target_y < self.side_length):
            return self.cells[target_x][target_y]
        
        # from this point on, assume at least one of the coords is unreachable
        match self.boundry_conditions:
            case BoundryConditions.Periodic:
                return self.cells[target_x % self.side_length][target_y % self.side_length]
            case BoundryConditions.Dirichlet0:
                return Cell(0)
            case BoundryConditions.Dirichlet1:
                return Cell(1)
            case BoundryConditions.Neumann:
                result_x: int = CA_2D.fit_in_range(target_x, 0, self.side_length)
                result_y: int = CA_2D.fit_in_range(target_y, 0, self.side_length)
                return self.cells[result_x][result_y]

    @staticmethod
    def fit_in_range(value: int, lower_bound: int, upper_bound: int) -> int:
        """
        returns the value itself if it is between lower_bound (inclusive) and upper_bound (exclusive).
        If value is less than minimum, minimum is returned.
        If value is greater than or equal to maximum, (maximum - 1) is returned.
        """
        return max(min(upper_bound - 1, value), lower_bound)
            
    def evolve(self) -> None:
        
        # first, we figure out what al new states should be
        result: list[list[int]] = []
        for column in self.cells:
            new_column: list[int] = []
            for cell in column:
                neighbourhood: list[Cell] = cell.get_neighbourhood()
                neighbourhood_code = self.convert_to_neighbourhood_code(neighbourhood)
                index: int = 511 - int(neighbourhood_code, 2) # e.g '111111111' has index 0; '000000000' has index 255 within the ruleset
                new_state: int = int(self.ruleset[index])
                new_column.append(new_state)
            result.append(new_column)

        # finally, we update all cells with their new state
        for column, new_column_values in zip(self.cells, result):
            for cell, new_value in zip(column, new_column_values):
                cell.state = new_value