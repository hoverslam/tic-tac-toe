from tic_tac_toe import Game, Karen

def main():
    g = Game()
    p1 = Karen()
    p2 = Karen()
    g.train_ai(p1, p2, 100000)


if __name__ == "__main__":
    main()