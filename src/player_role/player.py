from random import randint
from typing import List, Dict, TypedDict

from enums.faction_flag import FactionFlag
from src.voting_system.vote import Vote

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
    
    # def known_roles(self) -> List[str]:
    #     res = []
    #     for mem in self.memories.values():
    #         if mem["role_known"]:
    #             res.append({"role":mem["player"].role})
    #     return res
    
    def death(self):
        self.alive = False
        self.role_is_revealed = True
        if self.lover:
            self.lover.death()
        print(f"Player {self.name} is now dead and was a {self.display_role}")
        














# villagerRoles = {
#     "Villager": Villager,
#     "Villager-Villager": Player,
#     "Fortune Teller": FortuneTeller,
#     "Cupid": Player,
#     "Witch": Player,
#     "Hunter": Player,
#     "Little Girl": Player,
#     "Guard": Player,
#     "Ancient": Player,
#     "Scapegoat": Player,
#     "Idiot": Player,
#     "Savior": Player,
#     "Two Sisters": Player,
#     "Three Brothers": Player,
#     "Devoted Maid": Player,
#     "Fox": Player,
#     "Bear Tamer": Player,
#     "Stuttering Judge": Player,
#     "Rusted Sword Knight": Player,
#     "Shaman": Player,
#     "Puppeteer": Player,
#     "Ankou": Player,
#     "Night Owl": Player,
#     "Astronomer": Player,
# }


# werewolfRoles = {
#     "Werewolf": Werewolf,
#     "Big Bad Wolf": Player,
#     "Vile Father of Wolves": Player,
#     "Fortune Teller Wolf": Player,
# }
# ambiguousRoles = {
#     "Thief": Player,
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
