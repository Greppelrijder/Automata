from boundry_conditions import BoundryConditions

class Grid:

    def __init__(self, cells: int, dimensions: int, states: int, neighbours: int, rules: str, boundry_conditions: BoundryConditions):
        self.amount_of_cells: int = cells
        self.amount_of_dimensions: int = dimensions
        self.amount_of_states: int = states
        self.amount_of_neighbours: int = neighbours
        self.ruleset: str = rules
        self.boundry_conditions: BoundryConditions = boundry_conditions

        # logic to construct the grid goes here
        # one big list of cells is not the way to go
        # we might switch to for example multi-dimensional arrays
        self.cells = []


    def next_state(self) -> None:
        
        # we should update all cells simultaneously
        # again, one big list is not the way to go
        result = []

        for cell in self.cells:
            result.append(self.evolve(cell))

        # update happens all at once
        self.cells = result


    def evolve(self, cell_number) -> int:
        neighbours = self.get_neighbourhood(cell_number)

        # logic to determine the cell's next state goes here
        # we determine the next state based on the ruleset
        # ruleset will be an integer
        # the neighbourhood itself forms an integer, k, that has a position
        # e.g if k consists of only 0's, the corresponding position is 0
        # the cell's new state will be equal to whatever digit is in the k'th position in the ruleset

        return 0

    def get_neighbourhood(self, cell_number):
        
        # logic to find neighbours of a given cell goes here
        # refering to a cell by only one number is not very practical; we might switch to a different reference system later (e.g. by using multi-dimensional arrays)
        # algorithm depends on the grid's dimensionality and the amount of neighbours per cell
        # we should design a consitent procedure for choosing neighbours

        return []
