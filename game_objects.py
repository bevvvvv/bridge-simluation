"""
Physical Game Object clases - Deck, Card, Hand
"""
from typing import List, Tuple, Union
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
        if rank not in range(1, 14) or suit not in range(1, 6):
            raise ValueError("Improper int received for suit or rank.")
        self.rank = rank
        self.suit = suit
        self.suit_list = ("Club", "Diamond", "Heart", "Spade", "No Trump")

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
    
    def remove_card(self, card: Card) -> Union[Card, None]:
        """ Remove specificed card from deck if exists
        """
        rank = card.get_rank()
        suit = card.get_suit()
        for indx, card in enumerate(self.deck):
            if card.get_rank() == rank and card.get_suit() == suit:
                return self.deck.pop(indx)

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

class CardsInTrick:
    """ Represents a trick in play.
    """

    def __init__(self) -> None:
        self.cards_played = []
        self.suit = None

    def play_card(self, card: Card, player: str) -> None:
        """ Allow user to play card in suit
        """
        if self.suit is None:
            self.suit = card.get_suit()
        self.cards_played.append((card, player))

    def get_winner(self, trump_suit: int) -> Union[Tuple[Card, str], None]:
        """ If four cards have been played, the winning card and player is returned.
        """
        if len(self.cards_played) == 4:
            winner, winning_player = self.cards_played[0]
            for card, player in self.cards_played:
                higher = False
                if card.get_rank() > winner.get_rank():
                    higher = True
                if higher and card.get_suit() == winner.get_suit():
                    winner = card
                    winning_player = player
                elif not higher and card.get_suit() == trump_suit and winner.get_suit() != trump_suit:
                    winner = card
                    winning_player = player
            return winner, winning_player

class Trick:
    """
    Trick that stores details of a Trick.

    Attributes
    ----------
    suit: int
        Suits coded as int -> (Clubs, Diamonds, Hearts, Spades, NoTrump)
    suit_list: Tuple
        ("Club", "Diamond", "Heart", "Spade", "No Trump")
    """

    def __init__(self, suit: int) -> None:
        """ A trick that has a winning suit

        Parameters
        ----------
        suit: int
            Suits coded as int -> (Clubs, Diamonds, Hearts, Spades, NoTrump)
        """
 
        self.suit = suit
        self.suit_list = ("Club", "Diamond", "Heart", "Spade", "No Trump")

    def get_suit(self) -> int:
        """ Returns the winning suit.

        Returns
        -------
        suit: int
            Suits coded as int -> (Clubs, Diamonds, Hearts, Spades, NoTrump)
        """
        return self.suit

    def get_suit_string(self) -> str:
        """ Returns winning suit as text.

        Returns
        -------
        suit: int
            Suits coded as int -> (Clubs, Diamonds, Hearts, Spades, NoTrump)
        """
        return self.suit_list[(self.suit-1)]
   
    def __str__(self) -> str:
        """ Overloaded string function

        Returns
        -------
        str
            Object output as string.
        """
        return "Suit: {}".format(self.get_suit_string())

class Team:
    """
    Stores details of a team.

    Attributes
    ----------
    name: str
        can either be Contracting or Defending
    players: List[Player]
        contains 2 players
    vulnerable: bool
    """

    def __init__(self, name: str, players: List, vulnerable: bool = False) -> None:
        """ Creates a team with 2 players.

        Parameters
        ----------
        vulnerable: bool = False
            Whether thee team is vulnerable.
        """
        self.name = name
        self.players = players
        self.vulnerable = vulnerable


    def get_name(self) -> str:
        """ Returns the name of the team.

        Returns
        -------
        name: str
            name coded as str -> (Contracting, Defending)
        """
        return self.name
    
    def is_vulnerable(self) -> bool:
        """ Returns if the team is in vulnerable status
        
        Returns
        -------
        vulnerable: bool
        """
        return self.vulnerable