import networkx as nx


graph = "GEO"

N = 500

print(f"Generating {N} 0k graphs based on source network {graph}...")



read_path = "data/%s/%s.txt" %(graph, graph)
write_path = "data/%s/dk0/dk0.0_%s" %(graph, graph)


G = nx.read_edgelist(read_path)
n = G.number_of_nodes()
m = G.number_of_edges()

for i in range(N):
    H = nx.gnm_random_graph(n, m, seed=i*13)
    nx.write_edgelist(H, write_path+str(i)+".txt")