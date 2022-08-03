#!/usr/bin/env python3

import csv
import sys
import argparse
import networkx as nx
import random
import plotly.graph_objects as go
import pickle

parser = argparse.ArgumentParser(description='Create test network for temp nets.')
parser.add_argument('-n', dest='noNodes', type=int, default=10000,
                    help='number of nodes')             
parser.add_argument('-i', dest='interEdge', type=int, default=100,
                    help='number of inter comm edges')     
parser.add_argument('-w', dest='intraEdge', type=int, default=1000,
                    help='number of intra (within) comm edges') 
parser.add_argument('-t', dest='timesteps', type=int, default=10,
                    help='number of timesteps')
parser.add_argument('-m', dest='movers', type=int, default=500,
                    help='number of nodes that move comm every timestep')     
parser.add_argument ('-c', dest='noComms', type= int, default=10,
					help='number of communities')
parser.add_argument ('-p', dest='probSwitch', type= float, default=0.1,
					help='prob a node switches communiy')
parser.add_argument (dest='fileName', type= str, help='filename to write')
args = parser.parse_args()


G = nx.Graph()
#nx.set_node_attributes(G,[],"community")
for i in range(args.noNodes):
    comm= random.randint(1,args.noComms)
    for t in range(args.timesteps):
        n= str(i)+"_"+str(t)
        G.add_node(n)
        G.nodes[n]["community"]= comm
        if random.random() < args.probSwitch:
            comm= random.randint(1,args.noComms)
        #print(n, G.nodes[n]["community"])
	#print(G.nodes[i]["community"])
for i in range(args.interEdge):
    for t in range(args.timesteps):
        n1= random.randint(0,args.noNodes-1)
        while (True):
            n2= random.randint(0,args.noNodes-1)
            if n1 == n2:
                continue
            n1name=str(n1)+"_"+str(t)
            n2name=str(n2)+"_"+str(t)
            if G.nodes[n1name]["community"] == G.nodes[n2name]["community"]:
                continue
            G.add_edge(n1name,n2name)
            break
for i in range(args.intraEdge):
    for t in range(args.timesteps):
        n1= random.randint(0,args.noNodes-1)
        while (True):
            n2= random.randint(0,args.noNodes-1)
            if n1 == n2:
                continue
            n1name=str(n1)+"_"+str(t)
            n2name=str(n2)+"_"+str(t)
            if G.nodes[n1name]["community"] != G.nodes[n2name]["community"]:
                continue
            G.add_edge(n1name,n2name)
            break        

for t in range(args.timesteps - 1):
    for n in range(args.noNodes):
        n1name= str(n)+"_"+str(t)
        n2name= str(n)+"_"+str(t+1)
        G.add_edge(n1name,n2name)
        



fptr= open(args.fileName,"wb")
pickle.dump((G,args.noComms), fptr, protocol=pickle.HIGHEST_PROTOCOL)
fptr.close()
	

# fig = go.Figure(data=[go.Sankey(
    # node = dict(
      # pad = 15,
      # thickness = 20,
      # line = dict(color = "black", width = 0.5),
      # label = labels,
      # color = "blue",
      
    # ),
    # link = dict(
      # source = src, # indices correspond to labels, eg A1, A2, A1, B1, ...
      # target = tgt,
      # value= val
  # ))])

# fig.update_layout(title_text="Basic Sankey Diagram", font_size=10)
# fig.show()
