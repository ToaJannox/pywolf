from random import randint
from enums.roleType import RoleType


class Player:
    def __init__(self):
        self.name = ""
        self.role = "role"
        self.role_type = None
        self.votes = 0
        self.alive = True
        self.has_power = False
        self.is_captain = False
        self.memory = []
        self.lover = None
        self.role_is_revealed = False

    def display(self):
        if self.alive:
            print(self.name)
        else:
            print(self.name + "(" + self.role + ")")

    def check_role(self, role):
        return type(self.role) is role

    def vote(self, list):
        chosen_player = self
        choice = list.index(self)
        while (chosen_player == self) or not chosen_player.alive:
            choice = randint(0, len(list) - 1)
            chosen_player = list[choice]
        return choice

    def death(self):
        self.alive = False
        self.role_is_revealed = True
        if self.lover:
            self.lover.death()
        print(f"Player {self.name} is now dead and was a {self.role}")


class Villager(Player):
    def __init__(self):
        self.role = "Villager"
        self.roleType = RoleType.VILLAGER


class VillagerVillager(Player):
    def __init__(self):
        self.role = "Villager-Villager"
        self.roleType = RoleType.VILLAGER
        self.role_is_revealed = True


class Werewolf(Player):
    def __init__(self):
        self.role = "Werewolf"
        self.roleType = Werewolf
        self.allies = []

    def vote(self, list):
        chosen_player = self
        choice = list.index(self)
        while ((chosen_player == self) or not chosen_player.alive) or (
            chosen_player in self.allies
        ):
            choice = randint(0, len(list) - 1)
            chosen_player = list[choice]
        return choice


class Ambiguous(Player):
    def __init__(self):
        self.name = "Ambiguous"

    def vote(self, list):
        pass


class Loner(Player):
    def __init__(self):
        self.name = "Loner"

    def vote(self, list):
        pass


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


villagerRoles = {
    "Villager": Villager,
    "Villager-Villager": Player,
    "Fortune Teller": FortuneTeller,
    "Cupid": Player,
    "Witch": Player,
    "Hunter": Player,
    "Little Girl": Player,
    "Guard": Player,
    "Ancient": Player,
    "Scapegoat": Player,
    "Idiot": Player,
    "Savior": Player,
    "Two Sisters": Player,
    "Three Brothers": Player,
    "Devoted Maid": Player,
    "Fox": Player,
    "Bear Tamer": Player,
    "Stuttering Judge": Player,
    "Rusted Sword Knight": Player,
    "Shaman": Player,
    "Puppeteer": Player,
    "Ankou": Player,
    "Night Owl": Player,
    "Astronomer": Player,
}


werewolfRoles = {
    "Werewolf": Werewolf,
    "Big Bad Wolf": Player,
    "Vile Father of Wolves": Player,
    "Fortune Teller Wolf": Player,
}
ambiguousRoles = {
    "Thief": Player,
    "Devoted Maid": Player,
    "Actor": Player,
    "Wild Child": Player,
    "Wolf-Dog": Player,
    "Abominable Sectarian": Player,
}
lonerRoles = {
    "White Wolf": Player,
    "Angel": Player,
    "Pied Pipper": Player,
    "White Rabbit": Player,
}
specialRoles = {"Pyromaniac": Player, "Raven": Player, "Gypsy": Player}
