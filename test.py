from player import *
from game import *
from unittest import TestCase

testAmount = 10000
class WerewolfTest(TestCase):

    def testAll(self):
        try:
            self.testFrameWork()
            print("testFramework passed")
        except:
            print("testFramework failed")
        try:
            self.testGameSetup()
            print("testGameSetup passed")
        except:
            print("testGameSetup failed")
        try:
            self.testVote()
            print("testVote passed")
        except:
            print("testVote failed")
        try:
            self.testGetPlayers()
            print("testGetPlayers passed")
        except:
            print("testGetPlayers failed")
        try:
            self.testWolfVote()
            print("testWolfVote passed")
        except:
            print("testWolfVote failed")
        try:
            self.testLoverVote()
            print("testLoverVote passed")
        except:
            print("testLoverVote failed")
        try:
            self.testLoverCriticalVote()
            print("testLoverCriticalVote passed")
        except:
            print("testLoverCriticalVote failed")
        try:
            self.testWitch()
            print("testWitch passed")
        except:
            print("testWitch failed")

            
            
    
    def testFrameWork(self):
        self.assertTrue(True)
        self.assertFalse(False)
    
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
    def testVote(self):
        g = Game(verbose=False)
        g.addPlayer(Player())
        g.addPlayer(Player())
        g.addPlayer(Player())
        for p in g.getPlayerList():
            for _ in range(0,testAmount):
                self.assertNotEqual(p,p.vote(g.getPlayerList()))
                self.assertNotEqual(None,p.vote(g.getPlayerList()))
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
            for _ in range(0,testAmount):
                t = p.vote(g.getPlayerList())
                self.assertFalse(t in w)
                self.assertTrue(t in v)
        for p in w:
            for _ in range(0,testAmount):
                t = p.vote(g.getPlayerList(),night=True)
                self.assertFalse(t in w)
                self.assertTrue(t in v)
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
        for _ in range(0,testAmount):
            self.assertNotEqual(l1.vote(g.getPlayerList()),l2)
            self.assertNotEqual(l2.vote(g.getPlayerList()),l1)
    def testLoverCriticalVote(self):
        l1 = Villager()
        l2 = Werewolf()
        l1.lover = l2
        l2.lover = l1
        w = []
        v = []
        for _ in range(0,4):
            w.append(Werewolf())
        for _ in range(0,10):
            v.append(Villager())
        # testing that a villager lover can betray correctly it's fellow villagers to save his love
        g = Game(verbose=False)
        g.addPlayer(l1)
        g.addPlayer(l2)
        for p in v :
            g.addPlayer(p)

        for _ in range(0,testAmount):
            t1 = l1.vote(g.getPlayerList())
            t2 = l2.vote(g.getPlayerList())
            self.assertTrue(t1 in v)
            self.assertTrue(t2 in v)
        # testing that a wolf lover can betray correctly it's fellow wolves to save his love
        g = Game(verbose=False)
        g.addPlayer(l1)
        g.addPlayer(l2)
        for p in w :
            g.addPlayer(p)

        for _ in range(0,testAmount):
            t1 = l1.vote(g.getPlayerList())
            t2 = l2.vote(g.getPlayerList())
            self.assertTrue(t1 in w)
            self.assertTrue(t2 in w)
        for _ in range(0,testAmount):
            t = l2.vote(g.getPlayerList(),True)
            self.assertTrue(t in w)
    
    def testWitch(self):
        witch = Witch()
        l1 = Villager()
        l2= Werewolf()
        villagers =[]
        wolves = []
        victims = []
        for _ in range(0,4):
            villagers.append(Villager())

        for _ in range(0,2):
            wolves.append(Werewolf())
        g = Game(verbose=False)
        
        g.addPlayer(witch)
        g.addPlayer(l1)
        g.addPlayer(l2)
        for w in wolves:
            g.addPlayer(w)
        for v in villagers:
            g.addPlayer(v)
        
        witch.lover = l1
        victims.append(l1)
        s = witch.heal(victims)
        # self.assertEqual(witch.heal([l1]),l1)
        # self.assertEqual(witch.heal(self),self)
        



    



wt = WerewolfTest()
wt.testAll()