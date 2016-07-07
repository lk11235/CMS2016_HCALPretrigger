
from CoreObject import CoreObject

class Analyzer(CoreObject):
    def __init__(self,name):
        self.name = name
        self.hists = {}

    def beginJob(self):
        pass

    def analyze(self,event):
        pass

    def endJob(self):
        for histName,hist in self.hists.iteritems():
            hist.Write()
        pass

    def applySelection(self,event):
        return True
