"""
Bridge game simulation execution module.
"""
from game_objects import Deck, Hand
from score import Contract
import numpy as np

def deal_game():
    d = Deck(shuffle=True)
    players = {"North": Hand(), "South": Hand(), "West": Hand(), "East": Hand()}
    for i in range(0, 52, 4):
        players["North"].deal_card(d.draw_card())
        players["South"].deal_card(d.draw_card())
        players["West"].deal_card(d.draw_card())
        players["East"].deal_card(d.draw_card())
    return players

def bid_sequence(players):
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
