from typing import List
from player_role.player import Player,FactionFlag
class Uncertain(Player):
    def __init__(self):
        self.name = "Ambiguous"
        self.faction = FactionFlag.UNCERTAIN

    def vote(self, list):
        pass
class Thief(Uncertain):
    def __init__(self):
        super().__init__()
        self.role = "thief"
        self.display_role = "Thief"
    
    def steal_role(self, role_to_steal: List[str]):
        pass

class Maid(Uncertain):
    def __init__(self):
        super().__init__()
        self.role = "maid"
        self.display_role = "Devoted Maid"
        self.has_power = True
        self.master: Player = None
        self.new_role: Player = None
    
    def obtain_role(self, player: Player):
        self.role = player.role
        self.display_role = player.display_role

class Comedian(Uncertain):
    def __init__(self):
        super().__init__()
        self.role = "comedian"
        self.display_role = "Comedian"
        self.has_power = True
        self.available_roles: List[Player] = []
        self.current_role: Player = None
    
    def pick_role(self):
        chosen_role = None
        if chosen_role:
            self.available_roles.remove(chosen_role)
            self.current_role = chosen_role
            if not self.available_roles:
                self.has_power = False

class WildChild(Uncertain):
    def __init__(self):
        super().__init__()
        self.role = "wild_child"
        self.display_role = "Wild Child"
        self.faction |= FactionFlag.VILLAGER
        self.has_power = True
        self.mentor: Player = None
    
    def pick_mentor(self, targets: List[Player]):
        self.mentor = None
    
    def check_mentor(self):
        if not self.mentor.alive:
            self.faction ^= FactionFlag.VILLAGER
            self.faction |= FactionFlag.WEREWOLF


class WolfDog(Uncertain):
    def __init__(self):
        super().__init__()
        self.role = "wolf_dog"
        self.display_role = "Wolf-Dog"
        self.faction = FactionFlag.UNCERTAIN
    
    def pick_faction(self):
        if True:
            self.faction = FactionFlag.VILLAGER
        else:
            self.faction = FactionFlag.WEREWOLF