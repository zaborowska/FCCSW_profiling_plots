from ROOT import TFile, TGraph, TCanvas, TLegend, TPad
from array import array
import sys

# plot all on canvas

graphs = {}
print(len(sys.argv[1:]))
for filename in sys.argv[1:]:
    f = TFile(filename+'.root','READ')
    f.GetList().ls()
    for i in range(0,f.GetNkeys()):
        g = f.Get('igprof_cumulative'+str(i))
        graphs.setdefault(g.GetTitle(), [[],[]])[0].append(g)
        graphs[g.GetTitle()][1].append(filename)

for title, graphsList in graphs.items():
    # check Y axis range
    minval=[]
    maxval=[]
    for g in graphsList[0]:
        minval.append(g.GetYaxis().GetXmin())
        maxval.append(g.GetYaxis().GetXmax())
    canv = TCanvas("igprof","igprof runtime",0,0,1600,1000)
    canv.Divide(2,1)
    pad = canv.cd(1)
    leg = TLegend(0.1,0.1,0.9,0.9)
    for i, g in enumerate(graphsList[0]):
        g.SetMarkerColor(i+1)
        g.SetLineColor(i+1)
        g.SetMarkerStyle(20+i)
        leg.AddEntry(g,graphsList[1][i],"p")
        if(i==0):
            g.Draw("AP")
            g.GetYaxis().SetRangeUser(min(minval),max(maxval))
            g.GetXaxis().SetRangeUser(0,200000)
        else:
            g.Draw("sameP")
    canv.cd(2)
    leg.Draw()
    canv.Print("plots/"+title+".png")
