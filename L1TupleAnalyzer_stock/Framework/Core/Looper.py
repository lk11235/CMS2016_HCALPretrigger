
import ROOT
from Events import Events

class Looper(object):
    def __init__(self,treeHandler,sequence):
        self.treeHander = treeHandler
        self.sequence = sequence

    def run(self,nEvents):

        for tree in self.treeHander.treeList:
            events = Events(tree)
            print "Total Number of events to be run: ",len(events)
            for ana in self.sequence:
                ana.beginJob()
            for i,event in enumerate(events):
                if (i+1) % 10000 == 0: print "Processed events: ",i
                if (i > nEvents) and (nEvents != -1): break
                for ana in self.sequence:
                    if not ana.applySelection(event): continue
                    ana.analyze(event)
            for ana in self.sequence:
                ana.endJob()

