from models.ca_2d import CA_2D
from models.boundry_conditions import BoundryConditions

def run(initial_state: list[list[int]], steps: int, ruleset: str, boundry_conditions: BoundryConditions):
    ca: CA_2D = CA_2D(len(initial_state)*len(initial_state[0]), ruleset, boundry_conditions)
    ca.configure_initial_state(initial_state)

    last_grid_state: list[list[int]] = initial_state
    for i in range(steps):
        print(f"step {i}: {last_grid_state}")
        print()        
        ca.evolve()

        if (new_grid_state := ca.get_states()) == last_grid_state:
            print("--- program stopped because the grid's state isn't changing anymore")
            break
        else:
            last_grid_state = new_grid_state

if __name__ == "__main__":
    #run([0,0,0,0,1,0,0,0,0], 100, "00011110", BoundryConditions.Dirichlet0) # works as expected (stopped at step 15)
    #run([0,0,0,0,1,0,0,0,0], 100, "00011110", BoundryConditions.Dirichlet1) # works as expected (stopped at step 21)
    #run([0,0,0,0,1,0,0,0,0], 100, "00011110", BoundryConditions.Neumann) # works as expected (didn't stop)
    run([[1,0,1,0,0],[1,1,0,0,1],[0,0,1,0,0],[1,1,0,1,0],[0,1,0,1,1]], 2, "00101101001011110100111001001011011110010101100010110100111010110101100101011110001001110100110100011011101001100101110010101010110101001110010110010010111010010111100101101001001110101101011001011110001001110100110100011011101001100101110010101010110101001110010110010010111010010111100101101001001110101101011001011110001001110100110100011011101001100101110010101010110101001110010110010010111010010111100101101001001110101101011001011110001001110100110100011011101001100101110010101010110101001110010110010010", BoundryConditions.Periodic)