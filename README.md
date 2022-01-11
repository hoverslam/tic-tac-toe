# Tic-Tac-Toe

An implementation of the familiar game "Tic-Tac-Toe". Currently you can play against another human, an "AI" that selects random positions or a Q-learning agent that was trained in 1 million games.

<https://en.wikipedia.org/wiki/Tic-tac-toe>

## Prerequisite

* Python v3.10.1
* Numpy v1.22.0
* Tqdm v4.62.3
* Typer v0.4.0
* Pygame v2.1.2

The packages above are required to play the game. All packages used are listed in the requirements.txt.

Install them with &nbsp;&nbsp;&nbsp;&nbsp; `pip install -r requirements.txt` 

## How to

Go to the game folder and run:

* `main.py play pvp` &nbsp;&nbsp;&nbsp;&nbsp; to play another human player

* `main.py play random` &nbsp;&nbsp;&nbsp;&nbsp; to play against random actions 

* `main.py play q-learning` &nbsp;&nbsp;&nbsp;&nbsp; to play a Q-learning opponent

* `main.py play q-learning True` &nbsp;&nbsp;&nbsp;&nbsp; if you set the last parameter to *True* you can play with a GUI. Replay by clicking on the result.

* `main.py training [n]` &nbsp;&nbsp;&nbsp;&nbsp; to train the AI by playing [n] games against itself

* `main.py results [n]` &nbsp;&nbsp;&nbsp;&nbsp; to see how well the AI performs in [n] games

The board layout corresponds to the numpad. For example, to place your symbol (X or O) in the center press 5, bottom left press 1, top left press 7, middle right press 6, etc.

## Important

At the moment there are **NO** user input checks.