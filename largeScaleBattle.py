import random
import csv
import sys
from prettytable import PrettyTable
from math import floor

def main():
    #main program here
    #global variables:
    #statblock will be used as the base for the current stats.  It should not be modified.
    global statBlock
    global callFunction
    global liveScoreCard
    dataPull()
    liveScoreCard = scoreCard(int(raw_input("How many battles? ")))
    callFunction = {
        "exit" : exit,
        "liveScoreCard.allForward" : liveScoreCard.allForward,
        "restart" : restart
    }
    Menu()

def Menu():
    global liveScoreCard
    menuItems = []
    liveScoreCard.combatStatus()
    exit = MenuItem("Quit", "exit")
    oneRoundForward = MenuItem("One Round", "liveScoreCard.allForward")
    restart = MenuItem("Restart Game", "restart")
    menuItems.append(exit)
    menuItems.append(oneRoundForward)
    menuItems.append(restart)
    for count, menuItem in enumerate(menuItems):
        print "%i: %s" % (count, menuItem.descr)
    selection = int(raw_input("Please make a selection: "))
    menuItems[selection].callAction()
    Menu()

def restart():
    main()

def dataPull():
    #read the csv and load the data
    file = open('C:\Users\Gandalf\PycharmProjects\untitled\import.csv', 'rb')
    reader = csv.reader(file)
    global statBlock
    statBlock = []

    rownum = 0
    try:
        for row in reader:
            if rownum == 0:
                header = row
            else:
                #create the individual statblock
                indivBlock = { "objectID" : rownum}
                colnum = 0
                for col in row:
                     indivBlock[header[colnum]] = col
                     colnum += 1
                statBlock.append(indivBlock)

            rownum += 1
    finally:
        file.close()
    print "StatBlock loaded!"

def exit():
    quit()

class MenuItem(object):
    def __init__(self, descr, action):
        self.descr = descr
        self.action = action

    def callAction(self):
        global callFunction
        callFunction[self.action]()

class scoreCard(object):
    #send it count from the initial menu.  count is the number of battles to create
    def __init__(self, count):
        self.battleList = []
        for x in xrange(count):
            battle = Battle()
            battle.setInitiative()
            battle.setCultists()
            battle.setGuards()
            self.battleList.append(battle)
        print len(self.battleList)

    def oneForward(self, battle): # send it a scoreCard.x as in a battle to advance
        if not battle.winner:
            battle.oneRount()
            battle.battleOver()

    def allForward(self):
        for battle in self.battleList:
            if not battle.winner:
                battle.oneRound()
                battle.battleOver()

    def listSurvivors(self, battle):
        returnList = []
        for combatants in battle.cultists.combatants:
            if combatants['stats'].HP >= 1:
                returnList.append([combatants['stats'].name, combatants['stats'].HP])
        for combatants in battle.guards.combatants:
            if combatants['stats'].HP >= 1:
                returnList.append([combatants['stats'].name, combatants['stats'].HP])
        return returnList

    def combatStatus(self):
        displayTables = []
        for x, battle in enumerate(self.battleList):
            display = ["  "]
            rounds = ["R: "]
            turns = ["I: "]
            guards = ["G: "]
            cultists = ["C: "]
            winner = ["W: "]
            display.append(str(x))
            rounds.append(str(floor(battle.turns /2)))
            turns.append(battle.initiative)
            #todoOptomize the next two could be combined.  the liveCount could return the howAlive value
            #update the howAlive value which is a count of Combatants with positive HP per side
            battle.cultists.liveCount()
            battle.guards.liveCount()
            #query Combatant value howAlive and add
            guards.append(battle.guards.howAlive)
            cultists.append(battle.cultists.howAlive)
            #query Combatant value totalHP and add
            guards.append(battle.guards.totalHP)
            cultists.append(battle.cultists.totalHP)
            #query the battle for a winner and add
            winner.append(str(battle.winner))

            table = PrettyTable([display])
            table.add_row([rounds])
            table.add_row([turns])
            table.add_row([guards])
            table.add_row([cultists])
            table.add_row([winner])
            #if there is a winner for the side output their information
            if not not battle.winner:
                #form a list of the remaining combatants' name and HP then add that list to the row to be displayed
                survivors = ["S: "]
                survivors.append(self.listSurvivors(battle))
                table.add_row([survivors])
            displayTables.append(table)

        for displaytable in displayTables:
            print displaytable

