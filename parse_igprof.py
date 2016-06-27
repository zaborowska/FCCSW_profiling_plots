import re
import os
import glob
import sys
import glob
from ROOT import TGraphErrors, TFile
from array import array

#TODO: move to config
filename_format = 'test/igreport_perf_E*.res' 
# substring just needs to be contained in line for it to match
method_list = ['sim::RunManager::processEvent(', 'G4']

# create result dict
result = {}

# igprof strings
ig_cumulative_string = """----------------------------------------------------------------------
Flat profile (cumulative >= 1%)"""
ig_flat_string = """----------------------------------------------------------------------
Flat profile (self >= 0.01%)"""

# loop over all files in directory
for filename in glob.glob(filename_format):
    print('Parsing file %s' % filename)
    parameter = re.findall(r"[-+]?\d*\.\d+|\d+",filename)[0]
    if not parameter:
        print('WARNING: omitting file: '+filepath)
    else:
        ## open each file that contains energy
        with open(filename) as f:
            content = f.read()
            # get part between the 'cumulative' and 'flat' header
            cumulative_part = content.split(ig_cumulative_string)[1]
            cumulative_part = cumulative_part.split(ig_flat_string)[0]
            all_lines = cumulative_part.split('\n')
            relevant_lines = []
            for method in method_list:
                for line in all_lines:
                    if method in line:
                        relevant_lines.append(line)
            for line in relevant_lines:
                """ p.ex. ['78.9', '28.23', 'G4EventManager::DoProcessing(G4Event*)', '[33]']
                """
                line_parts = line.split()
                print(line_parts)
                
                percent = line_parts[0]
                total = line_parts[1],
                method_name = ' '.join(line_parts[2:-1])
                igprof_number = line_parts[-1]
                # make sure the dict contains a nested list
                result.setdefault(method_name, [[], []])[0].append(float(parameter))
                result[method_name][1].append(float(percent))
                #TODO: add total column as well?

print(result)
"""
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
"""
