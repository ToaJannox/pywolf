import math
from player import *
from random import shuffle
from enum import Enum
from time import sleep


class Phase(Enum):
    SETUP = 0
    FIRST_NIGHT = 1
    NIGHT = 2
    DAY = 3


delay = 3
playerAmount = 0
werewolfAmount = 0
villagerAmount = 0
ambiguousAmount = 0
lonerAmount = 0
specialAmount = 0

playerList = []
phase = Phase.SETUP



def setup(roleList=[("Villager", 7), ("Werewolf", 3)]):
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
            ambiguousRoles += amount
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
        
    shuffle(playerList)
    i = 0
    for player in playerList:
        player.name = str(i)+"p"
        i += 1


def play():
    global phase, playerList
    max_turn = 10
    cpt = 0
    running = True
    victims = []
    while running:
        if phase == Phase.SETUP:
            print("\nSetup\n")
            phase = Phase.FIRST_NIGHT
        elif phase == Phase.FIRST_NIGHT:
            print("\nFirst Night\n")
            wolfSetup()
            victims.append(wolfVote())
            phase = Phase.DAY
        elif phase == Phase.NIGHT:
            print("\nNight\n")
            victims.append(wolfVote())
            phase = Phase.DAY
        elif phase == Phase.DAY:
            print("Day\n")
            cpt += 1
            victims.append(dayVote())
            phase = Phase.NIGHT
        killVictims(victims)
        victims.clear()
        if cpt == max_turn or villagerAmount == 0 or werewolfAmount == 0:
            running = False
        print("\nRemaining players: \n")
        for p in playerList:
            p.display()
            p.votes = 0
        print("-----------------------------------")
        sleep(delay)

    print("Game ended")
    print("Villager alive " + str(villagerAmount))
    print("Werewolves alive " + str(werewolfAmount))
    if villagerAmount == 0:
        print("The wolves have won!!")
    elif werewolfAmount == 0:
        print("The villagers have won!!")


def wolfSetup():
    global playerList
    wolfList = []
    for p in playerList:
        if p.role == "Werewolf":
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
    print("Chosen villager: "+playerList[result].name +
          " with "+str(playerList[result].votes)+" votes")
    return result


def killVictims(list):
    global playerList, werewolfAmount, villagerAmount
    for victim in list:
        p = playerList[victim]
        p.display
        p.alive = False
        print("Player " + p.name + " is now dead and was a " + p.role)
    villagers = 0
    wolves = 0
    for p in playerList:
        if p.alive:
            if p.role == "Villager":
                villagers += 1
            else:
                wolves += 1
    if villagers < villagerAmount:
        villagerAmount = villagers
    if wolves < werewolfAmount:
        werewolfAmount = wolves


setup()
play()
