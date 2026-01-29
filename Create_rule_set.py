def determine_ruleset(amount_of_neighbours: int, amount_of_alive_neighbours_to_live: list, amount_to_come_alive: list):
    ruleset = ""
    if amount_of_neighbours % 2 != 0:
        raise ValueError("Amount of neighbours must be even")
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

#e.g. determine_ruleset(8,[2,3],[3]) returns the rules for Conway's Game of Life