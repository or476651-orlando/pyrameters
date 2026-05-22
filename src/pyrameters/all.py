from collections import deque
from math import inf
import networkx as nx

#############################
#FUNCIONES AUXILIARES
#############################

#Eliminar los vertices con grado 1, hasta que no haya ninguno
def clean(graph: nx.Graph, min_degree: int = 2):
    """Elimina iterativamente los vértices con grado menor al especificado.

    Funciona como un pre-procesamiento para limpiar la gráfica de nodos que 
    no pueden pertenecer a un ciclo (como hojas o nodos aislados).

    Args:
        graph (networkx.Graph): La gráfica original.
        min_degree (int, opcional): Grado mínimo requerido. Por defecto es 2.

    Returns:
        networkx.Graph: Una nueva gráfica sin los vértices de grado bajo.
    """
    G = graph.copy()
    changed = True
    while changed:
        changed = False
        to_remove = [v for v in G.nodes() if G.degree(v) < min_degree]
        if to_remove:
            changed = True
            G.remove_nodes_from(to_remove)
    return G

#Coloración glotona para acotar
def greedy_color(G_sub: nx.Graph, N: dict):
    """Aplica un algoritmo de coloración voraz (greedy) para encontrar una cota.

    Args:
        G_sub (networkx.Graph): El subgrafo inducido a colorear.
        N (dict): Diccionario de adyacencias precalculado para acceso rápido en O(1).

    Returns:
        int: El número de colores utilizados (k) para iluminar el subgrafo.
    """
    color_classes = []
    k = 0
    nodes = sorted(G_sub.nodes(), key = lambda v: G_sub.degree(v), reverse = True)
    for v in nodes:
        h = 0
        while (h < k and (N[v] & color_classes[h])):
            h += 1
        if h == k:
            k += 1
            color_classes.append(set())
        color_classes[h].add(v)
    return k

#Cota con la coloración glotona
def greedy_bound(G: nx.Graph, clique_actual: list, candidatos_actuales: set, N: dict):
    """Calcula una cota superior para el tamaño del clique usando coloración voraz.

    Aprovecha la propiedad χ(G) >= ω(G) para podar el árbol de búsqueda en la 
    búsqueda del clique máximo.

    Args:
        G (networkx.Graph): La gráfica original.
        clique_actual (list): Nodos actualmente en el clique parcial.
        candidatos_actuales (set): Nodos que pueden expandir el clique.
        N (dict): Diccionario de vecindades precalculado.

    Returns:
        int: Cota superior del tamaño del clique para esta rama.
    """
    sub_candidates = G.subgraph(candidatos_actuales)
    return (len(clique_actual)+greedy_color(sub_candidates, N))


#############################
#NÚMERO DE CLAN
#############################
def maxclique(G: nx.Graph):
    """Calcula el clique máximo y el número de clan (ω(G)) de una gráfica simple.

    Implementa el algoritmo exacto Branch and Bound. Como optimización no trivial,
    utiliza una heurística de coloración voraz para calcular cotas superiores y 
    podar ramas que no pueden superar el tamaño del mejor clique encontrado.

    Args:
        G (networkx.Graph): Gráfica de NetworkX a analizar.

    Returns:
        tuple: Una tupla que contiene:
            - set: El conjunto de vértices que conforman el clique máximo.
            - int: El tamaño del clique máximo (ω(G)).
    """
    opt_clique = set()
    opt_size = 0
    V = set(G.nodes())
    N = {v: set(G.neighbors(v)) for v in V}
    order = {v:i for i,v in enumerate(sorted(G.nodes()))}
    grado = dict(G.degree())
    
    def expand(level, clique, candidates):
        nonlocal opt_clique
        nonlocal opt_size
        if len(clique) > opt_size:
            opt_size = len(clique)
            opt_clique = set(clique)

        if level == 0:
            C_l = V
        else:
            C_l = candidates

        #Cota simple
        if (len(clique) + len(C_l) <= opt_size):
            return

        #Cota de coloración
        M = greedy_bound(G, clique, C_l, N)
        if M <= opt_size:
            return

        #Primero los vertices con mayor grado
        for x in sorted(C_l, key = lambda v: grado[v], reverse=True):
            new_candidates = (C_l & N[x] & {v for v in C_l if order[v] > order[x]})
            expand(level+1, clique + [x], new_candidates)

    expand(0, [],set())
    return opt_clique, opt_size
    

