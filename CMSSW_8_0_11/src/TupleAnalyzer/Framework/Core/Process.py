
import ROOT
from CoreObject import CoreObject
from TreeHandler import TreeHandler
from Events import *

import numpy as np
import matplotlib.pyplot as plt

class Process(CoreObject):

    def run(self,nEvents=-1):
   
	temp = [] 
	bx_list = [1, 1786]

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
                if int(event.GetLeaf("bx").GetValue()) not in bx_list: continue

		print event.GetLeaf("bx").GetValue()#GetLeaf("Event", "bx").GetName()#GetEvent(i)#.getattr
                temp.append(event.GetLeaf("bx").GetValue())#event.GetEvent(i)
		
		if (i+1) % 10000 == 0: print "Processed events: ",i
        	if (i > nEvents) and (nEvents != -1): break
                for ana in self.sequence:
                    if not ana.applySelection(event): continue
                    ana.analyze(event)
	
	if len(temp) == 0:
	    temp.append(0)
	binwidth=1
	plt.hist(temp, bins=range(int(min(temp)), int(max(temp)) + binwidth, binwidth))
	plt.savefig('events.png')
	#print temp
	
	for ana in self.sequence:
            ana.endJob()
        self.treeHandler.end()
        self.outFile.Close()
