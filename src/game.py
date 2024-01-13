import math

from random import shuffle

from time import sleep
from typing import List, Dict

from enums.phase_enum import PhaseEnum
from src.enums.faction_flag import FactionFlag
from factions.faction_dict import FactionDict

from player_role.player import Player
from player_role.werewolves import Werewolf
from player_role.villagers import Villager
from voting_system.vote_system import VoteSystem

DEFAULT_MAX_TURNS = 10
DELAY = 1
MIN_PLAYER = 8
MAX_WOLF_ROLES = 8


vote_system = VoteSystem()

class Game:
    def __init__(self):
        self.player_list: List[Player]  = []
        self.player_amount: int = 0
        self.phase: PhaseEnum = PhaseEnum.SETUP
        self.role_dict: Dict[str,int] = dict()
        self.victims: List[Player] = []
        self.max_turns: int = DEFAULT_MAX_TURNS
        self.current_turn: int = 0
        self.running: bool = False
        self.player_factions: FactionDict
        self.winning_faction: FactionFlag = None

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
        for _ in range(0,werewolves):
            p = Werewolf()
            self.player_list.append(p)
            self.player_factions["werewolves"].append(p)
        for _ in range(0,villagers):
            p = Villager()
            self.player_list.append(p)
            self.player_factions["villagers"].append(p)
        shuffle(self.player_list)
        self.show_faction_status()
        
        for idx,p in enumerate(self.player_list):
            p.set_name(f"Player {idx}")
        for p in self.player_list:
            p.init_memory(self.player_list)
        self.true_show_players()
        
        

    def first_night(self):
        w = self.player_factions["werewolves"]
        for p in w:
            p.learn_allies(w)
        # self.night()



    def night(self):
        victim = self.wolf_vote()
        if victim:
            self.victims.append(self.wolf_vote())
        self.phase = PhaseEnum.DAY

    def day(self):
        self.current_turn += 1
        victim = self.day_vote()
        if victim:
            self.victims.append(victim)
        self.phase = PhaseEnum.NIGHT

    def play(self):
        self.running = True
        while self.running:
            if self.phase == PhaseEnum.SETUP:
                print("\nSetup\n")
                self.phase = PhaseEnum.FIRST_NIGHT
            elif self.phase == PhaseEnum.FIRST_NIGHT:
                print("\nFirst Night\n")
                self.first_night()
            elif self.phase == PhaseEnum.NIGHT:
                print("\nNight\n")
                self.night()
            elif self.phase == PhaseEnum.DAY:
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
        if self.winning_faction == FactionFlag.VILLAGER:
            print("The wolves have won!!")
        elif self.winning_faction == FactionFlag.WEREWOLF:
            print("The villagers have won!!")
        else:
            print("Player win")

    def count_alive_player_per_factions(self):
        for p in self.player_list:
            if FactionFlag.VILLAGER in p.faction:
                self.player_factions["villagers"].append(p)
            elif FactionFlag.WEREWOLF in p.faction:
                self.player_factions["werewolves"].append(p)
            else:
                self.player_factions["others"].append(p)

    def check_game_end(self):
        return len(self.player_factions["villagers"]) == 0 or len(self.player_factions["werewolves"]) == 0

    def wolf_setup(self):
        wolf_list = []
        for p in self.player_list:
            if p.role == "Werewolf":
                self.wolf_list.append(p)
        for p in wolf_list:
            p.allies = [a for a in wolf_list if a != p]

    def wolf_vote(self) -> Player:
        return vote_system.vote(self.player_factions["werewolves"])

    def day_vote(self) -> Player:
        return vote_system(self.player_list)

    def kill_victims(self) -> None:
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
