# Tic-Tac-Toe

An implementation of the simple game "Tic-Tac-Toe". Currently you can play against another human, an "AI" that selects random positions or an Q-learning agent that was trained in 1 million games.

<https://en.wikipedia.org/wiki/Tic-tac-toe>

## Prerequisits

* Python v3.10.1
* Numpy v1.22.0
* Tqdm v4.62.3
* Typer v0.4.0

All packages used are listed in the requirements.txt. Install them with &nbsp;&nbsp;&nbsp;&nbsp; `pip install -r requirements.txt` 

## How to
The inputs ("X" or "O") correspond to the numpad layout. For example, to place your symbol in the middle press 5, bottom left press 1, top left press 7, etc.

Go to the game folder and run:

`main.py play pvp` &nbsp;&nbsp;&nbsp;&nbsp; to play another human player

`main.py play random` &nbsp;&nbsp;&nbsp;&nbsp; to play against random actions 

`main.py play q-learning` &nbsp;&nbsp;&nbsp;&nbsp; to play a Q-learning opponent

`main.py training [n]` &nbsp;&nbsp;&nbsp;&nbsp; to train the AI with [n] being the number of games it plays

`main.py results [n]` &nbsp;&nbsp;&nbsp;&nbsp; to see how well the AI performs in [n] games