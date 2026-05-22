import networkx as nx

def calcular_numero_cromatico(G: nx.Graph) -> int:
    """
    Calcula el número cromático (χ(G)) usando backtracking optimizado 
    con ruptura de simetría y branch & bound.
    """
    n = G.number_of_nodes()
    if n == 0:
        return 0
        
    # Precalculamos grados para un ordenamiento más limpio y rápido
    grados = dict(G.degree())
    nodos = sorted(G.nodes(), key=lambda x: grados[x], reverse=True)
    
    best_chi = n 
    asignacion_colores = {}

    def es_seguro(nodo, color):
        """Verifica que ningún vecino tenga el mismo color."""
        for vecino in G.neighbors(nodo):
            # Usamos .get() para evitar comprobar primero si existe en el diccionario
            if asignacion_colores.get(vecino) == color:
                return False
        return True

    def resolver(idx, max_color_usado):
        nonlocal best_chi
        
        # Caso base: Todos los nodos han sido coloreados
        if idx == n:
            # Ya no necesitamos el 'if', la poda garantiza que si llegamos 
            # aquí, max_color_usado es estrictamente menor que best_chi
            best_chi = max_color_usado
            return

        nodo = nodos[idx]
        limite_color = min(max_color_usado + 1, best_chi - 1)

        for c in range(1, limite_color + 1):
            if es_seguro(nodo, c):
                asignacion_colores[nodo] = c
                resolver(idx + 1, max(max_color_usado, c))
                del asignacion_colores[nodo]

    resolver(0, 0)
    return best_chi
