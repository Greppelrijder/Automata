from enum import Enum

class BoundryConditions(Enum):
    Dirichlet0 = 0
    Dirichlet1 = 1
    Periodic = 2
    Neumann  = 3