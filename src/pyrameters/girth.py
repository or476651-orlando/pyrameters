from dataclasses import dataclass, field
from typing import Dict, Set, List
import networkx as nx

@dataclass
class Graph:

    G: nx.Graph
    @property
    def copy(self):
        return Graph(self.G.copy)
   
#Function that cleans my graph to use just cicles    
def clean(Graph, min_degree):
    G = graph.copy()
    changed = True
    
    while changed:
        changed = False
        to_remove = [v for v in G.vertices if G.degree(v) < 2]
        
        if to_remove:
            changed = True
            
            for v in to_remove:
                G.remove_vertex(v)
                   
    return G

def gith(graph: Graph):
    G = clean(graph)
    
    shortest = inf
    
    for start in G.vertices:
        dist = {start: 0}
        parent = {start: None}
        
        queue = deque([start])
        
        while queue:
            u = queue.popleft()
            
            #Pruning
            for v in G.neighbors(u):
                #Not visited
                 if v not in dist:
                    dist[v] = dist[u] + 1
                    parent[v] = u
                    
                    queue.append(v)
                
                #Found a cycle
                elif parent[u] != v:
                    cycle_length = (dist[u] + dist[v]+1)
                    
                    shortest = min(shortest, cycle_length)
                    
    if shortest == inf:
        return None
    return shortest
                 
