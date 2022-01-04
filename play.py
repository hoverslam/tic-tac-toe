from tic_tac_toe import Game

# [TODO] CLI to select game mode

def main():
    g = Game("Karen")
    g.play_game()
    print("")
    input("Press ENTER to exit.")
       
if __name__ == "__main__":
    main()