"""Minmax search
"""
from typing import Tuple, List
from treelib import Node, Tree

from game_objects import CardsInTrick, Hand, Deck

def build_trick_tree(current_played: CardsInTrick, dummy_position: int, dummy_hand: Hand, player_hand: Hand, played_cards: List[CardsInTrick]) -> Tree:
    """current_played gives the current game state and dummy_position is
    relative to the current player with a -1 value meaning already played.
    """
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

    print(len(unknown_cards.deck))
    trick_tree = Tree()
    # tag is rank_suit
    # identifier is index_level
    trick_tree.create_node("root", "root")

    for level in range(0, levels_past_root):
        print(trick_tree)
        all_nodes = trick_tree.nodes
        prev_level_nodes = []
        for node in all_nodes.keys():
            if trick_tree.depth(all_nodes[node]) == level:
                prev_level_nodes.append(node)

        count = 0
        if level == dummy_position:
            for node in prev_level_nodes:
                for card in dummy_hand.hand:
                    tag = str(card.get_rank()) + "_" + str(card.get_suit())
                    identifier = str(count) + "_" + str(level)
                    trick_tree.create_node(tag, identifier, parent=node)
                    count += 1
        else:
            for node in prev_level_nodes:
                for card in unknown_cards.deck:
                    tag = str(card.get_rank()) + "_" + str(card.get_suit())
                    identifier = str(count) + "_" + str(level)
                    trick_tree.create_node(tag, identifier, parent=node)
                    count += 1
    return trick_tree


def decide(tree: Tree):

    while True:
        leaves = tree.leaves()
        if tree.depth() == 1:
            for leaf in leaves:
                choice_payoff = leaf.data
                choice_id = leaf.identifier

                if leaf.data > choice_payoff:
                    choice_payoff = leaf.data
                    choice_id = leaf.identifier
            
            return choice_payoff, choice_id

        else:
            for leaf in leaves:
                siblings = tree.siblings(leaf.identifier)
                choice_payoff = leaf.data
                choice_id = leaf.identifier
                tree.get_node(tree.ancestor(leaf.identifier)).data = choice_payoff

                for child in siblings:
                    if child.data < choice_payoff:
                        choice_payoff = child.data
                        choice_id = child.identifier
                        tree.get_node(tree.ancestor(leaf.identifier)).data = choice_payoff
                    
                    tree.remove_node(child.identifier)
                    leaves.remove(child)

                tree.remove_node(leaf.identifier)

    return choice_payoff, choice_id

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