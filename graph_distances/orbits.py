import numpy as np

def ordered(n1,n2):
    if n1 < n2:
        return n1,n2
    else:
        return n2,n1



### ORCA algorithm: compute orbits of three- and four-node graphlets for every node based on equations.
### See Hočevar, Tomaž, and Janez Demšar. "A combinatorial approach to graphlet counting." Bioinformatics 30.4 (2014): 559-565.


def orbit4(G):

    # Precompute triangles per edge and 4-cliques
    
    tri = {ordered(n1,n2):0 for (n1,n2) in G.edges()}
    K4 = {node:0 for node in G.nodes()}
    
    for (n1,n2) in G.edges():
        nb12 = set(G.neighbors(n1)) & set(G.neighbors(n2))
        tri[ordered(n1,n2)] += len(nb12)
        
        for n3 in nb12:
            if n3 < n2 or n3 < n1:
                continue
            for n4 in nb12 & set(G.neighbors(n3)):
                if n4 < n3:
                    continue
                K4[n1] += 1
                K4[n2] += 1
                K4[n3] += 1
                K4[n4] += 1
    
    # Set up a system of equations relating orbits for every node
    
    orbit = {node:np.zeros(15, dtype=int) for node in G.nodes()}
    common = {node:0 for node in G.nodes()}
    common_list = {}
    nc = 0
    for n1 in G.nodes():
        
        f_12_14, f_10_13 = 0, 0
        f_13_14, f_11_13 = 0, 0
        f_7_11, f_5_8 = 0, 0
        f_6_9, f_9_12, f_4_8, f_8_12 = 0, 0, 0, 0
        f_14 = K4[n1]
        
        for i in range(nc):
            common[common_list[i]] = 0
        nc = 0
        
        deg1 = G.degree(n1)
        orbit[n1][0] = deg1
        
        for n2 in G.neighbors(n1):
            for n3 in G.neighbors(n2):
                if G.has_edge(n1,n3):
                    if n3 < n2:
                        f_12_14 += tri[(n3,n2)] - 1
                        f_10_13 += (G.degree(n2) - 1 - tri[(n3,n2)]) + (G.degree(n3) - 1 - tri[(n3,n2)])
                else:
                    if common[n3] == 0:
                        common_list[nc] = n3
                        nc += 1
                    common[n3] += 1
            for n3 in G.neighbors(n1):
                if n3 <= n2:
                    continue
                pair12 = ordered(n1,n2)
                pair13 = ordered(n1,n3)
                if G.has_edge(n2,n3):
                    orbit[n1][3] += 1
                    f_13_14 += tri[pair12] - 1 + tri[pair13] - 1
                    f_11_13 += (deg1 - 1 - tri[pair12]) + (deg1 - 1 - tri[pair13])
                else:
                    orbit[n1][2] += 1
                    f_7_11 += (deg1 - 1 - tri[pair12] - 1) + (deg1 - 1 - tri[pair13] - 1)
                    f_5_8 += (G.degree(n2) - 1 - tri[pair12]) + (G.degree(n3) - 1 - tri[pair13])
        for n2 in G.neighbors(n1):
            for n3 in G.neighbors(n2):
                if n1 == n3:
                    continue
                if not G.has_edge(n1,n3):
                    orbit[n1][1] += 1
                    f_6_9 += (G.degree(n2) - 1 - tri[ordered(n1,n2)] - 1)
                    f_9_12 += tri[ordered(n2,n3)]
                    f_4_8 += (G.degree(n3) - 1 - tri[ordered(n2,n3)])
                    f_8_12 += (common[n3] - 1)

        # Solve system of equations
        orbit[n1][14] = f_14
        orbit[n1][13] = (f_13_14 - 6 * f_14) // 2
        orbit[n1][12] = f_12_14 - 3 * f_14
        orbit[n1][11] = (f_11_13 - f_13_14 + 6 * f_14) // 2
        orbit[n1][10] = f_10_13 - f_13_14 + 6 * f_14
        orbit[n1][9] = (f_9_12 - 2 * f_12_14 + 6 * f_14) // 2
        orbit[n1][8] = (f_8_12 - 2 * f_12_14 + 6 * f_14) // 2
        orbit[n1][7] = (f_13_14 + f_7_11 - f_11_13 - 6 * f_14) // 6
        orbit[n1][6] = (2 * f_12_14 + f_6_9 - f_9_12 - 6 * f_14) // 2
        orbit[n1][5] = (2 * f_12_14 + f_5_8 - f_8_12 - 6 * f_14)
        orbit[n1][4] = (2 * f_12_14 + f_4_8 - f_8_12 - 6 * f_14)
    
    return orbit