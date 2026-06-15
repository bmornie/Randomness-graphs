import sys
from pathlib import Path
import numpy as np
import networkx as nx
from pickle import load

sys.path.append(str(Path(__file__).resolve().parents[2]))

from graph_distances.orbits import orbit4
from graph_distances.distances import GCM11, GCD11, NetSimile_signature, NetSimile, JDM, JDD, RNN, RNND, JGM, JGD, RGD, RGDD




name = "BA"
n_graphs = 1000


print(f"Computing Randomness for {name} source network...")


with open("%s_rand.txt" %name, 'w') as f:
    f.write("model \t GCD \t NetSimile \t JDD \t RNND \t JGD \t RGDD\n")

# GRAIP

all_GCMs = []
all_signatures = []
all_JDMs = []
all_RNNs = []
all_JGMs = []
all_RGDs = []

for i in range(n_graphs):
    if name == "Ecoli":
        G = nx.read_edgelist("graphs/GRAIP/%s/IntAct_Escherichia_coli_4_%s%s.txt" %(name,i//100,i%100), nodetype=int)
    elif name == "Hpylori":
        G = nx.read_edgelist("graphs/GRAIP/%s/MINT_Helicobacter_pylori_4_%s%s.txt" %(name,i//100,i%100), nodetype=int)
    else:
        G = nx.read_edgelist("graphs/GRAIP/%s/%s_%s.txt" %(name,name,i), nodetype=int)
    
    orbits = orbit4(G)
    all_GCMs.append(GCM11(orbits))
    all_signatures.append(NetSimile_signature(G))
    all_JDMs.append(JDM(G))
    all_RNNs.append(RNN(orbits))
    all_JGMs.append(JGM(orbits))
    all_RGDs.append(RGD(G, orbits))

GCD_dist = GCD11(all_GCMs)
GCD_mean = np.mean(GCD_dist)

NetSimile_dist = NetSimile(all_signatures)
NetSimile_mean = np.mean(NetSimile_dist)

JDM_dist = JDD(all_JDMs)
JDM_mean = np.mean(JDM_dist)

RNN_dist = RNND(all_RNNs)
RNN_mean = np.mean(RNN_dist)

JGM_dist = JGD(all_JGMs)
JGM_mean = np.mean(JGM_dist)

RGD_dist = RGDD(all_RGDs)
RGD_mean = np.mean(RGD_dist)

with open("%s_rand.txt" %name, 'a') as f:
    f.write("GRAIP \t %s \t %s \t %s \t %s \t %s \t %s\n" %(GCD_mean, NetSimile_mean, JDM_mean, RNN_mean, JGM_mean, RGD_mean))

# SwapCon

all_GCMs = []
all_signatures = []
all_JDMs = []
all_RNNs = []
all_JGMs = []
all_RGDs = []

for i in range(n_graphs):
    if name == "Ecoli":
        G = nx.read_edgelist("graphs/SwapCon/%s/IntAct_Escherichia_coli_4_%s%s.txt" %(name,i//100,i%100), nodetype=int)
    elif name == "Hpylori":
        G = nx.read_edgelist("graphs/SwapCon/%s/MINT_Helicobacter_pylori_4_%s%s.txt" %(name,i//100,i%100), nodetype=int)
    else:
        G = nx.read_edgelist("graphs/SwapCon/%s/%s_%s.txt" %(name,name,i), nodetype=int)
    
    orbits = orbit4(G)
    all_GCMs.append(GCM11(orbits))
    all_signatures.append(NetSimile_signature(G))
    all_JDMs.append(JDM(G))
    all_RNNs.append(RNN(orbits))
    all_JGMs.append(JGM(orbits))
    all_RGDs.append(RGD(G, orbits))

GCD_dist = GCD11(all_GCMs)
GCD_mean = np.mean(GCD_dist)

NetSimile_dist = NetSimile(all_signatures)
NetSimile_mean = np.mean(NetSimile_dist)

JDM_dist = JDD(all_JDMs)
JDM_mean = np.mean(JDM_dist)

RNN_dist = RNND(all_RNNs)
RNN_mean = np.mean(RNN_dist)

JGM_dist = JGD(all_JGMs)
JGM_mean = np.mean(JGM_dist)

RGD_dist = RGDD(all_RGDs)
RGD_mean = np.mean(RGD_dist)

with open("%s_rand.txt" %name, 'a') as f:
    f.write("SwapCon \t %s \t %s \t %s \t %s \t %s \t %s\n" %(GCD_mean, NetSimile_mean, JDM_mean, RNN_mean, JGM_mean, RGD_mean))


# GraphGen

all_GCMs = []
all_signatures = []
all_JDMs = []
all_RNNs = []
all_JGMs = []
all_RGDs = []

for i in range(n_graphs):
    with open("graphs/GraphGen/%s/graph%s.dat" %(name, i), "rb") as f:
        G = load(f)
    if G.number_of_edges() < 30:    # Ignore poorly generated graphs
        continue
    
    orbits = orbit4(G)
    all_GCMs.append(GCM11(orbits))
    all_signatures.append(NetSimile_signature(G))
    all_JDMs.append(JDM(G))
    all_RNNs.append(RNN(orbits))
    all_JGMs.append(JGM(orbits))
    all_RGDs.append(RGD(G, orbits))

GCD_dist = GCD11(all_GCMs)
GCD_mean = np.mean(GCD_dist)

NetSimile_dist = NetSimile(all_signatures)
NetSimile_mean = np.mean(NetSimile_dist)

JDM_dist = JDD(all_JDMs)
JDM_mean = np.mean(JDM_dist)

RNN_dist = RNND(all_RNNs)
RNN_mean = np.mean(RNN_dist)

JGM_dist = JGD(all_JGMs)
JGM_mean = np.mean(JGM_dist)

RGD_dist = RGDD(all_RGDs)
RGD_mean = np.mean(RGD_dist)

with open("%s_rand.txt" %name, 'a') as f:
    f.write("GraphGen \t %s \t %s \t %s \t %s \t %s \t %s" %(GCD_mean, NetSimile_mean, JDM_mean, RNN_mean, JGM_mean, RGD_mean))
