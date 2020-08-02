import math
from player import *
from random import shuffle
from enum import Enum
from time import sleep
import os


class Phase(Enum):
    SETUP = 0
    NIGHT = 1
    DAY = 2


class Game:
    def __init__(self):
        self.__playerAmount = 0
        self.__villagerAmount = 0
        self.__werewolfAmount = 0
        self.__ambiguousAmount = 0
        self.__lonerAmount = 0
        self.__specialAmount = 0
        self.__turns = 0
        self.__maxFailedVotes = 20

        self.__playerList = []
        self.__presentRoles =[]
        self.__victimsList =[]

        self.__phase = Phase.SETUP

        self.__running = False
    
    def setup(self,roleList):
        self.__playerList.clear()
        for role, amount in roleList:
            if role in villagerRoles:
                self.__villagerAmount += amount
                for i in range(0,amount):
                    self.__playerList.append(villagerRoles[role]())
            elif role in werewolfRoles:
                self.__werewolfAmount += amount
                for i in range(0,amount):
                    self.__playerList.append(werewolfRoles[role]())
            elif role in ambiguousRoles:
                self.__ambiguousAmount += amount
                for i in range(0,amount):
                    self.__playerList.append(ambiguousRoles[role]())
            elif role in lonerRoles:
                self.__lonerAmount += amount
                for i in range(0,amount):
                    self.__playerList.append(lonerRoles[role]())
            elif role in specialRoles:
                self.__specialAmount +=amount
                for i in range(0,amount):
                    self.__playerList.append(specialRoles[role]())
            else: #if role is unknown put villager instead
                raise ValueError("Unknown role",role)
            if role not in self.__presentRoles:
                self.__presentRoles.append(role)
            print(str(amount)+" * "+role)
        shuffle(self.__playerList)
        i = 0
        for player in self.__playerList:
            player.name = str(i)+"p"
            i += 1

    def play(self):
        self.__running = True
        while self.__running:
            if self.__phase == Phase.SETUP:
                print("Setup - Turn "+str(self.__turns))
                print("-----------------------------------")
                self.__phase = Phase.NIGHT
            elif self.__phase == Phase.NIGHT:
                if self.__turns ==0:
                    print("First Night - Turn "+ str(self.__turns))
                else:
                    print("Night - Turn "+str(self.__turns))
                print("-----------------------------------")
                self.night()
                self.__phase = Phase.DAY
            elif self.__phase == Phase.DAY:
                print("Day - Turn "+str(self.__turns))
                print("-----------------------------------")
                self.day()
                self.__turns += 1
                self.__phase = Phase.NIGHT
            self.killVictims()
            self.__victimsList.clear()
            if self.__victimsList:
                raise ValueError("List should be clear",self.__victimsList)
            if self.__villagerAmount == 0 or self.__werewolfAmount == 0:
                self.__running = False
            print("-----------------------------------")
            print("Remaining players: ",end="")
            print("\tvillagers:" +str(self.__villagerAmount),end="")
            print("\twolves:" +str(self.__werewolfAmount),end="")
            print("\tloners:" +str(self.__lonerAmount),end="")
            print("\tambiguous:" +str(self.__ambiguousAmount),end="")
            print("\tspecials:" +str(self.__specialAmount))
            print("-----------------------------------")
            for p in self.__playerList:
                p.display()
                p.votes = 0
            print("+---------------------------------+")
            input("Press any key to continue...")
            # os.system('cls' if os.name =='nt' else 'clear')
            print("+---------------------------------+")
        os.system('cls' if os.name =='nt' else 'clear')
        print("Game ended")
        print("Villager alive " + str(self.__villagerAmount))
        print("Werewolves alive " + str(self.__werewolfAmount))

        if self.__villagerAmount == 0:
            print("The wolves have won!!")
        elif self.__werewolfAmount == 0:
            print("The villagers have won!!")
            
    def day(self):
        victim = self.dayVote()
        self.__victimsList.append(victim)
    
    def night(self):
        firstNight = self.__turns == 0
        if firstNight:
            self.playerUsePower("Cupid")

        self.playerUsePower("Fortune Teller")
        
        if firstNight:
            self.wolfSetup()
        victim = self.nightVote()
        self.__victimsList.append(victim)

        self.playerUsePower("Witch")

    def wolfSetup(self):
        wolfList = []
        for p in self.__playerList:
            if p.role in werewolfRoles:
                wolfList.append(p)
        for p in wolfList:
            p.allies = [a for a in wolfList if a != p]
    
    def dayVote(self):
        print("The village is deciding who it will eliminate")
        voteDone = False
        failedVotes = 0
        while not voteDone:
            equality = False
            result = None
            highestVote = 0
            if failedVotes!=0:
                for player in self.__playerList:
                    player.votes = 0
            if failedVotes == self.__maxFailedVotes:
                raise ValueError("Vote Failed")
            for player in self.__playerList:
                if player.alive:
                    # print("Player "+player.name+" votes")
                    votedPlayer = player.vote(self.getPlayerList())
                    if player.isCaptain:
                        votedPlayer.votes += 2
                    else:
                        votedPlayer.votes += 1
            for player in self.__playerList:
                if player.votes > highestVote:
                    equality = False
                    highestVote = player.votes
                    result = player
            for player in self.__playerList:
                if player.votes == result.votes and player != result:
                    equality = True

            if equality:
                print("An equality occured! Vote restarts!!")
                print("\tPlayer "+result.name+" was the chosen player")
                failedVotes += 1
            elif not result.alive:
                print("Victim chosen among the deads! Vote Restarts!!")
                print("\tThe chosen victim: "+ result.name +" is already dead!")
                failedVotes += 1
            else:
                voteDone = True

        print("Chosen villager: "+result.name + " with "+str(result.votes)+" votes")
        return result

    def nightVote(self):
        print("The Werewolves are choosing their victim!")
        voteDone = False
        failedVotes = 0
        while not voteDone:
            equality = False
            result = None
            highestVote = 0
            if failedVotes!=0:
                for player in self.__playerList:
                    player.votes = 0
            if failedVotes == self.__maxFailedVotes:
                raise ValueError("Vote Failed")
            
            for player in self.__playerList:
                if player.camp == "Werewolf" and player.alive:
                    # print("Player "+player.name+" votes")
                    votedPlayer = player.vote(self.getPlayerList())
                    votedPlayer.votes += 1
            for player in self.__playerList:
                if player.camp == "Villager":
                    if player.votes > highestVote:
                        equality = False
                        highestVote = player.votes
                        result = player

            for player in self.__playerList:
                if player.votes == result.votes and player != result:
                    equality = True

            if equality:
                print("An equality occured. Vote restarts!")
                print("\tPlayer "+result.name+" was the chosen player")
                failedVotes+=1
            elif not result.alive:
                print("Victim chosen among the deads! Vote Restarts!!")
                print("\tThe chosen victim: "+ result.name +" is already dead!")
                failedVotes += 1
            else:
                voteDone = True
        print("Wolfs victim: "+result.name)
        return result
    
    def killVictims(self):
        if not self.__victimsList:
            print("Nobody died !!!!")
        additionalVictims= []
        for victim in self.__victimsList:
            victim.display
            victim.alive = False
            print("Player " + victim.name + " is now dead and was a " + victim.role)
            if victim.lover:
                victim.lover.deathAnnounced = True
                print(victim.name+" lover: "+victim.lover.name+", followed his love in death")
                print("Player " + victim.lover.name + " is now dead and was a " + victim.lover.role)
                additionalVictims.append(victim.lover)
            if victim.role == "Hunter":
                hunterVictim = victim.usePower(self)
                print("On his dying breath, the Hunter killed "+hunterVictim.name)
                print("Player " + hunterVictim.name + " is now dead and was a " + hunterVictim.role)
                additionalVictims.append(hunterVictim) 
        for victim in additionalVictims:
            victim.alive = False

        villagers = 0
        wolves = 0
        ambiguous = 0
        loner = 0
        special = 0
        for p in self.__playerList:
            if p.alive:
                if p.role in villagerRoles:
                    villagers += 1
                elif p.role in werewolfRoles:
                    wolves += 1
                elif p.role in ambiguousRoles:
                    ambiguous += 1
                elif p.role in lonerRoles:
                    loner += 1
                elif p.role in specialRoles:
                    special += 1
        self.__villagerAmount = villagers
        self.__werewolfAmount = wolves
        self.__ambiguousAmount = ambiguous
        self.__lonerAmount = loner
        self.__specialAmount = special
        for p in self.__playerList:
                p.forgetDeadPlayers()
    
    def playerUsePower(self,role):
        player = None
        if role in self.__presentRoles:
            for p in self.__playerList:
                if p.role == role and p.alive:
                    player = p
        if player:
            return player.usePower(self)
    
    def getPlayerList(self):
        return self.__playerList[:]
    
    def getVictimsList(self):
        return self.__victimsList


roleList =[
    ("Werewolf",4),
    ("Villager",6),
    ("Fortune Teller",1),
    ("Hunter",1),
    ("Cupid",1),
    ("Witch",1)
]
g = Game()
# os.system('cls' if os.name =='nt' else 'clear')
g.setup(roleList)
print("+---------------------------------+")
g.play()
