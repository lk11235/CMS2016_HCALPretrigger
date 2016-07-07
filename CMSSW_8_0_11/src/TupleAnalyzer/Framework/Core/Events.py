
import ROOT
from collections import OrderedDict
from CoreObject import CoreObject

##__________________________________________________________________||

class Events(CoreObject):
    """
    event class to read data from one single tree
    """
    def __init__(self,tree):
        self.tree = tree
        self.nEvents = self.tree.GetEntries()
        self.branches = [ item.GetName() for item in self.tree.GetListOfLeaves() ]

    def __getitem__(self,i):
        if i >= self.nEvents:
            raise IndexError
        self.iEvent = i
        self.tree.GetEntry(i)
        return self

    def __getattr__(self,name):
        return getattr(self.tree,name)

class MultiEvents(object):
    def __init__(self,trees):
        self.trees = trees
        if any([self.trees[0].GetEntries() != tree.GetEntries() for tree in self.trees]):
            raise RuntimeError
        self.nEvents = self.trees[0].GetEntries()
        self.eventDict = OrderedDict()
        for tree in trees:
            self.eventDict[tree.GetName()] = Events(tree)

    def __getitem__(self,i):
        if i >= self.nEvents:
            raise IndexError
        self.iEvent = i
        for tree in self.trees:
            tree.GetEntry(i)
        return self

    def __getattr__(self,name):
        for treeName,events in self.eventDict.iteritems():
            if name in events.branches:
                break
        return getattr(events,name)
