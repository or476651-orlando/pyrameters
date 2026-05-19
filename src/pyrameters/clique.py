import networkx as nx


# Grados potenciales a considerar para la clique máxima:
def potencial_grades(G: nx.Graph) -> dict:
    grades = {v: G.degree(v) for v in G.nodes()}

    valid_vertices = {}

    max_degree = max(grades.values())

    for k in range(max_degree, -1, -1):
        verts = [v for v, d in grades.items() if d >= k]

        if len(verts) >= k + 1:
            for v in verts:
                valid_vertices[v] = grades[v]

    return valid_vertices

@dataclass
class Graph:
    neighbors: Dict[int, Set[int]] = field(default_factory=dict)

    def add_vertex(self, v: int) -> None:
        self.neighbors.setdefault(v, set())

    def add_edge(self, u: int, v: int) -> None:
        self.add_vertex(u)
        self.add_vertex(v)

        self.neighbors[u].add(v)
        self.neighbors[v].add(u)
      
    @property
    def vertices(self) -> List[int]:
        return list(self.neighbors.keys())

    def induced_subgraph(self, vertices: Set[int]) -> "Graph":

        subgraph = Graph()

        for v in vertices:
            subgraph.neighbors[v] = (
                self.neighbors[v] & vertices
            )

        return subgraph


def greedy_color(graph: Graph):

    ordering = graph.vertices

    color_classes: List[Set[int]] = []

    for v in ordering:

        h = 0

        while h < len(color_classes):

            if not (graph.neighbors[v] & color_classes[h]):
                break

            h += 1

        if h == len(color_classes):
            color_classes.append(set())

        color_classes[h].add(v)

    return color_classes, len(color_classes)


def greedy_bound(
    graph: Graph,
    clique: Set[int],
    candidates: Set[int]
) -> int:

    induced = graph.induced_subgraph(candidates)

    num_colors = greedy_color(induced)[1]

    return len(clique) + num_colors


def maxclique2_vol2(graph: Graph) -> Set[int]:
    """
    MAXCLIQUE2 from the book.

    Returns
    -------
    set[int]
        A maximum clique.
    """

    best_clique: Set[int] = set()

    def expand(
        clique: Set[int],
        candidates: Set[int]
    ) -> None:

        nonlocal best_clique

        # Update best solution
        if len(clique) > len(best_clique):
            best_clique = clique.copy()

        # Bounding function
        bound = greedy_bound(
            graph,
            clique,
            candidates
        )

        # Pruning
        if bound <= len(best_clique):
            return

        # Recursive expansion
        while candidates:

            v = candidates.pop()

            new_clique = clique | {v}

            new_candidates = (
                candidates &
                graph.neighbors[v]
            )

            expand(
                new_clique,
                new_candidates
            )

    expand(
        clique=set(),
        candidates=set(graph.vertices)
    )

    return best_clique

