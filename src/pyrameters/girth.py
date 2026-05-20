from collections import deque
from math import inf

import networkx as nx


# Removes vertices with degree < min_degree
# until no more can be removed
def clean(graph: nx.Graph, min_degree: int = 2):

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


# Returns the girth (shortest cycle length)
def girth(graph: nx.Graph):

    G = clean(graph)

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

                # New vertex
                if v not in dist:

                    dist[v] = dist[u] + 1
                    parent[v] = u

                    queue.append(v)

                # Found cycle
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
                 
