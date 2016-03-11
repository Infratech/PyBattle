import random
import csv
import sys

print random.randrange(1,20)

def main():
    #main program here
    #global variables:
    #statblock will be used as the base for the current stats.  It should not be modified.
    global statBlock
    global instanceList
    instanceList = []
    global callFunction
    callFunction = { 
        "testAction" : testAction,
        "dataPull" : dataPull,
        "exit" : exit
    }

    initialMenu()


    #start pulling in data
    #dataPull()
    #where we actually start doing work
    #operations()
    #verify global
    #globalCheck()
    #need a saved export
    #dataExport()

def initialMenu():
    global battleCount    
    battleCount = int(raw_input("How battles? "))
    for i in xrange(battleCount):
        addCombantants()
    print combatStatus()
    dataPull = MenuItem("Import Data","dataPull")
    exit = MenuItem("Quit", "exit")
    displayMenu([firstMenuItem, dataPull, exit])

def combatStatus():
    print 

def addCombantants():
    datapull()


def displayMenu(menuItems):
    print "display Status here"
    for count, menuItem in enumerate(menuItems):
        print "%i: %s" % (count, menuItem.descr)
    selection = int(raw_input("Please make a selection: "))
    menuItems[selection].callAction()
        

def testAction():
    print "Test action complete!"
    initialMenu()

def dataPull():
    #read the csv and load the data
    file = open('C:\Users\jcbaker\Documents\Visual Studio 2015\Projects\PythonApplication1\PythonApplication1\import.csv', 'rb')
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

def genInstance(onecount, twocount):
    #this will return a unique copy of the list of the data
    #need to pull the instanceCount from the specific ObjectID
    global statBlock
    instanceList = []
    instanceCount = 0

    for object in statBlock:
        if object['objectID'] == 1:
            for x in xrange(onecount):
                newobject = object.copy()
                newobject['instanceID'] = instanceCount
                instanceList.append(newobject)
                instanceCount += 1
        if object['objectID'] == 2:
            for x in xrange(twocount):
                newobject = object.copy()
                newobject['instanceID'] = instanceCount
                instanceList.append(newobject)
                instanceCount += 1

    return instanceList

def operations():
    #generate an instance
    print genInstance(2,2)

    #update a stat
    updateStat(2,'updatestat',7)

def updateStat(id, stat, value):
    global statBlock
    updateItem = next((item for item in statBlock if item['objectID'] == id), None)
    statBlock.remove(updateItem)
    updateItem[stat] = value
    statBlock.append(updateItem)

def globalCheck():
    global statBlock
    for object in statBlock:
        print object
    #for objects in statBlock:
    #    for stats in objects:
    #        print objects.get(stats)

def exit():
    quit()

class MenuItem(object):
    def __init__(self, descr, action):
        self.descr = descr
        self.action = action

    def callAction(self):
        global callFunction
        callFunction[self.action]()

class Combatant(object):
    def __init__(self):
        pass

if __name__ == "__main__":
    #kick off the program
    main()