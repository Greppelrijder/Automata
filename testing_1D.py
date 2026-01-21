from models.ca_1d import CA_1D
from models.boundry_conditions import BoundryConditions

def run(initial_state: list[int], steps: int, ruleset: str, boundry_conditions: BoundryConditions):
    ca: CA_1D = CA_1D(len(initial_state), ruleset, boundry_conditions)
    ca.configure_initial_state(initial_state)

    last_grid_state: list[int] = initial_state
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
    #run([0,0,0,0,1,0,0,0,0], 100, "00011110", BoundryConditions.Dirichlet0) # works as expected (stopped at step 15)
    run([0,0,0,0,1,0,0,0,0], 100, "00011110", BoundryConditions.Dirichlet1) # works as expected (stopped at step 21)
    #run([0,0,0,0,1,0,0,0,0], 100, "00011110", BoundryConditions.Neumann) # works as expected (didn't stop)
    #run([0,0,0,0,1,0,0,0,0], 100, "00011110", BoundryConditions.Periodic) # works as expected (didn't stop)