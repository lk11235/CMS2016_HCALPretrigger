
import os,ROOT
from CoreObject import CoreObject

##__________________________________________________________________||

class TreeHandler(CoreObject):
    """
    class that deal with the IO of ROOT trees
    instances of this class are used by looper to run analysis 
    """
    def __init__(self):
        self.treeList = []
        self.fileList = []

    def addFile(self,file):
        self.fileList.append(file)

    def addTree(self,tree):
        self.treeList.append(tree)

    def readTreeFromDir(self,inputDir,treePaths):
        fileList = [os.path.join(inputDir,f) for f in os.listdir(inputDir) if os.path.isfile(os.path.join(inputDir,f)) and f.endswith(".root")]
        for path in fileList:
            file = ROOT.TFile(path,"READ")
            self.addFile(file)
            tempTreeList = []
            for treePath in treePaths:
                tree = file.Get(treePath)
                tempTreeList.append(tree)
            self.addTree(tempTreeList)

    def end(self):
        for file in self.fileList:
            file.Close()
 
