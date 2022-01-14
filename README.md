# Tic-Tac-Toe

An implementation of the familiar game "Tic-Tac-Toe". You can play against another player or an Reinforcement Learning (RL) agent that was trained in 500000 games.

<https://en.wikipedia.org/wiki/Tic-tac-toe>

<https://en.wikipedia.org/wiki/Q-learning>

## Prerequisite

* Python v3.10.1
* Numpy v1.22.1
* Tqdm v4.62.3
* Typer v0.4.0
* Pygame v2.1.2

The packages above are required to play the game. All packages used are listed in the requirements.txt.

Install them with &nbsp;&nbsp;&nbsp;&nbsp; `pip install -r requirements.txt` 

## How to

From the game folder run:

* `main.py play pvp` &nbsp;&nbsp;&nbsp;&nbsp; to play another human player 

* `main.py play ai` &nbsp;&nbsp;&nbsp;&nbsp; to play an AI opponent

* `main.py training [n]` &nbsp;&nbsp;&nbsp;&nbsp; to train the AI by playing [n] games against itself