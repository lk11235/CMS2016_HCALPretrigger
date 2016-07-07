
from CoreObject import CoreObject

class Sequence(CoreObject):
    def __init__(self):
        self.seq = []

    def load(self,Ana):
        self.seq.append(Ana)

    def delete(self,Ana):
        if Ana in self.seq:
            self.seq.pop(self.seq.index(Ana))
        else:
            raise RuntimeError, "Analyzer not in Sequence."

    def __getitem__(self,index):
        if index >= len(self.seq):
            raise IndexError
        else:
            return self.seq[index]

    def __len__(self):
        return len(self.seq)
