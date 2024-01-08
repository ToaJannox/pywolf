
from random import randint
from roleType import RoleType
class Player:
    def __init__(self):
        self.name =""
        self.role = "role"
        self.roleType = None
        self.votes = 0
        self.alive = True
        self.hasPower = False
        self.isCaptain = False
        self.memory = []
        self.lover = None

    def display(self):
        if self.alive:
            print(self.name)
        else:
            print(self.name +"("+self.role +")")
    def checkRoleIs(self,role):
        return (type(self.role) is role)

    def vote(self,list):
        chosenPlayer = self
        choice = list.index(self)
        while (chosenPlayer == self) or not chosenPlayer.alive:
            choice = randint(0,len(list)-1)
            chosenPlayer = list[choice]
        return choice
    def death(self):
        pass


class Villager(Player):
    def __init__(self):
        super().__init__()
        self.role = "Villager"
        self.roleType = RoleType.VILLAGER

        
class Werewolf(Player): 
    def __init__(self):
        super().__init__()
        self.role ="Werewolf"
        self.roleType = Werewolf
        self.allies = []
    def vote(self,list):
        chosenPlayer = self
        choice = list.index(self)
        while ((chosenPlayer == self) or not chosenPlayer.alive) or (chosenPlayer in self.allies):
            choice = randint(0,len(list)-1)
            chosenPlayer = list[choice]
        return choice

class Ambiguous(Player):
    def __init__(self):
        super().__init__()
        self.name = "Ambiguous"
    def vote(self,list):
        pass
class Loner(Player):
    def __init__(self):
        super().__init__()
        self.name = "Loner"
    def vote(self,list):
        pass
#TODO finish  test FortuneTeller
class FortuneTeller(Villager):
    def __init__(self):
        super().__init__()
        self.role="Fortune Teller"
        self.hasPower = True
    def vote(self,list):
        if not self.memory:
            choice = super.vote(list)
        else:
            targets = []
            for player,role in self.memory:
                if role == "Werewolf":
                    targets.append(player)
            choice = list.index(targets[randint(0,len(targets)-1)])
        return choice
    def tellFortune(self,list):
        chosenTarget = self
        while(chosenTarget == self or (chosenTarget,chosenTarget.role) in self.memory):
            chosenTarget = list[randint(0,len(list)-1)]
        print("The Fortune Teller saw that "+chosenTarget.name + " is a "+chosenTarget.role)

villagerRoles = {
    "Villager":Villager,
    "Villager-Villager":Player,
    "Fortune Teller":FortuneTeller,
    "Cupid":Player,
    "Witch":Player,
    "Hunter":Player,
    "Little Girl":Player,
    "Guard":Player,
    "Ancient":Player,
    "Scapegoat":Player,
    "Idiot":Player,
    "Savior":Player,
    "Two Sisters":Player,
    "Three Brothers":Player, 
    "Devoted Maid":Player,
    "Fox":Player, 
    "Bear Tamer":Player,
    "Stuttering Judge":Player, 
    "Rusted Sword Knight":Player, 
    "Shaman":Player, 
    "Puppeteer":Player, 
    "Ankou":Player,
    "Night Owl":Player
    "Astronomer":Player
    }


werewolfRoles = {
    "Werewolf":Werewolf,
    "Big Bad Wolf":Player,
    "Vile Father of Wolves":Player
    "Fortune Teller Wolf": Player
    }
ambiguousRoles = {
    "Thief":Player,
    "Devoted Maid":Player,
    "Actor":Player,
    "Wild Child":Player,
    "Wolf-Dog":Player,
    "Abominable Sectarian":Player
    }
lonerRoles = {
    "White Wolf":Player,
    "Angel":Player,
    "Pied Pipper":Player,
    "White Rabbit":Player
    }
specialRoles = {
    "Pyromaniac":Player,
    "Raven":Player,
    "Gypsy":Player}