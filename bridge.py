"""
Bridge game simulation execution module.
"""
from game_objects import Deck, Hand
from score import Contract
import numpy as np
from typing import Dict, Tuple, List
from random import seed, randint
from game_objects import Deck, Hand, CardsInTrick, Team, Trick
from score import Contract, ScoreBoard


def run_game() -> None:
    """ Run bridge game.
    """
    ns_vuln = False
    ew_vuln = False
    ns_score = [0, 0] # game, match
    ew_score = [0, 0] # game, match

    while True:
        players = setup_game()

        # TODO make actual game object to track total state
        # Bid Sequence
        current_contract, bid_winner = bid_sequence(players)
        print("The winning bid is {} from player {}".format(str(current_contract), bid_winner))
        
        # setup scoreboard 
        ns_team_name = "Defending"
        ew_team_name = "Contracting"
        if bid_winner is "North" or bid_winner is "South":
            ns_team_name = "Contracting"
            ew_team_name = "Defending"
        testTeams = [Team(ns_team_name, ["North", "South"], ns_vuln), Team(ew_team_name, ["West", "East"], ew_vuln)]
        
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

        # check if game is over
        ns_score[0] += scoreboard.teamScoreMap[ns_team_name]
        ew_score[0] += scoreboard.teamScoreMap[ew_team_name]

        if ns_score[0] >= 100 or ew_score[0] >= 100:
            # tally score
            ns_score[1] += ns_score[0]
            ew_score[1] += ew_score[0]
            if ns_score[0] > ew_score[0]:
                print('NS Wins')
                if ns_vuln:
                    break
                else:
                    ns_vuln = True
            else:
                print('EW Wins')
                if ew_vuln:
                    break
                else:
                    ew_vuln = True
            ns_score[0] = 0
            ew_score[0] = 0
    print(ns_score[1])
    print(ew_score[1])

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
    card_array = np.arange(13)
    while True:
        print("{}'s hand is...".format(current_player))
        print(players[current_player])

        #CALCULATE LC/PC RATING
        PC = 0
        LC = 0
        PC_potential = 0
        Doubleton = 0
        Singleton = 0
        Min_suit_count = 0
        Suit_inventory = [0,0,0,0]
        Suit_max = [0,0,0,0]
        Suit_missing_inventory = [[1,1,1],[1,1,1],[1,1,1],[1,1,1]]
        for i in card_array:
            PC_potential = max(0,players[current_player].get_card(i).get_rank() - 9)
            cur_suit = players[current_player].get_card(i).get_suit()-1

            if PC_potential >= 2:
                A_K_Q_index = PC_potential - 2
                Suit_missing_inventory[cur_suit][A_K_Q_index] = 0

            Suit_max[cur_suit] = Suit_max[cur_suit] + 1
            PC = PC + PC_potential
            if Suit_inventory[cur_suit] == 0:
                Suit_inventory[cur_suit] = 1

        if min(Suit_inventory) == 0: 
            Min_suit_count = 3 #Void
        elif min(Suit_inventory) == 1: 
            Min_suit_count = 2 #Singleton
        elif min(Suit_inventory) == 2:
            Min_suit_count = 1 #Doubleton        

        for suit in np.arange(4):
            if Suit_max[suit] >= 4:
                LC = sum(Suit_missing_inventory[suit])
        PC = PC + Min_suit_count        
        if PC <= 3:
            pc_group = 0
        elif PC <= 6:
            pc_group = 1
        elif PC <= 9:
            pc_group = 2
        elif PC <= 12:
            pc_group = 3
        elif PC <= 15:
            pc_group = 4
        elif PC <= 18: 
            pc_group = 5
        elif PC <= 21:
            pc_group = 6
        elif PC <= 25:
            pc_group = 7
        LC_rev = LC + pc_group
        Eval_index = LC_rev - 11
        LC_PC = (LC,PC)
        print('LC / PC Rating: ', LC_PC)
        print('HAND STRENGTH INDEX: ', Eval_index)    
        #END PC/LC RATING
        
        pass_chance = randint(0, 2)
        double_chance = randint(0, 4)
        suit = randint(1, 6)
        rank = randint(1, 14)
        if contract is not None:
            if suit <= contract.get_suit() and rank <= contract.get_rank():
                pass_chance = 1
        # decision switch
        if pass_chance == 1:
            pass_count += 1
        elif double_chance == 1:
            pass_count = 0
            try:
                contract.double()
            except:
                print("Cannot double. Try again...")
                continue
        else:
            pass_count = 0
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
