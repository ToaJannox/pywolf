
# TODO manage situation when lovers are from Villager and Werewolf camp and are last alive wih another player
from random import randint
from enum import Enum
class Camp(Enum):
    VILLAGERS = 0
    WEREWOLVES = 1
    AMBIGUOUS = 2
    LONERS = 3
    NONE = 4


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
        self.memory = []
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
            print(" ✝ ", end="")
        else:
            print("   ", end="")
        if self.lover:
            print(" ❤ ", end="")
        else:
            print("   ", end="")
        print("\t(" + self.role + ")")
        print("Memory: [", end="")
        for player, role in self.memory:
            print("(" + player.name + "," + role + ") ", end="")
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
        while (not chosenPlayer.alive) or (chosenPlayer == self):
            choice = randint(0, len(playerList) - 1)
            chosenPlayer = playerList[choice]
        return chosenPlayer

    def forgetDeadPlayers(self):
        """Remove tuples containing dead player from current player memory
        """"""Remove tuples containing dead player from current player memory
        """
        self.memory[:] = [mem for mem in self.memory if mem[0].alive]
    def usePower(self, game):
        """Use current player power to influence the game
        """
        pass


class Villager(Player):
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
        targetList = playerList[:]
        if self.lover: 
            if len(targetList) == 3 and (self.camp != self.lover.camp):
                targetList.remove(self)
                targetList.remove(self.lover)
                return targetList[0]
        priorityTargets = []
        for player, role in self.memory:  # if the player now the roles of some other player we must review them first
            if player.camp != self.camp:  # if any wolf is found they must be targetted
                priorityTargets.append(player)
            else:  # if any villager is found, they must not be targeted
                targetList.remove(player)
        if priorityTargets:  # if wolves have been found the player will vote among them, if not the vote is normal
            targetList = priorityTargets
        return super().vote(targetList)


class Werewolf(Player):
    """Defines a Werewolf Player. Must kill all the Villagers
        Possess the same data as a Player, with the following addition:

        allies(list) : a list containing all the current werewolf allies. Filled during the first night.
    """
    def __init__(self):
        """Constructor.
        """
        super().__init__()
        self.role = "Werewolf"
        self.camp = Camp.WEREWOLVES
        self.allies = []

    def vote(self, playerList,night=False):
        """Vote against a player from a list. Prunes the list to only select valid targets then use parent method.

        Parameters:

        playerList(list) : list of Player from which to choose from

        night(bool) : a boolean that indicates if the vote happend during the night or during the day.
            default value = False

        Returns:

        Player: the chosen player

        """
        targetList = playerList[:]
        if not night:
            if self.lover:
                if len(targetList) == 3 and (self.camp != self.lover.camp):
                    targetList.remove(self)
                    targetList.remove(self.lover)
                    return targetList[0]
        priorityTargets = []
        for player, role in self.memory:
            if player.camp != self.camp:
                priorityTargets.append(player)
        for a in self.allies:
            targetList.remove(a)
        if priorityTargets:
            targetList = priorityTargets
        if night:    
            if len(targetList)==1 and self.lover in targetList:
                print("This wolf cannot vote against his allies or his love")
                return None
        return super().vote(targetList)

    def forgetDeadPlayers(self):
        """Remove tuples containing dead players from current player memory
            Addtionnaly removes all dead allies from current werewolf list
        """
        super().forgetDeadPlayers()
        # forget all dead allies
        self.allies[:] = [ally for ally in self.allies if ally.alive]


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
        list = playerList[:]
        list.remove(self)
        chosenTarget = self
        if len(self.memory) != len(list):
            while chosenTarget == self or (chosenTarget, chosenTarget.role) in self.memory or not chosenTarget.alive:
                chosenTarget = list[randint(0, len(list) - 1)]
            self.memory.append((chosenTarget, chosenTarget.role))
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
        list = victimsList[:]
        victim = None

        if (self.lover in victimsList) or (self in victimsList):
            self.healthPotion = False
            if victim == self.lover and victim:
                print("The witch healed her love: " + self.lover.name)
                victimsList.remove(self.lover)
            elif victim == self:
                print("The witch healed herself")
                victimsList.remove(self)
            return victim
        # if there is a victim she can save it
        if list and randint(0, 101) >= self.healUseChance:
            self.healthPotion = False
            targets = []

            for player, role in self.memory:
                if player.camp == self and player in list:
                    targets.append(player)
                elif player.camp != self and player in list:
                    # if she knows a werewolf, she will not attempt to heal it
                    list.remove(player)
            if targets:  # if she knows villager among the victims she'll heal one
                victim = targets[randint(0, len(targets) - 1)]
                print("The witch healed a villager " + victim.name)
                return victim
            else:  # if she don't know anyone, she'll choose randomly  among
                victim = list[randint(0, len(list) - 1)]
                print("The witch healed " + victim.name)
                victimsList.remove(victim)
                return victim
        else:
            print("The witch did not use her healing potion")
            return None

    def poison(self, saved, playerList, victimsList=[]):
        """Chooses a player and kills it.
        
        Parameters:

        saved(Player or NoneType) : the previously saved power. Set to "None" if the witch did not heal someone previously. 
        
        playerList(list) : list of players from which to choose from.

        victimsList(list) : a list of player that were designated as victims. Only available if the witch's health potion is still available;
            default value is an empty list.
        """
        targets = []
        list = playerList[:]
        if saved:
            list.remove(saved)
        for player, role in self.memory:  # the witch first targets are the wolves she is aware of
            if player.camp != self.camp:
                targets.append(player)
            elif player.camp == self.camp:
                list.remove(player)
        if targets:  # if she is aware of werewolves the then kill one
            self.poisonVial = False
            print("The witch use poison on a wolf")
            return targets[randint(0, len(targets) - 1)]
        if victimsList:
            for v in victimsList:
                list.remove(v)
        # if she doesn't know any wolf she still can decide to kill someone
        if randint(0, 101) >= self.poisonUseChance:
            self.poisonVial = False
            chosenTarget = self
            chosenTarget = super().vote(list)
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
    "Rusted Sword Knight": Player,
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
    "Wolf-Dog": Player,
    "Abominable Sectarian": Player
}
lonerRoles = {
    "White Wolf": Player,
    "Angel": Player,
    "Pied Pipper": Player,
    "White Rabbit": Player
}
specialRoles = {
    "Pyromaniac": Player,
    "Raven": Player,
    "Gypsy": Player
}
