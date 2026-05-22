import networkx as nx
# Importamos las funciones individuales además de la integradora
from pyrameters.all import maxclique, numero_cromatico, cuello, pyrameters

#############################
# AUXILIAR
#############################
def es_clique(G, C):
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
    G = nx.complete_graph(15)
    clique, omega = maxclique(G)
    assert es_clique(G, clique)
    assert omega == 15
    assert len(clique) == 15

def test_unit_maxclique_petersen():
    G = nx.petersen_graph()
    clique, omega = maxclique(G)
    assert es_clique(G, clique)
    assert omega == 2

def test_unit_maxclique_empty():
    G = nx.empty_graph(10)
    clique, omega = maxclique(G)
    assert omega == 1


###########################################################
# UNIT TESTS: MÓDULO NÚMERO CROMÁTICO
###########################################################

def test_unit_cromatico_cycle_odd():
    G = nx.cycle_graph(7)
    # Se prueba la función de forma aislada sin depender de pyrameters
    assert numero_cromatico(G, lower_bound = 2) == 3 

def test_unit_cromatico_bipartite():
    G = nx.complete_bipartite_graph(5, 10)
    assert numero_cromatico(G, lower_bound = 2) == 2

def test_unit_cromatico_petersen():
    G = nx.petersen_graph()
    assert numero_cromatico(G, lower_bound = 2) == 3


###########################################################
# UNIT TESTS: MÓDULO GIRTH / CUELLO
###########################################################

def test_unit_cuello_heawood():
    G = nx.heawood_graph()
    # Le pasamos un valor neutro de clique (ej. 2) para evaluar el algoritmo de BFS puro
    assert cuello(G, clique=2) == 6 

def test_unit_cuello_petersen():
    G = nx.petersen_graph()
    assert cuello(G, clique=2) == 5

def test_unit_cuello_path():
    G = nx.path_graph(20)
    assert cuello(G, clique=2) is None


###########################################################
# TEST GLOBAL PYRAMETERS
###########################################################

def test_pyrameters_wheel():
    G = nx.wheel_graph(8)
    resultado = pyrameters(G)
    assert es_clique(G, resultado["maximum_clique"])
    assert resultado["clique_number"] == 3
    assert resultado["girth"] == 3
    assert resultado["chromatic_number"] == 4

def test_pyrameters_tutte():

    G = nx.tutte_graph()
    resultado = pyrameters(G)
    assert es_clique(G, resultado["maximum_clique"])
    assert resultado["clique_number"] == 2
    assert len(resultado["maximum_clique"]) == 2
    assert resultado["girth"] == 4
    assert resultado["chromatic_number"] == 3

def test_pyrameters_disconnected():

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

