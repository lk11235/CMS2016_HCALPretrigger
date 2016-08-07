
import ROOT
from CoreObject import CoreObject
from TreeHandler import TreeHandler
from Events import *

import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

class Process(CoreObject):

    def run(self,nEvents=-1):
   
	choice = input('\n(1) automated choice of bx or (2) manual specification: ')
	if choice == 1: num_bx = input('\n# of bx to include in analysis: '); pedestal = input('\n# of events required to select filled BX: '); auto = True
	elif choice == 2: filled_bx = [int(x) for x in raw_input('\nall bx to analyze separated by spaces: ').split()]; auto = False #range(1787)
	else: print('please specify choice (1) or (2)...\n'); self.run()

	all_bx = []
	trimmed_bx = []

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
	    
	    if auto:
	    	for i,event in enumerate(events):
                    bx = int(event.GetLeaf("bx").GetValue())
	 	    all_bx.append(bx)

	    	all_bx = sorted(all_bx)
	    	
		freq = Counter(all_bx).most_common()
		old_count = freq[0][1]
		
		if old_count >= pedestal: select = True
		else: select = False

		for word, count in Counter(all_bx).most_common():
		    if (old_count/count > 10) or (old_count/count < 1/10): select = not select
		    print old_count/count, select
		    old_count = count

		    if select: trimmed_bx.append(word)
 
		print "Found all BX and respective frequencies of events\n"
		print freq, "\n" #.most_common(num_bx), "\n"
	    
	    else:
		for i,event in enumerate(events):
                    bx = int(event.GetLeaf("bx").GetValue())
                    all_bx.append(bx)

                all_bx = sorted(all_bx)
		trimmed_bx = sorted(list(set(filled_bx)))
		
		freq = Counter(all_bx).most_common()
	
		print "Found all BX and respective frequencies of events\n"
		print freq, "\n"

	    """
	    for bunch in reversed(trimmed_bx):
		if (bunch-1) in trimmed_bx:
		    trimmed_bx.remove(bunch)
	    """

	    print "Trimmed events to following BX\n"
	
	    print trimmed_bx, "\n"
    
	    #############################################################################################
	
	    for i,event in enumerate(events):
		bx = int(event.GetLeaf("bx").GetValue())	
		if (i+1) % 10000 == 0: print "Processed events: ",i
        	if (i > nEvents) and (nEvents != -1): break
                
		for ana in self.sequence:
                    if not ana.applySelection(event): continue
		    elif bx not in trimmed_bx: continue #ana.count(event)
		    else: ana.analyze(event)

	binwidth=1
	plt.hist(all_bx, bins=range(int(min(all_bx)), int(max(all_bx)) + binwidth, binwidth))
	plt.savefig('events.png')
	
	for ana in self.sequence:
            ana.endJob()

        self.treeHandler.end()
        self.outFile.Close()
