class Cell:
    """
    A cell is defined by its state and its neighbours; this is the only relevant information for CA
    """
    def __init__(self, starting_state: int = 0):
        self.state: int = starting_state
        self.neighbourhood: list[Cell] = []

    def add_to_neighbourhood(self, neighbour: "Cell") -> None:
        """
        Register 'neighbour' as part of this cell's neighbourhood
        """
        self.neighbourhood.append(neighbour)

    def get_neighbourhood(self) -> list["Cell"]:
        """
        Retrieve this cell's neighbourhood
        """
        # Note that this attribute can be accessed directly, but it should only be gettable -not settable- byt other classes
        return self.neighbourhood