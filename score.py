"""
Score Related Objects and Methods
"""
from game_objects import Card

class Contract(Card):
    """ Represents a contract one can bid on.
    """

    def __init__(self, rank: int = 1, suit: int=1) -> None:
        super(Contract, self).__init__(rank, suit)

        if rank not in range(1, 14):
            raise ValueError("Improper int received for rank.")

        if suit not in range(1, 6):
            raise ValueError("Improper int received for suit.")

        self.multiplier = 1
        self.suit_list = ("Club", "Diamond", "Heart", "Spade", "No Trump")
        # return rank, suit

    def double(self) -> None:
        if self.multiplier < 4:
            self.multiplier *= 2
        else:
            raise RuntimeError("Cannot double after re-doubling.")

    def upgrade(self, rank: int, suit: int) -> None:
        if rank not in range(1, 14) or suit not in range(1, 6):
            raise ValueError("Improper int received for suit or rank.")

        if rank <= self.rank and suit <= self.suit:
            raise ValueError("Not a valid bid. Must raise.")

        self.rank = rank
        self.suit = suit
        # reset multiplier
        self.multiplier = 1

    def get_multiplier(self) -> int:
        return self.multiplier

    def get_suit(self) -> int:
        return self.suit

    def __str__(self) -> str:
        """ Overloaded string function

        Returns
        -------
        str
            Object output as string.
        """
        return "Rank: {}, Trump Suit: {}".format(self.get_rank(), self.get_suit())

class ScoreBoard:

    def __init__(self) -> None:
        pass
