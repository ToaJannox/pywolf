from random import randint
from typing import List, Dict, TypedDict

from enums.faction_flag import FactionFlag

class Memory(TypedDict):
    player: 'Player'
    role_known: bool
    faction_known: bool


class Player:
    def __init__(self):
        self.role: str = "role"
        self.display_role: str = "Role"
        self.name: str = "name"

        self.alive: bool = True
        self.has_power: bool = False
        self.is_captain: bool = False
        self.role_is_revealed: bool = False
        self.faction_is_revealed: bool = False

        self.faction: FactionFlag = None
        self.lover: 'Player' = None
        self.memories: Dict[str,Memory]

    def set_name(self,name: str) -> None:
        self.name = name

    def display(self) -> None:
        if not self.alive or self.role_is_revealed:
            self.true_display()
        else:
            print(self.name)

    def true_display(self) -> None:
        print(f"{self.name} ({self.display_role})")

    def debug_display(self) -> None:
        from inspect import getmembers
        data = getmembers(self)
        for v in data:
            print(f"name: {v[0]} value: {v[1]}")

    def vote(self, targets: List['Player']) -> 'Player':
        """
            Randomly select a player
        """
        chosen_player = targets[randint(0, len(targets) - 1)]
        return chosen_player

    def init_memory(self,players: List['Player']):
        """
            Populates the memory of the player with all know information
            at the start of the game.
        """
        player_set = set(players)
        if self in player_set:
            player_set.remove(self)
        for p in players:
            memory= Memory(player=p,role_known=False,faction_known=False)
            self.memories[p.name] = memory
            
    def learn_role(self,player: 'Player'):
        """
            Allows the player to look into another 
        """
        self.memories[player.name]["role_known"] = True
    
    def learn_faction(self,player: 'Player'):
        """
            Allows the player to look into another 
        """
        self.memories[player.name]["faction_known"] = True

    def death(self):
        self.alive = False
        self.role_is_revealed = True
        if self.lover:
            self.lover.death()
        print(f"Player {self.name} is now dead and was a {self.display_role}")
        
    def forget_player(self, player: 'Player') -> None:
        del self.memories[player.name]













# villagerRoles = {


#     "Devoted Maid": Player,
#     "Rusted Sword Knight": Player,
#     "Shaman": Player,
#     "Puppeteer": Player,
#     "Ankou": Player,
#     "Night Owl": Player,
#     "Astronomer": Player,
# }



# ambiguousRoles = {
#     "Devoted Maid": Player,
#     "Actor": Player,
#     "Wild Child": Player,
#     "Wolf-Dog": Player,
#     "Abominable Sectarian": Player,
# }
# lonerRoles = {
#     "White Wolf": Player,
#     "Angel": Player,
#     "Pied Pipper": Player,
#     "White Rabbit": Player,
# }
# specialRoles = {"Pyromaniac": Player, "Raven": Player, "Gypsy": Player}
