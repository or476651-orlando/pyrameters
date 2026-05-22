from collections import deque
from math import inf
import networkx as nx

def clean(graph: nx.Graph, min_degree: int = 2) -> nx.Graph:
    """Elimina iterativamente los vértices con grado menor al especificado.

    Esta función realiza un pre-procesamiento o poda estructural de la gráfica. 
    Es útil como optimización antes de buscar ciclos, ya que los vértices con 
    grado menor a 2 (nodos aislados o "hojas") no pueden formar parte de ningún 
    ciclo. Al eliminar un vértice, el grado de sus vecinos puede disminuir, por 
    lo que el proceso se repite hasta estabilizarse.

    Args:
        graph (networkx.Graph): La gráfica original a limpiar.
        min_degree (int, opcional): El grado mínimo que debe tener un vértice 
            para ser conservado. Por defecto es 2.

    Returns:
        networkx.Graph: Una copia de la gráfica original excluyendo los vértices
            que no alcanzan el grado mínimo.
    """
    G = graph.copy()
    changed = True

    while changed:
        changed = False

        to_remove = [
            v for v in G.nodes()
            if G.degree(v) < min_degree
        ]

        if to_remove:
            changed = True
            G.remove_nodes_from(to_remove)

    return G


def girth(graph: nx.Graph):
    """Calcula el girth (longitud del ciclo más corto) de una gráfica simple.

    Utiliza el algoritmo de Búsqueda a lo Ancho (BFS) iterando desde cada vértice 
    como raíz. Como optimización no trivial, aplica una poda temprana (pruning) 
    para detener la búsqueda en un nivel si la distancia actual ya no permite 
    encontrar un ciclo más corto que el mejor hallado hasta el momento.

    Args:
        graph (networkx.Graph): La gráfica sobre la cual buscar los ciclos.

    Returns:
        int | None: La longitud del ciclo más corto encontrado en la gráfica.
            Devuelve None si la gráfica no contiene ciclos (por ejemplo, si es 
            un árbol o un bosque vaciado por la función `clean`).
    """
    # Se optimiza limpiando la gráfica primero
    G = clean(graph)

    shortest = inf

    # Búsqueda a lo ancho (BFS) desde cada vértice
    for start in G.nodes():
        dist = {start: 0}
        parent = {start: None}

        queue = deque([start])

        while queue:
            u = queue.popleft()

            # Optimización (Poda): Si la distancia actual desde este nodo ya no puede 
            # producir un ciclo más corto que el mejor conocido, dejamos de explorar.
            if 2 * dist[u] + 1 >= shortest:
                continue

            for v in G.neighbors(u):
                # Vértice nuevo (no visitado)
                if v not in dist:
                    dist[v] = dist[u] + 1
                    parent[v] = u
                    queue.append(v)

                # Si el vecino ya tiene una distancia registrada y no es el 
                # padre directo de donde venimos, ¡hemos encontrado un ciclo!
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
