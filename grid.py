from boundry_conditions import BoundryConditions
from cell import Cell
from abc import ABC, abstractmethod

class InvalidRulesetError(Exception):
    
    def __init__(self, message) -> None:
        self.message = message
        super().__init__(self.message)

class Grid(ABC):

    def __init__(self, cells: int, states: int, neighbours: int, rules: str, boundry_conditions: BoundryConditions):
        
        self.amount_of_cells: int = cells
        self.amount_of_states: int = states
        self.amount_of_neighbours: int = neighbours
        self.ruleset: str = rules
        self.boundry_conditions: BoundryConditions = boundry_conditions

        if not self.is_valid_ruleset(states, neighbours, rules):
            raise InvalidRulesetError("[descriptive error message]")

    def is_valid_ruleset(self, states: int, neighbours: int, rules: str) -> bool:
        # check if the given ruleset is compatible with the given amount of states and beighbours
        # first, check if the ruleset has the correct length by comparing it against amount_of_neighbour_states
        # then, check if the ruleset contains any invalid digits
        raise NotImplemented

    def amount_of_neighbourhood_states(self) -> int:
        # based on the amount of neighbours per cell, and the amount of states a cell can be in, the total amount of different neighbourhoods can be calculated
        raise NotImplemented
        
    def get_neighbourhood_code(self, neighbourhood: list[Cell]) -> int:
        # this method should concat the states of the neighbourhood cells, in order
        # this method is necessary to apply the rules; each neighbourhood_code corresponds to a position in the ruleset
        raise NotImplemented


    @abstractmethod
    def evolve(self) -> int:
        pass