from typing import List
from random import randint

from player_role.player import Player,FactionFlag
from player_role.werewolves import Werewolf
class Villager(Player):
    def __init__(self):
        super().__init__()
        self.role = "villager"
        self.display_role = "Villager"
        self.roleType = FactionFlag.VILLAGER


class VillagerVillager(Villager):
    def __init__(self):
        self.role = "villager_villager"
        self.display_role = "Villager-Villager"
        self.role_is_revealed = True

class FortuneTeller(Villager):
    def __init__(self):
        self.role = "fortune_teller"
        self.display_role = "Fortune Teller"
        self.has_power = True


    def tell_fortune(self, players: List[Player]) -> None:
        valid_targets = [p for p in players if not self.memories[p.name]["role_known"]]
        chosen_player = valid_targets[randint(0, len(valid_targets) - 1)]
        self.learn_role(chosen_player)

class Cupid(Villager):
    def __init__(self):
        super().__init__()
        self.role = "cupid"
        self.display_role("Cupid")
    
    def match_lovers(self, targets: List[Player]) -> None:
        # first_target = targets[randint(0, len(targets) - 1)]
        # targets.remove(first_target)
        # second_target = targets[randint(0, len(targets) - 1)]
        # first_target.lover = second_target
        # second_target.lover = first_target
        pass

class Witch(Villager):
    def __init__(self):
        super().__init__()
        self.role = "witch"
        self.display_role = "Witch"
        self.has_power = True
        self.has_healing = True
        self.has_poison = True
    
    def use_potions(self,players:List[Player],wolf_victim: Player) -> Player:
        if not self.has_healing and not self.has_poison:
            self.has_power = False
        return None
    
class Hunter(Villager):
    def __init__(self):
        super().__init__()
        self.role = "hunter"
        self.display_role = "Hunter"
        self.has_power = True

    def death(self,targets:List[Player]) -> Player:

        super().death()
        last_breath_victim = None    
        if last_breath_victim:
            print(f"{self.name} shoots {last_breath_victim.name} in their last breath!")
        return last_breath_victim

class LittleGirl(Villager):
    def __init__(self):
        super().__init__()
        self.role = "little_girl"
        self.display_role = "Little Girl"

class Savior(Villager):
    def __init__(self):
        super().__init__()
        self.role = "savior"
        self.display_role = "Savior"
        self.has_power = True
        self.last_saved_victim: Player = None
    
    def save_someone(self,targets:List[Player]) -> Player:
        if self.last_saved_victim:
            targets.remove(self.last_saved_victim)
        chosen_player = None
        self.last_saved_victim = chosen_player
        return self.last_saved_victim

class Elder(Villager):
    def __init__(self):
        super().__init__()
        self.role = "elder"
        self.display_role = "Elder"
        self.has_power = True
    
    def death(self, villagers: List[Villager]):
        if self.has_power:
            self.has_power = False
        else:
            for p in villagers:
                p.has_power = False
            super().death()
            print("All Villagers lose their powers !!!")

class Scapegoat(Villager):
    def __init__(self):
        super().__init__()
        self.role = "scapegoat"
        self.display_role = "Scapegoat"
        self.has_power = True
    
    def voted_against(self,targets:List[Player]) -> List[Player]:
        # select list of player who can't vote
        return []
    
class Fool(Villager):
    def __init__(self):
        super().__init__()
        self.role = "fool"
        self.display_role = "Village's Fool"
        self.has_power = True
    
    def voted_against(self,targets:List[Player]) -> List[Player]:
        self.role_is_revealed = True
        return []

class Sister(Villager):
    def __init__(self):
        super().__init__()
        self.role = "sister"
        self.display_role = "Sister"
        self.sister: 'Sister' = None
    def learn_sister(self, sister:'Sister'):
        self.sister = sister

class Brother(Villager):
    def __init__(self):
        super().__init__()
        self.role = "brother"
        self.display_role = "Brother"
        self.brothers: List['Brother'] = []
    def learn_sister(self, brothers:'Brother'):
        self.brothers = brothers

class Fox(Villager):
    def __init__(self):
        super().__init__()
        self.role = "fox"
        self.display_role = "Fox"
        self.has_power = True
    
    def detect_wolves(self,targets: List[Player]):
        chosen_target: int = None

class BearTamer(Villager)    :
    def __init__(self):
        super().__init__()
        self.role = "bear_tamer"
        self.display_role = "Bear Tamer"
        self.has_power = True
    
    def detect_wolves(self,neighbors:List[Player]):
        # if one direct neighbors is wolf then growl
        if True:
            print("The Bear Growls!")

class StutteringJudge(Villager):
    def __init__(self):
        super().__init__()
        self.role = "stuttering_judge"
        self.display_role = "Stuttering Judge"
        self.has_power = True
    
    def second_vote(self) -> bool:
        return False

class RustedKnight(Villager):
    def __init__(self):
        super().__init__()
        self.role = "rusted_knight"
        self.display_role = "Rusted Sword Knight"
        self.has_power = True
    
    def death(self,targets: List[Player]) -> Werewolf:
        poisoned_wolf = None
        super().death()
        return poisoned_wolf

class Raven(Villager):
    def __init__(self):
        super().__init__()
        self.role = "raven"
        self.display_role = "Raven"
        self.has_power = True
    
    def curse_player(self, targets:List[Player]) -> Player:
        return None

class Arsonist(Villager):
    def __init__(self):
        super().__init__()
        self.role = "arsonist"
        self.display_role = "Arsonist"
        self.has_power = True
    
    def burn_player_home(self, targets:List[Player]) -> Player:
        self.has_power = False
        return None

class Gypsy(Villager):
    def __init__(self):
        super().__init__()
        self.role = "gipsy"
        self.display_role = "Gipsy"
        self.has_power = True
        self.spiritism_questions = []

class Shaman(Villager):
    def __init__(self):
        super().__init__()
        self.role = "shaman"
        self.display_role = "Shaman"
        self.has_power = True

class Puppeteer(Villager):
    def __init__(self):
        super().__init__()
        self.role = "puppeteer"
        self.display_role = "Puppeteer"
        self.has_power = True
        self.controlled_wolf: Werewolf = None

class Ankou(Villager):
    def __init__(self):
        super().__init__()
        self.role = "ankou"
        self.display_role = "Ankou"
        self.has_power = True

class Sleepwalker(Villager):
    def __init__(self):
        super().__init__()
        self.role = "sleepwalker"
        self.display_role = "Sleepwalker"
        self.has_power = True
        self.visited_player: Player = None

class Astronomer(Villager):
    def __init__(self):
        super().__init__()
        self.role = "astronomer"
        self.display_role = "Astronomer"
        self.has_power = True
