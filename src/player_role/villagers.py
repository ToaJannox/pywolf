from player import Player,Faction

class Villager(Player):
    def __init__(self):
        super().__init__()
        self.role = "villager"
        self.display_role = "Villager"
        self.roleType = Faction.VILLAGER


class VillagerVillager(Villager):
    def __init__(self):
        self.role = "villager_villager"
        self.display_role = "Villager-Villager"
        self.role_is_revealed = True

# TODO finish  test FortuneTeller
class FortuneTeller(Villager):
    def __init__(self):
        self.role = "Fortune Teller"
        self.hasPower = True

    def vote(self, list):
        if not self.memory:
            choice = super.vote(list)
        else:
            targets = []
            for player, role in self.memory:
                if role == "Werewolf":
                    targets.append(player)
            choice = list.index(targets[randint(0, len(targets) - 1)])
        return choice

    def tellFortune(self, list):
        chosenTarget = self
        while chosenTarget == self or (chosenTarget, chosenTarget.role) in self.memory:
            chosenTarget = list[randint(0, len(list) - 1)]
        print(
            "The Fortune Teller saw that "
            + chosenTarget.name
            + " is a "
            + chosenTarget.role
        )
