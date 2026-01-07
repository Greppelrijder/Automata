from enum import Enum

class BoundryConditions(Enum):
    Periodic = 1
    Dirichlet = 2
    Neumann  = 3