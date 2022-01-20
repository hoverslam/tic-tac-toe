import random, itertools, pickle, sys, pygame
from tqdm import tqdm
import numpy as np

class Board:
    """ The 'Tic-Tac-Toe' game board with a size of 3x3.  """
    def __init__(self):
        self.state = np.zeros(9, dtype=int)
        
    def update_state(self, player, action):
        """ Update the state with a given player-action pair. """       
        self.state[action] = player
        
    def available_positions(self):
        """ Return the positions a player can take. """
        positions = []
        for i, s in enumerate(self.state):
            if s == 0: 
                positions.append(i)            
        return positions
    
    def player_to_symbol(self, player):
        """ Convert the player to the known 'tic-tac-toe' symbol. """
        if player == 1: 
            return "X"
        elif player == 0:
            return "O"

    def show(self):
        """ Print the board in the console. """
        print("--------------------------------------------")
        for row in self.state.reshape((3, 3)):            
            print(" {}".format(row))
        print("")
        print(" Select action: {}".format(self.available_positions()))            
        print("--------------------------------------------")
 
       
class Game:
    def __init__(self):
        pass
        
    def reset(self):
        """ Reset the environment to start a new game. """
        self.b = Board()
        self.round = 1
          
        return (self.b.state, (0, 0), False)    # state, reward and done
    
    def current_player(self):
        """ Player 1 moves on uneven rounds and player 2 on even. """
        if self.round % 2 == 0:
            return 2
        else:
            return 1
        
    def state_space(self):
        """ Return all possible states in the game. """
        return list(itertools.product([0, 1, 2], repeat = 9))
    
    def action_space(self):
        """ Return all actions a player can make. """
        return np.arange(9)
    
    def actions(self):
        return self.b.available_positions()
        
    def check_outcome(self, state):
        """ Determine the outcome of a given board layout: 
            -1 = not finished, 0 = draw, 1 = player 1 wins, 2 = player 2 wins """        
        outcome = -1
        # Check rows
        if state[0] == state[1] == state[2] and state[0] != 0:
            outcome = state[0]
        elif state[3] == state[4] == state[5] and state[3] != 0:
            outcome = state[3]
        elif state[6] == state[7] == state[8] and state[6] != 0:
            outcome = state[6]
        # Check columns
        elif state[0] == state[3] == state[6] and state[0] != 0:
            outcome = state[0]
        elif state[1] == state[4] == state[7] and state[1] != 0:
            outcome = state[1]
        elif state[2] == state[5] == state[8] and state[2] != 0:
            outcome = state[2]
        # Check diagonals
        elif state[0] == state[4] == state[8] and state[0] != 0:
            outcome = state[0]
        elif state[2] == state[4] == state[6] and state[2] != 0:
            outcome = state[2]
        # Check for draw
        elif len(self.b.available_positions()) == 0:
            outcome = 0

        return outcome

    def give_rewards(self, outcome):
        """ Return the rewards for both players. """
        if outcome == 1:
            rewards = (1.0, 0.0)
        elif outcome == 2:
            rewards = (0.0, 1.0)
        elif outcome == 0: 
            rewards = (0.5, 0.5)
        else:
            rewards = (0.0, 0.0)
            
        return rewards
    
    def get_winner(self, reward):
        """ Return winner from reward 
            0 = draw, 1 = win player 1, 2 = win player 2 """        
        if reward[0] == 1:
            return 1
        elif reward[1] == 1:
            return 2
        else:
            return 0

    def step(self, action):
        """ Given an action update the game and return the new state, the rewards and
            the outcome of the current board layout. """
        player = self.current_player()
        self.b.update_state(player, action)
        self.round += 1
        state = self.b.state
        result = self.check_outcome(state)
        reward = self.give_rewards(result)
        if result == -1: 
            done = False
        else:
            done = True
            
        return (state, reward, done)
    
    def play(self, ai):
        """ Play a game against another human player or an AI player. """
        gui = GUI()
        state, reward, done = self.reset() 

        ai_turn = 0
        if ai == True:
            ai1 = QPlayer()
            ai1.load_table("p1")
            ai2 = QPlayer()
            ai2.load_table("p2")
            ai_turn = random.choice([1, 2])

        while not done:
            if (ai_turn == self.current_player()) and (ai_turn == 1):
                action = ai1.select_action(state, self.actions(), 0)
                state, reward, done = self.step(action)                
            elif(ai_turn == self.current_player()) and (ai_turn == 2):
                action = ai2.select_action(state, self.actions(), 0)
                state, reward, done = self.step(action)
            else:
                action = gui.render(state, self.actions())
                if action is not None:
                    state, reward, done = self.step(action)
    
        winner = self.get_winner(reward)        
        replay = False
        while not replay: 
            replay = gui.show_results(state, winner)

     
