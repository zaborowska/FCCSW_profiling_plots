import re
import os
import glob
import sys
import glob
from ROOT import TGraphErrors, TFile
from array import array

#TODO: move to config
filename_format = './igprof_res*' 

method__list = ['sim::RunManager::processEvent(', 'G4EventManager']

# create lists
param = []
time = []
time_err = []
hits_num = []
# loop over all files in directory
for filename in glob.glob(nameDir):
    parameter = re.findall(r"[-+]?\d*\.\d+|\d+",filename)
    if not parameter:
        print('WARNING: omitting file: '+filepath)
    else:
        ## open each file that contains energy
        with open(filename) as f:
            ## add energy to the list
            param.append(float(parameter))
            content = f.read()
            # get timing information and unit
            time.append(float(numbers[2])*un)

    #TODO:
    # here create a graph and save to tfile
    en_arr = array('f', en)
    en_err_arr = array('f', [0]*len(en))
    time_arr = array('f', time)
    time_err_arr = array('f', time_err)
    graph = TGraphErrors(len(en), en_arr, time_arr, en_err_arr,time_err_arr)
    graphname = subdir.split('/')
    print(graphname)
    graph.SetTitle(graphname[len(graphname)-1])
    graph.GetXaxis().SetTitle("energy (GeV)")
    graph.GetYaxis().SetTitle("time/event (s)")
    graph.SetMarkerColor(1)
    graph.SetMarkerStyle(20)
    graph.SetMarkerSize(1.5)
    print(subdir+os.sep+'time.root')
    file = TFile(subdir+os.sep+'time.root','RECREATE')
    graph.Write()
