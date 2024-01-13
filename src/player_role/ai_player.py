from player import Player

from random import randint
from typing import List

from src.enums.factions.faction_type import Faction
from src.voting_system.vote import Vote

class Player(Player):
    def __init__(self):
        super().__init__()

    def vote(self, targets: List[str]) -> str:
        """
            Randomly select a player
        """
        chosen_player: str = targets[randint(0, len(targets) - 1)]
        return chosen_player











