"""
Bridge game simulation execution module.
"""
from typing import Dict
from game_objects import Deck, Hand
from score import Contract

def run_game() -> None:
    """ Run bridge game.
    """
    players = setup_game()
    # TODO make actual game object to track total state
    #print(players["North"])


    # Bid Sequence
    current_contract, bid_winner = bid_sequence(players)
   
    print("The winning bid is {} from player {}".format(str(current_contract), bid_winner))

def setup_game() -> Dict[str, Hand]:
    """ Setup a bridge game by dealing cards.
    """
    d = Deck(shuffle=True)
    players = {"North": Hand(), "South": Hand(), "West": Hand(), "East": Hand()}
    for i in range(0, 52, 4):
        players["North"].deal_card(d.draw_card())
        players["South"].deal_card(d.draw_card())
        players["West"].deal_card(d.draw_card())
        players["East"].deal_card(d.draw_card())
    return players

def bid_sequence(players: Dict[str, Hand]):
    """ Run the bidding sequence.
    """
    contract = None
    pass_count = 0
    player_list = list(players.keys())
    current_player = player_list[0]
    while True:
        print("{}'s hand is...".format(current_player))
        print(players[current_player])
        action = input("What should {} bid?".format(current_player))
        # decision switch
        if action.lower() == "pass":
            pass_count += 1
        elif action.lower() == "double":
            pass_count = 0
            try:
                contract.double()
            except:
                print("Cannot double. Try again...")
                continue
        else:
            pass_count = 0
            bid = [int(x.strip()) for x in action.split(",")]
            rank, suit = tuple(bid)
            try:
                if contract is None:
                    contract = Contract(rank, suit)
                else:
                    contract.upgrade(rank, suit)
            except:
                print("Invalid bid. Try again...")
                continue
        if pass_count == 3:
            winning_player = player_list[(player_list.index(current_player)+1) % len(player_list)]
            break
        current_player = player_list[(player_list.index(current_player)+1) % len(player_list)]

    return contract, winning_player
        

if __name__ == "__main__":
    run_game()
