import sys
from pathlib import Path
import networkx as nx
from time import perf_counter

sys.path.append(str(Path(__file__).resolve().parents[2]))

from graph_distances.orbits import orbit4
from graph_distances.distances import JDM, JDD, RNN, RNND, JGM, JGD, RGD, RGDD





d = sys.argv[1]
N = int(sys.argv[2])
m = int(sys.argv[3])
M = m*N
runs = int(sys.argv[4])


if d != "JDD" and d != "RNND" and d != "JGD" and d != "RGDD":
    print("Error: unknown distance.")
    sys.exit(1)

graphs_A = [nx.gnm_random_graph(N, M) for _ in range(runs)]
graphs_B = [nx.gnm_random_graph(N, M) for _ in range(runs)]


runtimes = []

if d == "JDD":
    for i in range(runs):
        A = graphs_A[i]
        B = graphs_B[i]
        
        start = perf_counter()
        
        JDD([JDM(A), JDM(B)])
        
        runtimes.append(perf_counter() - start)

elif d == "RNND":
    for i in range(runs):
        A = graphs_A[i]
        B = graphs_B[i]
        
        start = perf_counter()
        
        RNND([RNN(orbit4(A)), RNN(orbit4(B))])
        
        runtimes.append(perf_counter() - start)

elif d == "JGD":
    for i in range(runs):
        A = graphs_A[i]
        B = graphs_B[i]
        
        start = perf_counter()
        
        JGD([JGM(orbit4(A)), JGM(orbit4(B))])
        
        runtimes.append(perf_counter() - start)

elif d == "RGDD":
    for i in range(runs):
        A = graphs_A[i]
        B = graphs_B[i]
        
        start = perf_counter()
        
        RGDD([RGD(A, orbit4(A)), RGD(B, orbit4(B))])
        
        runtimes.append(perf_counter() - start)


with open(f"timing_{d}_{N}_{M}.txt", "w") as f:
    for t in runtimes:
        f.write(str(t))
        f.write("\n")