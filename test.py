from player import *
from game import *
from unittest import TestCase

testAmount = 10000
class WerewolfTest(TestCase):
    totalTest = 0
    currentTestRunned = 0
    totalTestPassed = 0

    def test(self,func):
        
        print("\nRunning test "+str(self.currentTestRunned)+"/"+str(self.totalTest)+" : "+func.__name__)
        try:
            func()
            print("\t\033[38;5;10m"+func.__name__+ " passed\033[m")
            self.totalTestPassed += 1
        except Exception as e:
            print("\t\033[38;5;9m"+func.__name__ +" failed\033[m")
            print(e)
    def testAll(self):
        testList = []
        testList.append(self.testFrameWork)
        testList.append(self.testGameSetup)
        testList.append(self.testVote)
        testList.append(self.testGetPlayers)
        testList.append(self.testWolfVote)
        testList.append(self.testLoverVote)
        testList.append(self.testLoverCriticalVote)
        testList.append(self.testWitchHeal)
        self.totalTest = len(testList)
        for t in testList:
            self.currentTestRunned += 1
            self.test(t)

        print("\n"+str(self.totalTestPassed) + " out of "+str(self.totalTest) +" passed")
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
    
    def testWitchHeal(self):
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
        # lovers tests
        witch.lover = l1
        victims.append(l1)
        self.assertEqual(witch.heal(victims),l1)
        witch.lover = None
        victims.clear()

        witch.lover = l2
        victims.append(l2)
        self.assertEqual(witch.heal(victims),l2)
        witch.lover = None
        victims.clear()
        #  self heal test
        victims.append(witch)
        self.assertEqual(witch.heal(victims),witch)
        victims.clear()
        
        # no memory test
        victims.append(villagers[0])
        victims.append(villagers[2])
        
        for _ in range(0,testAmount):
            self.assertTrue(witch.heal(victims[:]) in [villagers[0],villagers[2],None])
        victims.clear()

        victims.append(wolves[0])
        victims.append(wolves[1])
        
        for _ in range(0,testAmount):
            self.assertTrue(witch.heal(victims[:]) in [wolves[0],wolves[1],None])
        victims.clear()

        # memory test
        witch.addMemory(villagers[0],villagers[0].role)
        victims.append(villagers[0])
        victims.append(villagers[2])

        for _ in range(0,testAmount):
            self.assertTrue(witch.heal(victims[:]) in [villagers[0],None])
        victims.clear()

        witch.addMemory(wolves[0],wolves[0].role)
        victims.append(wolves[0])
        victims.append(wolves[1])

        for _ in range(0,testAmount):
            self.assertTrue(witch.heal(victims[:]) in [wolves[1],None])
        victims.clear()


    



wt = WerewolfTest()
wt.testAll()