class QPlayer:
    """ A RL agent that utilizes Q-learning. """
    def __init__(self):
        self.table = None
        
    def create_table(self, state_space, action_space):
        """ Initialize the Q-table with zeros """
        table = {}
        for state in state_space:
            table[tuple(state)] = [0.0 for x in range(len(action_space))]            
        self.table = table
            
    def load_table(self, name):
        """ Load the Q-table from .pickle """
        with open("{}.pickle".format(name), "rb") as handle:
            self.table = pickle.load(handle)            
    
    def save_table(self, name):
        """ Save the Q-table to .pickle """
        with open("{}.pickle".format(name), "wb") as handle:
            pickle.dump(self.table, handle)

    def update_table(self, history, reward, alpha, discount):
        """ Sutton (2020) Reinforcement Learning, Chapter 6.5: Q-learning """
        """ https://en.wikipedia.org/wiki/Q-learning """
        for i in range(len(history)):
            old_state, action = history[i]
            if i == len(history)-1:
                # The last state has no future q-value
                old_q = self.table[tuple(old_state)][action]        
                new_q = (1 - alpha) * old_q + alpha * reward
            else:
                # All other states discount future q-values, but get no rewards
                new_state, _ = history[i+1] 
                old_q = self.table[tuple(old_state)][action]        
                future_max_q = self.maxQ(new_state)[0]
                new_q = (1 - alpha) * old_q + alpha * discount * future_max_q
             
            self.table[tuple(old_state)][action] = new_q

    def maxQ(self, state):
        """ Return the maximum q-value and its action from a given state """
        actions = self.table[tuple(state)]
        action = 0
        max_q = -10e10
        for i, q in enumerate(actions):
            if q > max_q and state[i] == 0:
                max_q = q
                action = i
            
        return (max_q, action)

    def select_action(self, state, actions, epsilon):
        """ Select action with an epsilon-greedy policy """          
        if random.random() < epsilon:
            return random.choice(actions)
        else:
            return self.maxQ(state)[1]
        

