from typing import List
from player import Player,FactionFlag

class Werewolf(Player):
    def __init__(self):
        super().__init__()
        self.role = "werewolf"
        self.faction = FactionFlag.WEREWOLF
        self.display_role = "Werewolf"
        self.roleType = Werewolf
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
        self.role="white wolf"
        self.display_role="White Wolf"
        self.faction = self.faction | FactionFlag.LONER