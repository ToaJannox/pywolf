
# Pywolf

Python3.x version of the werewolf game

# How to Play  
For now the game plays itself and now real interaction can be made.
You'll have to edit the code for changing certains parameters
Nevertheless to launch the game just type:

	python3 game.py
## Game rules

The goal of this game is simple:

- **Villagers** are trying to eliminate all the werewolves either by vote during the day or by using their powers
- **Werewolves** are trying to eliminate all the villagers by killing them during the night and trying to kill them during the day vote
- **Other players** might receive *certains* roles that make them play by themselves against  all the villagers and the wolves, so they can only count on them
- Once there is no more villager, werewolf or that special conditions (that comes with certains characters) are met, the game is over

## Current implemented roles

- **Villager:** The simplest role. During the day they try to eliminate all the werewolves by voting during the day.
- **Werewolves:** They have to kill all the villagers. During the night they vote for a victim. They can also vote during the day. Either way, a werewolf can't vote against another one.
- **Fortune Teller:** Each night, the Fortune Teller can choose one another player and discover it's role.
- **Hunter:** Upon it's death, he choose a player to join him in death.
- **Cupid:** During the first night, Cupid choose two player (he can choose himself), those two will be lovers. Upon one of the lover's death, the other will rejoin him in death.
- **Witch:** Possess a healing potion and a poison vial. She can use each once per game. Each night while she still can use here healing potion, the victim will be revealed to her. She can decide to heal that victim or not.
Each night she can also use here poison vial to kill someone she suspect

## Game flow

### 1st night
- Roles are give
