"""
Bridge game simulation execution module.
"""
from typing import Dict, Tuple, List
from random import seed, randint
from game_objects import Deck, Hand, CardsInTrick, Team, Trick
from score import Contract, ScoreBoard


def run_game() -> None:
    """ Run bridge game.
    """
    players = setup_game()
    # TODO make actual game object to track total state
    # Bid Sequence
    current_contract, bid_winner = bid_sequence(players)
    print("The winning bid is {} from player {}".format(str(current_contract), bid_winner))
    
    # setup scoreboard 
    testTeams = [Team("Contracting", ["North", "South"], True), Team("Defending", ["West", "East"], False)]
    
    scoreboard = ScoreBoard(current_contract, testTeams)
    
    # play hands until cards run out
    num_cards = 13
    trick_results = []
    while num_cards > 0:
        current_trick = play_trick(players, "North", num_cards)
        trick_results.append(current_trick)
        winning_card, winning_player = current_trick.get_winner(current_contract.get_suit())
        num_cards -= 1
        print(winning_player, "wins the trick with", winning_card)
    
        if winning_player is "North" or winning_player is "South":
            scoreboard.win_trick(testTeams[0], Trick(current_contract.get_suit()))
        else:
            scoreboard.win_trick(testTeams[1], Trick(current_contract.get_suit()))
    
    ns_wins, ew_wins = calculate_result(trick_results, current_contract.get_suit())
    print("North/South won {} tricks meeting the contract suit {} times.".format(ns_wins[0], ns_wins[1]))
    print("East/West won {} tricks meeting the contract suit {} times.".format(ew_wins[0], ew_wins[1]))

    scoreboard.score_at_end_of_round()
    
    print(scoreboard)

def setup_game() -> Dict[str, Hand]:
    """ Setup a bridge game by dealing cards.
    """
    d = Deck(shuffle=True)
    players = {"North": Hand(), "East": Hand(), "South": Hand(), "West": Hand()}
    for i in range(0, 52, 4):
        players["North"].deal_card(d.draw_card())
        players["South"].deal_card(d.draw_card())
        players["West"].deal_card(d.draw_card())
        players["East"].deal_card(d.draw_card())
    return players

def play_trick(players: Dict[str, Hand], starting_player: str="North", num_cards: int = 13) -> CardsInTrick:
    """ Plays a single trick using randomness.
    """
    trick = CardsInTrick()
    player_list = list(players.keys())
    current_player = player_list.index(starting_player)
    for i in range(4):
        player_name = player_list[current_player]
        card_index = randint(0, num_cards-1)
        card = players[player_name].play_card(card_index)
        print(card, player_name)
        trick.play_card(card, player_name)

        current_player = (current_player+1) % len(player_list)
    
    return trick

def calculate_result(trick_results: List[CardsInTrick], trump_suit: int):
    ns_wins = (0, 0)
    ew_wins = (0, 0)
    for trick in trick_results:
        winning_card, winning_player = trick.get_winner(trump_suit)
        if winning_player == "North" or winning_player == "South":
            if winning_card.get_suit() == trump_suit:
                ns_wins = (ns_wins[0] + 1, ns_wins[1] +1)
            else:
                ns_wins = (ns_wins[0] + 1, ns_wins[1])
        else:
            if winning_card.get_suit() == trump_suit:
                ew_wins = (ew_wins[0] + 1, ew_wins[1] +1)
            else:
                ew_wins = (ew_wins[0] + 1, ew_wins[1])
    return (ns_wins, ew_wins)


def bid_sequence(players: Dict[str, Hand]) -> Tuple[Contract, str]:
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
        
def test_scorecard():
    
    testContract = Contract(5, 5)         
    testTeams = [Team("Contracting", [], True), Team("Defending", [], False)]
    
    scoreboard = ScoreBoard(testContract, testTeams)
    
    scoreboard.win_trick(testTeams[0], Trick(5))
    scoreboard.win_trick(testTeams[0], Trick(5))
    scoreboard.win_trick(testTeams[0], Trick(5))
    
    scoreboard.score_at_end_of_round()
    
    print(scoreboard)

if __name__ == "__main__":

    run_game()
