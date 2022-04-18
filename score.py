"""
Score Related Objects and Methods
"""
from game_objects import Card, Trick, Team
from typing import List

class Contract(Card):
    """ Represents a contract one can bid on.
    """

    def __init__(self, rank: int = 1, suit: int=1) -> None:

        if rank not in range(1, 14) or suit not in range(1, 6):
            raise ValueError("Improper int received for suit or rank.")
        super(Contract, self).__init__(rank, suit)
        self.multiplier = 1
        self.suit_list = ("Club", "Diamond", "Heart", "Spade", "No Trump")
    
    def double(self) -> None:
        if self.multiplier < 4:
            self.multiplier *= 2
        else:
            raise RuntimeError("Cannot double after re-doubling.")

    def get_multiplier(self) -> int:
        return self.multiplier

    def upgrade(self, rank: int, suit: int) -> None:
        if rank not in range(1, 14) or suit not in range(1, 6):
            raise ValueError("Improper int received for suit or rank.")

        if rank <= self.rank and suit <= self.suit:
            raise ValueError("Not a valid bid. Must raise.")
        
        self.rank = rank
        self.suit = suit
        # reset multiplier
        self.multiplier = 1
    
    def __str__(self) -> str:
        """ Overloaded string function

        Returns
        -------
        str
            Object output as string.
        """
        return "Rank: {}, Trump Suit: {}".format(self.get_rank(), self.get_suit_string())

class ScoreBoard:
    
    """
    Scoreboard class to update and keep track of the teams score

    Attributes
    ----------
    contract: Contract
        The contract for the game
    teams: List[Team]
        List containing the details of the teams playing the game
    """
    
    teamsMap = {}
    teamScoreMap = {}
    teamTricksMap = {}

    def __init__(self, contract: Contract, teams: List) -> None:
        """ Scoreboard needs a contract and the team details to maintain scores

        Parameters
        -------
        contract: Contract
            The contract for the game
        teams: List[Team]
            List containing the details of the teams playing the game
        """
        self.contract = contract
        
        for team in teams:
            self.teamsMap[team.name] = team
            self.teamScoreMap[team.name] = 0
            self.teamTricksMap[team.name] = 0
            
    def win_trick(self, team: Team, trick: Trick) -> None:
        """ 
        Call when a trick is complete to capture tricks and update score for teams
        
        Parameters
        -------
        team: Team
            The team that won the trick
        trick: Trick
            Details of the trick won
        """
        
        
        if self.contract.suit != trick.get_suit():
            print("Suit of Contract and Suit of Trick do not match. Contract suit = " + self.contract.suit)
            return
        
        if self.teamTricksMap["Defending"] + self.teamTricksMap["Contracting"] == 13:
            print("Sorry, the round is complete with 13 tricks already won")
            return
        
        """ Increment team's trick score """
        self.teamTricksMap[team.name] += 1
        
        scoreToAdd = 0
        if self.contract.suit == 1 or self.contract.suit == 2:
            scoreToAdd = 20 * self.contract.multiplier
        elif self.contract.suit == 3 or self.contract.suit == 4:
            scoreToAdd = 30 * self.contract.multiplier
        else:
            scoreToAdd = 40 * self.contract.multiplier
            
        """ Increment the team's score """
        self.teamScoreMap[team.name] += scoreToAdd
        
    def score_at_end_of_round(self) -> None:
        
        """ 
        Call when a round is complete to update scores in the game
        """
        
        contractingTeam = self.teamsMap["Contracting"]
        defendingTeam = self.teamsMap["Defending"]
        
        """ Check if Contracting team met the bid in the contract """
        if self.teamTricksMap["Contracting"] >= self.contract.rank:
            """ Check for slams """     
            slamsScore = 0
            numOfTricksWon = self.teamTricksMap["Contracting"]
            
            if numOfTricksWon == 12:
                if contractingTeam.vulnerable:
                    slamsScore = 750
                else:
                    slamsScore = 500
            
            if numOfTricksWon == 13:
                if contractingTeam.vulnerable:
                    slamsScore = 1500
                else:
                    slamsScore = 1000
            
            self.teamScoreMap[contractingTeam.name] += slamsScore
            
        else:
            """ Add points to defending team """
            numOfUnderTricks = self.contract.rank - self.teamTricksMap["Contracting"]
            
            self.teamScoreMap[defendingTeam.name] += self.calculate_penalty_points(numOfUnderTricks, contractingTeam.vulnerable)


    def calculate_penalty_points(self, numOfUnderTricks: int, vulnerable: bool) -> int:
        """ 
        Call to calculate penalty points when the bid is not matched by the contracting team
        
        Parameters
        -------
        numOfUnderTricks: int
            Number of under tricks
        vulnerable: bool
            A flag to indicate whether the contracting team is vulnerable or not
            
        Returns
        -------
        int
            penalty points to add to the defending team      
        """
        
        penaltyPoints = 0
        
        """ Check if contracting team is vulnerable or not """
        if vulnerable:
            for x in range(0, numOfUnderTricks):
                if x == 0:
                    penaltyPoints += 100 * self.contract.multiplier
                else:
                    if self.contract.multiplier > 1:
                        penaltyPoints += 150 * self.contract.multiplier
                    else:
                        penaltyPoints += 100
        else:
            for x in range(0, numOfUnderTricks):
                if x == 0:
                    penaltyPoints += 50 * self.contract.multiplier
                elif x == 1 or x == 2:
                    if self.contract.multiplier > 1:
                        penaltyPoints += 100 * self.contract.multiplier
                    else:
                        penaltyPoints += 50
                else:
                    if self.contract.multiplier > 1:
                        penaltyPoints += 150 * self.contract.multiplier
                    else:
                        penaltyPoints += 50
                        
        return penaltyPoints
    
    def __str__(self) -> str:
        """ Overloaded string function

        Returns
        -------
        str
            Object output as string.
        """
        return "Teams: {}, Teams Tricks Won: {}, Teams Score: {}".format(self.teamsMap, self.teamTricksMap, self.teamScoreMap)