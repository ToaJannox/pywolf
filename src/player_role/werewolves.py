from typing import List
from player_role.player import Player,FactionFlag
from player_role.villagers import FortuneTeller
class Werewolf(Player):
    def __init__(self):
        super().__init__()
        self.role = "werewolf"
        self.faction = FactionFlag.WEREWOLF
        self.display_role = "Werewolf"
        self.role_type = Werewolf
        self.wolf_allies = set()

    def learn_allies(self, allies: List['Werewolf']):
        self.wolf_allies = set(allies)
        if self in self.wolf_allies:
            self.wolf_allies.remove(self)

    def vote(self, targets: List[str]) -> str:
        pass
        # chosen_player = self
        # choice = list.index(self)
        # while ((chosen_player == self) or not chosen_player.alive) or (
        #     chosen_player in self.allies
        # ):
        #     choice = randint(0, len(list) - 1)
        #     chosen_player = list[choice]
        # return choice
class WhiteWolf(Werewolf):
    def __init__(self):
        super().__init__()
        self.role="white_wolf"
        self.display_role="White Wolf"
        self.faction |= FactionFlag.LONER

class BigBadWolf(Werewolf):
    def __init__(self):
        super().__init__()
        self.role="big_bad_wolf"
        self.display_role="Big Bad Wolf"
        self.has_power = True


class FatherWolf(Werewolf):
    def __init__(self):
        super().__init__()
        self.role="father_wolf"
        self.display_role="Vile Father of Wolves"
        self.has_power = True
    
    def infect_player(self, target: Player):
        target.faction = FactionFlag.WEREWOLF

class FortuneTellerWolf(Werewolf,FortuneTeller):
    def __init__(self):
        super().__init__()
        self.role="fortune_teller_wolf"
        self.display_role="Fortune Teller Wolf"