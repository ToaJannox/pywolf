import math

from player import Player
from random import shuffle

from time import sleep


from enums.phase import Phase
from enums.roleType import RoleType

DEFAULT_MAX_TURNS = 10
DELAY = 1


class Game:
    def __init__(self):
        self.player_list = []
        self.player_amount = 0
        self.phase = Phase.SETUP
        self.role_list = dict()
        self.victims = []
        self.max_turns = DEFAULT_MAX_TURNS
        self.current_turn = 0
        self.running = False
        self.player_factions = {"villagers": 0, "werewolves": 0, "others": 0}
        self.winning_faction = None

    def setup(self, roleList=[("Villager", 7), ("Werewolf", 3)]):
        print("Setting game up.")
        self.player_list = []
        for role, amount in roleList:
            pass
            # if role in villagerRoles:
            #     villagerAmount += amount
            #     for i in range(0, amount):
            #         player_list.append(villagerRoles[role]())
            # elif role in werewolfRoles:
            #     werewolfAmount += amount
            #     for i in range(0, amount):
            #         player_list.append(werewolfRoles[role]())
            # elif role in ambiguousRoles:
            #     ambiguousRoles += amount
            #     for i in range(0, amount):
            #         player_list.append(ambiguousRoles[role]())
            # elif role in lonerRoles:
            #     lonerAmount += amount
            #     for i in range(0, amount):
            #         player_list.append(lonerRoles[role]())
            # elif role in specialRoles:
            #     specialAmount += amount
            #     for i in range(0, amount):
            #         player_list.append(specialRoles[role]())
            # else:  # if role is unknown put villager instead
            #     raise ValueError("Unknown role", role)

        shuffle(self.player_list)
        i = 0
        for player in self.player_list:
            player.name = str(i) + "p"
            i += 1

    def first_night(self):
        self.night()

    def night(self):
        self.victims.append(self.wolfVote())
        self.phase = Phase.DAY

    def day(self):
        self.current_turn += 1
        self.victims.append(self.dayVote())
        self.phase = Phase.NIGHT

    def play(self):
        self.running = True
        while self.running:
            if self.phase == Phase.SETUP:
                print("\nSetup\n")
                self.phase = Phase.FIRST_NIGHT
            elif self.phase == Phase.FIRST_NIGHT:
                print("\nFirst Night\n")
                self.first_night()
            elif self.phase == Phase.NIGHT:
                print("\nNight\n")
                self.night()
            elif self.phase == Phase.DAY:
                print("Day\n")
                self.day()
            self.killVictims()
            self.victims = []
            if self.current_turn >= self.max_turns or self.check_game_end():
                self.running = False
            print("\nRemaining players: \n")
            for p in self.player_list:
                p.display()
                p.votes = 0
            print("-----------------------------------")
            sleep(DELAY)

        print("Game ended")
        print(f"Villager alive {self.player_factions['villagers']}")
        print(f"Werewolves alive {self.player_factions['werewolves']}")
        if self.winning_faction == RoleType.VILLAGER:
            print("The wolves have won!!")
        elif self.winning_faction == RoleType.WEREWOLF:
            print("The villagers have won!!")
        else:
            print("Player win")

    def count_alive_player_per_factions(self):
        for p in self.player_list:
            if p.role_type == RoleType.VILLAGER:
                self.player_factions["villagers"].append(p)
            elif p.role_type == RoleType.WEREWOLF:
                self.player_factions["werewolves"].append(p)
            else:
                self.player_factions["others"].append(p)

    def check_game_end(self):
        return self.player_factions["werewolves"] >= self.player_factions["villagers"]

    def wolf_setup(self):
        wolf_list = []
        for p in self.player_list:
            if p.role == "Werewolf":
                self.wolf_list.append(p)
        for p in wolf_list:
            p.allies = [a for a in wolf_list if a != p]

    def wolf_vote(self):
        result = 0
        highest_vote = 0
        for player in self.player_list:
            if player.role == "Werewolf" and player.alive:
                vote = player.vote(self.player_list)
                self.player_list[vote].votes += 1
        for player in self.player_list:
            if player.role == "Villager" and player.votes > highest_vote:
                highest_vote = player.votes
                result = self.player_list.index(player)
        print(f"Wolfs victim: {self.player_list[result].name}")
        return result

    def day_vote(self):
        result = 0
        highest_vote = 0
        for player in self.player_list:
            if player.alive:
                vote = player.vote(self.player_list)
                if player.isCaptain:
                    self.player_list[vote].votes += 2
                else:
                    self.player_list[vote].votes += 1
        for player in self.player_list:
            if player.votes > highest_vote:
                highest_vote = player.votes
                result = self.player_list.index(player)
        print(
            f"Chosen villager: {self.player_list[result].name} with  {self.player_list[result].votes} votes"
        )
        return result

    def kill_victims(self):
        for victim in self.victims:
            p = self.player_list[victim]
            p.death()
        self.count_alive_player_per_factions()


g = Game()

g.setup()
g.play()
