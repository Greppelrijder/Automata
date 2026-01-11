def run(start_overview: list, amount: int, rule:str):
    for _ in range(amount):
        new_overview = cells_overview(start_overview, rule)
        if new_overview == start_overview:
            return new_overview
        start_overview = new_overview
        #als we de tussenstappen willen laten zien
        #print(new_overview)
    return start_overview

def cells_overview(start_overview: list, rule:str):
    new_overview = []
    for i in range(len(start_overview)):
        update_cell_value = find_neigbours_update_cell(i, start_overview, rule)
        new_overview.append(update_cell_value)
    return new_overview

def find_neigbours_update_cell(celltuple:tuple, cells, rule:str):
    #cells is a list with rows with cellstates: eg [[1,1,0,1,0],[0,1,1,0,0],[1,1,0,0,0],[0,0,1,0,1]], first position is cellnumber 0[0]
    #rule is a list with rules eg "00011110"
    #cell states must be correct
    cellx = celltuple[0]
    celly = celltuple[1]
    cell_state = cells[cellx][celly]
    if cell_state not in [0,1]:
        raise ValueError("No valid status for cell")
    
    left_nb = cells[cellx][celly - 1]
    if celly < len(cells[cellx]) - 1:
        right_nb = cells[cells[cellx[celly + 1]]]
    elif celly == len(cells[cellx]) - 1:
        right_nb = cells[cellx[0]]
    if cellx > 0:
        up_nb = cells[cellx - 1][celly]
    elif cellx == 0:
        up_nb = cells[-1][celly]
    if cellx 
    #pattern = f"{left_nb}{cell_state}{right_nb}"
    newcell_state = rule[7 - 4*left_nb - 2*cell_state - right_nb]
    return int(newcell_state)

#print(find_neigbours_update_cell(6, [1,1,1,0,0,1,0], "00011110"))
#print(cells_overview([1,1,1,0,0,1,0,0,1,1], "00011110"))
print(run([1,1,1,0,0,1,0,0,1,1], 5, "00011110"))