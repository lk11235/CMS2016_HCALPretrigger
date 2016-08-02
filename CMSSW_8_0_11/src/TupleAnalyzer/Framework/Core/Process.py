
import ROOT
from CoreObject import CoreObject
from TreeHandler import TreeHandler
from Events import *

import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

class Process(CoreObject):

    def run(self,nEvents=-1):
   
	filled_bunches = [1, 1786]
	all_events = []
	bx_list = []

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

            #############################################################################################
	    
	    for i,event in enumerate(events):
                bx = int(event.GetLeaf("bx").GetValue())
		all_events.append(bx)
		if bx in bx_list: continue
		bx_list.append(bx)
	    
	    all_events = sorted(all_events)
	    bx_list = sorted(bx_list)
	    print Counter(all_events).most_common(5), "\n"

	    """
	    for bunch in reversed(bx_list):
		if (bunch-1) in bx_list:
		    bx_list.remove(bunch)
	    """

	    print "Found all BX\n" #"Trimmed events -- leaving isolated and leading bunches\n"
	    print bx_list, "\n"
	    
	    #############################################################################################

	    for i,event in enumerate(events):
                if int(event.GetLeaf("bx").GetValue()) not in filled_bunches: continue

		#print event.GetLeaf("bx").GetValue()#GetLeaf("Event", "bx").GetName()#GetEvent(i)#.getattr
                #temp.append(event.GetLeaf("bx").GetValue())#event.GetEvent(i)
		
		if (i+1) % 10000 == 0: print "Processed events: ",i
        	if (i > nEvents) and (nEvents != -1): break
                for ana in self.sequence:
                    if not ana.applySelection(event): continue
                    ana.analyze(event)

	binwidth=1
	plt.hist(all_events, bins=range(int(min(all_events)), int(max(all_events)) + binwidth, binwidth))
	plt.savefig('events.png')
	
	for ana in self.sequence:
            ana.endJob()
        self.treeHandler.end()
        self.outFile.Close()
