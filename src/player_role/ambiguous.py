from typing import List
from player_role.player import Player,FactionFlag
class Ambiguous(Player):
    def __init__(self):
        self.name = "Ambiguous"
        self.faction = FactionFlag.UNCERTAIN

    def vote(self, list):
        pass
class Thief(Ambiguous):
    def __init__(self):
        super().__init__()
        self.role = "thief"
        self.display_role = "Thief"
    
    def steal_role(self, role_to_steal: List[str]):
        pass

class Maid(Ambiguous):
    def __init__(self):
        super().__init__()
        self.role = "maid"
        self.display_role = "Devoted Maid"
        self.has_power = True
    
    def obtain_role(self, player: Player):
        self.role = player.role
        self.display_role = player.display_role
