def determine_ruleset(amount_of_neighbours: int, amount_of_alive_neighbours_to_live: list[int], amount_to_come_alive: list[int]):
    """
    The determineruleset function generates a rule-set for cellular automa with an even amount of neighbours
    
    :param amount_of_neighbours: The amount of neighbours a cell has, this amount should be even and greater than 1
    :type amount_of_neighbours: int
    :param amount_of_alive_neighbours_to_live: The list inputted here contains all amount of neighbours, whereby a cell will be able to stay alive.
    For any other amount of neighbours, the cell dies to either loneliness or overpopulation.
    :type amount_of_alive_neighbours_to_live: list[int]
    :param amount_to_come_alive: The list inputted here contains all amount of neighbours, whereby a dead cell will be able to come alive.
    :type amount_to_come_alive: list[int]
    """
    validate_amount_of_neighbours(amount_of_neighbours)
    validate_amount_of_neighbours_to_live(amount_of_neighbours, amount_of_alive_neighbours_to_live)
    validate_amount_of_neighbours_to_live(amount_of_neighbours, amount_of_alive_neighbours_to_live)
    ruleset = ""
    length_ruleset = 2**(amount_of_neighbours + 1)
    for i in range(length_ruleset):
        in_base = str(bin(length_ruleset - 1 - i)[2:])
        while len(in_base) < amount_of_neighbours + 1:
            in_base = "0" + in_base
        total = 0
        for j in range(amount_of_neighbours + 1):
            if in_base[j] == "1":
                total += 1
        if in_base[int(amount_of_neighbours / 2)] == "1":
            total -= 1
            if int(total) in amount_of_alive_neighbours_to_live:
                ruleset += "1"
            else:
                ruleset += "0"
        elif in_base[int(amount_of_neighbours / 2)] == "0":
            if int(total) in amount_to_come_alive:
                ruleset += "1"
            else:
                ruleset += "0"
        else:
            raise ValueError("State must be 0 or 1")
    print(ruleset)

def validate_amount_of_neighbours(amount_of_neighbours: int):
    """"
    This function checks if the amount of neighbours is valid. That is, even and greater than 1.
    
    Errors:
        * ValueError: this error will be raised if any of the given input is invalid (e.g. a negative amount of neighbours)
    """
    if amount_of_neighbours % 2 != 0:   # Without specified order, an odd amount of neighbours gives uncertainties
        raise ValueError("Amount of neighbours must be even")
    if amount_of_neighbours < 1: # To create a useful rule-set, a cell must have at least 2 neighbours
        raise ValueError("amount of neighbours must be greater than 1")
    pass

def validate_amount_of_neighbours_to_live(amount_of_neighbours, amount_of_neighbours_to_live: list[int]):
    """"
    This function checks if given list for the required amount of neighbours for a cell to come or stay alive, are correct
    These lists must consist of only integers greater than 0 and smaller than the amount of neighbours
    
    Errors:
        * ValueError: this error will be raised if any of the given input is of incorrect value (e.g. a negative amount of alive neighbours required to live)
        * TypeError: this error will be raised if any of the given input if of incorrect type (e.g. a string or list inside the list amount_of_alive_neighbours_to_live)
    """
    for i in amount_of_neighbours_to_live:
        if type(i) is not type(1):
            raise TypeError("All arguments in the inputted lists must be of type 'int'.")
        if i < 0 or i > amount_of_neighbours:
            raise ValueError("All arguments in the inputted lists must be non-negative or smaller than the amount of neighbours a cell has.")
    pass

# determine_ruleset(8,[2,3],[3]) returns the rules for Conway's Game of Life