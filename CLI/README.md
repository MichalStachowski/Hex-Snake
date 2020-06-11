##### Implementation of Snake game in CLI  
A basic hex board was prepared. The Snake, HexField, HexBoard classes were used. The board prepared in this way is drawn in the console.  
  
The colors used - S is marked in green, while the fruit is marked in red.  
  
Environmental rules and movement mechanics have been implemented. The snake moves in a hexagonal grid and eats the fruit 
generated in a random position. After eating it, the snake lengthens and the player scores a point. If you hover over yourself, 
the game ends. The same happens when snake leave the board.  
  
To move the snake we use "qweasd" keys loaded from standard input. (Directions: Q = upper left, W = upper, E = upper right, A = lower left, S = lower, D = lower right)
  
Two players participate in the game. The first player plays his game, and then it is the turn of the second player. On the end score of each player is compare and the winner is selected
