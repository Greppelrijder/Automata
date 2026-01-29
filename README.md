# Automata
final project for 'Programmeren voor wiskunde'

# How our project is structured
Our project contains classes for cellular automa. The grid class is generic and works for a number of states between 1 and 10. The number of neighbours can be any finite positive integer.
We have distinct classes for 1D and 2D cellular automa.
The 1D CA has the number of neighbours and states preset to 2, the 2D CA has them set to respectivly 2 and 8.
We made a visualization program, so the user can visualize a created grid, with a self chosen size, rule-set and broundry conditions.

# Users guide
To run the program, run the visualisation.py document. This will open a new window on your screen. After you've pressed the "Main menu" button, you can choose which CA you want to create.
- If you chose for a 1D CA, you can choose the amount of cells, the boundry conditions*, you can create your own ruleset** and you can choose a name for the CA consisting of max. 15 characters. You can also choose a color for the cells when they are either dead or alive. The standard ruleset here is set to "Rule 30".
- If you chose for a 2D CA, the boundry conditions, name and colors of the cells work the same. The difference is that you choose for the length of one side of the grid and the length of the ruleset is now 512. The standard ruleset here is set to the rules of Conway's Game of Life.
- If you chose for a 2D CA with 4 neighbours, everything except the length of the ruleset is the same as a 2D CA. The required length of a ruleset in this case is 32.
* You can choose the boundr conditions from the following list:
  * Dirichlet0: A constant cell with state 0 is used (this cell is not part of the Grid)
  * Dirichlet1: A constant cell with state 1 is used (this cell is not part of the Grid)
  * Periodic: The Grid is 'wrapped around', so that the cell on the other side of the grid is used
  * Neumann: A cell with the same state as the border cell is used (this cell is not part of the Grid)
** The ruleset tells the grid what the next state for a cell should be, based of the current state of the cell and its neighbours. \
  e.g. a cell in a 1D grid with state 1 and both neigbours with state 0 has as neighbour string "010". \
  The ruleset "00001110" means the following: \
  State (with neighbours)&nbsp;&nbsp;&nbsp;&nbsp;Next state \
          111 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;0 \
          110 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;0 \
          101 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;0 \
          100 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;0 \
          011 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1 \
          010 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1 \
          001 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1 \
          000 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;0

# Useful
generating callular automa with the rueles from for example Conway's Game of Life shows that complex behavior can arise from very simple rules. It can be used to visualize or model complex problems.

# Suggestions for 1D cellular automa
- Ruleset: 00011100; boundry conditions: doesn't matter; starting state: cell 2,5,8,... alive.
- Ruleset: 10101010; boundry conditions: periodic; starting state: first, third, fifth, ... alive.

# Suggestions for 2D cellular automa
- Ruleset Game of Life (standard); boundry conditions: periodic; grid size: 3x3; starting state: [[0,1,0],[0,1,0],[0,1,0]].
- Ruleset: Game of Life; boundry conditions: periodic; grid size: doesn't matter; starting state: Make a this 3x3 figure somewhere on the grid [[0,1,0],[0,0,1],[1,1,1]] (Gospers glider)


Why the project is useful
How users can get started with the project
