import math

from player import Player,Werewolf,Villager
from random import shuffle

from time import sleep


from enums.phase import Phase
from enums.roleType import RoleType

DEFAULT_MAX_TURNS = 10
DELAY = 1
MIN_PLAYER = 8
MAX_WOLF_ROLES = 8

class Game:
    def __init__(self):
        self.player_list = []
        self.player_amount = 0
        self.phase = Phase.SETUP
        self.role_dict = dict()
        self.victims = []
        self.max_turns = DEFAULT_MAX_TURNS
        self.current_turn = 0
        self.running = False
        self.player_factions = {"villagers": [], "werewolves": [], "others": []}
        self.winning_faction = None

    def setup(self):
        print("Setting game up.")
        while True:
            self.player_amount = int(input(f"How many player? (>={MIN_PLAYER})  "))
            if self.player_amount >= MIN_PLAYER:
                break;
            print(f"Number of Players must at least be {MIN_PLAYER}")
        print(f"{self.player_amount} playing")
        werewolves = min(math.floor(self.player_amount*0.25),MAX_WOLF_ROLES)
        villagers = self.player_amount - werewolves
        for w in range(0,werewolves):
            p = Werewolf()
            self.player_list.append(p)
            self.player_factions["werewolves"].append(p)
        for v in range(0,villagers):
            p = Villager()
            self.player_list.append(p)
            self.player_factions["villagers"].append(p)
        shuffle(self.player_list)
        self.show_faction_status()
        
        for idx,p in enumerate(self.player_list):
            p.set_name(f"Player {idx}")
        for p in self.player_list:
            p.set_memory(self.player_list)
        self.true_show_players()
        
        

    def first_night(self):
        w = self.player_factions["werewolves"]
        for p in w:
            p.learn_allies(w)
        # self.night()



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

    def show_faction_status(self):
        v = len(self.player_factions["villagers"])
        w = len(self.player_factions["werewolves"])
        print(f"{v} villagers | {w} werewolves")
    def show_players(self):
        for p in self.player_list:
            p.display()

    def true_show_players(self):
        for p in self.player_list:
            p.true_display()

    def game_credits(self):
        print(
            """
            Thanks for playing my game
            Made as a side project for my own fun and love of programming
            """)
