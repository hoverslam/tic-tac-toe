import random

class Board:
    """ The board on which the game is played. """
    
    def __init__(self):
        self.state = ["-", "-", "-", "-", "-", "-", "-", "-", "-"]
        
    def available_postions(self):
        p = []
        for index, key in enumerate(self.state):
            if key == "-" : p.append(index)            
        return p
    
    def update_state(self, player, position):
        self.state[position] = player
    
    def show_board(self):
        print("{} {} {}\n{} {} {}\n{} {} {}".format(
            self.state[0], self.state[1], self.state[2],
            self.state[3], self.state[4], self.state[5],
            self.state[6], self.state[7], self.state[8])) 
    
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
    
    def play_round(self, player, action):
        self.b.update_state(player, action)
        actions = self.b.available_postions()
        state = self.b.state
        done = self.check_winner()
        
        return (state, actions, done) 

    def play_game(self):      
        actions = self.b.available_postions()
        ai = random.choice(["X", "O"])
        current_player = "X"    
        done = False
        i = 1
        
        # [TODO] check user input
        
        while done == False:
            print("### ROUND {}: Player '{}' ###".format(i, current_player))
            if self.players == "Karen" and current_player == ai:
                action = self.karen_ai(actions)
            elif self.players == "God" and current_player == ai:
                pass
            elif self.players == "Training":
                action = self.karen_ai(actions)
            else:
                action = int(input("Select position: {} ".format(actions))) 
            
            state, actions, done = self.play_round(current_player, action)
            self.b.show_board()
            print("")      
            
            i = i + 1 
            if current_player == "X": 
                current_player = "O"
            else:
                current_player = "X" 
            
        if done == "Draw":
            print("###################")    
            print("!!! IT'S A DRAW !!!")
            print("###################")
        else:               
            print("############################")    
            print("!!! WINNER IS PLAYER '{}' !!!".format(done))
            print("############################")
     

    # [TODO] GUI -> pygame 

 