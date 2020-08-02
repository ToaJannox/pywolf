
from random import randint
class Player:
    camp = "None"
    def __init__(self):
        self.name =""
        self.role = "role"
        self.votes = 0
        self.alive = True
        self.hasPower = False
        self.isCaptain = False
        self.memory = []
        self.lover = None
        self.deathAnnounced = False

    def display(self):
        print(self.name,end="")
        print("\tVotes: ",str(self.votes),end="")
        if not self.alive:
            print(" ✝ ",end="")
        else:
            print("   ",end="")
        if self.lover:
                print(" ❤ ",end="")
        else:
                print("   ",end="")
        print("\t("+self.role +")")
        print("Memory: [",end="")
        for player,role in self.memory:
            print("("+player.name+","+role+") ",end="")
        print("]")
    def isAlly(self,player):
        return self.camp == player.camp

    def vote(self,playerList):
        choice = -1
        chosenPlayer = self
        list = playerList[:]
        for p in playerList:
            if p in list and (p.alive == False):
                list.remove(p)
        if self in  list:
            list.remove(self)
        if self.lover and (self.lover in list):
            list.remove(self.lover)
        while (not chosenPlayer.alive) or (chosenPlayer == self):
            choice = randint(0,len(list)-1)
            chosenPlayer = list[choice]
        return chosenPlayer

    def forgetDeadPlayers(self):
        self.memory[:] =[mem for mem in self.memory if mem[0].alive]
    
    def usePower(self,game):
        pass


class Villager(Player):
    camp = "Villager"
    def __init__(self):
        super().__init__()
        self.role = "Villager"
    def vote(self,playerList):
        list = playerList[:]
        targets = []
        for player,role in self.memory: #if the player now the roles of some other player we must review them first
            # if role in werewolfRoles or role in lonerRoles: #if any wolf is found they must be targetted
            if player.camp != self.camp: #if any wolf is found they must be targetted
                targets.append(player)
            # if role in villagerRoles: #if any villager is found, they must not be targeted
            else: #if any villager is found, they must not be targeted
                list.remove(player)
        if targets: #if wolves have been found the player will vote among them, if not the vote is normal
            list = targets
        return super().vote(list)


        
class Werewolf(Player): 
    camp = "Werewolf"
    def __init__(self):
        super().__init__()
        self.role ="Werewolf"
        self.allies = []
    def vote(self,playerList):
        list = playerList[:]
        targets = []
        for player,role in self.memory:
            if player.camp != self.camp:
                targets.append(player)
            # if role in lonerRoles:
            #     targets.append(player)
            # if player.hasPower:
            #     targets.append(player)
        for a in self.allies:
            list.remove(a)
        if targets:
            list= targets
        return super().vote(list)

    def forgetDeadPlayers(self):
        super().forgetDeadPlayers()
        self.allies[:] =[ally for ally in self.allies if ally.alive] #forget all dead allies

class Ambiguous(Player):
    camp = "Ambiguous"
    def __init__(self):
        super().__init__()
        self.name = "Ambiguous"
    def vote(self,list):
        pass
class Loner(Player):
    camp = "Loner"
    def __init__(self):
        super().__init__()
        self.name = "Loner"
    def vote(self,list):
        pass


class FortuneTeller(Villager):
    def __init__(self):
        super().__init__()
        self.role = "Fortune Teller"
        self.hasPower = True
    def tellFortune(self, playerList):
        list = playerList[:]
        list.remove(self)
        chosenTarget = self
        while(chosenTarget == self or (chosenTarget, chosenTarget.role) in self.memory or not chosenTarget.alive):
            chosenTarget = list[randint(0, len(list)-1)]
        self.memory.append((chosenTarget,chosenTarget.role))
        print("The Fortune Teller saw that " +chosenTarget.name + " is a "+chosenTarget.role)
    
    def usePower(self,game):
        if self.hasPower:
            self.tellFortune(game.getPlayerList())

class Hunter(Villager):
    def __init__(self):
        super().__init__()
        self.role = "Hunter"
        self.hasPower = True

    def shootOnDeath(self,list):
        print("The Hunter shoot someone on is dying breath")
        return self.vote(list) 
    
    def usePower(self,game):
        if self.hasPower:
            return self.shootOnDeath(game.getPlayerList())


