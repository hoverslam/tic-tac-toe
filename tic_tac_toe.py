import random
from colorama import init
from termcolor import colored

class Board:
    """ The board on which the game is played. """
    
    def __init__(self):
        self.state = [7, 8, 9, 4, 5, 6, 1, 2, 3]
        
    def available_postions(self):
        p = []
        for k, v in enumerate(self.state):
            if isinstance(v, int) : p.append(k)            
        return p
    
    def update_state(self, player, position):
        self.state[position] = player
        
    def colored_players(self):
        colors = self.state.copy()
        for k, v in enumerate(self.state):
            if v == "X" : colors[k] = "green"
            elif v == "O" : colors[k] = "red"
            else : colors[k] = "white"
            
        return colors            
    
    def show_board(self):
        colors = self.colored_players()
        print(colored(self.state[0], colors[0]) + " " + 
              colored(self.state[1], colors[1]) + " " + 
              colored(self.state[2], colors[2]) + "\n" + 
              colored(self.state[3], colors[3]) + " " + 
              colored(self.state[4], colors[4]) + " " + 
              colored(self.state[5], colors[5]) + "\n" + 
              colored(self.state[6], colors[6]) + " " + 
              colored(self.state[7], colors[7]) + " " + 
              colored(self.state[8], colors[8]))
    
class Game:
    """ The logic to play the game. """
    
    def __init__(self, players, render=True):
        self.b = Board()
        self.players = players
        self.render = render

    def check_winner(self):
        winner = False
        # check rows
        if self.b.state[0] == self.b.state[1] == self.b.state[2] and self.b.state[0] != "-":
            winner = self.b.state[0]
        elif self.b.state[3] == self.b.state[4] == self.b.state[5] and self.b.state[3] != "-":
            winner = self.b.state[3]
        elif self.b.state[6] == self.b.state[7] == self.b.state[8] and self.b.state[6] != "-":
            winner = self.b.state[6]
        # check columns
        elif self.b.state[0] == self.b.state[3] == self.b.state[6] and self.b.state[0] != "-":
            winner = self.b.state[0]
        elif self.b.state[1] == self.b.state[4] == self.b.state[7] and self.b.state[1] != "-":
            winner = self.b.state[1]
        elif self.b.state[2] == self.b.state[5] == self.b.state[8] and self.b.state[2] != "-":
            winner = self.b.state[2]
        # check diagonals
        elif self.b.state[0] == self.b.state[4] == self.b.state[8] and self.b.state[0] != "-":
            winner = self.b.state[0]
        elif self.b.state[2] == self.b.state[4] == self.b.state[6] and self.b.state[2] != "-":
            winner = self.b.state[2]
        # check for draw
        elif len(self.b.available_postions()) == 0:
            winner = "Draw"       
        
        return winner

    def karen_ai(self, positions):
        action = random.choice(positions) 
        return action
    
    def convert_input(self, input):
        action = None        
        if input == 7 : action = 0
        elif input == 8 : action = 1
        elif input == 9 : action = 2
        elif input == 4 : action = 3
        elif input == 5 : action = 4
        elif input == 6 : action = 5
        elif input == 1 : action = 6
        elif input == 2 : action = 7
        elif input == 3 : action = 8
        
        return action
            
    
    def play_round(self, player, action):
        self.b.update_state(player, action)
        actions = self.b.available_postions()
        state = self.b.state
        done = self.check_winner()
        
        return (state, actions, done) 

    def play_game(self):
        init()  # use colorama to make termcolor work on Windows too     
        actions = self.b.available_postions()        
        ai = random.choice(["X", "O"])
        current_player = "X" 
        done = False
        i = 1
        
        while done == False:
            print("### ROUND {}: Player '{}' ###".format(i, current_player))
            self.b.show_board() 
            if self.players == "Karen" and current_player == ai:
                action = self.karen_ai(actions)
            elif self.players == "God" and current_player == ai:
                pass
            elif self.players == "Training":
                action = self.karen_ai(actions)
            else:
                action = int(input("Select position: "))
                action = self.convert_input(action)
            
            state, actions, done = self.play_round(current_player, action)
            print("")      
            
            i = i + 1 
            if current_player == "X": 
                current_player = "O"
            else:
                current_player = "X" 
             
        self.b.show_board()
        print("")  
        
        if done == "Draw":
            print("###################")    
            print("!!! IT'S A DRAW !!!")
            print("###################")
        else:               
            print("############################")    
            print("!!! WINNER IS PLAYER '{}' !!!".format(done))
            print("############################")