class cell:
    def __init__(self, cells, states):
        self.state = cells
        pass

def find_neigbours_update_cell(cellnumber:int, cells, rule:str):
    #cells is a list with cellstates: eg [0,1,0,0,0,0,1,1,1,,0], first position is cellnumber 0
    #rule is a list with rules eg "0001111"
    #cell states must be correct
    cell_state = cells[cellnumber]
    left_nb = cells[cellnumber - 1]
    if cellnumber < len(cells) - 1:
        right_nb = cells[cellnumber + 1]
    elif cellnumber == len(cells) - 1:
        right_nb = cells[0]
    pattern = f"{left_nb}{cell_state}{right_nb}"
    match pattern:
        case "111":
            newcell_state = rule[0]
        case "110":
            newcell_state = rule[1]
        case "101":
            newcell_state = rule[2]
        case "100":
            newcell_state = rule[3]
        case "011":
            newcell_state = rule[4]
        case "010":
            newcell_state = rule[5]
        case "001":
            newcell_state = rule[6]
        case "000":
            newcell_state = rule[1]
    return newcell_state

print(find_neigbours_update_cell(6, [1,1,1,0,0,1,0], "0001111"))