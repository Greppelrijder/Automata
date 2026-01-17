from copy import deepcopy
from .boundry_conditions import BoundryConditions
from .grid import Grid, InvalidStateError
from .cell import Cell

class CANotInitializedError(Exception):
    
    def __init__(self, message) -> None:
        self.message = message
        super().__init__(self.message)


class CA_1D(Grid):

    neighbour_directions: list[int] = [-1, 0, 1] # in order

    def __init__(self, cells: int, rules: str, boundry_conditions: BoundryConditions):

        super().__init__(cells, states=2, neighbours = 2, rules=rules, boundry_conditions=boundry_conditions)
        
        # we'll use lists for now, then transition to arrays
        self.cells: list[Cell] = [Cell() for _ in range(cells)]
        
        self.history: list[list[int]] = []
        self.current_state_index: int | None = None

        # assigning neighbours
        for position, cell in enumerate(self.cells):
            for dir in self.neighbour_directions:
                neighbour: Cell = self.apply_boundry_rules(position + dir)
                cell.add_to_neighbourhood(neighbour)

    def apply_boundry_rules(self, target_index: int) -> Cell:

        # check if boundry rules are unnecessary
        if 0 <= target_index < self.amount_of_cells:
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
    
    def configure_initial_state(self, states: list[int]) -> None:

        if not all(s in range(0, self.amount_of_states) for s in states):
            raise InvalidStateError(f"Cannot set this CA's state to '{states}'; the only allowed cell states are: {[range(0, self.amount_of_states)]}")

        for cell, state in zip(self.cells, states):
            cell.state = state
        
        self.history = []
        self.history.append(states)
        self.current_state_index = 0

    def get_state(self, index: int | None = None) -> list[int]:
        if index is None:
            return [c.state for c in self.cells]
        try:
            return [s for s in self.history[index]]
        except IndexError:
            raise IndexError(f"Cannot get state with index {index}, because it does not exist")
    
    def get_state_string(self, index: int | None = None) -> str:
        return "".join(str(s) for s in self.get_state(index))

    def evolve(self) -> None:

        if self.current_state_index == None:
            raise CANotInitializedError("Cannot evolve CA because it has no starting state")
        if self.current_state_index < (len(self.history) - 1): # next state has already been calculated
            self.goto_state(self.current_state_index + 1)
            return
        
        # standard case
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

        # record state
        self.history.append(deepcopy(result))
        self.current_state_index += 1
    
    def goto_state(self, index: int) -> None:

        try:
            target_state = self.history[index]
        except IndexError:
            raise IndexError(f"Cannot go to state {index} for this CA, because it does not exist")
        
        self.current_state_index = index
        for cell, state in zip(self.cells, target_state):
            cell.state = state
        
    def devolve(self) -> None:
        if self.current_state_index is None or self.current_state_index == 0:
            raise IndexError(f"Cannot devolve CA because there is no previous state")
        else:
            self.goto_state(self.current_state_index - 1)

    def reset(self) -> None:
        for cell in self.cells:
            cell.state = 0
        self.history = []
        self.current_state_index = None