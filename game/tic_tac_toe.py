import random, itertools, pickle, pygame
from tqdm import tqdm
import numpy as np

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
    
    def current_turn(self):
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
            rewards = (1, 0)
        elif done == 2:
            rewards = (0, 1)
        else:
            rewards = (0.5, 0.5)
            
        return rewards
    
    def show_results(self, result):
        print("")           
        if result == 0:
            print("#######################")    
            print("  !!! IT'S A DRAW !!!")
            print("#######################")
        else:             
            print("###########################")    
            print("  !!! PLAYER -{}- WINS !!!".format(result))
            print("###########################")
            
        self.b.show()
               
    def check_user_input(self, input):
        """ Check if the user inputs are feasible and convert numpad inputs to the state indices """
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
    
    def play_human(self, mode):
        """ Human plays against another human or an AI. Modes: pvp, random, q-learning """     
        actions = self.b.available_positions()
        state = self.b.get_state() 
        done = -1
        ai_turn = random.choice([1, 2])
        
        if mode == "pvp":
            ai = False
        elif mode == "random":
            ai = True
            ai1 = RandomPlayer()
            ai2 = RandomPlayer()
        elif mode == "q-learning":
            ai = True
            ai1 = QPlayer(0, 0, 0)
            ai1.load_table("p1")
            ai2 = QPlayer(0, 0, 0)
            ai2.load_table("p2")     
        
        while done == -1:
            turn = self.current_turn()
            print("") 
            print("### ROUND {}: Player -{}- ###".format(self.round, turn[1]))
            self.b.show()
            if ai and turn[0] == ai_turn:
                if turn[0] == 1:
                    action = ai1.select_action(actions, state, 0)
                else:
                    action = ai2.select_action(actions, state, 0)
                
                print("  Select position: AI -> {}".format(action))
            else: 
                action = int(input("  Select position: "))
                action = self.check_user_input(action)
            
            state, actions, done = self.step(action, turn[0])
            
        self.show_results(done)
        
    def play_gui(self):
        gui = GUI()
        
        player = 1
        
        while 1:
            gui.render(self, player)
        
    def play_ai(self, p1, p2, games, render=True):
        """ Two AIs play against each other for experiment purposes. """
        stats = []
              
        for g in tqdm(range(games), disable=not render):      
            actions = self.b.available_positions()
            state = self.b.get_state()
            done = -1
           
            while done == -1:
                turn = self.current_turn()            
                if turn[0] == 1:
                    action = p1.select_action(actions, state, 0)                  
                else: 
                    action = p2.select_action(actions, state, 0)
                
                state, actions, done = self.step(action, turn[0])                   

            stats.append(done)
            self.b = Board()
            self.round = 1

        return stats

    def train_ai(self, games, render=True):
        """ Two AIs play against each other to train them. """
        p1 = QPlayer(0.95, 0.2, [1.0, 0.01, 0.5])
        p1_epsilons = p1.decay_schedule(games)
        p2 = QPlayer(0.95, 0.2, [1.0, 0.01, 0.5])
        p2_epsilons = p2.decay_schedule(games)
        
        for g in tqdm(range(games), disable=not render):
            p1_history = []       
            p2_history = []       
            actions = self.b.available_positions()
            state = self.b.get_state()
            done = -1
           
            while done == -1:
                turn = self.current_turn()  
                if turn[0] == 1:
                    action = p1.select_action(actions, state, p1_epsilons[g])
                    p1_history.append([state[:], action])                    
                else: 
                    action = p2.select_action(actions, state, p2_epsilons[g])
                    p2_history.append([state[:], action]) 
                
                state, actions, done = self.step(action, turn[0])                   
            
            p1_reward = self.get_rewards(done)[0]
            p1.update_table(p1_history, p1_reward)
            p2_reward = self.get_rewards(done)[1]
            p2.update_table(p2_history, p2_reward)

            self.b = Board()
            self.round = 1
        
        p1.save_table("p1")
        p2.save_table("p2")
        
        return (p1, p2)
              
class RandomPlayer:
    """ A simple 'AI' that selects actions randomly. """
    def __init__(self):
        pass
        
    def select_action(self, actions, state, epsilon):        
        return random.choice(actions)

    def update_table(self, history, reward):
        pass
    
