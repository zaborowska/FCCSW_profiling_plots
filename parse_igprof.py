import re
import os
import glob
import sys
import glob
from ROOT import TFile, TGraph
from array import array

inname = sys.argv[1]
#TODO: move to config
filename_format = 'data/igprof.'+inname+'.'+'*.txt'
# substring just needs to be contained in line for it to match
method_list = ['DD4hep::Simulation','::ProcessHits']

# create result dict
result = {}
threshold = 0

# igprof strings
ig_cumulative_string = """----------------------------------------------------------------------
Flat profile (cumulative >= 1%)"""
ig_flat_string = """----------------------------------------------------------------------
Flat profile (self >= 0.01%)"""
ig_end_string = """----------------------------------------------------------------------
Call tree profile (cumulative)"""

# loop over all files in directory
for filename in glob.glob(filename_format):
    print('Parsing file %s' % filename)
    parameter = re.findall(r"[-+]?\d+\.\d*|\d+",filename)[1]
    print(parameter)
    if not parameter:
        print('WARNING: omitting file: '+filepath)
    else:
        ## open each file that contains energy
        with open(filename) as f:
            content = f.read()
            # get part between the 'cumulative' and 'flat' header
            cumulative_part = content.split(ig_cumulative_string)[1]
            cumulative_part = cumulative_part.split(ig_flat_string)[0]
            self_part = content.split(ig_end_string)[0].split(ig_flat_string)[1]
            all_lines = self_part.split('\n')
            relevant_lines = []
            for method in method_list:
                for line in all_lines:
                    if method in line:
                        relevant_lines.append(line)
            for line in relevant_lines:
                """ p.ex. ['78.9', '28.23', 'G4EventManager::DoProcessing(G4Event*)', '[33]']
                """
                line_parts = line.split()
                percent = line_parts[0]
                total = line_parts[1].replace("'", "")
                method_name = ' '.join(line_parts[2:-1])
                igprof_number = line_parts[-1]
                if float(total)>threshold:
                    # make sure the dict contains a nested list
                    result.setdefault(method_name, [[], []])[0].append(float(parameter))
                    result[method_name][1].append(float(total))
                    #TODO: add total column as well?

#print(result)
paramname="energy (GeV)"
accuracy = 1.e-1
file = TFile(sys.argv[1]+'.root','RECREATE')
i=0
for name, x in result.items(): #iteritems():
    if len(x[0]) != len(x[1]):
        print("Lengths of x0 and x1 differ! Terminating.")
        exit()
    # check if sth is const
    mean = sum(x[1])/len(x[1])
    if not (all( abs(item - mean) < accuracy for item in x[1])):
        x_arr = array('f', x[0])
        y_arr = array('f', x[1])
        graph = TGraph(len(x[0]), x_arr, y_arr)
        graph.SetName("igprof_cumulative"+str(i))
        graph.SetTitle(name)
        i+=1
        graph.GetXaxis().SetTitle(paramname)
        graph.GetYaxis().SetTitle("total")
        graph.SetMarkerColor(1)
        graph.SetMarkerStyle(20)
        graph.SetMarkerSize(1.5)
        graph.Write()
print("Created "+str(file.GetNkeys())+" graphs")
file.Close()
