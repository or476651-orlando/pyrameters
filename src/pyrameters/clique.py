import networkx as nx

def greedy_color(G_sub):
    color_class = []
    k = 0
    for i in G_sub.nodes():
        h = 0
        while h < k and (set(G_sub.neighbors(i)) & color_class[h]):
            h += 1
        if h == k:
            k += 1
            color_class.append(set())
        color_class[h] = color_class[h] | {i}
    return k, color_class

def greedy_bound(G, X: set):
    if not X:
        return len(G.nodes())
    clique_nodes = list(X)
    candidates = set(G.neighbors(clique_nodes[0]))
    for nodo in clique_nodes[1:]:
        candidates &= set(G.neighbors(nodo))
    sub_candidates = G.subgraph(candidates)
    return len(X) + greedy_color(sub_candidates)[0]

def maxclique_solver(G):
    opt_clique = set()
    opt_size = 0

    def _cliquebacktracking(X):
        nonlocal opt_clique, opt_size
        
        if len(X) > opt_size:
            opt_size = len(X)
            opt_clique = X.copy()
            
        if not X:
            candidates = set(G.nodes())
        else:
            ultimo_nodo = max(X)
            candidates = set(G.neighbors(ultimo_nodo)) & {v for v in G.nodes() if v not in X and v > ultimo_nodo}
            
        M = greedy_bound(G, X)
        
        for nodo in candidates:
            if M <= opt_size:
                return
            _cliquebacktracking(X | {nodo})

    _cliquebacktracking(set())
    return opt_clique, opt_size

