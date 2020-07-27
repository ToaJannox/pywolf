import math
from player import *
from random import shuffle
from enum import Enum
from time import sleep
import os


class Phase(Enum):
    SETUP = 0
    FIRST_NIGHT = 1
    NIGHT = 2
    DAY = 3


delay = 5
playerAmount = 0
werewolfAmount = 0
villagerAmount = 0
ambiguousAmount = 0
lonerAmount = 0
specialAmount = 0
playerList = []
presentRoles = []
phase = Phase.SETUP



def setup(roleList):
    global playerList, playerAmount, werewolfAmount, villagerAmount
    print("Setting game up.")
    playerList = []
    for role, amount in roleList:
        if role in villagerRoles:
            villagerAmount += amount
            for i in range(0,amount):
                playerList.append(villagerRoles[role]())
        elif role in werewolfRoles:
            werewolfAmount += amount
            for i in range(0,amount):
                playerList.append(werewolfRoles[role]())
        elif role in ambiguousRoles:
            ambiguousAmount += amount
            for i in range(0,amount):
                playerList.append(ambiguousRoles[role]())
        elif role in lonerRoles:
            lonerAmount += amount
            for i in range(0,amount):
                playerList.append(lonerRoles[role]())
        elif role in specialRoles:
            specialAmount +=amount
            for i in range(0,amount):
                playerList.append(specialRoles[role]())
        else: #if role is unknown put villager instead
            raise ValueError("Unknown role",role)
        if role not in presentRoles:
            presentRoles.append(role)
        print(str(amount)+" * "+role)
    shuffle(playerList)
    i = 0
    for player in playerList:
        player.name = str(i)+"p"
        i += 1


def play():
    global phase, playerList
    running = True
    victims = []
    turn = 0
    while running:
        if phase == Phase.SETUP:
            print("Setup - Turn "+str(turn))
            print("-----------------------------------")
            phase = Phase.FIRST_NIGHT
        elif phase == Phase.FIRST_NIGHT:
            print("First Night - Turn "+ str(turn))
            print("-----------------------------------")
            night(victims,True)
            phase = Phase.DAY
        elif phase == Phase.NIGHT:
            print("Night - Turn "+str(turn))
            print("-----------------------------------")
            night(victims)
            phase = Phase.DAY
        elif phase == Phase.DAY:
            print("Day - Turn "+str(turn))
            print("-----------------------------------")
            day(victims)
            turn += 1
            phase = Phase.NIGHT
        killVictims(victims)
        victims.clear()
        if villagerAmount == 0 or werewolfAmount == 0:
            running = False
        print("-----------------------------------")
        print("Remaining players:")
        print("\tRemaining villagers:" +str(villagerAmount))
        print("\tRemaining wolves:" +str(werewolfAmount))
        print("\tRemaining loners:" +str(lonerAmount))
        print("\tRemaining ambiguous:" +str(ambiguousAmount))
        print("\tRemaining specials:" +str(specialAmount))
        print("-----------------------------------")
        for p in playerList:
            p.display()
            p.votes = 0
        print("+---------------------------------+")
        sleep(delay)
        os.system('cls' if os.name =='nt' else 'clear')
        print("+---------------------------------+")
    os.system('cls' if os.name =='nt' else 'clear')
    print("Game ended")
    print("Villager alive " + str(villagerAmount))
    print("Werewolves alive " + str(werewolfAmount))

    if villagerAmount == 0:
        print("The wolves have won!!")
    elif werewolfAmount == 0:
        print("The villagers have won!!")

def night(victims,firstNight=False):
    global playerList

    if firstNight:
        p = findPlayer("Cupid")
        if p:
            p.chooseLovers(playerList)

    p = findPlayer("Fortune Teller")
    if p:
        p.tellFortune(playerList)

    if firstNight:
        wolfSetup()
    victim = wolfVote()

    victims.append(victim)
    p = findPlayer("Witch")
    if p:
        witchSave = None
        if p.healthPotion:
            witchSave = p.heal(victim,victims,playerList)
        if p.poisonVial:
            witchVictim = p.poison(witchSave,playerList)
            if witchVictim:
                victims.append(witchVictim)



    if "Cupid" in presentRoles: #check if the lover were killed if Cupid is present
        victimLover = None
        for i in victims:
            p = playerList[i] 
            victimLover = p.lover 
        if victimLover:            
            victims.append(playerList.index(victimLover))

def day(victims):
    global playerList
    victim = dayVote()
    victims.append(victim)
    if "Cupid" in presentRoles: #check if the lover were killed if Cupid is present
        victimLover = None
        for i in victims:
            p = playerList[i] 
            victimLover = p.lover 
        if victimLover:            
            victims.append(playerList.index(victimLover))

def findPlayer(role):
    global playerList,presentRoles

    if role in presentRoles:
        for p in playerList:
            if p.role == role and p.alive:
                return p
    else:
        return None

def wolfSetup():
    global playerList
    wolfList = []
    for p in playerList:
        if p.role in werewolfRoles:
            wolfList.append(p)
    for p in wolfList:
        p.allies = [a for a in wolfList if a != p]


def wolfVote():
    global playerList
    result = 0
    highestVote = 0
    for player in playerList:
        if player.role == "Werewolf" and player.alive:
            vote = player.vote(playerList)
            playerList[vote].votes += 1
    for player in playerList:
        if player.role == "Villager":
            if player.votes > highestVote:
                highestVote = player.votes
                result = playerList.index(player)
    print("Wolfs victim: "+playerList[result].name)
    return result



def dayVote():
    global playerList
    result = 0
    highestVote = 0
    for player in playerList:
        if player.alive:
            vote = player.vote(playerList)
            if player.isCaptain:
                playerList[vote].votes += 2
            else:
                playerList[vote].votes += 1
    for player in playerList:
        if player.votes > highestVote:
            highestVote = player.votes
            result = playerList.index(player)
    print("Chosen villager: "+playerList[result].name + " with "+str(playerList[result].votes)+" votes")
    return result


def killVictims(list,displayResults = True):
    global playerList, werewolfAmount, villagerAmount
    if not list:
        print("Nobody died !!!!")
    for victim in list:
        p = playerList[victim]
        p.display
        p.alive = False
        print("Player " + p.name + " is now dead and was a " + p.role)
        if p.lover:
            print(p.name+" lover, "+p.lover.name+" followed his love in death")
        if p.role == "Hunter":
            killVictims([p.shootOnDeath(playerList)],False)
    if displayResults:
        villagers = 0
        wolves = 0
        ambiguous = 0
        loner = 0
        special = 0
        for p in playerList:
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
        villagerAmount = villagers
        werewolfAmount = wolves
        ambiguousAmount = ambiguous
        lonerAmount = loner
        special = special

list =[
    ("Werewolf",4),
    ("Villager",6),
    ("Fortune Teller",1),
    ("Hunter",1),
    ("Cupid",1),
    ("Witch",1)
]
os.system('cls' if os.name =='nt' else 'clear')
setup(list)
print("+---------------------------------+")
play()
