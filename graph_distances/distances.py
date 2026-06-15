import numpy as np
import networkx as nx
from scipy.stats import spearmanr, skew, kurtosis



### Graphlet Correlation Distance, as proposed in:
### Yaveroğlu, Ömer Nebil, et al. "Revealing the hidden language of complex networks." Scientific reports 4.1 (2014): 4547

def GCM11(orbits):
    orb11 = np.array([[val[0], val[2], val[5], val[7], val[8], val[10], val[11], val[6], val[9], val[4], val[1]] for val in orbits.values()] + [[1]*11])
    spearman = spearmanr(orb11).statistic
    return np.triu(spearman, k=1)

def GCD11(all_GCMs):
    N = len(all_GCMs)
    
    distances = []
    for i in range(N):
        GCM1 = all_GCMs[i]
        for j in range(i+1, N):
            GCM2 = all_GCMs[j]
            d = np.sqrt(np.sum((GCM1 - GCM2)**2))
            distances.append(d)
    
    return distances


### NetSimile, as proposed in:
### Berlingerio, Michele, et al. "Netsimile: A scalable approach to size-independent network similarity." arXiv preprint arXiv:1209.2684 (2012)

def NetSimile_signature(G):
    
    degrees = dict(G.degree())
    clustering = dict(nx.clustering(G))
    
    graph_features = np.zeros((G.number_of_nodes(), 7))
    for i, n in enumerate(G.nodes()):
        d = degrees[n]
        features = np.zeros(7)
        
        if d != 0:
            egonet = nx.ego_graph(G, n)
            features[0] = d
            features[1] = clustering[n]
            features[2] = sum([degrees[nb] for nb in G.neighbors(n)])/d
            features[3] = sum([clustering[nb] for nb in G.neighbors(n)])/d
            features[4] = egonet.number_of_edges()
            features[5] = d*features[2] - 2*features[4]
            features[6] = len(set([enb for nb in G.neighbors(n) for enb in G.neighbors(nb)]) - set(G.neighbors(n)) - set([n]))
        
        graph_features[i] = features
    
    
    signature = np.zeros((7,5))
    for k in range(7):
        signature[k, 0] = graph_features[:, k].mean()
        signature[k, 1] = np.median(graph_features[:, k])
        signature[k, 2] = graph_features[:, k].std()
        signature[k, 3] = skew(graph_features[:, k])
        signature[k, 4] = kurtosis(graph_features[:, k])

    return np.nan_to_num(signature)

def NetSimile(all_signatures):
    N = len(all_signatures)
    distances = []
    
    for i in range(N):
        for j in range(i+1, N):
            S1 = all_signatures[i]
            S2 = all_signatures[j]
            d = np.sum(np.abs(S1-S2)/(np.abs(S1)+np.abs(S2)+1e-10))
            distances.append(d)
    
    return distances




### Own methods


def JDM(G):
    degrees = dict(G.degree())
    max_deg = max(degrees.values())
    JDM = np.zeros((max_deg, max_deg), dtype=int)
    for e in G.edges():
        i = degrees[e[0]] - 1
        j = degrees[e[1]] - 1
        JDM[i,j] += 1
        if i != j:
            JDM[j,i] += 1
    return JDM

def JDD(all_JDMs):
    N = len(all_JDMs)
    distances = []
    for i in range(N):
        for j in range(i+1, N):
            max_size = max(len(all_JDMs[i]), len(all_JDMs[j]))
            JDM1 = np.triu(np.pad(all_JDMs[i], ((0, max_size - len(all_JDMs[i])), (0, max_size - len(all_JDMs[i]))), mode='constant'))
            JDM2 = np.triu(np.pad(all_JDMs[j], ((0, max_size - len(all_JDMs[j])), (0, max_size - len(all_JDMs[j]))), mode='constant'))
            
            d = np.sqrt(np.sum((JDM1/np.sum(JDM1) - JDM2/np.sum(JDM2))**2))
            distances.append(d)
    
    return distances



