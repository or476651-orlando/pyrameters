import networkx as nx

def greedy_color(G_sub):
    color_class = []
    for v in G_sub.nodes():
        h = 0
        while h < len(color_classes):
            if not ( set(G_sub.neighbors(v)) & color_classes[h]):
                break
            h +=1
            
        if h == len(color_classes):
            color_class.append(set())
        color_class[h].add(v)
    return len(color_classes), color_class

def greedy_bound(G, clique, candidates):
    sub_candidates = G.subgraph(candidates)
    num_colors = greedy_color(sub_candidates)[0]
    return len(clique) + num_colors

def maxclique_solver(G):
    opt_clique = set()
    opt_size = 0

    def expand(clique, candidate):
        nonlocal opt_clique, opt_size

        #actualizar mejor solución
        if len(clique) > opt_size:
            opt_size = len(clique)
            opt_clique = clique.copy()

        #Cota superior
        M = greedy_bound(G, clique, candidates)

        #Pruning
        if M <= opt_size:
            return

        while candidates:
            v = candidates.pop()
            new_clique = (clique | {v})
            new_candidates = (candidates & set(G.neighbors(v)))
            expand(new_clique, new_candidates)
    expand(clique=set(), candidates = set(G.nodes()))
    return opt_clique, opt_size
    
