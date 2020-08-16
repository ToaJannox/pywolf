
# TODO manage situation when lovers are from Villager and Werewolf camp and are last alive wih another player
from random import randint
from enum import Enum
class Camp(Enum):
    VILLAGERS = 0
    WEREWOLVES = 1
    AMBIGUOUS = 2
    LONERS = 3
    NONE = 4

class Memory:
    def __init__(self,player,role="",camp=Camp.NONE):
        self.player = player
        self.role = role
        self.camp = camp

class Player:
    """Defines a generic player.
        Every Player possess:

        - name (str) : a name
        - camp (Camp) : indicates to which a player belong
        - role (str): a role,
        - votes (int): the amount a voice against him during votes
        - alive (bool) : a boolean representing whether the player is alive or not
        - hasPower (bool):  a boolean representing if the player has a power he can used. Powers can be lost or not accessible anymore, if so this attribute will be set to False
        - isCaptain (bool): a boolean representing if the player has the Captain honorific role
        - memory (list): a list of tuple (Player,str) representing the knowledge a player has on other players, namely which role other players hold
        - lover (Player):  the lover of this player. This can get set if a player having the Cupid role is added to the game.
    

    """
    color = ""
    def __init__(self):
        """Constructor.
        """
        self.name = ""
        self.camp = Camp.NONE
        self.role = "role"
        self.votes = 0
        self.alive = True
        self.hasPower = False
        self.isCaptain = False
        self.memories = []
        self.lover = None
        self.deathAnnounced = False
    def display(self):
        """Displays current player informations.
        
        Displays the following information about a player:
            - status, if dead the "✝" is displayed
            - lover, if has a "❤", it means it has a lover
        """
        print(self.name, end="")
        print("\tVotes: ", str(self.votes), end="")
        if not self.alive:
            print(" \033[90m✝\033[m ", end="")
        else:
            print("   ", end="")
        if self.lover:
            print(" \033[38;5;199m❤\033[m ", end="")
        else:
            print("   ", end="")
        print("\t(" +self.color+ self.role + "\033[m)")
        print("Memory: [", end="")
        for mem in self.memories:
            if mem.camp == Camp.NONE:
                print("("+mem.player.color + mem.player.name + "," + mem.role +"\033[m) ", end="")
            else:
                print("("+mem.player.color + mem.player.name + "," + mem.role + ","+str(mem.camp)+ "\033[m) ", end="")
        print("]")

    def isAlly(self, player):
        """Check whethers a player is allied to current player.
        Parameters:
        
        player (Player) : Player to check
        
        Returns:
        bool : True if allied, False else
        """
        return self.camp == player.camp

    def vote(self, playerList):
        """Vote against a player from a list. The choice is random.
        Parameters:
        
        playerList (list) : a list a Player from which to choose from
        
        Returns:

        Player : the chosen player
        """
        choice = -1
        chosenPlayer = self
        targetList = playerList[:]
        if self in targetList:
            targetList.remove(self)
        if self.lover and self.lover in targetList:
            targetList.remove(self.lover)
        while (not chosenPlayer.alive) or (chosenPlayer == self):
            choice = randint(0, len(targetList) - 1)
            chosenPlayer = targetList[choice]
        return chosenPlayer
    def forgetDeadPlayers(self):
        """Remove tuples containing dead player from current player memory
        """"""Remove tuples containing dead player from current player memory
        """
        self.memories[:] = [mem for mem in self.memories if mem.player.alive]
    def usePower(self, game):
        """Use current player power to influence the game
        """
        pass
    def addMemory(self,player,role="",camp=Camp.NONE):
        self.memories.append(Memory(player,role,camp))

