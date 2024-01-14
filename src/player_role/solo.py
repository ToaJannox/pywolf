from typing import List,TypedDict

from enums.faction_flag import FactionFlag
from player_role.player import Player

class Solo(Player):
    def __init__(self):
        self.name = "Loner"
        self.faction = FactionFlag.SOLO

    def vote(self, list):
        pass

class Angel(Solo):
    def __init__(self):
        super().__init__()
        self.role = "angel"
        self.display_role = "Angel"
    
class Sectarian(Solo):
    def __init__(self):
        super().__init__()
        self.role = "sectarian"
        self.display_role = "Abominable Sectarian"

class Piper(Solo):
    def __init__(self):
        super().__init__()
        self.role = "piper"
        self.display_role = "Piper"
        self.has_power = True
        self.charmed_players: List[Player] = []

class WhiteRabbit(Solo):
    class GiftedPlayer(TypedDict):
        gifts: int
        player: Player
    
    def __init__(self):
        super().__init__()
        self.role = "white_rabbit"
        self.display_role = "White Rabbit"
        self.has_power = True
        self.gifted_player: List[self.GiftedPlayer] = []