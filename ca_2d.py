from boundry_conditions import BoundryConditions
from grid import Grid

class CA_2D(Grid):

    def __init__(self, cells: int, rules: str, boundry_conditions: BoundryConditions):
        super().__init__(cells, dimensions=2, states=2, neighbours = 8, rules=rules, boundry_conditions=boundry_conditions)

    def display(self) -> None:
        # visual functionality will be implemented here
        raise NotImplementedError
