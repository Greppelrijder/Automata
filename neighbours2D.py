import numpy as np
from cell import Cell

def run(start_overview: list, amount: int, rule:str):
    for _ in range(amount):
        new_overview = cells_overview(start_overview, rule)
        if new_overview == start_overview:
            return new_overview
        start_overview = new_overview
        #als we de tussenstappen willen laten zien
        #print(new_overview)
    return new_overview

def cells_overview(start_overview: list, ruleset:str):
    new_overview = []
    for i in range(len(start_overview)):
        for j in range(len(start_overview[0])):
            update_cell_value = find_neigbours_update_cell((i,j), start_overview, ruleset)
            new_overview.append(update_cell_value)
    return new_overview

def find_neigbours_update_cell(celltuple:tuple, cells,  boundry_conditions, ruleset:str):
    #cells is a list with rows with cellstates: eg [[1,1,0,1,0],[0,1,1,0,0],[1,1,0,0,0],[0,0,1,0,1]], first position is cellnumber 0[0]
    cellx = celltuple[0]
    celly = celltuple[1]
    cell_state = cells[celly][cellx]
    if cell_state not in [0,1]:
        raise ValueError("No valid status for cell")
                # #determine neigbours
                # left_nb = cells[cellx][celly - 1]
                # if celly < len(cells[cellx]) - 1:
                #     right_nb = cells[cellx][celly + 1]
                # elif celly == len(cells[cellx]) - 1:
                #     right_nb = cells[cellx][0]
                # if cellx > 0:
                #     up_nb = cells[cellx - 1][celly]
                # elif cellx == 0:
                #     up_nb = cells[-1][celly]
                # if cellx < len(cells) - 1:
                #     down_nb = cells[cellx + 1][celly]
                # elif cellx == len(cells) - 1:
                #     down_nb = cells[0][celly]
    #determine neigbours
    neighbour_directions: list[tuple] = [(-1,1),(0,1),(1,1),(-1,0),(0,0),(0,1),(-1,-1),(0,-1),(1,-1)] #In order
    neighbour_states = ""
    
    for i in range(len(neighbour_directions)):
        neighbour_states = neighbour_states + str(cells[celly - neighbour_directions[i][1]][cellx + neighbour_directions[i][0]]) 
    print(neighbour_states)

    # assigning neighbours
    for positionx, positiony, cell in enumerate(cells): #dit nog fixen
        for dir in neighbour_directions:
            dirx = dir[0]
            diry = dir[1]
            neighbour: Cell = apply_boundry_rules(positionx + dirx, positiony - diry,boundry_conditions)
            cell.add_to_neighbourhood(neighbour)

    #evolve to new state
    index: int = 511 - int(neighbour_states,2)
    new_state: int = int(ruleset[index])
    print(new_state)

def apply_boundry_rules(cellx: int, celly: int, cells, boundry_conditions: str):
    # check if boundry rules are unnecessary
    if 0 <= celly < len(cells) - 1 and 0 <= cellx < len(cells[0]) - 1:
        return cells[celly][cellx]
    
    # match boundry_conditions:
    #     case "Periodic":
    #         return cells[target_index % self.amount_of_cells]
    #     case "Dirichlet0":
    #         return Cell(0)
    #     case "Dirichlet1":
    #         return Cell(1)
    #     case "Neumann":
    #         return self.cells[0] if cellx < 0 else self.cells[-1]

    #evolve
    # first, we figure out what al new states should be
    #result: list[int] = np.array([])
    #for cell in range(len(cells) * len(cells[0])):

    #np.append(result,new_state)
    #print(result)

    #pattern = f"{leftup_nb}{up_nb}{rightup_nb}{left_nb}{cell_state}{right_nb}{leftdown_nb}{down_nb}{rightdown_nb}"

#print(find_neigbours_update_cell(6, [1,1,1,0,0,1,0], "00011110"))
#print(cells_overview([1,1,1,0,0,1,0,0,1,1], "00011110"))
#print(run([1,1,1,0,0,1,0,0,1,1], 5, "00011110"))
find_neigbours_update_cell((0,1),[[1,1,0,1,0],[0,1,1,0,0],[1,1,0,0,0],[0,0,1,0,1]],"Neumann","00101101001011110100111001001011011110010101100010110100111010110101100101011110001001110100110100011011101001100101110010101010110101001110010110010010111010010111100101101001001110101101011001011110001001110100110100011011101001100101110010101010110101001110010110010010111010010111100101101001001110101101011001011110001001110100110100011011101001100101110010101010110101001110010110010010111010010111100101101001001110101101011001011110001001110100110100011011101001100101110010101010110101001110010110010010")
