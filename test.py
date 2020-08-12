from player import *
from game import *
from unittest import TestCase


class WerewolfTest(TestCase):
    def testAll(self):
        self.testFrameWork()
        self.testGameSetup()
        self.testVote()
        self.testGetPlayers()
        self.testWolfVote()
        self.testLoverVote()
        self.testLoverCriticalVote()
    
    def testFrameWork(self):
        self.assertTrue(True)
        self.assertFalse(False)
        print("testFrameWork passed")
    
    def testGameSetup(self):
        g = Game(verbose=False)
        roleList = [
            ("Werewolf",2),
            ("Villager",10)
        ]
        g.setup(roleList)
        self.assertEqual(12,len(g.getPlayerList()))
        villagerCount = 0
        wereWolfCount = 0
        unknown = 0
        for p in g.getPlayerList():
            if p.role == "Villager":
                villagerCount+=1
            elif p.role  == "Werewolf":
                wereWolfCount+=1
            else:
                unknown +=1
        self.assertEqual(10,villagerCount)
        self.assertEqual(g.getVillagersAmount(),villagerCount)
        self.assertEqual(2,wereWolfCount)
        self.assertEqual(g.getWereWolvesAmount(),wereWolfCount)
        self.assertEqual(0,unknown)
        print("testGameSetup passed")
    def testVote(self):
        g = Game(verbose=False)
        g.addPlayer(Player())
        g.addPlayer(Player())
        g.addPlayer(Player())
        for p in g.getPlayerList():
            for _ in range(0,1000):
                self.assertNotEqual(p,p.vote(g.getPlayerList()))
                self.assertNotEqual(None,p.vote(g.getPlayerList()))
        print("testVote passed")
    def testGetPlayers(self):
        g = Game(verbose=False)
        for _ in range(0,10):
            g.addPlayer(Player())
        l = g.getPlayerList()
        del l[4]
        del l[1]
        self.assertEqual(len(l),8)
        self.assertEqual(len(g.getPlayerList()),10)
        self.assertNotEqual(l,g.getPlayerList())
        print("testGetPlayers passed")
    def testWolfVote(self):
        g = Game(verbose =False)
        v = []
        w = []
        for _ in range(0,4):
            p = Werewolf()
            g.addPlayer(p)
            w.append(p)
        for _ in range(0,20):
            p = Villager()
            g.addPlayer(p)
            v.append(p)
        g.wolfSetup()
        for p in w:
            for _ in range(0,1000):
                t = p.vote(g.getPlayerList())
                self.assertFalse(t in w)
                self.assertTrue(t in v)
        for p in w:
            for _ in range(0,1000):
                t = p.vote(g.getPlayerList(),night=True)
                self.assertFalse(t in w)
                self.assertTrue(t in v)
        print("testWolfVote passed")
    def testLoverVote(self):
        g = Game(verbose=False)
        l1 = Player()
        l2 = Player()
        for _ in range(0,5):
            g.addPlayer(Player())
        g.addPlayer(l1)
        g.addPlayer(l2)
        l1.lover = l2
        l2.lover = l1
        for _ in range(0,1000):
            self.assertNotEqual(l1.vote(g.getPlayerList()),l2)
            self.assertNotEqual(l2.vote(g.getPlayerList()),l1)
        print("testLoverVote passed")
    def testLoverCriticalVote(self):
        l1 = Villager()
        l2 = Werewolf()
        l1.lover = l2
        l2.lover = l1
        w = Werewolf()
        v = Villager()

        g = Game(verbose=False)
        g.addPlayer(l1)
        g.addPlayer(l2)
        g.addPlayer(v)
        for _ in range(0,1000):
            self.assertEqual(v , l1.vote(g.getPlayerList()) )
            self.assertEqual(v , l2.vote(g.getPlayerList()) )

        # g = Game(verbose=False)

        print("testLoverCriticalVote passed")
    
    
    



wt = WerewolfTest()
wt.testAll()