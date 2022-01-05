import random

class Board:
    def __init__(self):
        self.state = [0 for x in range(9)]
        
    def get_state(self):
        return self.state
    
    def update_state(self, action, player):        
        self.state[action] = player
        
    def available_positions(self):
        """ Return the actions a player can take. """
        p = []
        for i, s in enumerate(self.state):
            if s == 0: 
                p.append(i)            
        return p
    
    def convert_to_symbols(self, state):
        symbols = state.copy()
        for i, s in enumerate(symbols):
            if s == 0:
                symbols[i] = "-"
            elif s == 1:
                symbols[i] = "X"
            elif s == 2:
                symbols[i] = "O"
        return symbols
    
    def show(self):
        """ Displays the board with the known tic-tac-toe symbols in the console. """
        symbols = self.convert_to_symbols(self.state)
        print("\n")
        print("       |     |")
        print("    {}  |  {}  |  {}".format(symbols[0], symbols[1], symbols[2]))
        print("  _____|_____|_____")    
        print("       |     |")
        print("    {}  |  {}  |  {}".format(symbols[3], symbols[4], symbols[5]))
        print("  _____|_____|_____")    
        print("       |     |")    
        print("    {}  |  {}  |  {}".format(symbols[6], symbols[7], symbols[8]))
        print("       |     |")
        print("\n")
        
class Game:
    def __init__(self):
        self.b = Board()
        self.round = 1
        
    def step(self, action, player):
        """ Update the board with the action taken by a player and return the new state, 
        the available actions for the next player and the outcome of the move. """
        self.b.update_state(action, player)
        self.round = self.round + 1
        state = self.b.get_state()
        actions = self.b.available_positions()
        done = self.state_outcome(state)     
        
        return (state, actions, done)
    
    def current_player(self):
        """ Player 1 moves on uneven rounds and player 2 on even. """
        if self.round % 2 == 0:
            return (2, "O", "red")
        else:
            return (1, "X", "green")
        
    def state_outcome(self, state):
        """ Determines the outcome of the given board layout: 
        -1 = not finished, 0 = draw, 1 = player 1 wins, 2 = player 2 wins """
        result = -1
        # Check rows
        if state[0] == state[1] == state[2] and state[0] != 0:
            result = state[0]
        elif state[3] == state[4] == state[5] and state[3] != 0:
            result = state[3]
        elif state[6] == state[7] == state[8] and state[6] != 0:
            result = state[6]
        # Check columns
        elif state[0] == state[3] == state[6] and state[0] != 0:
            result = state[0]
        elif state[1] == state[4] == state[7] and state[1] != 0:
            result = state[1]
        elif state[2] == state[5] == state[8] and state[2] != 0:
            result = state[2]
        # Check diagonals
        elif state[0] == state[4] == state[8] and state[0] != 0:
            result = state[0]
        elif state[2] == state[4] == state[6] and state[2] != 0:
            result = state[2]
        # Check for draw
        elif len(self.b.available_positions()) == 0:
            result = 0

        return result
    
    def get_rewards(self, done):
        """ Returns the rewards for both players. """
        if done == 1:
            rewards = (1, -1)
        elif done == 2:
            rewards = (-1, 1)
        else:
            rewards = (0, 0)
            
        return rewards
    
    def show_results(self, result):
        print("")           
        if result == 0:
            print(" #######################")    
            print("   !!! IT'S A DRAW !!!")
            print(" #######################")
        else:             
            print(" ###########################")    
            print("   !!! PLAYER -{}- WINS !!!".format(result))
            print(" ###########################")
            
        self.b.show()
               
    def check_user_input(self, input):
        """ Checks if the user inputs are feasible and converts numpad inputs to the state indices """
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
    
    def play_human(self):
        """ Play a game against another human player. """     
        actions = self.b.available_positions() 
        done = -1
        
        while done == -1:
            player = self.current_player()
            print("") 
            print(" ### ROUND {}: Player -{}- ###".format(self.round, player[1]))
            self.b.show() 
            action = int(input("  Select position: "))
            action = self.check_user_input(action)
            
            state, actions, done = self.step(action, player[0])
            
        self.show_results(done)
        
    def play_ai(self):
        """ Play a game against an AI player. The beginner is selected randomly. """     
        actions = self.b.available_positions() 
        done = -1
        ai = Karen()
        ai_player = random.choice([1, 2])
        
        while done == -1:
            player = self.current_player()            
            print("") 
            print(" ### ROUND {}: Player -{}- ###".format(self.round, player[1]))
            self.b.show()
            if player[0] == ai_player:
                action = ai.select_action(actions)
                print("  Select position: '{}' selects an action randomly.".format(ai.get_name()))
            else: 
                action = int(input("  Select position: "))
                action = self.check_user_input(action)
            
            state, actions, done = self.step(action, player[0])
            
        self.show_results(done)
        
    def play_training(self, p1, p2, games):
        """ Let two AI players play against each other to train them. """        
        stats = [] 
        
        for g in range(games):    
            actions = self.b.available_positions()
            done = -1 

            print("Game: {}/{}".format(g+1, games))            
            while done == -1:
                player = self.current_player()            
                if player[0] == 1:
                    action = p1.select_action(actions)                    
                else: 
                    action = p2.select_action(actions)
                
                state, actions, done = self.step(action, player[0])
               
            stats.append(done)  
            self.b = Board()
            self.round = 1
        
        p1_wins = stats.count(1)
        p2_wins = stats.count(2)
        draws = stats.count(0)
        
        print("")   
        print("Player 1: {}".format(p1_wins/len(stats)))
        print("Player 2: {}".format(p2_wins/len(stats)))
        print("Draws: {}".format(draws/len(stats)))
        print("") 
              
class Karen:
    """ A simple 'AI' that selects actions randomly. """
    def __init__(self):
        self.name = "Karen"
        
    def select_action(self, actions):        
        return random.choice(actions)
    
    def get_name(self):
        return self.name