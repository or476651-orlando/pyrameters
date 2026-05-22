from collections import deque
from math import inf
import networkx as nx

#############################
#FUNCIONES AUXILIARES
#############################

#Eliminar los vertices con grado 1, hasta que no haya ninguno
def clean(graph: nx.Graph, min_degree: int = 2):
    G = graph.copy()
    changed = True
    while changed:
        changed = False
        to_remove = [v in G.nodes() if G.degree(v) < min_degree]
        if to_remove:
            changed = True
            G.remove_nodes_from(to_remove)
    return G

#Coloración glotona para acotar
def greedy_color(G_sub: nx.Graph, N: dict):
    color_classes = []
    k = 0
    for v in G_sub.nodes():
        h = 0
        while( h<k and (N[v] & color_classes[h])):
            h += 1
        if h == k:
            k += 1
            color_classes.append(set())
        color_classes[h].add(v)
    return k

#Cota con la coloración glotona
def greedy_bound(G: nx.Graph, clique_actual: list, candidatos_actuales: set, N: dict):
    sub_candidates = G.subgraph(candidatos_actuales)
    return (len(clique_actual)+greedy_color(sub_candidates, N))


#############################
#CLAN MAXIMO
#############################
def maxclique(G: nx.Graph):
    opt_clique = set()
    opt_size = 0
    V = set(G.nodes())
    N = {v: set(G.neighbors(v)) for v in v}

    def expand(level, clique, candidates):
        nonlocal opt_clique
        nonlocal opt_size
        if level > opt_size:
            opt_size = level
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
        for x in sorted(C_l, key = lambda v: G.degree(v), reverse=True):
            new_candidates = (C_l & N[x] & {v for v in C_l if v > x})
            expand(level+1, clique + [x], new_candidates)

    expand(0, [],set())
    return (opt_clique,opt_size)
    

            


def calcular_numero_cromatico(G: nx.Graph) -> int:
    """
    Calcula el número cromático (χ(G)) de una gráfica simple usando 
    backtracking con ruptura de simetría y branch & bound.
    """
    n = G.number_of_nodes()
    if n == 0:
        return 0
        
    # Optimización 3: Ordenar los nodos por grado descendente.
    # Los nodos más conectados son más restrictivos, lo que ayuda a podar rápido.
    nodos = sorted(G.nodes(), key=lambda x: G.degree(x), reverse=True)
    
    # Límite superior trivial: colorear cada nodo con un color distinto
    best_chi = n 
    asignacion_colores = {}

    def es_seguro(nodo, color, asignacion):
        """Verifica que ningún vecino tenga el mismo color."""
        for vecino in G.neighbors(nodo):
            if vecino in asignacion and asignacion[vecino] == color:
                return False
        return True

    def resolver(idx, max_color_usado):
        nonlocal best_chi
        
        # Caso base: Todos los nodos han sido coloreados
        if idx == n:
            if max_color_usado < best_chi:
                best_chi = max_color_usado
            return

        nodo = nodos[idx]
        
        # Optimizaciones 1 y 2 (Ruptura de Simetría y Branch & Bound):
        # - Límite superior de color a intentar: max_color_usado + 1 (evita permutaciones)
        # - Límite de poda: best_chi - 1 (no tiene sentido igualar o empeorar el mejor hallazgo)
        limite_color = min(max_color_usado + 1, best_chi - 1)

        for c in range(1, limite_color + 1):
            if es_seguro(nodo, c, asignacion_colores):
                # Hacer la elección
                asignacion_colores[nodo] = c
                
                # Explorar esa rama, actualizando el máximo color usado en esta ruta
                resolver(idx + 1, max(max_color_usado, c))
                
                # Backtrack (deshacer la elección)
                del asignacion_colores[nodo]

    # Iniciar la recursión desde el primer nodo, usando 0 colores inicialmente
    resolver(0, 0)
    
    return best_chi