class Battle(object):
    #Turns, leaderBonus, initiative, two sides which are lists of combatants
    def __init__(self):
        self.turns = 0
        self.initiative = 'N'
        self.leaderBonus = 1
        self.cultists = battleSide("Cultists")
        self.guards = battleSide("Guards")
        self.winner = False

    def setCultists(self, leader=1, minions=9):
        for x in xrange(leader):
            Leader = Combatant("CultLead", x)
            self.cultists.add(Leader)
        for x in xrange(minions):
            Minion = Combatant("Cultist", x)
            self.cultists.add(Minion)

    def setGuards(self, leader=1, minions=9):
        for x in xrange(leader):
            Leader = Combatant("Captain", x)
            self.guards.add(Leader)
        for x in xrange(minions):
            Minion = Combatant("Guard", x)
            self.guards.add(Minion)

    def setInitiative(self):
        #have the two leaders roll off.  sets self.iniative to winning leaders team
        while self.initiative == 'N':
            gd20roll = d20Roll()
            cd20roll = d20Roll()
            if gd20roll.value > cd20roll.value:
                self.initiative = 'G'
            if cd20roll.value > gd20roll.value:
                self.initiative = 'C'

    def targetAttack(self, attacker, defender):
        #send two combatants
        targetAC = int((defender.AC))
        damageDone = attacker.attack(targetAC)
        with open('C:\Users\Gandalf\PycharmProjects\untitled\export.txt', "a") as myfile:
            myfile.write("%s just did %s to %s\n" % (attacker.name, damageDone, defender.name))
        defender.takeDamage(damageDone)

    def setTarget(self, attacking, defending, orderNumber):
        target = defending.combatants[orderNumber]
        if target['stats'].isAlive:
            return orderNumber
        else:
            print "switching targets"
            print self.winner
            upOrDown = d2Roll()
            if upOrDown.value == 1:
                while True:
                    target = defending.combatants[orderNumber]
                    if target['stats'].isAlive:
                        return orderNumber
                    if orderNumber == 0:
                        self.battleOver()
                        if not not self.winner:
                            return 'x'
                        orderNumber = len(defending.combatants)
                    orderNumber -= 1
            else:
                while True:
                    target = defending.combatants[orderNumber]
                    if target['stats'].isAlive:
                        return orderNumber
                    if orderNumber == len(defending.combatants):
                        self.battleOver()
                        if not not self.winner:
                            return 'x'
                        orderNumber = 0
                    orderNumber += 1

    def checkTarget(self, side, targetnumber):
        if side.combatants[targetnumber]['stats'].HP >= 1:
            return targetnumber
        else:
            return self.setTarget(self.guards, self.cultists, targetnumber)

    def battleOver(self):
        if self.initiative == 'G':
            self.cultists.verifyAlive()
            if not self.cultists.isAlive:
                self.winner = "Guards"
        elif self.initiative == 'C':
            self.guards.verifyAlive()
            if not self.guards.isAlive:
                self.winner = "Cultists"

    def oneRound(self):
        self.battleOver()
        self.oneTurn()
        self.battleOver()
        self.oneTurn()
        self.battleOver()

    def oneTurn(self):
        if not self.winner:
            #check every combatant on one side.  if they have a target attack if not search for target
            if self.initiative == 'G':
                for guardside in self.guards.combatants: # each guard has stats, order, target
                    if guardside['stats'].isAlive:
                        if not guardside['target'] == 'no':
                            guardside['target'] = self.checkTarget(self.cultists, guardside['target'])
                        if guardside['target'] == 'no':
                            guardside['target'] = self.setTarget(self.guards, self.cultists, guardside['order'])
                        if not guardside['target'] == 'x':
                            self.targetAttack(guardside['stats'], self.cultists.combatants[guardside['target']]['stats'])
                self.initiative = 'C'
            elif self.initiative == 'C':
                for cultistside in self.cultists.combatants: # each guard has stats, order, target
                     if cultistside['stats'].isAlive:
                        if not cultistside['target'] == 'no':
                            cultistside['target'] = self.checkTarget(self.guards, cultistside['target'])
                        if cultistside['target'] == 'no':
                            cultistside['target'] = self.setTarget(self.cultists, self.guards, cultistside['order'])
                        if not cultistside['target'] == 'x':
                            self.targetAttack(cultistside['stats'], self.guards.combatants[cultistside['target']]['stats'])
                self.initiative = 'G'
            self.turns += 1

class battleSide(object):
    def __init__(self, name):
        self.name = name
        self.combatants = [] # a list of the combatant, it's order, and it
        self.order = 0
        self.isAlive = True
        self.howAlive = 0
        self.totalHP = 0

    def add(self, combatant):
        self.combatants.append({'stats' : combatant, 'order' : self.order, 'target' : 'no'})
        self.order += 1

    def liveCount(self):
        self.howAlive = 0
        for combatant in self.combatants:
            if combatant['stats'].isAlive:
                self.howAlive +=1
                self.totalHP += combatant['stats'].HP

    def verifyAlive(self):
        self.isAlive = False
        for combatant in self.combatants:
            if combatant['stats'].isAlive:
                    self.isAlive = True

class Combatant(object):
    #made from the stat box
    #Name,Proficiency,AC,HP,isLeader
    global statBlock

    def __init__(self, passedname, count):
        self.name = passedname
        self.isAlive = True
        for sBlock in statBlock:
            if sBlock['name'] == self.name:
                self.proficiency = sBlock['proficiency']
                self.AC = sBlock['AC']
                self.HP = sBlock['HP']
                self.isLeader = sBlock['isLeader']
                self.dex = sBlock['dex']
                self.dmg = sBlock['dmg']
                self.save = sBlock['save']
                self.name = self.name + str(count)

    def takeDamage(self, damage):
        self.HP = int(self.HP) - damage
        if int(self.HP) <= 0:
            self.isAlive = False

    def attack(self, targetAC):
        d20roll = d20Roll()
        d20roll.value += int(self.proficiency)
        if d20roll.value >= targetAC:
            d6roll = d6Roll()
            d6roll.value += int(self.dmg)
            return d6roll.value
        else:
            return 0

#todoOptomize all rolls could just become yield functions
class d2Roll(object):
    def __init__(self):
        self.value = random.randrange(1,2)

class d20Roll(object):
    def __init__(self):
        self.value = int(random.randrange(1,20))

class d6Roll(object):
    def __init__(self):
        self.value = int(random.randrange(1,6))



if __name__ == "__main__":
    #kick off the program
    main()