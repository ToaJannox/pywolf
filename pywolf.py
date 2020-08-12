from game import Game
roleList = [
    ("Werewolf", 4),
    ("Villager", 6),
    ("Fortune Teller",1),
    ("Hunter",1),
    ("Witch",1),
    ("Cupid",1),
    ("Villager-Villager",1)
]
g = Game()
g.setup(roleList)
g.play()