class Villager(Player):
    color = "\033[32m"
    """Defines a Villager player. Must kill all the Werewolves
        Possess the same data as a Player.
    """

    def __init__(self):
        """Constructor.
        """
        super().__init__()
        self.role = "Villager"
        self.camp = Camp.VILLAGERS
    def vote(self, playerList):
        """Vote against a player from a list. Prunes the list to only select valid targets then use parent method.

        Parameters:

        playerList(list) : list of Player from which to choose from

        Returns:

        Player: the chosen player

        """
        targetList = [p for p in playerList if p.alive]
        priorityTargets = []
        if not self.memories: # if memory is empty, vote with the rest of the list
            return super().vote(targetList)
        
        loverCriticalChoice = False
        
        for mem in self.memories:
            if mem.camp == Camp.WEREWOLVES: # check for wolves
                if mem.player != self.lover: # make sure the wolf isn't the Villager lover
                    priorityTargets.append(mem.player)
                else: #if the player lovers is a wolf, he might have to betray his allies
                    loverCriticalChoice = True
            elif mem.camp == Camp.VILLAGERS: #remove villagers from potential targets
                if mem.player in targetList:
                    targetList.remove(mem.player)
        if priorityTargets:# if wolves have been identified they must be eliminated
            targetList = priorityTargets
        elif not priorityTargets and loverCriticalChoice:# if the only wolf left is the player lover then he must targets his fellow villagers anyway
            targetList = [p for p in playerList if p.alive]
        return super().vote(targetList)


class Werewolf(Player):
    """Defines a Werewolf Player. Must kill all the Villagers
        Possess the same data as a Player, with the following addition:

        allies(list) : a list containing all the current werewolf allies. Filled during the first night.
    """
    color = "\033[31m"
    def __init__(self):
        """Constructor.
        """
        super().__init__()
        self.role = "Werewolf"
        self.camp = Camp.WEREWOLVES

    def vote(self, playerList,night=False):
        """Vote against a player from a list. Prunes the list to only select valid targets then use parent method.

        Parameters:

        playerList(list) : list of Player from which to choose from

        night(bool) : a boolean that indicates if the vote happend during the night or during the day.
            default value = False

        Returns:

        Player: the chosen player

        """
        targetList = [p for p in playerList if p.alive]
        priorityTargets = []
        loverCriticalChoice = False
        if not self.memories: # if memory is empty, vote with the rest of the list minus the wolves allies
            return super().vote(targetList)
        for mem in self.memories:
            if mem.camp == Camp.VILLAGERS: # check for Villagers
                if mem.player == self.lover: #if the player lovers is a villagers, he might have to betray his allies
                    loverCriticalChoice = True
                else: # make sure the wolf isn't the Villager lover 
                    priorityTargets.append(mem.player)
            elif mem.camp == Camp.WEREWOLVES: #remove allies from potential targets
                if mem.player in targetList:
                    targetList.remove(mem.player)
        if priorityTargets:# if villagers have been identified they must be eliminated
            targetList = priorityTargets
        elif not priorityTargets and loverCriticalChoice:# if the only villagers left is the player lover then he must targets his fellow wolves anyway
            if not night: # a wolf can betray his allies only during day
                targetList = [x for x in self.memories if mem.camp==Camp.WEREWOLVES]
            else: # during night he can't vote (the vote will be the majority among wolves)
                return None
        return super().vote(targetList)

    def registerAllies(self,playerList):
        for p in playerList:
            if p !=self and p.camp==Camp.WEREWOLVES:
                self.memories.append(Memory(p,role="",camp=Camp.WEREWOLVES))


class Ambiguous(Player):
    """Defines an Ambiguous player
    """
    def __init__(self):
        """Constructor.
        """
        super().__init__()
        self.name = "Ambiguous"
        self.camp = Camp.AMBIGUOUS

    def vote(self, list):
        pass

class Loner(Player):

    def __init__(self):
        """Constructor.
        """
        super().__init__()
        self.name = "Loner"
        self.camp = Camp.LONERS

    def vote(self, list):
        pass


