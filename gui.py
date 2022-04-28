from tkinter import *
from functools import partial
import random
from PIL import Image, ImageTk
from bridge import deal_game
from bridge import bid_sequence
from game_objects import Deck, Hand
from score import Contract
import numpy as np
from treelib import Node, Tree

def resize_card(Card):
    img_w_path = 'images/cards/' + Card.get_image_name()
    our_card_img = Image.open(img_w_path)
    our_card_resize_image = our_card_img.resize((103,150))
    global our_card_image
    our_card_image = ImageTk.PhotoImage(our_card_resize_image)
    return our_card_image
   

def deal_sequence():
    # Shuffle and deal
    global players
    global current_player
    d = Deck(shuffle=True)
    players = {"North": Hand(), "East": Hand(), "South": Hand(), "West": Hand()}
    for i in range(0, 52, 4):
        players["North"].deal_card(d.draw_card())
        players["South"].deal_card(d.draw_card())
        players["West"].deal_card(d.draw_card())
        players["East"].deal_card(d.draw_card())
    show_cards(current_player)
    cur_player_label.config(text=current_player) 
    return players


        
def show_cards(current_player):
    Card1 = players[current_player].get_card(0)
    Card2 = players[current_player].get_card(1)
    Card3 = players[current_player].get_card(2)
    Card4 = players[current_player].get_card(3)
    Card5 = players[current_player].get_card(4)
    Card6 = players[current_player].get_card(5)
    Card7 = players[current_player].get_card(6)
    Card8 = players[current_player].get_card(7)
    Card9 = players[current_player].get_card(8)
    Card10 = players[current_player].get_card(9)
    Card11 = players[current_player].get_card(10)
    Card12 = players[current_player].get_card(11)
    Card13 = players[current_player].get_card(12)
    
    global card1_image
    global card2_image
    global card3_image
    global card4_image
    global card5_image
    global card6_image
    global card7_image
    global card8_image
    global card9_image
    global card10_image
    global card11_image
    global card12_image
    global card13_image
    
    card1_image = resize_card(Card1)
    card2_image = resize_card(Card2) 
    card3_image = resize_card(Card3)     
    card4_image = resize_card(Card4)    
    card5_image = resize_card(Card5)    
    card6_image = resize_card(Card6)    
    card7_image = resize_card(Card7)    
    card8_image = resize_card(Card8)    
    card9_image = resize_card(Card9)    
    card10_image = resize_card(Card10)    
    card11_image = resize_card(Card11)    
    card12_image = resize_card(Card12)    
    card13_image = resize_card(Card13)    
        

    card1_label.config(image=card1_image)
    card2_label.config(image=card2_image)
    card3_label.config(image=card3_image)
    card4_label.config(image=card4_image)
    card5_label.config(image=card5_image)
    card6_label.config(image=card6_image)
    card7_label.config(image=card7_image)
    card8_label.config(image=card8_image)
    card9_label.config(image=card9_image)
    card10_label.config(image=card10_image)
    card11_label.config(image=card11_image)
    card12_label.config(image=card12_image)
    card13_label.config(image=card13_image)    

    
    #CALCULATE LC/PC RATING
    card_array = np.arange(13)    
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
    LC_PC_str = "LC: " + str(LC) + " PC: " + str(PC)
    
    eval_label.config(text=LC_PC_str)
    hand_strength_label.config(text=Eval_index)
    player_name_label.config(text=current_player)
    

def eval_bid(contract):
    tree = Tree()
    tree.create_node("Possible", "Possible")
    tree.create_node("Pass", "Pass", "Possible")
    if Contract.get_multiplier(contract) < 4:
        tree.create_node("Double", "Double", "Possible")
    suits_names = ("Club (1)","Diamond (2)","Heart (3)","Spade (4)","No Trump (5)")
    possible_suits = (1,2,3,4,5)
    possible_nums = (1,2,3,4,5,6)
    for s in possible_suits:
        if s >= Contract.get_suit(contract):
            suit_name = suits_names[s-1]
            tree.create_node(suit_name, suit_name, parent="Possible")
            for num in possible_nums:
                if s == Contract.get_suit(contract):
                    if num > Contract.get_rank(contract):
                        tree.create_node(str(num), suit_name+str(num) , parent=suit_name)
                else:
                    tree.create_node(str(num), suit_name+str(num) , parent=suit_name)
    tree.show()
    
    
