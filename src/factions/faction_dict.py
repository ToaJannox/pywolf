from typing import TypedDict,List
from player_role.player import Player

class FactionDict(TypedDict):
    villager: List[Player]
    werewolves: List[Player]
    others: List[Player]