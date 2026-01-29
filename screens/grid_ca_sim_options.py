import sys

sys.path.append("..")
from models.boundry_conditions import BoundryConditions

class GridCA_SimOptions:

    def __init__(self, size: int, ruleset: str, boundry_conditions: BoundryConditions, name: str, alive_cell_color: str, dead_cell_color: str):
        self.size = size
        self.ruleset = ruleset
        self.boundry_conditions = boundry_conditions
        self.name = name
        self.alive_cell_color = alive_cell_color
        self.dead_cell_color = dead_cell_color