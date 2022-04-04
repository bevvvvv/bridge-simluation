"""
Bridge game simulation execution module.
"""
from game_objects import Deck, Hand

def run_game():
    d = Deck(shuffle=True)
    players = {"North": Hand(), "South": Hand(), "West": Hand(), "East": Hand()}
    for i in range(0, 52, 4):
        players["North"].deal_card(d.draw_card())
        players["South"].deal_card(d.draw_card())
        players["West"].deal_card(d.draw_card())
        players["East"].deal_card(d.draw_card())
    # TODO make actual game object to track total state
    print(players)
    print(players["North"].get_card(0))
        

if __name__ == "__main__":
    run_game()
