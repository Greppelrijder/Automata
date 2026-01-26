from abc import ABC, abstractmethod

from .boundry_conditions import BoundryConditions
from .cell import Cell

class InvalidRulesetError(Exception):
    """
    This error occurs when the ruleset passed is incompatible with the rest of the grid
    E.g. if the grid has only two possible cell states, then no other characters than 0 and 1 should appear within the ruleset
    """
    def __init__(self, message) -> None:
        self.message = message
        super().__init__(self.message)

class InvalidStateError(Exception):
    """
    This error occurs when a cell within a Grid would receive a state that is not allowed
    """
    def __init__(self, message) -> None:
        self.message = message
        super().__init__(self.message)

class CANotInitializedError(Exception):
    """
    This error occurs when a CA is being evolved whilst it has not yet been assigned a starting state
    """
    def __init__(self, message) -> None:
        self.message = message
        super().__init__(self.message)

class Grid(ABC):

    """
    The Grid class provides an abstract layer for all different types of cellular automata (CA)
    """

    def __init__(self, cells: int, states: int, neighbours: int, rules: str, boundry_conditions: BoundryConditions):
        
        """
        Note that a 'Grid' can not be instantiated directly; rather, this method is responsible for setting up the basics shared among all CA. Child classes can use this default implementation and extend it if needed.
        
        :param cells: Determines the size of the grid
        :type cells: int (>0)
        :param states: Determines the amount of different states a cell can be in
        :type states: int (>0 and <11)
        :param neighbours: Determines the amount of cells that any particular cell is connected to (not counting the cell itself)
        :type neighbours: int (>0)
        :param rules: The ruleset is used to determine a cell's next state when evolving a grid. The ruleset is a string of digits which represents a mapping between possible 'neighbourhoods' and resulting new states. A neighbourhood is defined as the set of states of all the cells that a particular cell is connected to (including itself), in a particular order.
        :type rules: str (of digits)
        :param boundry_conditions: Determines what should happen when a cell's alleged neighbour does not exists
        :type boundry_conditions: BoundryConditions

        Errors:
        * ValueError: this error will be raised if any of the given input is invalid (e.g. a negative amount of states)
        """
        if states <= 0 or states >=11:
            # the reason for this limitation is that the ruleset must contain base-10 digits
            # the ruleset couldn't contain a '10' for example, because this would be read as a 0 and a 1
            # we could resolve this problem by allowing different bases (this is outside the scope of this project)
            raise ValueError(f"Parameter 'states' must be at least 1 and at most 10 (got {states})")
        if cells <= 0:
            raise ValueError(f"Parameter 'cells' must be at least 1 (got {cells})")
        if neighbours <= 0:
            raise ValueError(f"Parameter 'cells' must be at least 1 (got {neighbours})")
        self.validate_ruleset()
        
        
        self.amount_of_cells: int = cells
        self.amount_of_states: int = states
        self.amount_of_neighbours: int = neighbours
        self.ruleset: str = rules
        self.boundry_conditions: BoundryConditions = boundry_conditions


    def validate_ruleset(self) -> None:
        """
        Check if the assigned ruleset satisfies the following conditions:
        1) The length of the ruleset is equal to the amount of possible neighbourhoods for this Grid
        2) The ruleset contains only digits that are smaller than the amount of states for this Grid
        
        Errors:
        * InvalidRulesetError: this error will be raised if any of the above mentioned conditions are not met

        The ruleset is considered valid if this method does not raise any errors

        """
        if len(self.ruleset) != self.amount_of_neighbourhood_states():
            raise InvalidRulesetError(f"Incorrect length of ruleset, length must be {self.amount_of_neighbourhood_states()}.")
        
        possible_states = range(0, self.amount_of_states)
        if any(int(char) not in possible_states for char in self.ruleset):
            raise InvalidRulesetError(f"Incorrect new state, the only allowed new states are {[range(0,self.amount_of_states)]}.")

    def amount_of_neighbourhood_states(self) -> int:
        """
        Calculates and returns the amount of different neighbourhoods for this Grid, based on the amount of neighbours a particular cell has, and the amount of states each cell can be in
        """
        return self.amount_of_states ** (self.amount_of_neighbours + 1)
        
    def convert_to_neighbourhood_code(self, neighbourhood: list[Cell]) -> str:
        """
        Fetches the the state of each cell in the specified neighbourhood, and concatenates them as a string
        """
        return "".join(str(cell.state) for cell in neighbourhood)

    @abstractmethod
    def evolve(self) -> None:
        """
        This method is responsible for updating all cells to their next state, depending on the current state of the grid.
        This method cannot be implemented at an abstract level, because each CA may store its cells in a different way.
        Each child class therefore has to implement their own version.
        """
        pass