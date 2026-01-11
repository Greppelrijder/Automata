from boundry_conditions import BoundryConditions
from cell import Cell
from abc import ABC, abstractmethod
from typing import Collection


class InvalidRulesetError(Exception):
    
    def __init__(self, message) -> None:
        self.message = message
        super().__init__(self.message)

class InvalidStateError(Exception):
    
    def __init__(self, message) -> None:
        self.message = message
        super().__init__(self.message)

class Grid(ABC):

    def __init__(self, cells: int, states: int, neighbours: int, rules: str, boundry_conditions: BoundryConditions):
        
        if states <= 0:
            raise ValueError("Parameter 'states' must be at least 1")
        
        self.amount_of_cells: int = cells
        self.amount_of_states: int = states
        self.amount_of_neighbours: int = neighbours
        self.ruleset: str = rules
        self.boundry_conditions: BoundryConditions = boundry_conditions

        if not self.ruleset_is_valid():
            raise InvalidRulesetError("[descriptive error message]")

    def ruleset_is_valid(self) -> bool:

        if len(self.ruleset) != self.amount_of_neighbourhood_states():
            return False
        
        possible_states = range(0, self.amount_of_states)
        if any(char not in possible_states for char in self.ruleset):
            return False
        
        return True

    def amount_of_neighbourhood_states(self) -> int:
        return self.amount_of_states ** self.amount_of_neighbours
        
    def convert_to_neighbourhood_code(self, neighbourhood: list[Cell]) -> str:
        return "".join(str(cell.state) for cell in neighbourhood)

    @abstractmethod
    def evolve(self) -> None:
        pass