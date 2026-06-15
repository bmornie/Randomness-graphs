import sys
from pathlib import Path
import argparse
import numpy as np
import networkx as nx

from graph_distances.orbits import orbit4
from graph_distances.distances import GCM11, GCD11, NetSimile_signature, NetSimile, JDM, JDD, RNN, RNND, JGM, JGD, RGD, RGDD



parser = argparse.ArgumentParser()

parser.add_argument("-i", required=True)
parser.add_argument("-d", required=True)
parser.add_argument("-o")

args = parser.parse_args()


if args.d not in {"GCD", "NetSimile", "JDD", "RNND", "JGD", "RGDD"}:
    print("Error: unknown distance. Please choose one of the following: JDD, RNND, JGD, RGDD, GCD, NetSimile")
    sys.exit()



folder = Path(args.i)
count = len([f for f in folder.iterdir() if f.is_file()])

print(f"Computing Randomness in a set of {count} graphs using distance function {args.d}...")

filenames = []

if args.d == "JDD":
    all_JDMs = []
    
    for file in folder.iterdir():
        if not file.is_file():
            continue
        filenames.append(file.stem)
        
        G = nx.read_edgelist(str(file), nodetype=int)
        all_JDMs.append(JDM(G))
    
    distances = JDD(all_JDMs)

elif args.d == "RNND":
    all_RNNs = []
    
    for file in folder.iterdir():
        if not file.is_file():
            continue
        filenames.append(file.stem)
        
        G = nx.read_edgelist(str(file), nodetype=int)
        orbits = orbit4(G)
        all_RNNs.append(RNN(orbits))
    
    distances = RNND(all_RNNs)

elif args.d == "JGD":
    all_JGMs = []
    
    for file in folder.iterdir():
        if not file.is_file():
            continue
        filenames.append(file.stem)
        
        G = nx.read_edgelist(str(file), nodetype=int)
        orbits = orbit4(G)
        all_JGMs.append(JGM(orbits))
    
    distances = JGD(all_JGMs)

elif args.d == "RGDD":
    all_RGDs = []
    
    for file in folder.iterdir():
        if not file.is_file():
            continue
        filenames.append(file.stem)
        
        G = nx.read_edgelist(str(file), nodetype=int)
        orbits = orbit4(G)
        all_RGDs.append(RGD(G, orbits))
    
    distances = RGDD(all_RGDs)

elif args.d == "GCD":
    all_GCMs = []
    
    for file in folder.iterdir():
        if not file.is_file():
            continue
        filenames.append(file.stem)
        
        G = nx.read_edgelist(str(file), nodetype=int)
        orbits = orbit4(G)
        all_GCMs.append(GCM11(orbits))
    
    distances = GCD11(all_GCMs)

elif args.d == "NetSimile":
    all_signatures = []
    
    for file in folder.iterdir():
        if not file.is_file():
            continue
        filenames.append(file.stem)
        
        G = nx.read_edgelist(str(file), nodetype=int)
        all_signatures.append(NetSimile_signature(G))
    
    distances = NetSimile(all_signatures)


randomness = np.mean(distances)
print(f"Randomness: {randomness}")


if args.o is not None:
    with open(args.o, "w") as f:
        f.write(f"Randomness: {randomness}\n")
        f.write("graph 1\t graph 2 \t distance\n")
        
        d = 0
        for i in range(count):
            for j in range(i+1, count):
                f.write(f"{filenames[i]}\t {filenames[j]}\t {distances[d]}\n")
                d += 1
        
        if d != len(distances):
            print("Something went wrong...")

    print(f"Pairwise distances saved under {args.o}")