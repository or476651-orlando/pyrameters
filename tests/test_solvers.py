from pyrameters.solvers import solve_example

def test_solve_example_empty():
    """Prueba que el solucionador maneje correctamente una entrada vacía.
    
    Caso de borde: Se verifica que al ingresar una estructura de datos vacía, 
    la función no colapse y devuelva el resultado esperado (una lista vacía).
    """
    assert solve_example([]) == []

def test_solve_example_data():
    """Prueba el solucionador con datos de muestra básicos.
    
    Caso base: Se verifica que al ingresar una lista de elementos, 
    la función los procese y devuelva correctamente.
    """
    data = [1, 2, 3]
    assert solve_example(data) == data