class Training:
    """ Train two agents by playing against each other. """
    def __init__(self, discount, learning_rate, epsilon):
        self.discount = discount
        self.learning_rate = learning_rate
        self.epsilon = epsilon
        
        self.p1 = QPlayer()
        self.p1.create_table(Game().state_space(), Game().action_space())
        self.p2 = QPlayer()
        self.p2.create_table(Game().state_space(), Game().action_space())
        
    def decay_schedule(self, init_value, min_value, decay_ratio, max_steps, log_start=-2, log_base=10):
        """ Compute decaying values as an inverse log curve. """ 
        """ see: Morales (2020) Deep Reinforcement Learning """
        decay_steps = int(max_steps * decay_ratio)
        rem_steps = max_steps - decay_steps
        values = np.logspace(log_start, 0, decay_steps, base=log_base, endpoint=True)[::-1]
        values = (values - values.min()) / (values.max() - values.min())
        values = (init_value - min_value) * values + min_value
        values = np.pad(values, (0, rem_steps), "edge")
    
        return values    
        
    def start(self, episodes, render=True, history=False):
        """ Start the training. """
        epsilons = self.decay_schedule(self.epsilon[0], self.epsilon[1], self.epsilon[2], episodes)

        g = Game()
        state, reward, done = g.reset()
        
        state_history = []
        
        for episode in tqdm(range(episodes), disable=(not render)):  
            p1_history = []
            p2_history = []
            
            while not done:
                if g.current_player() == 1:
                    action = self.p1.select_action(state, g.actions(), epsilons[episode])
                    p1_history.append([np.copy(state), action])
                else:
                    action = self.p2.select_action(state, g.actions(), epsilons[episode])
                    p2_history.append([np.copy(state), action])

                state, reward, done = g.step(action)
            
            # Update Q-table
            self.p1.update_table(p1_history, reward[0], self.learning_rate, self.discount)            
            self.p2.update_table(p2_history, reward[1], self.learning_rate, self.discount)            
            state, reward, done = g.reset()
            
            # Save history for a selected state
            if history != False:
                state_p1 = self.p1.table[tuple(history)].copy()
                state_p2 = self.p2.table[tuple(history)].copy()
                state_history.append([episode+1, state_p1, state_p2])
                
        if history != False: 
            return state_history
        
    def results(self, games, render=True):
        """ Measure performance by playing against different types of opponents. """
        g = Game()
        state, reward, done = g.reset()
        results = []                    
        setup = [
            [0, 0, "Q-Player vs. Q-Player"],
            [0, 1, "Q-Player vs. Random"],
            [1, 0, "Random vs. Q-Player"]
        ]
        
        for s in setup:
            stats = []                     
            for game in tqdm(range(games), disable=(not render)):
                while not done:
                    if g.current_player() == 1:
                        action = self.p1.select_action(state, g.actions(), s[0])
                    else:
                        action = self.p2.select_action(state, g.actions(), s[1])
                    
                    state, reward, done = g.step(action)
                
                if reward[0] == 1:
                    stats.append(1)     # Player 1 won
                elif reward[1] == 1:
                    stats.append(2)     # Player 2 won
                else:
                    stats.append(0)     # Draw
                state, reward, done = g.reset()
            
            results.append((s[2], stats))
            
        return results

    def get_agents(self):
        """ Return both agents to use them right away. """
        return (self.p1, self.p2)
    
    def save_agents(self, p1_name, p2_name):
        """ Save the Q-table of both agents. """
        self.p1.save_table(p1_name)
        self.p2.save_table(p2_name)

        
class GUI:
    def __init__(self):
        # Initialize screen
        pygame.init()
        pygame.display.set_caption("Tic-Tac-Toe")
        self.screen = pygame.display.set_mode((300, 400))
        
        # Create symbols (X and O)
        self.p1 = pygame.image.load("img/x.png")
        self.p2 = pygame.image.load("img/o.png")
        
        # Set background image and icon
        self.bg_image = pygame.image.load("img/background.png")
        icon = pygame.image.load("img/icon.png")
        pygame.display.set_icon(icon)
      
    def render(self, state, actions):
        # Check events    
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN: 
                action = self.position_to_action(pygame.mouse.get_pos())
                if (action is not None) and (action in actions):
                    return action
        
        # Update screen    
        self.screen.blit(self.bg_image, [0, 0])
        for i, player in enumerate(state):
            coordinates = self.index_to_position(i)
            if player == 1:
                self.screen.blit(self.p1, coordinates)
            elif player == 2:
                self.screen.blit(self.p2, coordinates)            
        pygame.display.flip()
        
    def show_results(self, state, done):
        # Check events 
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if pos[1] > 300: return True    # Replay button
                
        # Screen after final move    
        self.screen.blit(self.bg_image, [0, 0])
        for i, player in enumerate(state):
            coordinates = self.index_to_position(i)
            if player == 1:
                self.screen.blit(self.p1, coordinates)
            elif player == 2:
                self.screen.blit(self.p2, coordinates)
                
        # Show outcome
        if done == 1:
            result = pygame.image.load("img/win1.png")   
        elif done == 2:
            result = pygame.image.load("img/win2.png")
        else:
            result = pygame.image.load("img/draw.png")
        self.screen.blit(result, [0, 303])        
        pygame.display.flip()
        
        return False # maintain loop
     
    def index_to_position(self, index):                
        if index == 0: return [0, 0]
        if index == 1: return [100, 0]
        if index == 2: return [200, 0]
        if index == 3: return [0, 100]
        if index == 4: return [100, 100]
        if index == 5: return [200, 100]
        if index == 6: return [0, 200]
        if index == 7: return [100, 200]
        if index == 8: return [200, 200]

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