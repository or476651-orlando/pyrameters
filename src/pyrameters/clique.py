import networkx as nx

def maxclique(G: nx.Graph):
    opt_clique: set = set()
    opt_size: int = 0
    
    # El algoritmo asume que los nodos están ordenados/etiquetados numéricamente
    # Grabamos el conjunto total de vértices V
    V = set(G.nodes())

    N = {v: set{G.neighbors(v) for v in v}

    def greedy_color(G_sub: nx.Graph):
        color_class: list[set[int]] = []
        k = 0
        for i in G_sub.nodes():
            h = 0
            while h < k and (N[i] & color_class[h]):
                h += 1
            if h == k:
                k += 1
                color_class.append(set())
            color_class[h] = color_class[h] | {i}
        return k

    def greedy_bound(clique_actual: list, candidatos_actuales: set):
        # El libro llama a la función externa B() pasándole el camino actual.
        # Nuestra cota es: tamaño actual + colores necesarios para el subgrafo de candidatos
        sub_candidates = G.subgraph(candidatos_actuales)
        return (len(clique_actual) + greedy_color(sub_candidates))

    # l representa el nivel (profundidad de la recursión)
    # clique_lista es la lista [x_0, x_1, ..., x_{l-1}]
    # candidatos_C es el conjunto C_l
    def _maxclique2(l: int, clique_lista: list, candidatos_C: set):
        nonlocal opt_clique, opt_size
        
        # if l > OptSize then OptSize <- l, OptClique <- [x_0, ..., x_{l-1}]
        if l > opt_size:
            opt_size = l
            opt_clique = set(clique_lista)
            
        # Al entrar al nivel l, calculamos los candidatos para este nivel (C_l)
        if l == 0:
            C_l = V
        else:
            # Corresponde a: A_{x_{l-1}} intersectado con B_{x_{l-1}} intersectado con C_{l-1}
            C_l = candidatos_C

        #Poda simple
        if len(clique_lista)+len(C_l) <= opt_size:
            return

        # M <- B([x_0, ..., x_{l-1}])
        M = greedy_bound(clique_lista, C_l)
        if M <= opt_size:
            return

        #Primero los de mayor grado
        for x in sorted(C_l, key=lambda v: G.degree(v), reverse = True):
            # x_l <- x y llamada recursiva para el nivel l + 1
            new_candidates = (C_l & N[x] & {v for v in C_l if v > x})
            _maxclique2(l+1, clique_lista + [x], new_candidates)
            
    # main: OptSize <- 0, MAXCLIQUE2(0)
    _maxclique2(0, [], set())
    return opt_clique, opt_size
