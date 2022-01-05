from tic_tac_toe import Game, RandomPlayer, QPlayer

def main():
    g = Game()
    
    #p1 = QPlayer(0.5, 0.95, 0.1)
    #p2 = RandomPlayer()
    #g.train_ai(p1, p2, 1000000)

    g.play_human("q-learning")

if __name__ == "__main__":
    main()