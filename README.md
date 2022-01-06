# Tic-Tac-Toe
An implementation of the simple game "Tic-Tac-Toe". Currently you can play against another human, an "AI" that selects random positions or an Q-learning agent that was trained on 1 million games.

## Prerequisits
* Python v3.10.1
* Tqdm v4.62.3
* Typer v0.4.0

## How to use
The playing board corresponds to a numpad. For example, to place your symbol ("X" or "O") in the middle press 5, bottom left press 1, top left press 7, etc.

`main.py play pvp` &nbsp;&nbsp;&nbsp;&nbsp; to play another human player

`main.py play random` &nbsp;&nbsp;&nbsp;&nbsp; to play against random actions 

`main.py play q-learning` &nbsp;&nbsp;&nbsp;&nbsp; to play a Q-learning agent

`main.py train [n]` &nbsp;&nbsp;&nbsp;&nbsp; to train the AI again with [n] being the number of games it plays

`main.py results` &nbsp;&nbsp;&nbsp;&nbsp; to see how well the AI performs in 10000 games
