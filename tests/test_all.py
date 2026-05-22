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
    clique, omega, g, chi = pyrameters(G)
    assert es_clique(G, clique)
    assert omega == 2
    assert len(clique) == 2
    assert g == 7
    assert chi == 3

def test_C20():

    G = nx.cycle_graph(20)
    clique, omega, g, chi = pyrameters(G)
    assert es_clique(G, clique)
    assert omega == 2
    assert len(clique) == 2
    assert g == 20
    assert chi == 2

def test_empty():

    G = nx.empty_graph(10)
    clique, omega, g, chi = pyrameters(G)
    assert es_clique(G, clique)
    assert omega == 1
    assert len(clique) == 1
    assert g == None
    assert chi == 1

def test_petersen():

    G = nx.petersen_graph()
    clique, omega, g, chi = pyrameters(G)
    assert es_clique(G, clique)
    assert omega == 2
    assert len(clique) == 2
    assert g == 5
    assert chi == 3

def test_complete_bipartite():

    G = nx.complete_bipartite_graph(5,10)
    clique, omega, g, chi = pyrameters(G)
    assert es_clique(G, clique)
    assert omega == 2
    assert len(clique) == 2
    assert g == 4
    assert chi == 2

def test_heawood():

    G = nx.heawood_graph()
    clique, omega, g, chi = pyrameters(G)
    assert es_clique(G, clique)
    assert omega == 2
    assert len(clique) == 2
    assert g == 6
    assert chi == 2

def test_tutte():

    G = nx.tutte_graph()
    clique, omega, g, chi = pyrameters(G)
    assert es_clique(G, clique)
    assert omega == 2
    assert len(clique) == 2
    assert g == 4
    assert chi == 3

def test_disconnected():

    G = nx.disjoint_union(
    nx.complete_graph(4),
    nx.path_graph(10)
    )
    clique, omega, g, chi = pyrameters(G)
    assert es_clique(G, clique)
    assert omega == 4
    assert len(clique) == 4
    assert g == 3
    assert chi == 4


def test_wheel():

    G = nx.wheel_graph(8)
    clique, omega, g, chi = pyrameters(G)
    assert es_clique(G, clique)
    assert omega == 3
    assert len(clique) == 3
    assert g == 3
    assert chi == 4


def test_path():

    G = nx.path_graph(20)
    clique, omega, g, chi = pyrameters(G)
    assert es_clique(G, clique)
    assert omega == 2
    assert len(clique) == 2
    assert g == None
    assert chi == 2



