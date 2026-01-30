from models.ca_2d import CA_2D
from models.boundry_conditions import BoundryConditions

"""
This document can be used to test our code for 2D cellular automa, although it is easer to test the code in the visualisation.
The input starting state should be a list consisting of the rows of your grid
"""

def run(initial_state: list[list[int]], steps: int, ruleset: str, boundry_conditions: BoundryConditions):
    ca: CA_2D = CA_2D(len(initial_state)*len(initial_state[0]), ruleset, boundry_conditions)
    ca.configure_initial_state(initial_state)

    last_grid_state: list[list[int]] = initial_state
    for i in range(steps):
        print(f"step {i}: {last_grid_state}")
        print()        
        ca.evolve()

        if (new_grid_state := ca.get_state()) == last_grid_state:
            print("--- program stopped because the grid's state isn't changing anymore")
            break
        else:
            last_grid_state = new_grid_state

if __name__ == "__main__":
    rules = "00000000000000000000000000000000000000000000000100000000000000010000000000000001000000000000000100000001000101110000000100010110000000000000000100000000000000010000000100010111000000010001011000000001000101110000000100010110000101110111111000010110011010000000000000000001000000000000000100000001000101110000000100010110000000010001011100000001000101100001011101111110000101100110100000000001000101110000000100010110000101110111111000010110011010000001011101111110000101100110100001111110111010000110100010000000" # Conway's rules for Game of Life
    run([[1,0,1,0,0],[1,1,0,0,1],[0,0,1,0,0],[1,1,0,1,0],[0,1,0,1,1]], 2, rules, BoundryConditions.Periodic)