class QPlayer:
    """ A RL agent that utilizes Q-learning. """
    def __init__(self, discount=None, learning_rate=None, epsilon=None):
        self.table = self.create_table()
        self.discount = discount
        self.learning_rate = learning_rate        
        self.epsilon = epsilon
        
    def create_table(self):
        table = {}
        keys = list(itertools.product([0, 1, 2], repeat = 9))
        for k in keys:
            table[k] = [0 for x in range(9)]
            
        return table
            
    def load_table(self, filename):
        with open("{}.pickle".format(filename), "rb") as handle:
            self.table = pickle.load(handle)            
    
    def save_table(self, filename):
        with open("{}.pickle".format(filename), "wb") as handle:
            pickle.dump(self.table, handle)

    def update_table(self, history, reward):
        """ Sutton (2020) Reinforcement Learning, Chapter 6.5: Q-learning """
        history.reverse()
        
        for i, (state, action) in enumerate(history):
            if i == 0:
                self.table[tuple(state)][action] = reward
            else:
                future_index = i - 1
                future_state = history[future_index][0]
                future_max_q = self.find_max_q(future_state)[0]
                current_q = self.table[tuple(state)][action]
                new_q = (1 - self.learning_rate) * current_q + self.learning_rate * self.discount * future_max_q
                self.table[tuple(state)][action] = new_q

    def find_max_q(self, state):
        actions = self.table[tuple(state)]
        action = 0
        max_q = -10e10
        for i, q in enumerate(actions):
            if q > max_q and state[i] == 0:
                max_q = q
                action = i
            
        return (max_q, action)

    def select_action(self, actions, state, epsilon):          
        if random.random() < epsilon:
            return random.choice(actions)
        else:
            return self.find_max_q(state)[1] 
        
    def decay_schedule(self, max_steps, log_start=-2, log_base=10):
        """ Morales (2020) Grokking Deep Reinforcement Learning """
        decay_steps = int(max_steps * self.epsilon[2])
        rem_steps = max_steps - decay_steps
        values = np.logspace(log_start, 0, decay_steps, base=log_base, endpoint=True)[::-1]
        values = (values - values.min()) / (values.max() - values.min())
        values = (self.epsilon[0] - self.epsilon[1]) * values + self.epsilon[1]
        values = np.pad(values, (0, rem_steps), "edge")
    
        return values
    
class GUI:
    def __init__(self):
        # Initialize screen
        pygame.init()
        pygame.display.set_caption("Tic-Tac-Toe")
        self.screen = pygame.display.set_mode((300, 450))
        
        # Create symbols (X and O)
        self.p1 = pygame.image.load("img/x.png")
        self.p2 = pygame.image.load("img/o.png")
        
        # Set background image and icon
        self.bg_image = pygame.image.load("img/background.png")
        icon = pygame.image.load("img/icon.png")
        pygame.display.set_icon(icon)
        
        self.game_history = []
      
    def render(self, game, player):
        # Check events    
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN: 
                action = self.position_to_action(pygame.mouse.get_pos())
                if (action is not None) and ([player, action] not in self.game_history): 
                    self.game_history.append([player, action])
                    state, actions, done = game.step(action, player)
                    return (state, actions, done)
        
        # Update screen    
        self.screen.blit(self.bg_image, [0, 0])
        for player, action in self.game_history:
            coordinates = self.action_to_position(action)
            self.screen.blit(self.p1, coordinates)            
        pygame.display.flip() 
        
    def action_to_position(self, action):                
        if action == 0: return [0, 0]
        if action == 1: return [100, 0]
        if action == 2: return [200, 0]
        if action == 3: return [0, 100]
        if action == 4: return [100, 100]
        if action == 5: return [200, 100]
        if action == 6: return [0, 200]
        if action == 7: return [100, 200]
        if action == 8: return [200, 200]

    def position_to_action(self, pos):
        if pos[0] in range(0, 100)      and pos[1] in range(0, 100):    return 0    # top left
        if pos[0] in range(100, 200)    and pos[1] in range(0, 100):    return 1    # top center
        if pos[0] in range(200, 300)    and pos[1] in range(0, 100):    return 2    # top right
        if pos[0] in range(0, 100)      and pos[1] in range(100, 200):  return 3    # middle left
        if pos[0] in range(100, 200)    and pos[1] in range(100, 200):  return 4    # middle center
        if pos[0] in range(200, 300)    and pos[1] in range(100, 200):  return 5    # middle right
        if pos[0] in range(0, 100)      and pos[1] in range(200, 300):  return 6    # bottom left
        if pos[0] in range(100, 200)    and pos[1] in range(200, 300):  return 7    # bottom center
        if pos[0] in range(200, 300)    and pos[1] in range(200, 300):  return 8    # bottom right   