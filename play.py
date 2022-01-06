from tic_tac_toe import Game, RandomPlayer, QPlayer

def training(games=1000000):
    g = Game()
        
    print("### Training as Player 1 ###")
    p1 = QPlayer(0.8, 0.9, 0.1)
    p2 = RandomPlayer()
    g.train_ai(p1, p2, games, "p1", 1)
    print("")    
    
    print("### Training as Player 2 ###")
    p1 = RandomPlayer()
    p2 = QPlayer(0.8, 0.9, 0.1)
    g.train_ai(p1, p2, games, "p2", 2)
    print("")
    
    input("Press any key to exit")

def results(games=10000):
    g = Game()
    
    print("### QPlayer vs. RandomPlayer ###") 
    p1 = QPlayer(0, 0, 0)
    p1.load_table("p1")
    p2 = RandomPlayer()
    g.play_ai(p1, p2, games)

    print("### RandomPlayer vs. QPlayer ###")
    p1 = RandomPlayer()
    p2 = QPlayer(0, 0, 0)
    p2.load_table("p2")
    g.play_ai(p1, p2, games)

    print("### QPlayer vs. QPlayer ###")
    p1 = QPlayer(0, 0, 0)
    p1.load_table("p1")
    p2 = QPlayer(0, 0, 0)
    p2.load_table("p2")
    g.play_ai(p1, p2, games)
    
    input("Press any key to exit")
    
def play_game(mode):
    g = Game()

    g.play_human(mode)
    input("Press any key to exit")  

def main():
    #training()
    #results()
    play_game("q-learning")
    
    # INTERESTING FINDINGS #
    # - One must train the agent as player 1 and player 2, there is no one fits them all
    # - If the rewards (win, draw, loss) are 1, 0.5, 0 then in a QPlayer vs. QPlayer scenario there are inconsistent results. Sometimes always Player 1 or Player 2 wins and sometimes there are always draws. 
    #   If the rewards (win, draw, loss) are 1, 1, 0 then in a QPlayer vs. QPlayer game there are 100% draws

if __name__ == "__main__":
    main()