class Cupid(Villager):
    def __init__(self):
        super().__init__()
        self.role = "Cupid"
        self.hasPower = True
    def chooseLovers(self,list):
        loverA = list[randint(0,len(list)-1)]
        loverB = loverA
        while loverB == loverA:
            loverB = list[randint(0,len(list)-1)]
        loverA.lover = loverB
        loverB.lover = loverA
        print(loverA.name +" and "+loverB.name+" are lovers")
    def usePower(self,game):
        if self.hasPower:
            self.chooseLovers(game.getPlayerList())

class Witch(Villager):
    def __init__(self):
        super().__init__()
        self.role = "Witch"
        self.hasPower = True
        self.healthPotion = True
        self.healUseChange = 65
        self.poisonVial = True
        self.poisonUseChange = 30

    def heal(self,victimsList,playerList):
        list = victimsList[:]
        victim = None
        
        if (self.lover in victimsList) or (self in victimsList):
            self.healthPotion = False
            if victim == self.lover:
                print("The witch healed her love: "+self.lover.name)
            else:
                print("The witch healed herself")
            victimsList.remove(victimsList)
            return victim
        if list and randint(0,101) >= self.healUseChange: #if there is a victim she can save it
            self.healthPotion = False
            targets = []

            for player,role in self.memory:
                if player.camp== self and player in list:
                    targets.append(player)
                elif player.camp!= self and player in list:
                    list.remove(player) #if she knows a werewolf, she will not attempt to heal it
            if targets: #if she knows villager among the victims she'll heal one
                victim = targets[randint(0,len(targets)-1)]
                print("The witch healed a villager "+victim.name)
                return victim
            else: #if she don't know anyone, she'll choose randomly  among
                victim = list[randint(0,len(list)-1)]
                print("The witch healed "+victim.name)
                victimsList.remove(victim)
                return victim
        else:
            print("The witch did not use her healing potion")
            return None
            

    def poison(self,saved,playerList,victimsList=[]): #TODO make use of the victim list if given
        targets = []
        list = playerList[:]
        if saved:
            list.remove(saved)
        for player,role in self.memory: #the witch first targets are the wolves she is aware of
            if player.camp != self.camp:
                targets.append(player)
            elif player.camp == self.camp:
                list.remove(player)
        if targets: # if she is aware of werewolves the then kill one
            self.poisonVial = False
            print("The witch use poison on a wolf")
            return targets[randint(0,len(targets)-1)]

        if randint(0,101)>=self.poisonUseChange: #if she doesn't know any wolf she still can decide to kill someone
            self.poisonVial = False
            chosenTarget = self
            chosenTarget = super().vote(list)
            print("The witch killed "+chosenTarget.name)
            return chosenTarget
        else:
            print("The witch didn't use her poison")
            return None
    
    def usePower(self,game):
        if self.hasPower:
            witchSaved = None
            witchVictim = None
            playerList = game.getPlayerList()
            victims = game.getVictimsList()

            if self.healthPotion:
                witchSaved = self.heal(victims,playerList)
            if self.poisonVial:
                if self.healthPotion:
                    witchVictim = self.poison(witchSaved,playerList,victims)
                else:
                    witchVictim = self.poison(witchSaved,playerList)
                if witchVictim:
                    victims.append(witchVictim)
            if not self.healthPotion and not self.poisonVial:
                self.hasPower = False

villagerRoles = {
    "Villager":Villager,
    "Villager-Villager":Player,
    "Fortune Teller":FortuneTeller,
    "Cupid":Cupid,
    "Witch":Witch,
    "Hunter":Hunter,
    "Little Girl":Player,
    "Guard":Player,
    "Ancient":Player,
    "Scapegoat":Player,
    "Idiot":Player,
    "Two Sisters":Player,
    "Three Brothers":Player, 
    "Fox":Player, 
    "Bear Tamer":Player,
    "Stuttering Judge":Player, 
    "Rusted Sword Knight":Player, 
    "Shaman":Player, 
    "Puppeteer":Player, 
    "Ankou":Player,
    "Night Owl":Player
    }


werewolfRoles = {
    "Werewolf":Werewolf,
    "Big Bad Wolf":Player,
    "Vile Father of Wolves":Player
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
    "Gypsy":Player
    }
