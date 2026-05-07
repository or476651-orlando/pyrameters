import networkx as nx

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

# --- Ejemplo de uso ---
#  ejemplo (Petersen tiene χ(G) = 3)
G = nx.petersen_graph()
chi = calcular_numero_cromatico(G)
print(f"El número cromático χ(G) es: {chi}")
