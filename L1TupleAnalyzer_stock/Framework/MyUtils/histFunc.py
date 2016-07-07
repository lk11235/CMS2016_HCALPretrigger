import ROOT
from probFunc import binoError

def makeBinoHist(numHist,demHist):
    nbins = numHist.GetNbinsX()
    ratio = ROOT.TH1D(numHist.GetName().replace("num","ratio"),"",nbins,-0.5,nbins-0.5)
    for ibin in range(1,nbins+1):
        num = numHist.GetBinContent(ibin)
        dem = demHist.GetBinContent(ibin)
        binLabel = numHist.GetXaxis().GetBinLabel(ibin)
        ratio.GetXaxis().SetBinLabel(ibin,binLabel)
        if num and dem:
            ratio.SetBinContent(ibin,num/dem)
            ratio.SetBinError(ibin,binoError(num,dem))
    return ratio