def RNN(orbits):
    graphlets = {key:[val[1]+val[2], val[3], val[6]+val[7], val[4]+val[5], val[9]+val[10]+val[11], val[8], val[12]+val[13], val[14]] for key, val in orbits.items()}
    
    total_counts = np.zeros(8)
    for val in graphlets.values():
        total_counts += np.array(val)
    
    reduced_node_vector = np.zeros(len(total_counts))
    for i in range(len(total_counts)):
        for val in graphlets.values():
            if val[i] != 0:
                reduced_node_vector[i] += 1
    
    reduced_node_vector /= (total_counts + 1e-10)
    return reduced_node_vector

def RNND(all_RNNs):
    N = len(all_RNNs)
    
    distances = []
    for i in range(N):
        RNN1 = all_RNNs[i]
        for j in range(i+1, N):
            RNN2 = all_RNNs[j]
            d = np.sqrt(np.sum((RNN1 - RNN2)**2))
            distances.append(d)
    
    return distances



def JGM(orbits):
    Ng = 8
    graphlets = {key:np.array([val[1]+val[2], val[3], val[6]+val[7], val[4]+val[5], val[9]+val[10]+val[11], val[8], val[12]+val[13], val[14]]) for key, val in orbits.items()}
    total = np.zeros(Ng)
    for val in graphlets.values():
        total += val
    total /= np.array([3,3,4,4,4,4,4,4])

    JGM = np.zeros((Ng,Ng))
    n = [0]*Ng
    for key in graphlets.keys():
        for i in range(Ng):
            if graphlets[key][i] == 0:
                continue
            n[i] += graphlets[key][i]
            JGM[i] += graphlets[key]*graphlets[key][i]
    
    for i in range(Ng):
        JGM[i] /= (n[i]*total+1e-10)
    
    return JGM

def JGD(all_JGMs):
    N = len(all_JGMs)
    
    distances = []
    for i in range(N):
        JGM1 = all_JGMs[i]
        for j in range(i+1, N):
            JGM2 = all_JGMs[j]
            distances.append(np.sqrt(np.sum((JGM1 - JGM2)**2)))
    
    return distances



def RGD(G, orbits):

    Gc = G.subgraph(max(nx.connected_components(G), key=len)).copy()

    lengths = dict(nx.all_pairs_shortest_path_length(Gc))

    nodes = list(lengths.keys())
    idx = {n: i for i, n in enumerate(nodes)}
    N = len(nodes)

    # dense distance matrix
    D = np.full((N, N), -1, dtype=np.int16)

    for u, dist_dict in lengths.items():
        i = idx[u]
        for v, d in dist_dict.items():
            D[i, idx[v]] = d

    diameter = int(D.max())

    # orbit matrix (11 x N)
    O = np.zeros((11, N), dtype=np.float64)

    for k, v in orbits.items():
        if k in idx:
            O[:, idx[k]] = np.array([
                v[0], v[2], v[5], v[7], v[8],
                v[10], v[11], v[6], v[9], v[4], v[1]
            ])

    rgd = []

    for i in range(11):

        w = O[i]
        mask = w > 0

        good_idx = np.where(mask)[0]

        if len(good_idx) <= 1:
            rgd.append(np.zeros(diameter + 1))
            continue

        w_good = w[good_idx]
        total = w_good.sum()

        D_sub = D[np.ix_(good_idx, good_idx)]

        # nrgd[d] accumulates contributions from column-wise weights
        node_rgds_sum = np.zeros(diameter + 1)

        for j in range(len(good_idx)):
            col = D_sub[:, j]
            weights = w_good

            # histogram for fixed n1
            nrgd = np.bincount(col, weights=weights, minlength=diameter + 1)

            node_rgds_sum += nrgd

        rgd.append(node_rgds_sum / (len(good_idx) * total))

    return rgd

def RGDD(all_RGDs):
    N = len(all_RGDs)
    n_orbits = len(all_RGDs[0])
    
    distances = []
    for i in range(N):
        for j in range(i+1, N):
            d = []
            for k in range(n_orbits):
                rgd1 = all_RGDs[i][k]
                rgd2 = all_RGDs[j][k]
                max_size = max(len(rgd1), len(rgd2))
                rgd1 = np.pad(rgd1, (0, max_size-len(rgd1)), mode='constant')
                rgd2 = np.pad(rgd2, (0, max_size-len(rgd2)), mode='constant')
                d.append(np.sqrt(np.sum((rgd1 - rgd2)**2)))
            
            distances.append(np.mean(d))
    
    return distances
