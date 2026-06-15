import sys
from pathlib import Path
import numpy as np
import networkx as nx
from pickle import load
from sklearn.metrics import precision_recall_curve, auc

sys.path.append(str(Path(__file__).resolve().parents[2]))

from graph_distances.orbits import orbit4
from graph_distances.distances import GCM11, GCD11, NetSimile_signature, NetSimile, JDM, JDD, RNN, RNND, JGM, JGD, RGD, RGDD



name = "BA"
n_graphs = 1000


print(f"Computing AUPR for {name} source network...")


all_models = []
all_GCMs = []
all_signatures = []
all_JDMs = []
all_RNNs = []
all_JGMs = []
all_RGDs = []


# GRAIP
for i in range(n_graphs):
    if name == "Ecoli":
        G = nx.read_edgelist("graphs/GRAIP/%s/IntAct_Escherichia_coli_4_%s%s.txt" %(name,i//100,i%100), nodetype=int)
    elif name == "Hpylori":
        G = nx.read_edgelist("graphs/GRAIP/%s/MINT_Helicobacter_pylori_4_%s%s.txt" %(name,i//100,i%100), nodetype=int)
    else:
        G = nx.read_edgelist("graphs/GRAIP/%s/%s_%s.txt" %(name,name,i), nodetype=int)
    
    all_models.append(0)
    
    orbits = orbit4(G)
    all_GCMs.append(GCM11(orbits))
    all_signatures.append(NetSimile_signature(G))
    all_JDMs.append(JDM(G))
    all_RNNs.append(RNN(orbits))
    all_JGMs.append(JGM(orbits))
    all_RGDs.append(RGD(G, orbits))

# SwapCon
for i in range(n_graphs):
    if name == "Ecoli":
        G = nx.read_edgelist("graphs/SwapCon/%s/IntAct_Escherichia_coli_4_%s%s.txt" %(name,i//100,i%100), nodetype=int)
    elif name == "Hpylori":
        G = nx.read_edgelist("graphs/SwapCon/%s/MINT_Helicobacter_pylori_4_%s%s.txt" %(name,i//100,i%100), nodetype=int)
    else:
        G = nx.read_edgelist("graphs/SwapCon/%s/%s_%s.txt" %(name,name,i), nodetype=int)
    
    all_models.append(1)
    
    orbits = orbit4(G)
    all_GCMs.append(GCM11(orbits))
    all_signatures.append(NetSimile_signature(G))
    all_JDMs.append(JDM(G))
    all_RNNs.append(RNN(orbits))
    all_JGMs.append(JGM(orbits))
    all_RGDs.append(RGD(G, orbits))

# GraphGen
for i in range(n_graphs):
    with open("graphs/GraphGen/%s/graph%s.dat" %(name, i), "rb") as f:
        G = load(f)
    if G.number_of_edges() < 30:    # Ignore poorly generated graphs
        continue
    
    all_models.append(2)
    
    orbits = orbit4(G)
    all_GCMs.append(GCM11(orbits))
    all_signatures.append(NetSimile_signature(G))
    all_JDMs.append(JDM(G))
    all_RNNs.append(RNN(orbits))
    all_JGMs.append(JGM(orbits))
    all_RGDs.append(RGD(G, orbits))


same_model = []
for i in range(len(all_models)):
    for j in range(i+1, len(all_models)):
        same_model.append(1*(all_models[i]==all_models[j]))


print("GCD11:")
distances = np.array(GCD11(all_GCMs))
GCD11_precision, GCD11_recall, _ = precision_recall_curve(same_model, -distances)  # Negative because lower distance = higher similarity
GCD11_aupr = auc(GCD11_recall, GCD11_precision)
print("AUPR: ", GCD11_aupr)
print("")

print("Netsimile:")
distances = np.array(NetSimile(all_signatures))
NetSimile_precision, NetSimile_recall, _ = precision_recall_curve(same_model, -distances)
NetSimile_aupr = auc(NetSimile_recall, NetSimile_precision)
print("AUPR: ", NetSimile_aupr)
print("")

print("JDD:")
distances = np.array(JDD(all_JDMs))
JDM_precision, JDM_recall, _ = precision_recall_curve(same_model, -distances)
JDM_aupr = auc(JDM_recall, JDM_precision)
print("AUPR: ", JDM_aupr)
print("")

print("RNND:")
distances = np.array(RNND(all_RNNs))
RNN_precision, RNN_recall, _ = precision_recall_curve(same_model, -distances)
RNN_aupr = auc(RNN_recall, RNN_precision)
print("AUPR: ", RNN_aupr)
print("")

print("JGD:")
distances = np.array(JGD(all_JGMs))
JGM_precision, JGM_recall, _ = precision_recall_curve(same_model, -distances)
JGM_aupr = auc(JGM_recall, JGM_precision)
print("AUPR: ", JGM_aupr)
print("")

print("RGDD:")
distances = np.array(RGDD(all_RGDs))
RGD_precision, RGD_recall, _ = precision_recall_curve(same_model, -distances)
RGD_aupr = auc(RGD_recall, RGD_precision)
print("AUPR: ", RGD_aupr)
print("")


np.savez("%s_AUPR.npz"%name, GCD11_precision=GCD11_precision, GCD11_recall=GCD11_recall, GCD11_aupr=GCD11_aupr, 
         NetSimile_precision=NetSimile_precision, NetSimile_recall=NetSimile_recall, NetSimile_aupr=NetSimile_aupr, 
         JDM_precision=JDM_precision, JDM_recall=JDM_recall, JDM_aupr=JDM_aupr, 
         RNN_precision=RNN_precision, RNN_recall=GCD11_recall, RNN_aupr=RNN_aupr, 
         JGM_precision=JGM_precision, JGM_recall=JGM_recall, JGM_aupr=JGM_aupr, 
         RGD_precision=RGD_precision, RGD_recall=RGD_recall, RGD_aupr=RGD_aupr)