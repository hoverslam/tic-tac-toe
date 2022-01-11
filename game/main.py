from tic_tac_toe import Game, RandomPlayer, QPlayer
import typer

app = typer.Typer()

@app.command()
def training(games:int):
    g = Game()
        
    print("### Training ###")
    g.train_ai(games)
    print("")     
    
    input("Press any key to exit")

@app.command()
def results(games:int):
    g = Game()
    
    # QPlayer vs. RandomPlayer
    print("### QPlayer vs. RandomPlayer ###") 
    p1 = QPlayer()
    p1.load_table("p1")
    p2 = RandomPlayer()
    res = g.play_ai(p1, p2, games)    
    print("Player 1: {}".format(res.count(1) / games))
    print("Player 2: {}".format(res.count(2) / games))
    print("Draws:    {}".format(res.count(0) / games))
    print("")

    # RandomPlayer vs. QPlayer
    print("### RandomPlayer vs. QPlayer ###")
    p1 = RandomPlayer()
    p2 = QPlayer()
    p2.load_table("p2")
    res = g.play_ai(p1, p2, games)    
    print("Player 1: {}".format(res.count(1) / games))
    print("Player 2: {}".format(res.count(2) / games))
    print("Draws:    {}".format(res.count(0) / games))
    print("")
    
    # QPlayer vs. QPlayer
    print("### QPlayer vs. QPlayer ###")
    p1 = QPlayer()
    p1.load_table("p1")
    p2 = QPlayer()
    p2.load_table("p2")
    res = g.play_ai(p1, p2, games)    
    print("Player 1: {}".format(res.count(1) / games))
    print("Player 2: {}".format(res.count(2) / games))
    print("Draws:    {}".format(res.count(0) / games))
    print("")
    
    # RandomPlayer vs. RandomPlayer (Baseline)
    print("### RandomPlayer vs. RandomPlayer ###")
    p1 = RandomPlayer()
    p2 = RandomPlayer()
    res = g.play_ai(p1, p2, games)    
    print("Player 1: {}".format(res.count(1) / games))
    print("Player 2: {}".format(res.count(2) / games))
    print("Draws:    {}".format(res.count(0) / games))
    print("")
    
    input("Press any key to exit")

@app.command()    
def play(mode:str):
    g = Game()

    g.play_human(mode)
    input("Press any key to exit")
      
if __name__ == "__main__":
    #app()
    g = Game()
    g.play_gui()