class FortuneTeller(Villager):
    """Defines a Fortune Teller. Can learn roles from other players.
    Has a power
    """
    color = "\033[38;5;128m"
    def __init__(self):
        """Constructor.
        """
        super().__init__()
        self.role = "Fortune Teller"
        self.hasPower = True

    def tellFortune(self, playerList):
        """Reveal a Player role to itself

        Parameters:

        playerList(list): list of player which to choose from
        """
        targetList = playerList[:]
        targetList.remove(self)
        chosenTarget = self
        if len(self.memories) != len(targetList):
            while chosenTarget == self or chosenTarget in [x.player for x in self.memories]:
                chosenTarget = targetList[randint(0, len(targetList) - 1)]
            self.memories.append(Memory(chosenTarget,role=chosenTarget.role))
            print("The Fortune Teller saw that " +
                chosenTarget.name + " is a " + chosenTarget.role)
        else:
            print("The Fortune Teller knows everything already")

    def usePower(self, game):
        """Fortune Teller power.
        Parameters:

        game (Game) : the game object from which to extract data used for character power
        """
        if self.hasPower:
            self.tellFortune(game.getPlayerList())


class Hunter(Villager):
    """Defines a Hunter. Kills someone on death.
    Has a power.
    """
    color = "\033[38;5;58m"
    def __init__(self):
        """Constructor;
        """
        super().__init__()
        self.role = "Hunter"
        self.hasPower = True



class Cupid(Villager):
    """Defines a Cupid. Can charm two player to make them lovers.
    Has a power
    """
    color = "\033[38;5;213m"
    def __init__(self):
        """Constructor method
        """
        super().__init__()
        self.role = "Cupid"
        self.hasPower = True

    def chooseLovers(self, playerList):
        """Select 2 players and make them lovers.
        Parameters:

        playerList(list) : list
        """
        loverA = playerList[randint(0, len(playerList) - 1)]
        loverB = loverA
        while loverB == loverA:
            loverB = playerList[randint(0, len(playerList) - 1)]
        loverA.lover = loverB
        loverB.lover = loverA
        print(loverA.name + " and " + loverB.name + " are lovers")

    def usePower(self, game):
        """Cupid Power.
        Parameters:

        game (Game) : the game object from which to extract data used for character power
        """
        if self.hasPower:
            self.chooseLovers(game.getPlayerList())


class Witch(Villager):
    """Defines a Witch. Have two potions, one to save, the other to kill.
    Has a power. Additionnal data:

        - healthPotion(bool) : a boolean that states if the Witch can still use it's health potion
        - poisonVial(bool) : a boolean that states if the Witch can still use it's poison
        - healUseChance(int) : chance that the witch will use it's health potion on a victim except her and it's lover
        - poisonUseChance(int) : chance that the witch will use it's poison on a random player
    """
    color = "\033[38;5;202m"
    def __init__(self):
        """Constructor.
        """
        super().__init__()
        self.role = "Witch"
        self.hasPower = True
        self.healthPotion = True
        self.poisonVial = True
        self.healUseChance = 65
        self.poisonUseChance = 30

    def heal(self, victimsList):
        """Heals someone and removes it from the victims List

        Parameters:

        victimsList(list) : list of player that were designated as a victim

        Returns:
        Either of the following:
            NoneType : if the witch saves no one
            Player: the victim the witch saves
        """
        targetList = victimsList[:]

        if (self.lover in victimsList) or (self in victimsList):
            self.healthPotion = False
            if self.lover in victimsList:
                # print("The witch healed her love: " + self.lover.name)
                victimsList.remove(self.lover)
                return self.lover
            elif self in victimsList:
                # print("The witch healed herself")
                victimsList.remove(self)
                return self
        # if there is a victim she can save it
        if targetList and randint(0, 101) >= self.healUseChance:
            priorityTargets = []

            for mem in self.memories:
                if mem.role in villagerRoles and mem.player in targetList:
                    priorityTargets.append(mem.player)
                elif mem.role in werewolfRoles and mem.player in targetList:
                    # if she knows a werewolf, she will not attempt to heal it
                    targetList.remove(mem.player)
            if priorityTargets:  # if she knows villager among the victims she'll heal one
                victim = priorityTargets[randint(0, len(priorityTargets) - 1)]
                # print("The witch healed a villager " + victim.name)
                self.healthPotion = False
                return victim
            elif len(targetList)>0:  # if she don't know anyone, she'll choose randomly  among
                victim = targetList[randint(0, len(targetList) - 1)]
                # print("The witch healed " + victim.name)
                victimsList.remove(victim)
                self.healthPotion = False
                return victim
        # print("The witch did not use her healing potion")
        return None

    def poison(self, saved, playerList, victimsList=[]):
        """Chooses a player and kills it.
        
        Parameters:

        saved(Player or NoneType) : the previously saved power. Set to "None" if the witch did not heal someone previously. 
        
        playerList(list) : list of players from which to choose from.

        victimsList(list) : a list of player that were designated as victims. Only available if the witch's health potion is still available;
            default value is an empty list.
        """
        targetList = playerList[:]
        if saved:
            targetList.remove(saved)
        if victimsList:
            print("The Witch can see the victims")
            for v in victimsList:
                v.display()
                if v in targetList:
                    targetList.remove(v)
        if self.memories:
            return super().vote(targetList)
        # if she doesn't know any wolf she still can decide to kill someone
        if randint(0, 101) >= self.poisonUseChance:
            self.poisonVial = False
            chosenTarget = self
            chosenTarget = super().vote(targetList)
            print("The witch killed " + chosenTarget.name)
            return chosenTarget
        else:
            print("The witch didn't use her poison")
            return None

    def usePower(self, game):
        """Witch Power.
        Parameters:

        game (Game) : the game object from which to extract data used for character power
        """

        if self.hasPower:
            witchSaved = None
            witchVictim = None
            victims = game.getVictimsList()

            if self.healthPotion:
                witchSaved = self.heal(victims)
            if self.poisonVial:
                playerList = game.getPlayerList()
                if self.healthPotion:
                    witchVictim = self.poison(witchSaved, playerList, victims)
                else:
                    witchVictim = self.poison(witchSaved, playerList)
                if witchVictim:
                    victims.append(witchVictim)
            if not self.healthPotion and not self.poisonVial:
                self.hasPower = False

