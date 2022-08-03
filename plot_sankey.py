#!/usr/bin/env python3

import csv
import sys
import argparse
import networkx as nx
import random
import plotly.graph_objects as go
import pickle

parser = argparse.ArgumentParser(description='Plot a sankey diagram from a network file with communities.')

parser.add_argument (dest='fileName', type= str, help='filename to read')
args = parser.parse_args()
fptr= open(args.fileName,"rb")
(G,noComms) = pickle.load(fptr)
fptr.close()

# Plot sankey
labels=[]
nt= 4#args.timesteps
src=[]
tgt=[]
val=[]
clook={}
for i in range(nt):
    for j in range(1,noComms+1):
        n= str(j)+"_"+str(i)
        clook[n]= len(labels)
        labels.append(n)
for i in range(nt-1):
    for j in range(int(G.number_of_nodes()/100)):
        n1= str(j)+"_"+str(i)
        n2= str(j)+"_"+str(i+1)
        c1=str(G.nodes[n1]["community"])+"_"+str(i)
        c2=str(G.nodes[n2]["community"])+"_"+str(i+1)
        src.append(clook[c1])
        tgt.append(clook[c2])
        val.append(1)

fig = go.Figure(data=[go.Sankey(
    node = dict(
      pad = 15,
      thickness = 20,
      line = dict(color = "black", width = 0.5),
      label = labels,
      color = "blue",
      
    ),
    link = dict(
      source = src, # indices correspond to labels, eg A1, A2, A1, B1, ...
      target = tgt,
      value= val
  ))])

fig.update_layout(title_text="Basic Sankey Diagram", font_size=10)
fig.show()
