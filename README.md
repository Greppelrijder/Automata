# Automata
final project for 'Programmeren voor wiskunde'

# How our project is structured
Our project contains classes for cellular automa. The grid class is generic and works for a number of states between 1 and 10. The number of neighbours can be any finite positive integer.
We have distinct classes for 1D and 2D cellular automa.
The 1D CA has the number of neighbours and states preset to 2, the 2D CA has them set to respectivly 2 and 8.
We made a visualization program, so the user can visualize a created grid, with a self chosen size, rule-set and broundry conditions.

# Users guide
To run the program, run the visualisation.py document. This will open a new window on your screen. After you've pressed the "Main menu" button, you can choose which CA you want to create.
- If you chose for a 1D CA, you can choose the amount of cells, the boundary conditions*, you can create your own ruleset** and you can choose a name for the CA consisting of max. 15 characters. You can also choose a colour for the cells when they are either dead or alive. The standard ruleset here is set to "Rule 30".
- If you chose for a 2D CA, the boundary conditions, name and colors of the cells work the same. The difference is that you choose for the length of one side of the grid and the length of the ruleset is now 512. The standard ruleset here is set to the rules of Conway's Game of Life.
- If you chose for a 2D CA with 4 neighbours, everything except the length of the ruleset is the same as a 2D CA. The required length of a ruleset in this case is 32. 


\* You can choose the boundary conditions from the following list:
  * Dirichlet0: A constant cell with state 0 is used (this cell is not part of the Grid)
  * Dirichlet1: A constant cell with state 1 is used (this cell is not part of the Grid)
  * Periodic: The Grid is 'wrapped around', so that the cell on the other side of the grid is used
  * Neumann: A cell with the same state as the border cell is used (this cell is not part of the Grid) \


\** The ruleset tells the grid what the next state for a cell should be, based of the current state of the cell and its neighbours. \
  e.g. a cell in a 1D grid with state 1 and both neigbours with state 0 has as neighbour string "010". \
  The ruleset "00001110" means the following: \
  State (with neighbours)&nbsp;&nbsp;&nbsp;&nbsp;Next state \
          &nbsp;&nbsp;&nbsp;&nbsp;111 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;0 \
          &nbsp;&nbsp;&nbsp;&nbsp;110 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;0 \
          &nbsp;&nbsp;&nbsp;&nbsp;101 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;0 \
          &nbsp;&nbsp;&nbsp;&nbsp;100 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;0 \
          &nbsp;&nbsp;&nbsp;&nbsp;011 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1 \
          &nbsp;&nbsp;&nbsp;&nbsp;010 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1 \
          &nbsp;&nbsp;&nbsp;&nbsp;001 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1 \
          &nbsp;&nbsp;&nbsp;&nbsp;000 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;0 \
     \
The scale is preset to have a maximum length of 21. This is to keep the overview of the grid nice. Or in other words, to prevent the cells from becoming to small. You can change the maximum size of the grid, by enlarging the scale maximum. you can change the maximum of the scale in the grid_ca_prep_screen.py file in line 48.\
 When you create a 2D CA with a relativly large side size, the FPS of the visualisation drops quite a bit. The advice is to keep the side size lower than 21.
After you've created the CA and added a starting state (by pressing the white squares and pressing the confirm button), you can go to the next or previous state with their repective buttons. If there is no previous state, nothing wil happen. There is also a reset button that, when clicked once, puts the CA in the starting state, and when pressed again clears the entire grid and sets the state of all the cells to "0" / dead. The auto butten runs the CA automatic with an, on the scale to the right modifiable number of milliseconds in between each step.

The master branch also contains the files testing_1D and testing_2D, these files can be used to test the 1D and 2D CA without visualisation, but it is not recommended.

# Generate your own rule set
In the master branch we also included a file called Create_rule_set. This file contains a function called determine_ruleset which can generate a rule set on the following inputs:
- You can enter the amount of neighbours a cell has. (We fixed the amount of states to 2)
- The second parameter wants a list with the amount of neighbours, whereby a cell will be able to stay alive.
- The third parameter wants a list with the amount of neighbours, whereby a dead cell will be able to come alive. 

There are however a few restriction to the function:
- The amount of neighbours must be even and greater than 1. In the 1D and 2D CA, the amount of neighbours is always even.
- The list, with the required number of alive neighbours to stay alive, may only contain integers non-negative and smaller than or equal to the amount of neighbours the cell has.
- The list, with the required number of alive neighbours to come alive, may only contain integers non-negative and smaller than or equal to the amount of neighbours the cell has.

Caution: This rule set generator file does not contain a GUI, so the user should run the file itself and call the function. (Look at the example in the last line.)

# Useful
generating callular automa with the rueles from for example Conway's Game of Life shows that complex behavior can arise from very simple rules. It can be used to visualize or model complex problems.

# Suggestions for 1D cellular automa
- Ruleset: 00011100; boundry conditions: doesn't matter; starting state: cell 2,5,8,... alive.
- Ruleset: 10101010; boundry conditions: periodic; starting state: first, third, fifth, ... alive.

# Suggestions for 2D cellular automa
- Ruleset Game of Life (standard); boundry conditions: periodic; grid size: 3x3; starting state: [[0,1,0],[0,1,0],[0,1,0]].
- Ruleset: Game of Life; boundry conditions: periodic; grid size: doesn't matter; starting state: Make a this 3x3 figure somewhere on the grid [[0,1,0],[0,0,1],[1,1,1]] (Gospers glider)
