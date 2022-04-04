"""
Physical Game Object clases - Deck, Card, Hand
"""
from typing import List
import random

class Card:
    """
    Card that stores combination of rank and suit attributes.

    Attributes
    ----------
    rank: int
        Rank from 1 to 13 (2 to A)
    suit: int
        Suits coded as int -> (Clubs, Diamonds, Hearts, Spades)
    suit_list: Tuple
        ("Club", "Diamond", "Heart", "Spade")
    """

    def __init__(self, rank: int, suit: int) -> None:
        """ A card is a combination of rank and suit.

        Parameters
        ----------
        rank: int
            Rank from 1 to 13 (2 to A)
        suit: int
            Suits coded as int -> (Clubs, Diamonds, Hearts, Spades)
        """
        if rank not in range(1, 14) or suit not in range(1, 5):
            raise ValueError("Improper int received for suit or rank.")
        self.rank = rank
        self.suit = suit
        self.suit_list = ("Club", "Diamond", "Heart", "Spade")

    def get_rank(self) -> int:
        """ Returns rank of card.

        Returns
        -------
        rank: int
        """
        return self.rank

    def get_suit(self) -> int:
        """ Returns suit of card.

        Returns
        -------
        suit: int
            Suits coded as int -> (Clubs, Diamonds, Hearts, Spades)
        """
        return self.suit

    def get_suit_string(self) -> str:
        """ Returns suit of card as text.

        Returns
        -------
        suit: int
            Suits coded as int -> (Clubs, Diamonds, Hearts, Spades)
        """
        return self.suit_list[(self.suit-1)]
   
    def __str__(self) -> str:
        """ Overloaded string function

        Returns
        -------
        str
            Object output as string.
        """
        return "Rank: {}, Suit: {}".format(self.get_rank(), self.get_suit_string())

class Deck:
    """
    A deck of 52 different cards. Stores order state and allows shuffling.

    Attributes
    ----------
    deck: List[Card]
        A deck contains 52 or less cards.
    """

    def __init__(self, shuffle: bool = False) -> None:
        """ Creates a deck of 52 cards and shuffles it.

        Parameters
        ----------
        shuffle: bool = False
            Whether to shuffle deck on creation.
        """
        self.deck = []
        self.reset(shuffle)

    def draw_card(self) -> Card:
        """ Draws a card from the deck.

        Returns
        -------
        Card
            Card drawn from the deck.
        """
        return self.deck.pop(0)

    def shuffle_deck(self) -> None:
        """ Shuffle cards in the deck.
        """
        random.shuffle(self.deck)

    def reset(self, shuffle: bool = False) -> None:
        """ Insert cards into deck and shuffle if true.

        Parameters
        ----------
        shuffle: bool = False
            Whether to shuffle the deck.
        """ 
        for suit in range(1, 5):
            for rank in range(1, 14):
                self.deck.append(Card(rank, suit))

        if shuffle:
            self.shuffle_deck()

class Hand:
    """ Contains the cards in a single hand.

    Attributes
    ----------
    hand: List[Card]
        Similar to deck
    """

    def __init__(self, hand: List[Card] = []) -> None:
        self.hand = hand

    def play_card(self, card_index: int) -> Card:
        pass

    def get_hand(self) -> List[Card]:
        pass

if __name__ == "__main__":
    d = Deck()
    for i in range(52):
        print(d.draw_card())
    print("Reset deck...")
    d.reset(True)
    for i in range(52):
        print(d.draw_card())
