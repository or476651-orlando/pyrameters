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
