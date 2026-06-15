import sys
from pathlib import Path
import numpy as np
import networkx as nx

sys.path.append(str(Path(__file__).resolve().parents[2]))

from graph_distances.orbits import orbit4
from graph_distances.distances import GCM11, GCD11, NetSimile_signature, NetSimile, JDM, JDD, RNN, RNND, JGM, JGD, RGD, RGDD



n = 1000
k = 20      # m = n * k/2
samples_per_p = 1000


base_graph = nx.watts_strogatz_graph(n, k, 0)


clustering_base = nx.average_clustering(base_graph)
shortest_path_base = nx.average_shortest_path_length(base_graph)

orbits_base = orbit4(base_graph)

GCM_base = GCM11(orbits_base)
signature_base = NetSimile_signature(base_graph)
JDM_base = JDM(base_graph)
RNN_base = RNN(orbits_base)
JGM_base = JGM(orbits_base)
RGD_base = RGD(base_graph, orbits_base)


C_av = []
L_av = []

GCD11_av = []
NetSimile_av = []
JDD_av = []
RNND_av = []
JGD_av = []
RGDD_av = []


prob = np.logspace(-4, 0, 20)

for p in prob:
    
    clustering_distances = []
    shortest_path_distances = []
    
    GCD11_distances = []
    NetSimile_distances = []
    JDM_distances = []
    RNN_distances = []
    JGM_distances = []  
    RGD_distances = []
    
    for _ in range(samples_per_p):
        G = nx.watts_strogatz_graph(n, k, p)
        orbits = orbit4(G)
        
        clustering_distances.append(abs(clustering_base-nx.average_clustering(G)))
        shortest_path_distances.append(abs(shortest_path_base-nx.average_shortest_path_length(G)))
        
        GCD11_distances.append(GCD11([GCM_base, GCM11(orbits)])[0])
        NetSimile_distances.append(NetSimile([signature_base, NetSimile_signature(G)])[0])
        JDM_distances.append(JDD([JDM_base, JDM(G)])[0])
        RNN_distances.append(RNND([RNN_base, RNN(orbits)])[0])
        JGM_distances.append(JGD([JGM_base, JGM(orbits)])[0])
        RGD_distances.append(RGDD([RGD_base, RGD(G, orbits)])[0])
    
    C_av.append(np.mean(clustering_distances))
    L_av.append(np.mean(shortest_path_distances))
    
    GCD11_av.append(np.mean(GCD11_distances))
    NetSimile_av.append(np.mean(NetSimile_distances))
    JDD_av.append(np.mean(JDM_distances))
    RNND_av.append(np.mean(RNN_distances))
    JGD_av.append(np.mean(JGM_distances))
    RGDD_av.append(np.mean(RGD_distances))


np.savez("WS_data.npz", C=C_av, L=L_av, GCD11=GCD11_av, NetSimile=NetSimile_av, JDD=JDD_av, RNND=RNND_av, JGD=JGD_av, RGDD=RGDD_av)
