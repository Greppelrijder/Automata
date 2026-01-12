from boundry_conditions import BoundryConditions
from grid import Grid, InvalidStateError
from cell import Cell

class CA_1D(Grid):

    neighbour_directions: list[int] = [-1, 0, 1] # in order

    def __init__(self, cells: int, rules: str, boundry_conditions: BoundryConditions):

        super().__init__(cells, states=2, neighbours = 2, rules=rules, boundry_conditions=boundry_conditions)
        
        # we'll use lists for now, then transition to arrays
        self.cells: list[Cell] = [Cell() for _ in range(cells)]

        # assigning neighbours
        for position, cell in enumerate(self.cells):
            for dir in self.neighbour_directions:
                if (target_index := position + dir) in range(0, cells):
                    neighbour: Cell = self.cells[target_index]
                else: # we're outside the grid
                    neighbour: Cell = self.apply_boundry_rules(target_index)
                cell.add_to_neighbourhood(neighbour)

    def apply_boundry_rules(self, target_index: int) -> Cell:

        # check if boundry rules are unnecessary
        if target_index in range(0, self.amount_of_cells):
            return self.cells[target_index]
        
        match self.boundry_conditions:
            case BoundryConditions.Periodic:
                return self.cells[target_index % self.amount_of_cells]
            case BoundryConditions.Dirichlet0:
                return Cell(0)
            case BoundryConditions.Dirichlet1:
                return Cell(1)
            case BoundryConditions.Neumann:
                return self.cells[0] if target_index < 0 else self.cells[-1]

    def evolve(self) -> None:

        # first, we figure out what al new states should be
        result: list[int] = []
        for cell in self.cells:
            neighbourhood: list[Cell] = cell.get_neighbourhood()
            neighbourhood_code = self.convert_to_neighbourhood_code(neighbourhood)
            index: int = 7 - int(neighbourhood_code, 2) # e.g '111' has index 0; '000' has index 7 within the ruleset
            new_state: int = int(self.ruleset[index])
            result.append(new_state)

        # finally, we update all cells with their new state
        for cell, state in zip(self.cells, result):
            cell.state = state

    def configure_initial_state(self, states: list[int]) -> None:

        if not all(s in range(0, self.amount_of_states) for s in states):
            raise InvalidStateError(f"Cannot configure initial state '{states}'; the only allowed states are: {[range(0, self.amount_of_states)]}")

        for cell, state in zip(self.cells, states):
            cell.state = state