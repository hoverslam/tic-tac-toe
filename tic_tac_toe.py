import random
from colorama import init
from termcolor import colored

class Board:
    """ The board on which the game is played. """
    
    def __init__(self):
        self.state = ["-", "-", "-", "-", "-", "-", "-", "-", "-"]
        
    def available_postions(self):
        p = []
        for k, v in enumerate(self.state):
            if v == "-": 
                p.append(k)            
        return p
    
    def update(self, action, player):        
        self.state[action] = player
        
    def colored_players(self):
        colors = self.state.copy()
        for k, v in enumerate(self.state):
            if v == "X": 
                colors[k] = "green"
            elif v == "O": 
                colors[k] = "red"
            else: 
                colors[k] = "white"
            
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
    
    def __init__(self):
        self.b = Board()
        self.round = 0
        init()  # use colorama to make termcolor work on Windows too

    def winner(self):
        results = False
        # Check for draw
        if len(self.b.available_postions()) == 0:
            results = "Draw"
        # Check rows
        elif self.b.state[0] == self.b.state[1] == self.b.state[2] and self.b.state[0] != "-":
            results = self.b.state[0]
        elif self.b.state[3] == self.b.state[4] == self.b.state[5] and self.b.state[3] != "-":
            results = self.b.state[3]
        elif self.b.state[6] == self.b.state[7] == self.b.state[8] and self.b.state[6] != "-":
            results = self.b.state[6]
        # Check columns
        elif self.b.state[0] == self.b.state[3] == self.b.state[6] and self.b.state[0] != "-":
            results = self.b.state[0]
        elif self.b.state[1] == self.b.state[4] == self.b.state[7] and self.b.state[1] != "-":
            results = self.b.state[1]
        elif self.b.state[2] == self.b.state[5] == self.b.state[8] and self.b.state[2] != "-":
            results = self.b.state[2]
        # Check diagonals
        elif self.b.state[0] == self.b.state[4] == self.b.state[8] and self.b.state[0] != "-":
            results = self.b.state[0]
        elif self.b.state[2] == self.b.state[4] == self.b.state[6] and self.b.state[2] != "-":
            results = self.b.state[2]

        return results
    
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
    
    def step(self, action, player):
        self.b.update(action, player)
        self.round = self.round + 1
        actions = self.b.available_postions()
        state = self.b.state
        done = self.winner()
        
        return (state, actions, done)
    
    def current_player(self):
        if self.round % 2 == 0:
            return ("X", "green")
        else:
            return ("O", "red") 

    def play_human(self):     
        actions = self.b.available_postions() 
        done = False
        
        while done == False:
            player = self.current_player()
            print("") 
            print("### ROUND {}: Player '{}' ###".format(self.round, colored(player[0], player[1])))
            self.b.show_board() 
            action = int(input("Select position: "))
            action = self.convert_input(action)
            
            state, actions, done = self.step(action, player[0])
            
        self.show_results(done)

    def play_ai(self, mode):
        actions = self.b.available_postions() 
        done = False
        ai = random.choice(["X", "O"])
        
        while done == False:
            player = self.current_player()
            print("") 
            print("### ROUND {}: Player '{}' ###".format(self.round, colored(player[0], player[1])))
            self.b.show_board() 
            if ai == player[0] and mode == "Karen":
                action = random.choice(actions)
            elif ai == player[0] and mode == "God":
                pass
            else: 
                action = int(input("Select position: "))
                action = self.convert_input(action)
            
            state, actions, done = self.step(action, player[0])
            
        self.show_results(done)
    
    def training(self):
        pass

    def show_results(self, result):
        print("")           
        if result == "Draw":
            print("###################")    
            print("!!! IT'S A DRAW !!!")
            print("###################")
        else:               
            print("############################")    
            print("!!! WINNER IS PLAYER '{}' !!!".format(result))
            print("############################")
            
        print("")   
        self.b.show_board()        