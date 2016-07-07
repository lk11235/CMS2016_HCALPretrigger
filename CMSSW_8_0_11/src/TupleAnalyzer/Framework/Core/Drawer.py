import ROOT
from CoreObject import CoreObject

class Drawer(CoreObject):
    
    @staticmethod
    def drawEverything(histDict,outputDir):
        ROOT.gStyle.SetPaintTextFormat("4.2f")
        c = ROOT.TCanvas()
        for fileName,itemList in histDict.iteritems():
            c.Print(outputDir+"/"+fileName+"[")
            for item in itemList:
                className = item.__class__.__name__
                if className == "tuple" or className == "list":
                    maximum = max( [ hist.GetMaximum() for hist in item ] )
                    minimum = max( [ hist.GetMinimum() for hist in item ] )
                    leg = ROOT.TLegend(0.7,0.7,0.9,0.9)
                    for i,hist in enumerate(item):
                        hist.GetYaxis().SetRangeUser(0.5*minimum,1.5*maximum)
                        hist.SetStats(0)
                        #hist.SetTitle(hist.GetName())
                        hist.SetLineColor(i+2)
                        leg.AddEntry(hist,hist.GetName())
                        if i == 0:
                            hist.DrawCopy()
                        else:
                            hist.DrawCopy("same")
                    leg.Draw()
                elif "TH1" in className:
                    item.SetStats(0)
                    item.SetTitle(item.GetName())
                    item.DrawCopy("TEXT E1")
                elif "TH2" in className:
                    item.SetStats(0)
                    item.SetTitle(item.GetName())
                    #item.DrawCopy("colz")
                    item.DrawCopy("colztexte")
                c.Print(outputDir+"/"+fileName)
            c.Print(outputDir+"/"+fileName+"]")
