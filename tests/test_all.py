import networkx as nx
from pyrameters.all import pyrameters

#############################
# AUXILIAR
#############################

def es_clique(G, C):
    """
    Verifica que C induce un clique en G.
    """
    C = list(C)

    for i in range(len(C)):
        for j in range(i + 1, len(C)):
            if not G.has_edge(C[i], C[j]):
                return False

    return True

#######################
# TESTS
#######################

def test_K15():

    G = nx.complete_graph(15)
    resultado = pyrameters(G)
    assert es_clique(G, resultado["maximum_clique"])
    assert resultado["clique_number"] == 15
    assert len(resultado["maximum_clique"]) == 15
    assert resultado["girth"] == 3
    assert resultado["chromatic_number"] == 15

def test_C7():

    G = nx.cycle_graph(7)
    resultado = pyrameters(G)
    assert es_clique(G, resultado["maximum_clique"])
    assert resultado["clique_number"] == 2
    assert len(resultado["maximum_clique"]) == 2
    assert resultado["girth"] == 7
    assert resultado["chromatic_number"] == 3

def test_C20():

    G = nx.cycle_graph(20)
    resultado = pyrameters(G)
    assert es_clique(G, resultado["maximum_clique"])
    assert resultado["clique_number"] == 2
    assert len(resultado["maximum_clique"]) == 2
    assert resultado["girth"] == 20
    assert resultado["chromatic_number"] == 2

def test_empty():

    G = nx.empty_graph(10)
    resultado = pyrameters(G)
    assert es_clique(G, resultado["maximum_clique"])
    assert resultado["clique_number"] == 1
    assert len(resultado["maximum_clique"]) == 1
    assert resultado["girth"] == None
    assert resultado["chromatic_number"] == 1

def test_petersen():

    G = nx.petersen_graph()
    resultado = pyrameters(G)
    assert es_clique(G, resultado["maximum_clique"])
    assert resultado["clique_number"] == 2
    assert len(resultado["maximum_clique"]) == 2
    assert resultado["girth"] == 5
    assert resultado["chromatic_number"] == 3

def test_complete_bipartite():

    G = nx.complete_bipartite_graph(5,10)
    resultado = pyrameters(G)
    assert es_clique(G, resultado["maximum_clique"])
    assert resultado["clique_number"] == 2
    assert len(resultado["maximum_clique"]) == 2
    assert resultado["girth"] == 4
    assert resultado["chromatic_number"] == 2

def test_heawood():

    G = nx.heawood_graph()
    resultado = pyrameters(G)
    assert es_clique(G, resultado["maximum_clique"])
    assert resultado["clique_number"] == 2
    assert len(resultado["maximum_clique"]) == 2
    assert resultado["girth"] == 6
    assert resultado["chromatic_number"] == 2

def test_tutte():

    G = nx.tutte_graph()
    resultado = pyrameters(G)
    assert es_clique(G, resultado["maximum_clique"])
    assert resultado["clique_number"] == 2
    assert len(resultado["maximum_clique"]) == 2
    assert resultado["girth"] == 4
    assert resultado["chromatic_number"] == 3

def test_disconnected():

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


def test_wheel():

    G = nx.wheel_graph(8)
    resultado = pyrameters(G)
    assert es_clique(G, resultado["maximum_clique"])
    assert resultado["clique_number"] == 3
    assert len(resultado["maximum_clique"]) == 3
    assert resultado["girth"] == 3
    assert resultado["chromatic_number"] == 4


def test_path():

    G = nx.path_graph(20)
    resultado = pyrameters(G)
    assert es_clique(G, resultado["maximum_clique"])
    assert resultado["clique_number"] == 2
    assert len(resultado["maximum_clique"]) == 2
    assert resultado["girth"] == None
    assert resultado["chromatic_number"] == 2