def get_bid():
    global pass_count
    global contract
    global winning_player
    global bid_leader
    global current_player
    
    action = e.get()
    e.delete(0, END)

    if action.lower() == "pass":
        pass_count += 1
    elif action.lower() == "double":
        pass_count = 0
        try:
            contract.double()
            bid_leader = current_player
        except:
            print("Cannot double. Try again...")

    else:
        pass_count = 0
        bid = [int(x.strip()) for x in action.split(",")]
        rank, suit = tuple(bid)
        try:
            if contract is None:
                contract = Contract(rank, suit)
                bid_leader = current_player
            else:
                contract.upgrade(rank, suit)
                bid_leader = current_player
        except:
            print("Invalid bid. Try again...")
            
    print("Player ",current_player," submitted bid of: ",action)        
    if pass_count == 3:
        winning_player = player_list[(player_list.index(current_player)+1) % len(player_list)]
        print("Contract finalized at rank: ",Contract.get_rank(contract),", suit: ",Contract.get_suit(contract), " won by ", winning_player)        
    current_player = player_list[(player_list.index(current_player)+1) % len(player_list)]
    cur_player_label.config(text=current_player) 
    print("Contract is currently rank: ",Contract.get_rank(contract),", suit: ",Contract.get_suit(contract), " led by ", bid_leader)    

#Instantiate players and current player
players = {"North": Hand(), "South": Hand(), "West": Hand(), "East": Hand()}
current_player = 'North'   
winning_player = None
bid_leader = None


root = Tk()
root.title('Card Deck')
root.geometry("1600x900")
root.configure(background="green")

my_frame = Frame(root, bg="green")
my_frame.grid(row=0, column=0, padx=4, ipadx=4)

#Create hand frame
hand_frame = LabelFrame(root, text="Player Hand")
hand_frame.grid(row=0, column=0, padx=4, ipadx=4)

#Create card image frames

card1_frame = LabelFrame(hand_frame, text="Card1", bd=0)
card1_frame.grid(row=0, column=0, padx=4, ipadx=4)
card1_label = Label(card1_frame, text='')
card1_label.pack(pady=20)

card2_frame = LabelFrame(hand_frame, text="Card2", bd=0)
card2_frame.grid(row=0, column=1, padx=4, ipadx=4)
card2_label = Label(card2_frame, text='')
card2_label.pack(pady=20)

card3_frame = LabelFrame(hand_frame, text="Card3", bd=0)
card3_frame.grid(row=0, column=2, padx=4, ipadx=4)
card3_label = Label(card3_frame, text='')
card3_label.pack(pady=20)

card4_frame = LabelFrame(hand_frame, text="Card4", bd=0)
card4_frame.grid(row=0, column=3, padx=4, ipadx=4)
card4_label = Label(card4_frame, text='')
card4_label.pack(pady=20)

card5_frame = LabelFrame(hand_frame, text="Card5", bd=0)
card5_frame.grid(row=0, column=4, padx=4, ipadx=4)
card5_label = Label(card5_frame, text='')
card5_label.pack(pady=20)

card6_frame = LabelFrame(hand_frame, text="Card6", bd=0)
card6_frame.grid(row=0, column=5, padx=4, ipadx=4)
card6_label = Label(card6_frame, text='')
card6_label.pack(pady=20)

card7_frame = LabelFrame(hand_frame, text="Card7", bd=0)
card7_frame.grid(row=0, column=6, padx=4, ipadx=4)
card7_label = Label(card7_frame, text='')
card7_label.pack(pady=20)

card8_frame = LabelFrame(hand_frame, text="Card8", bd=0)
card8_frame.grid(row=0, column=7, padx=4, ipadx=4)
card8_label = Label(card8_frame, text='')
card8_label.pack(pady=20)

card9_frame = LabelFrame(hand_frame, text="Card9", bd=0)
card9_frame.grid(row=0, column=8, padx=4, ipadx=4)
card9_label = Label(card9_frame, text='')
card9_label.pack(pady=20)

