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

    def get_image_name(self) -> str:
        image_name = 'not found'
        if self.suit == 1 and self.rank == 1:
        	image_name = '2_of_clubs.png'
        elif self.suit == 1 and self.rank == 2:
        	image_name = '3_of_clubs.png'
        elif self.suit == 1 and self.rank == 3:
        	image_name = '4_of_clubs.png'
        elif self.suit == 1 and self.rank == 4:
        	image_name = '5_of_clubs.png'
        elif self.suit == 1 and self.rank == 5:
        	image_name = '6_of_clubs.png'
        elif self.suit == 1 and self.rank == 6:
        	image_name = '7_of_clubs.png'
        elif self.suit == 1 and self.rank == 7:
        	image_name = '8_of_clubs.png'
        elif self.suit == 1 and self.rank == 8:
        	image_name = '9_of_clubs.png'
        elif self.suit == 1 and self.rank == 9:
        	image_name = '10_of_clubs.png'
        elif self.suit == 1 and self.rank == 10:
        	image_name = '11_of_clubs.png'
        elif self.suit == 1 and self.rank == 11:
        	image_name = '12_of_clubs.png'
        elif self.suit == 1 and self.rank == 12:
        	image_name = '13_of_clubs.png'
        elif self.suit == 1 and self.rank == 13:
        	image_name = '14_of_clubs.png'
        elif self.suit == 2 and self.rank == 1:
        	image_name = '2_of_diamonds.png'
        elif self.suit == 2 and self.rank == 2:
        	image_name = '3_of_diamonds.png'
        elif self.suit == 2 and self.rank == 3:
        	image_name = '4_of_diamonds.png'
        elif self.suit == 2 and self.rank == 4:
        	image_name = '5_of_diamonds.png'
        elif self.suit == 2 and self.rank == 5:
        	image_name = '6_of_diamonds.png'
        elif self.suit == 2 and self.rank == 6:
        	image_name = '7_of_diamonds.png'
        elif self.suit == 2 and self.rank == 7:
        	image_name = '8_of_diamonds.png'
        elif self.suit == 2 and self.rank == 8:
        	image_name = '9_of_diamonds.png'
        elif self.suit == 2 and self.rank == 9:
        	image_name = '10_of_diamonds.png'
        elif self.suit == 2 and self.rank == 10:
        	image_name = '11_of_diamonds.png'
        elif self.suit == 2 and self.rank == 11:
        	image_name = '12_of_diamonds.png'
        elif self.suit == 2 and self.rank == 12:
        	image_name = '13_of_diamonds.png'
        elif self.suit == 2 and self.rank == 13:
        	image_name = '14_of_diamonds.png'
        elif self.suit == 3 and self.rank == 1:
        	image_name = '2_of_hearts.png'
        elif self.suit == 3 and self.rank == 2:
        	image_name = '3_of_hearts.png'
        elif self.suit == 3 and self.rank == 3:
        	image_name = '4_of_hearts.png'
        elif self.suit == 3 and self.rank == 4:
        	image_name = '5_of_hearts.png'
        elif self.suit == 3 and self.rank == 5:
        	image_name = '6_of_hearts.png'
        elif self.suit == 3 and self.rank == 6:
        	image_name = '7_of_hearts.png'
        elif self.suit == 3 and self.rank == 7:
        	image_name = '8_of_hearts.png'
        elif self.suit == 3 and self.rank == 8:
        	image_name = '9_of_hearts.png'
        elif self.suit == 3 and self.rank == 9:
        	image_name = '10_of_hearts.png'
        elif self.suit == 3 and self.rank == 10:
        	image_name = '11_of_hearts.png'
        elif self.suit == 3 and self.rank == 11:
        	image_name = '12_of_hearts.png'
        elif self.suit == 3 and self.rank == 12:
        	image_name = '13_of_hearts.png'
        elif self.suit == 3 and self.rank == 13:
        	image_name = '14_of_hearts.png'
        elif self.suit == 4 and self.rank == 1:
        	image_name = '2_of_spades.png'
        elif self.suit == 4 and self.rank == 2:
        	image_name = '3_of_spades.png'
        elif self.suit == 4 and self.rank == 3:
        	image_name = '4_of_spades.png'
        elif self.suit == 4 and self.rank == 4:
        	image_name = '5_of_spades.png'
        elif self.suit == 4 and self.rank == 5:
        	image_name = '6_of_spades.png'
        elif self.suit == 4 and self.rank == 6:
        	image_name = '7_of_spades.png'
        elif self.suit == 4 and self.rank == 7:
        	image_name = '8_of_spades.png'
        elif self.suit == 4 and self.rank == 8:
        	image_name = '9_of_spades.png'
        elif self.suit == 4 and self.rank == 9:
        	image_name = '10_of_spades.png'
        elif self.suit == 4 and self.rank == 10:
        	image_name = '11_of_spades.png'
        elif self.suit == 4 and self.rank == 11:
        	image_name = '12_of_spades.png'
        elif self.suit == 4 and self.rank == 12:
        	image_name = '13_of_spades.png'
        elif self.suit == 4 and self.rank == 13:
        	image_name = '14_of_spades.png'

        return image_name


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

    def __init__(self, hand: List[Card] = None) -> None:
        """ Creates a hand with any number of cards.

        Parameters
        ----------
        hand: List[Card] = []
            Defaults to empty hand.
        """
        self.hand = hand
        if self.hand is None:
            self.hand = []

    def deal_card(self, card: Card):
        """ Deal card to hand.

        Parameters
        ----------
        card: Card
            Card to insert.
        """
        self.hand.append(card)

    def play_card(self, card_index: int) -> Card:
        """ Remove card from hand.

        Parameters
        ----------
        card_index: int
            Index of card in hand to play.
        """
        return self.hand.pop(card_index)

    def get_card(self, card_index: int) -> Card:
        """ Retrieve card at index.

        Parameters
        ----------
        card_index: int
            Index of card in hand.
        """
        return self.hand[card_index]

    def __str__(self) -> str:
        """ Overloaded string function

        Returns
        -------
        str
            Object output as string.
        """
        return str([str(card) for card in self.hand])

if __name__ == "__main__":
    d = Deck()
    for i in range(52):
        print(d.draw_card())
    print("Reset deck...")
    d.reset(True)
    for i in range(52):
        print(d.draw_card())
