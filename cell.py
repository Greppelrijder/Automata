class Cell:

    def __init__(self, starting_state: int = 0):
        self.state: int = starting_state
        self.neighbourhood: list[Cell] = []

    def add_to_neighbourhood(self, neighbours: list[Cell]) -> None:
        self.neighbourhood.extend(neighbours)

    def get_neighbourhood(self) -> list[Cell]:
        return self.neighbourhood