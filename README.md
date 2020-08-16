
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

## Roles
**Legend**
 - [ ] not yet implemented
 - [x] implemented

### Villager Camp

Their goal is to survive and eliminate all the werewolves

- [x] **Villager:** It's task is to survive and eliminate all the Werewolves

- [x] **Villager-Villager:** A Villager whose role isn't hidden

- [x] **Fortune Teller:** Each night, the Fortune Teller is called and can choose any other player. That player role will be revealed to the Fortune Teller

- [x] **Hunter:** Upon death, the Hunter will choose any other player that will be also eliminated

- [x] **Cupid:** During the first night, Cupid chooses two players and make them fall in love.
Lovers must survive until the end of the game. If one of them die, the other will follow.

- [x] **Witch:** The Witch has healing potion and a poison vial. Each night The Witch can choose to use any of it once per game.
The healing potion save any victim from death. The poison kill someone else.

- [ ] **Little Girl:** The Little girl can try to discretly observe the Werewolves when they are waked up. Will be killed if caught.

- [ ] **Guard:** The Guard can each night choose a player that will be protected from dying. However he can't choose twice the same player in a row.

- [ ] **Ancient:** The Ancient can survive twice against Werewolves attack. If the Ancient dies by any other way, all players will lose their power if they posses one.

- [ ] **Scapegoat:** The Scapegoat gets automatically  eliminated during day votes if a tie occurs. He will choose who can't vote the next day.

- [ ] **Idiot:** The Idiot can be eliminated through vote. Instead he'll loose is right to vote afterwards.

- [ ] **Two Sisters:** The Two sisters know each other and can take decisions together

- [ ] **Three Brothers:** The Three Brothers know each other and can take decision together

- [ ] **Fox:** The Fox can each night choose a player along it's left and right direct neighbors. If any of them is a Werewolf the Fox will get informed. If none are, the Fox loses it's power.

- [ ] **Bear Tamer:** Each day, if any of the Bear Tamer's direct neighbor is a Werewolf, the Bear Tamer get's notified.

- [ ] **Stuttering Judge:** The Stuttering Judge can once per game, make a second day vote take place.

- [ ] **Rusty Sword Knight:** If The Rusty Sword Knight is killed by the Werewolves, the first Werewolf on it's left will die the follwing night.

### Wolf Camp

Their goal is to devour and eliminate all villagers and survive until the end

- [x] **Werewolves:** It'stask is to survive and eliminate all the Villagers

- [ ] **Big Bad Wolf:** Until any Werewolf dies, he can alone, choose an additionnal victim.

- [ ] **Vile Father of Wolves:** Once per game, the Vile Father of Wolves can decide that the Werewolves victim will be infected instead of being killed. The infected is now a Werewolf.

### Uncertain Role

Those role can switch camp during the game. Their goal is tied to the camp they currently are in, they can play as villagers, as werewolves or bmaybe both.

- [ ] **Thief:** The first night the Thief can choose between one of two unknown roles that were prepared and incarnate it until the end of the game. To win, the Thief must win with the camp the new role represents

- [ ] **Devoted Maid:** Before any death annoucement, the Devoted Servant can reveal it's identiy and take the role of the deceased player. She then get's that role power.

- [ ] **Actor:** The Actor starts the game with 3 additionnal roles. Those roles are revealed to the other player, it cannot be Werewolves. The Actor can use any of those 3 roles until the next night once per game.

- [ ] **Wild Child:** At the start of the game the Wild Child chooses another player to be it's person to look up to. As long as that player is alive, the Wild Child is a Villager. If that player dies, the Wild Child will now act like a Werewolf

- [ ] **Dog-Wolf:** During the first night, the Dog-Wolf can choose to act like a Villager or like a Werewolf. This is a definitive choice.

### Loner Roles

They have only one interest: themselves. They must achieve their own personal goal in order to win.

- [ ] **White Wolf:** The White Wolf is a Werewolf that can kill another Werewolf every two-night. He must be the last man standing in ordr to win.

- [ ] **Angel:** The Angel goals is to be killed during the first turn in order to win. For that the game will first begin with a day vote, followed by the normal first night. The Angel turns into a Villager if he did not get executed during the first turn.

- [ ] **Pied Pipper:** Each night the Pied Pipper charms two players. When all players except the Pied Pipper are charmed, the game ends with the Pied Pipper being victorious. Charmed players are called each night to know how much uncharmed player is left.

- [ ] **Abominable Sectarian:** At the begining of the game, the players are divided in two groups. The goal of the Abominable Sectarian is to kill all players in the group he's not present.

## Game flow

### 1st night
- Roles are give

# TODOs
fix the vote functions