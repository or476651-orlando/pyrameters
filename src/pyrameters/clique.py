import networkx as nx

def calcular_clique(G: nx.Graph) -> int:
    """Calcula el número de clan (ω(G)) de una gráfica simple.

    Utiliza un algoritmo exacto basado en ramificación y poda (branch & bound).
    Como optimización no trivial, emplea un algoritmo de coloración voraz 
    (greedy coloring) para estimar una cota superior en cada rama y podar el 
    árbol de búsqueda eficientemente.

    Args:
        G (networkx.Graph): La gráfica simple sobre la cual calcular el número de clan.

    Returns:
        int: El tamaño del clique máximo (ω(G)).
    """
    opt_clique: set = set()
    opt_size: int = 0
    
    # El algoritmo asume que los nodos están ordenados/etiquetados numéricamente
    # Grabamos el conjunto total de vértices V
    V = set(G.nodes())

    N = {v: set(G.neighbors(v)) for v in V}

    def greedy_color(G_sub: nx.Graph) -> int:
        """Aplica un algoritmo de coloración voraz a un subgrafo.

        Dado que en cualquier gráfica el número cromático es mayor o igual al 
        tamaño de su clique máximo (χ(G) >= ω(G)), los colores usados sirven 
        como una cota superior para podar la búsqueda.

        Args:
            G_sub (networkx.Graph): El subgrafo inducido por los nodos candidatos.

        Returns:
            int: La cantidad de colores utilizados (k) para colorear el subgrafo.
        """
        color_class: list[set[int]] = []
        k = 0
        nodes = sorted(G_sub.nodes(), key = lambda v: G_sub.degree(v), reverse = True)
        for i in nodes:
            h = 0
            while h < k and (N[i] & color_class[h]):
                h += 1
            if h == k:
                k += 1
                color_class.append(set())
            color_class[h] = color_class[h] | {i}
        return k

    def greedy_bound(clique_actual: list, candidatos_actuales: set) -> int:
        """Calcula la cota superior del tamaño del clique para el estado actual.

        Args:
            clique_actual (list): Lista de nodos que conforman el clique actual.
            candidatos_actuales (set): Conjunto de nodos que podrían expandir el clique.

        Returns:
            int: Cota superior calculada (tamaño del clique actual + colores 
                 necesarios para el subgrafo de candidatos).
        """
        # El libro llama a la función externa B() pasándole el camino actual.
        # Nuestra cota es: tamaño actual + colores necesarios para el subgrafo de candidatos
        sub_candidates = G.subgraph(candidatos_actuales)
        return (len(clique_actual) + greedy_color(sub_candidates))

    # l representa el nivel (profundidad de la recursión)
    # clique_lista es la lista [x_0, x_1, ..., x_{l-1}]
    # candidatos_C es el conjunto C_l
    def _maxclique2(l: int, clique_lista: list, candidatos_C: set):
        """Explora el árbol de búsqueda recursivamente buscando el clique máximo.

        Utiliza retroceso (backtracking) y descarta ramas si su cota superior
        no puede superar el tamaño del mejor clique encontrado hasta el momento.

        Args:
            l (int): Nivel actual de profundidad de la recursión.
            clique_lista (list): Lista de vértices en el clique parcial actual.
            candidatos_C (set): Conjunto de vértices candidatos para el nivel l.
        """
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

        # Poda simple: si sumando todos los candidatos no superamos el óptimo, podamos
        if len(clique_lista) + len(C_l) <= opt_size:
            return

        # M <- B([x_0, ..., x_{l-1}])
        # Poda avanzada: usando la coloración voraz como cota superior
        M = greedy_bound(clique_lista, C_l)
        if M <= opt_size:
            return

        # Primero los de mayor grado
        for x in sorted(C_l, key=lambda v: G.degree(v), reverse = True):
            # x_l <- x y llamada recursiva para el nivel l + 1
            new_candidates = (C_l & N[x] & {v for v in C_l if v > x})
            _maxclique2(l+1, clique_lista + [x], new_candidates)
            
    # main: OptSize <- 0, MAXCLIQUE2(0)
    _maxclique2(0, [], set())
    return opt_size