##########################            
#NÚMERO CROMÁTICO
##########################
def numero_cromatico(G: nx.Graph, lower_bound: int):
    """Calcula el número cromático (χ(G)) de una gráfica simple.
    
    Utiliza un algoritmo de backtracking optimizado con ruptura de simetría y 
    branch & bound. Además, acepta una cota inferior (como el número de clan ω) 
    para detener tempranamente la búsqueda si se alcanza el óptimo teórico.

    Args:
        G (networkx.Graph): La gráfica a colorear.
        lower_bound (int): Cota inferior teórica conocida, típicamente ω(G).

    Returns:
        int: El número mínimo de colores necesarios (χ(G)).
    """
    n = G.number_of_nodes()
    if n == 0:
        return 0
    V = set(G.nodes())
    N = {v: set(G.neighbors(v)) for v in V}
    grado = dict(G.degree())
    
    # Optimización 3: Ordenar los nodos por grado descendente.
    # Los nodos más conectados son más restrictivos, lo que ayuda a podar rápido.
    vertices = sorted(G.nodes(), key=lambda v: grado[v], reverse=True)
    
    # Límite superior trivial: colorear cada nodo con un color distinto
    best_chi = greedy_color(G,N)
    asignacion_colores = {}
    
    if best_chi == lower_bound:
        return best_chi
        
    def es_seguro(vertice, color):
        """Verifica que ningún vecino tenga el mismo color."""
        for vecino in G.neighbors(vertice):
            if (vecino in asignacion_colores and asignacion_colores[vecino] == color):
                return False
        return True

    def resolver(idx, max_color_usado):
        nonlocal best_chi
        
        # Caso base: Todos los nodos han sido coloreados
        if idx == n:
            best_chi = min(best_chi, max_color_usado)
            return

        
        vertice = vertices[idx]
        
        # Optimizaciones 1 y 2 (Ruptura de Simetría y Branch & Bound):
        # - Límite superior de color a intentar: max_color_usado + 1 (evita permutaciones)
        # - Límite de poda: best_chi - 1 (no tiene sentido igualar o empeorar el mejor hallazgo)
        limite_color = min(max_color_usado + 1, best_chi - 1)

        for c in range(1, limite_color + 1):
            if es_seguro(vertice, c):
                # Hacer la elección
                asignacion_colores[vertice] = c
                
                # Explorar esa rama, actualizando el máximo color usado en esta ruta
                resolver(idx + 1, max(max_color_usado, c))
                
                # Backtrack (deshacer la elección)
                del asignacion_colores[vertice]

    # Iniciar la recursión desde el primer nodo, usando 0 colores inicialmente
    resolver(0, lower_bound - 1)
    
    return best_chi



#######################
#CUELLO O GIRTH
#######################
def cuello(graph: nx.Graph, clique: int):
    #Detección de Triangulos
    if clique >= 3:
        return 3
    
    G = clean(graph)
    if G.number_of_nodes() == 0:
        return None

    shortest = inf

    # BFS from every vertex
    for start in G.nodes():

        dist = {start: 0}
        parent = {start: None}

        queue = deque([start])

        while queue:

            u = queue.popleft()

            # Pruning
            if 2 * dist[u] + 1 >= shortest:
                continue

            for v in G.neighbors(u):

                #Nuevo vertice
                if v not in dist:

                    dist[v] = dist[u] + 1
                    parent[v] = u

                    queue.append(v)

                # Ciclo encontrado
                elif parent[u] != v:

                    cycle_length = (
                        dist[u]
                        + dist[v]
                        + 1
                    )

                    shortest = min(
                        shortest,
                        cycle_length
                    )

    if shortest == inf:
        return None

    return shortest


#######################
#PARAMETROS
#######################
def pyrameters(G: nx.Graph):
    clique, omega = maxclique(G)
    chi = numero_cromatico(G, lower_bound = omega)
    g = cuello(G, omega)
    return { "maximum_clique": clique, "clique_number": omega, "girth": g, "chromatic_number": chi}