card10_frame = LabelFrame(hand_frame, text="Card10", bd=0)
card10_frame.grid(row=0, column=9, padx=4, ipadx=4)
card10_label = Label(card10_frame, text='')
card10_label.pack(pady=20)

card11_frame = LabelFrame(hand_frame, text="Card11", bd=0)
card11_frame.grid(row=0, column=10, padx=4, ipadx=4)
card11_label = Label(card11_frame, text='')
card11_label.pack(pady=20)

card12_frame = LabelFrame(hand_frame, text="Card12", bd=0)
card12_frame.grid(row=0, column=11, padx=4, ipadx=4)
card12_label = Label(card12_frame, text='')
card12_label.pack(pady=20)

card13_frame = LabelFrame(hand_frame, text="Card13", bd=0)
card13_frame.grid(row=0, column=12, padx=4, ipadx=4)
card13_label = Label(card13_frame, text='')
card13_label.pack(pady=20)

player_name_frame = LabelFrame(hand_frame, text="Player Name:")
player_name_frame.grid(row=1, column=5, padx=4, ipadx=4)
player_name_label = Label(player_name_frame, text='')
player_name_label.pack(pady=20)

eval_frame = LabelFrame(hand_frame, text="LC/PC Eval")
eval_frame.grid(row=1, column=6, padx=4, ipadx=4)
eval_label = Label(eval_frame, text='')
eval_label.pack(pady=20)

hand_strength_frame = LabelFrame(hand_frame, text="Hand Strength \n Index")
hand_strength_frame.grid(row=1, column=7, padx=4, ipadx=4)
hand_strength_label = Label(hand_strength_frame, text='')
hand_strength_label.pack(pady=20)

# contract_frame = LabelFrame(root, text="Contract,")
# contract_frame.pack



# create button frame
button_frame1 = LabelFrame(root, bd=0, bg="green")
button_frame1.grid(row=1, column=0, padx=4, ipadx=4)

button_frame2 = LabelFrame(root, bd=0, bg="green")
button_frame2.grid(row=2, column=0, padx=4, ipadx=4)

# create some buttons
deal_button = Button(button_frame1, text="Deal", font=("Helvetica", 14), command=deal_sequence)
deal_button.grid(row=0, column=0, pady=20)

show_north_button = Button(button_frame2, text="Show North", font=("Helvetica", 14), command=partial(show_cards,'North'))
show_north_button.grid(row=0, column=1, pady=20)

show_south_button = Button(button_frame2, text="Show South", font=("Helvetica", 14), command=partial(show_cards,'South'))
show_south_button.grid(row=0, column=2, pady=20)

show_east_button = Button(button_frame2, text="Show East", font=("Helvetica", 14), command=partial(show_cards,'East'))
show_east_button.grid(row=0, column=3, pady=20)

show_west_button = Button(button_frame2, text="Show West", font=("Helvetica", 14), command=partial(show_cards,'West'))
show_west_button.grid(row=0, column=4, pady=20)




#Bid Sequence Loop

params = {'rank': 1, 'suit': 1}
contract = Contract(**params)
pass_count = 0
player_list = list(players.keys())
   



button_frame3 = LabelFrame(root, bd=0, bg="green")
button_frame3.grid(row=4, column=0, padx=4, ipadx=4)

cur_player_frame = LabelFrame(button_frame3, text="Current Player")
cur_player_frame.grid(row=0, column=0)
cur_player_label = Label(cur_player_frame, text=current_player)
cur_player_label.pack()

eval_bid_button = Button(button_frame3, text="Show Possible Bids", font=("Helvetica", 14), command=partial(eval_bid,contract))
eval_bid_button.grid(row=0, column=1, pady=20)



button_frame4 = LabelFrame(root, bd=0, bg="green")
button_frame4.grid(row=5, column=0, padx=4, ipadx=4)

# Create bid entry frame
e = Entry(button_frame4, text = "Enter Bid:")
e.grid(row=0, column=0, padx=4, ipadx=4)

submit_bid_button = Button(button_frame4, text="Submit Bid", font=("Helvetica", 14), command=get_bid)
submit_bid_button.grid(row=0, column=2, pady=20)







root.mainloop()