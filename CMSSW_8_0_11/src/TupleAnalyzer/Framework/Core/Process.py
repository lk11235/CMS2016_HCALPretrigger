
import ROOT
from CoreObject import CoreObject
from TreeHandler import TreeHandler
from Events import *

class Process(CoreObject):

    def run(self,nEvents=-1):
    
        self.treeHandler = TreeHandler()
        self.treeHandler.readTreeFromDir(self.inputDir,self.treePaths)
        self.outFile = ROOT.TFile(self.outputPath,"RECREATE")
        for ana in self.sequence:
            ana.beginJob()
        for treeList in self.treeHandler.treeList:
            self.printMessage("-"*50)
            self.printMessage("Processing trees: "+str(treeList))
            if len(treeList) == 1:
                events = Events(treeList[0])
            elif len(treeList) > 1:
                events = MultiEvents(treeList)
            for i,event in enumerate(events):
                if (i+1) % 10000 == 0: print "Processed events: ",i
                if (i > nEvents) and (nEvents != -1): break
                for ana in self.sequence:
                    if not ana.applySelection(event): continue
                    ana.analyze(event)
        for ana in self.sequence:
            ana.endJob()
        self.treeHandler.end()
        self.outFile.Close()