class LittleGirl(Villager):
    """Defines a Little Girl Player. Can try to observer who are the werewolves
    Has a power.
    Data:

    - chanceToSpy(int) : chance value the little girl has to spy on wolves.
    - chanceToGetCaught(int) : chance value the little girl has to be caught by wolves
    """
    
    def __init__(self):
        """Constructor
        """
        super().__init__()
        self.role = "Little Girl"
        self.hasPower = "True"
        self.chanceToSpy = 50
        self.chanceToBeCaught = 0
    def usePower(self,game):
        """Power invokinkg method
        """
        self.spyOnWolves(game.getPlayerList(),game.getWerewolvesAmount())
    def spyOnWolves(self,playerList,wolvesAmount):
        pass
        


class VillagerVillager(Villager): # todo adapt wolves votes to not always eliminate this player on the first night
    """Defines a Villager-Villager Player. His role is know by everyone at the start of the game.
    """
    color = "\033[38;5;119m"
    def __init__(self):
        super().__init__()
        self.role = "Villager-Villager"
    def usePower(self,game):
        game.revealRole(self)

villagerRoles = {
    "Villager": Villager,
    "Villager-Villager": VillagerVillager,
    "Fortune Teller": FortuneTeller,
    "Cupid": Cupid,
    "Witch": Witch,
    "Hunter": Hunter,
    "Little Girl": Player,
    "Guard": Player,
    "Ancient": Player,
    "Scapegoat": Player,
    "Idiot": Player,
    "Two Sisters": Player,
    "Three Brothers": Player,
    "Fox": Player,
    "Bear Tamer": Player,
    "Stuttering Judge": Player,
    "Rusty Sword Knight": Player,
    "Shaman": Player,
    "Puppeteer": Player,
    "Ankou": Player,
    "Night Owl": Player
}

werewolfRoles = {
    "Werewolf": Werewolf,
    "Big Bad Wolf": Player,
    "Vile Father of Wolves": Player
}
ambiguousRoles = {
    "Thief": Player,
    "Devoted Maid": Player,
    "Actor": Player,
    "Wild Child": Player,
    "Dog-Wolf": Player
}
lonerRoles = {
    "White Wolf": Player,
    "Angel": Player,
    "Pied Pipper": Player,
    "Abominable Sectarian": Player,
    "White Rabbit": Player
}
specialRoles = {
    "Pyromaniac": Player,
    "Raven": Player,
    "Gypsy": Player
}
