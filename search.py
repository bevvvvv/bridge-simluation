"""Minmax search
"""
from typing import Tuple, List
from copy import deepcopy
from treelib import Node, Tree

from game_objects import CardsInTrick, Hand, Deck, Card

def build_trick_tree(current_played: CardsInTrick, dummy_position: int, dummy_hand: Hand, player_hand: Hand, played_cards: List[CardsInTrick], trump_suit) -> Tree:
    """current_played gives the current game state and dummy_position is
    relative to the current player with a -1 value meaning already played.
    """
    print('Building search tree.')
    levels_past_root = 4 - len(current_played.cards_played)
    # dummy or not -> uknown depends on # of levels to expand -> dummy_position > -1; levels_past_root-1
    unknown_cards = Deck()
    for card in player_hand.hand: # we known what player has
        unknown_cards.remove_card(card)
    for card in dummy_hand.hand: # we know what dummy has
        unknown_cards.remove_card(card)
    for card, player in current_played.cards_played: # we know what has been played
        unknown_cards.remove_card(card)
    for trick in played_cards: # we have good memory
        for card, player in trick.cards_played:
            unknown_cards.remove_card(card)

    trick_tree = Tree()
    # tag is rank_suit
    # identifier is index_level
    trick_tree.create_node("root", "root")

    for level in range(0, levels_past_root):
        all_nodes = trick_tree.nodes
        prev_level_nodes = []
        for node in all_nodes.keys():
            if trick_tree.depth(all_nodes[node]) == level:
                prev_level_nodes.append(node)

        count = 0
        next_level_options = unknown_cards.deck
        unknown = True
        if level == dummy_position:
            next_level_options = dummy_hand.hand
            unknown = False
        elif level == 0:
            next_level_options = player_hand.hand
            unknown = False
        if not unknown and len(current_played.cards_played) > 0:
            # remove unplayable cards
            has_current = False
            for card in next_level_options:
                if card.get_suit() == current_played.cards_played[0][0].get_suit():
                    has_current = True
                    break
            if has_current:
                next_level_options = [c for c in next_level_options if c.get_suit() == current_played.cards_played[0][0].get_suit()]

        for node in prev_level_nodes:
            for card in next_level_options:
                tag = str(card.get_rank()) + "_" + str(card.get_suit())
                identifier = str(count) + "_" + str(level)
                trick_tree.create_node(tag, identifier, parent=node)

                if level == levels_past_root-1:
                    # calculate payoff
                    # compile trick
                    branch_trick = deepcopy(current_played)
                    player_name = 'other'
                    curr_node = trick_tree.get_node(identifier)
                    for branch_level in range(0, levels_past_root):
                        rank, suit = curr_node.tag.split('_')
                        if branch_level == levels_past_root-1:
                            # we traverse toward root, last palyed is root
                            player_name = 'player'
                        branch_trick.play_card(Card(int(rank), int(suit)), player_name)

                        if branch_level < levels_past_root-1:
                            curr_node = trick_tree.get_node(curr_node.predecessor(trick_tree.identifier))

                    # determine winner
                    card, winner = branch_trick.get_winner(trump_suit)
                    root_rank, root_suit = curr_node.tag.split('_')

                    # if winner non-root -> negative rank value OF root's card
                    payoff = -1 * int(root_rank)
                    if int(root_suit) == trump_suit:
                        payoff *= 2

                    # if winner root -> positive 1/rank
                    if winner == 'player':
                        payoff = 1 / card.get_rank()
                        if card.get_suit() == trump_suit:
                            payoff *= 2

                    trick_tree.remove_node(identifier)
                    trick_tree.create_node(tag, identifier, parent=node, data=payoff)

                count += 1
    return trick_tree


def decide(tree: Tree):
    print('Finding optimal play.')
    while True:
        leaves = tree.leaves()
        if tree.depth() == 1:
            for leaf in leaves:
                choice_payoff = leaf.data
                choice_tag = leaf.tag

                if leaf.data > choice_payoff:
                    choice_payoff = leaf.data
                    choice_tag = leaf.tag
            
            return choice_payoff, choice_tag

        else:
            for leaf in leaves:
                siblings = tree.siblings(leaf.identifier)
                choice_payoff = leaf.data
                choice_tag = leaf.tag
                tree.parent(leaf.identifier).data = choice_payoff

                for child in siblings:
                    if child.data < choice_payoff:
                        choice_payoff = child.data
                        choice_tag = child.identifier
                        tree.parent(leaf.identifier).data = choice_payoff
                    
                    tree.remove_node(child.identifier)
                    leaves.remove(child)

                tree.remove_node(leaf.identifier)

def create_tree() -> Tree:
    tree = Tree()
    # store trick state in data
    tree.create_node("Root", "root")
    tree.create_node("One", "one", parent="root")
    tree.create_node("Two", "two", parent="root")
    tree.create_node("Leaf One", "leaf_one", parent="one", data=1)
    tree.create_node("Leaf Two", "leaf_two", parent="one", data=-1)
    tree.create_node("Leaf Three", "leaf_three", parent="two", data=3)
    tree.create_node("Leaf Four", "leaf_four", parent="two", data=0)
    return tree

def create_tree_one() -> Tree:
    tree = Tree()
    # store trick state in data
    tree.create_node("Root", "root", data={})
    tree.create_node("One", "one", parent="root", data=1)
    tree.create_node("Two", "two", parent="root", data=-1)

    return tree

# https://github.com/caesar0301/treelib/blob/master/treelib/tree.py

if __name__ == "__main__":
    tree = create_tree()
    print(tree)
    decision = decide(tree)
    print(decision)