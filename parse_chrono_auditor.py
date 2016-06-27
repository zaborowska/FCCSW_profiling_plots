import re
import os
import glob
import sys
from ROOT import TGraphErrors, TFile
from array import array
for nameDir in sys.argv[1:]:
    # create lists
    en = []
    time = []
    time_err = []
    hits_num = []
    # loop over all files in directory
    for filename in glob(nameDir):
        filepath = subdir + os.sep + filename
        energy = re.findall(r'\d+',filename)
        if not energy:
            print('WARNING: omitting file: '+filepath)
        else:
            ## open each file that contains energy
            with open(filepath) as f:
                ## add energy to the list
                en.append(int(energy[0]))
                content = f.readlines()
                # get timing information and unit
                numbers = re.findall(r'\d+\.?\d*', content[0])
                if (len(numbers) < 4):
                    print('WARNING: run simulation for more than 1 event')
                    exit()
                unit = re.findall(r'\[[a-zA-Z]+\]', content[0])
                if not unit:
                    print("no unit specified ...")
                else:
                    if(unit[0] == unit[1] == '[us]'):
                        un = 1.e-6
                    if(unit[0] == unit[1] == '[ms]'):
                        un = 0.001
                    elif(unit[0] == unit[1] == '[s]'):
                        un = 1
                    elif(unit[0] == unit[1] == '[min]'):
                        un = 60
                    elif(unit[0] == unit[1] == '[h]'):
                        un = 60*60
                    else:
                        print('unknown or not the same units: '+ unit[0]+' '+ unit[1] +' ! Terminating...')
                        exit()
                time.append(float(numbers[2])*un)
                time_err.append(float(numbers[3])*un)
                # calculate avarege of hits
                hits = []
                for line in content[1:]:
                    numbers = re.findall(r'\d+\.?\d*', line)
                    hits.append(int(numbers[0]))
                hits_num.append(sum(hits)/len(hits))
    print(en, time, time_err, hits_num)

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
