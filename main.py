from tic_tac_toe import Game, RandomPlayer, QPlayer
import typer

app = typer.Typer()

@app.command()
def training(games:int):
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

@app.command()
def results():
    g = Game()
    games = 100000
    
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
    
    print("### RandomPlayer vs. RandomPlayer ###")
    p1 = RandomPlayer()
    p2 = RandomPlayer()
    g.play_ai(p1, p2, games)
    
    input("Press any key to exit")

@app.command()    
def play(mode:str):
    g = Game()

    g.play_human(mode)
    input("Press any key to exit")  

if __name__ == "__main__":
    app()