from abc import ABC, abstractmethod
from copy import deepcopy
from typing import Any
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
        
        self.amount_of_cells: int = cells
        self.amount_of_states: int = states
        self.amount_of_neighbours: int = neighbours
        self.ruleset: str = rules
        self.boundry_conditions: BoundryConditions = boundry_conditions
        self.validate_ruleset()

        # we need to remember previous states
        self.cells = []
        self.history: list = []
        self.current_state_index: int | None = None



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
            raise InvalidRulesetError(f"Invalid ruleset, the only allowed characters are in {[range(0,self.amount_of_states)]}.")

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


    def configure_initial_state(self, initial_state) -> None:
        """
        Set the state of each cell to the corresponding value in 'initial_state'
        """
        self.set_state(initial_state)
        self.history = []
        self.history.append(initial_state)
        self.current_state_index = 0


    def evolve(self) -> None:
        """
        Update each cell according to the given ruleset and the state of its neighbourhood.
        All cells are updated simultaneously.

        Errors:
        * CANotInitializedError: This error occurs when the CA has not yet been assigned a starting state
        """

        # non-standard cases
        if self.current_state_index == None:
            raise CANotInitializedError("Cannot evolve CA because it has no starting state")
        if self.current_state_index < (len(self.history) - 1): # next state has already been calculated
            self.goto_state(self.current_state_index + 1)
            return
        
        # standard case
        new_state = self.determine_next_state()
        self.set_state(new_state)
        # record state
        self.history.append(deepcopy(new_state))
        self.current_state_index += 1
    
    def goto_state(self, index: int) -> None:
        """
        Set this CA to one of its recorded states (e.g. go back to starting state, go forward to current state)

        Errors:
        * IndexError: this error occurs when 'index' is too large (the associated state has not yet been reached)
        """
        try:
            target_state = self.history[index]
        except IndexError:
            raise IndexError(f"Cannot go to state {index} for this CA, because it does not exist")
        
        self.current_state_index = index
        self.set_state(target_state)

    def devolve(self) -> None:
        """
        Set this Grid to its previous state

        Errors:
        * IndexError: this error is raised if the CA has no previous state
        """
        if self.current_state_index is None or self.current_state_index == 0:
            raise IndexError(f"Cannot devolve CA because there is no previous state")
        else:
            self.goto_state(self.current_state_index - 1)
    
    def get_state(self, index: int | None = None) -> Any:
        """
        Retrieve the full state of this CA (i.e. the combination of its cells' states).
        An index may be specified to access a different state than the current one.

        Errors:
        * IndexError: this error occurs when 'index' is too large (the associated state has not yet been reached)
        """
        if (index is None) and (self.current_state_index is not None): # assume current state
            return self.history[self.current_state_index]
        elif index is None: # no state to use
            raise CANotInitializedError(f"Cannot get this CA's state, because it has not yet been initialized")

        try: # from this point on, index is not None
            return self.history[index]
        except IndexError:
            raise IndexError(f"Cannot get state with index {index}, because it does not exist")
 
    @abstractmethod
    def reset(self) -> None:
        """
        Forget all recorded states; the resetting of the CA itself should be handled by child classes
        """
        self.history = []
        self.current_state_index = None

    @abstractmethod
    def determine_next_state(self) -> Any:
        """
        There is no uniform way to determine a CA's next state, since each child class might use a different datastructure to store its cells. Each childclass will therefore have to implement this functionality for its datastructure
        """
        pass

    @abstractmethod
    def set_state(self, state: Any) -> None:
        """
        There is no uniform way to set a CA's state, since each child class might use a different datastructure to store its cells. Each childclass will therefore have to implement this functionality for its datastructure
        """
        pass