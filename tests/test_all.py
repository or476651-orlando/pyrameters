import networkx as nx
# Importamos las funciones individuales además de la integradora
from pyrameters.all import maxclique, numero_cromatico, cuello, pyrameters

#############################
# AUXILIAR
#############################
def es_clique(G: nx.Graph, C: list) -> bool:
    """Verifica matemáticamente si un conjunto de nodos forma un clique.

    Un clique requiere que todos los nodos del conjunto estén conectados 
    directamente entre sí. Esta función valida el resultado de nuestros algoritmos.

    Args:
        G (networkx.Graph): La gráfica original.
        C (list o iterable): El conjunto de nodos que supuestamente forman el clique.

    Returns:
        bool: True si cada par de nodos en C comparte una arista, False en caso contrario.
    """
    C = list(C)
    for i in range(len(C)):
        for j in range(i + 1, len(C)):
            if not G.has_edge(C[i], C[j]):
                return False
    return True


###########################################################
# UNIT TESTS: MÓDULO CLIQUE MAXIMAL
###########################################################

def test_unit_maxclique_complete():
    """Prueba el cálculo del clique máximo en una gráfica completa K_15.
    
    Caso de borde/extremo: En una gráfica completa, todos los nodos están
    conectados con todos, por lo que el clique máximo (ω) es igual a n.
    """
    G = nx.complete_graph(15)
    clique, omega = maxclique(G)
    assert es_clique(G, clique)
    assert omega == 15
    assert len(clique) == 15

def test_unit_maxclique_petersen():
    """Prueba el clique máximo en la gráfica de Petersen.
    
    Caso de validación: Se sabe matemáticamente que la gráfica de Petersen 
    no tiene triángulos, por lo que su clique máximo es exactamente 2.
    """
    G = nx.petersen_graph()
    clique, omega = maxclique(G)
    assert es_clique(G, clique)
    assert omega == 2

def test_unit_maxclique_empty():
    """Prueba el clique máximo en una gráfica vacía (sin aristas).
    
    Caso de borde: Si no hay aristas, el clique máximo es simplemente 
    un solo vértice, es decir, ω(G) = 1.
    """
    G = nx.empty_graph(10)
    clique, omega = maxclique(G)
    assert omega == 1


###########################################################
# UNIT TESTS: MÓDULO NÚMERO CROMÁTICO
###########################################################

def test_unit_cromatico_cycle_odd():
    """Prueba el número cromático (χ) de un ciclo impar.
    
    Caso de validación: Cualquier ciclo de longitud impar C_{2k+1} 
    requiere exactamente 3 colores.
    """
    G = nx.cycle_graph(7)
    # Se prueba la función de forma aislada sin depender de pyrameters
    assert numero_cromatico(G, lower_bound=2) == 3 

def test_unit_cromatico_bipartite():
    """Prueba el número cromático (χ) de una gráfica bipartita completa.
    
    Caso de validación: Por definición, una gráfica bipartita (con 
    al menos una arista) tiene un número cromático exactamente igual a 2.
    """
    G = nx.complete_bipartite_graph(5, 10)
    assert numero_cromatico(G, lower_bound=2) == 2

def test_unit_cromatico_petersen():
    """Prueba el número cromático en la gráfica de Petersen.
    
    Caso de validación: Matemáticamente establecido que χ(Petersen) = 3.
    """
    G = nx.petersen_graph()
    assert numero_cromatico(G, lower_bound=2) == 3


###########################################################
# UNIT TESTS: MÓDULO GIRTH / CUELLO
###########################################################

def test_unit_cuello_heawood():
    """Prueba el cálculo del cuello (girth) en la gráfica de Heawood.
    
    Caso de validación: La gráfica de Heawood es una (3,6)-jaula, 
    por lo que su cuello es exactamente 6.
    """
    G = nx.heawood_graph()
    # Le pasamos un valor neutro de clique (ej. 2) para evaluar el algoritmo de BFS puro
    assert cuello(G, clique=2) == 6 

def test_unit_cuello_petersen():
    """Prueba el cuello (girth) en la gráfica de Petersen.
    
    Caso de validación: La gráfica de Petersen es una (3,5)-jaula,
    por lo que su cuello es exactamente 5.
    """
    G = nx.petersen_graph()
    assert cuello(G, clique=2) == 5

def test_unit_cuello_path():
    """Prueba el cuello en una gráfica de camino (Path Graph).
    
    Caso de borde (sin solución): Los caminos son árboles, no tienen ciclos. 
    Por lo tanto, la función debe devolver None.
    """
    G = nx.path_graph(20)
    assert cuello(G, clique=2) is None


###########################################################
# TEST GLOBAL PYRAMETERS
###########################################################

def test_pyrameters_wheel():
    """Prueba la integración global calculando todos los parámetros de una rueda W_8.
    
    En W_8: hay triángulos (cuello=3), su mayor clique es un triángulo (ω=3),
    y al tener un ciclo impar rodeado por un centro, χ=4.
    """
    G = nx.wheel_graph(8)
    resultado = pyrameters(G)
    assert es_clique(G, resultado["maximum_clique"])
    assert resultado["clique_number"] == 3
    assert resultado["girth"] == 3
    assert resultado["chromatic_number"] == 4

def test_pyrameters_tutte():
    """Prueba la integración en la gráfica de Tutte (gráfica cúbica compleja)."""
    G = nx.tutte_graph()
    resultado = pyrameters(G)
    assert es_clique(G, resultado["maximum_clique"])
    assert resultado["clique_number"] == 2
    assert len(resultado["maximum_clique"]) == 2
    assert resultado["girth"] == 4
    assert resultado["chromatic_number"] == 3

def test_pyrameters_disconnected():
    """Prueba el comportamiento de la librería completa en una gráfica disconexa.
    
    Caso de borde: Consta de una gráfica completa K_4 y un camino P_10 separados.
    Los parámetros globales deben reflejar el subgrafo con mayores restricciones (K_4).
    """
    G = nx.disjoint_union(
        nx.complete_graph(4),
        nx.path_graph(10)
    )
    resultado = pyrameters(G)
    assert es_clique(G, resultado["maximum_clique"])
    assert resultado["clique_number"] == 4
    assert len(resultado["maximum_clique"]) == 4
    assert resultado["girth"] == 3
    assert resultado["chromatic_number"] == 4
