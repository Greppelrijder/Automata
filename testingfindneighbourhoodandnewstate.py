from ca_1d import CA_1D
from boundry_conditions import BoundryConditions

def run(initial_state: list[int], steps: int, ruleset: str, boundry_conditions: BoundryConditions):
    ca: CA_1D = CA_1D(len(initial_state), ruleset, boundry_conditions)
    ca.configure_initial_state(initial_state)

    last_grid_state: list[int] = initial_state

    for i in range(steps):
        print(f"step {i}: {last_grid_state}")
        
        ca.evolve()
        if (new_grid_state := [cell.state for cell in ca.cells]) == last_grid_state:
            print("--- program stopped because the grid's state isn't changing anymore")
            break
        else:
            last_grid_state = new_grid_state

run([0,0,0,0,1,0,0,0,0], 100, "00011110", BoundryConditions.Dirichlet0)