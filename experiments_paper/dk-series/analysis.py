import sys
from pathlib import Path
import numpy as np
import networkx as nx

sys.path.append(str(Path(__file__).resolve().parents[2]))

from graph_distances.orbits import orbit4
from graph_distances.distances import GCM11, GCD11, NetSimile_signature, NetSimile, JDM, JDD, RNN, RNND, JGM, JGD, RGD, RGDD



name = "BA"
n_graphs = 500

print(f"Computing randomness for {name} source network...")


prefixes = {"dk0": "dk0.0", "dk1": "dk1.0", "dk2": "dk2.0"}

GCD_distances = []
NetSimile_distances = []
JDM_distances = []
RNN_distances = []
JGM_distances = []
RGD_distances = []



for dk in ["dk0", "dk1", "dk2"]:
    all_GCMs = []
    all_signatures = []
    all_JDMs = []
    all_RNNs = []
    all_JGMs = []
    all_RGDs = []
    
    for i in range(n_graphs):
        G = nx.read_edgelist("data/%s/%s/%s_%s%s.txt" %(name, dk, prefixes[dk], name, i), nodetype=int)
        orbits = orbit4(G)
        all_GCMs.append(GCM11(orbits))
        all_signatures.append(NetSimile_signature(G))
        all_JDMs.append(JDM(G))
        all_RNNs.append(RNN(orbits))
        all_JGMs.append(JGM(orbits))
        all_RGDs.append(RGD(G, orbits))
    
    GCD_dist = GCD11(all_GCMs)
    GCD_distances.append(np.mean(GCD_dist))
    
    NetSimile_dist = NetSimile(all_signatures)
    NetSimile_distances.append(np.mean(NetSimile_dist))
    
    JDM_dist = JDD(all_JDMs)
    JDM_distances.append(np.mean(JDM_dist))
    
    RNN_dist = RNND(all_RNNs)
    RNN_distances.append(np.mean(RNN_dist))
    
    JGM_dist = JGD(all_JGMs)
    JGM_distances.append(np.mean(JGM_dist))
    
    RGD_dist = RGDD(all_RGDs)
    RGD_distances.append(np.mean(RGD_dist))


dist_names = ["GCD11", "NetS", "JDM", "RNN", "JGM", "RGD"]
all_distances = [GCD_distances, NetSimile_distances, JDM_distances, RNN_distances, JGM_distances, RGD_distances]
with open("%s_results.txt" %name, "w") as f:
    f.write("distance \t dk0_dist \t dk1_dist \t dk2_dist\n")
    for i in range(len(dist_names)):
        f.write("%s \t " %dist_names[i])
        for j in range(3):
            f.write("%s \t" %all_distances[i][j])
        f.write("\n")
