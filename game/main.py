from tic_tac_toe import Game, Training
import typer

app = typer.Typer()

@app.command()
def training(games: int):
    print("### TRAINING ###")
    t = Training(0.95, 0.1, [1, 0.1, 0.5])
    t.start(games)
    t.save_agents("p1", "p2")
    print("Training DONE!")
    print("")
    
    print("### RESULTS: Outcomes from 10000 games as a percentage ###")
    results = t.results(10000) 
    for res in results:
        print(res[0])
        print("Player 1: {}".format(res[1].count(1) / 10000))
        print("Player 2: {}".format(res[1].count(2) / 10000))
        print("Draws:    {}".format(res[1].count(0) / 10000))
        print("")      
    
    input("Press any key to exit.")

@app.command()    
def play(mode: str):
    if mode == "pvp": ai = False
    elif mode == "ai": ai = True
    
    while 1:
        g = Game()
        g.play(ai)
      
if __name__ == "__main__":
    app()