# 📐 pyrameters

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-Activo-success)

¡Hola mundo! Como habrás podido notar (especialmente si estudias matemáticas o ciencias de la computación), las gráficas son uno de los objetos más interesantes en matemáticas. Tienen muchísimas aplicaciones en diversas ramas de las matemáticas (puras y aplicadas) y de las ciencias de la computación, tales como la combinatoria, redes, estructuras de datos y, curiosamente, son útiles al colorear un mapa de modo que dos provincias adyacentes no tengan el mismo color, o al estudiar cuántas personas se conocen entre sí en una fiesta.

Te presentamos **pyrameters**, una biblioteca escrita en Python para calcular algunos de los parámetros clásicos más importantes de una gráfica simple:

- **Número de clan** $\omega(G)$
- **Número cromático** $\chi(G)$
- **Cuello o girth** $g(G)$

El proyecto está desarrollado utilizando **NetworkX** y algoritmos de búsqueda con poda (*branch and bound*), coloración glotona (*greedy coloring*) y búsqueda en anchura (*BFS*). Este proyecto calcula los parámetros anteriomente mencionados para gráficas **simples**, es decir, asumimos que no puede haber más de una arista uniendo dos vértices. También, asumimos que las gráficas no tienen lazos.

---

# 🚀 Instalación

## Opción A: usando pip

Clona el repositorio e instala el paquete localmente:

```bash
git clone https://github.com/or476651-orlando/pyrameters.git
cd pyrameters
pip install .
```

## Opción B: modo desarrollador

Si deseas modificar el código mientras desarrollas:

```bash
git clone https://github.com/or476651-orlando/pyrameters.git
cd pyrameters
pip install -e .
```

## Opción C: usando pip, para trabajar en entornos como Jupyter

Si deseas trabajar con esta librería desde una libreta de Jupyter:

```bash
pip install git+https://github.com/or476651-orlando/pyrameters.git
```
---

# 📖 Uso básico

```python
import networkx as nx

from pyrameters import pyrameters
```

Crear una gráfica:

```python
G = nx.cycle_graph(5)
```

Calcular los parámetros:

```python
resultado = pyrameters(G)

print(resultado)
```

Salida esperada:

```python
{
    "maximum_clique": {0, 1},
    "clique_number": 2,
    "chromatic_number": 3,
    "girth": 5
}
```

---

# 📚 Parámetros calculados

## Número de clan

El **número de clan** (también llamado número de clique) es el tamaño de la clique máxima de una gráfica:

$$ 
\omega(G) = 
\max \{|K| : K \text{ es una clique de } G \} 
$$

Ejemplo:

```text
A ----- B
 \     /
   \ /
    C
```

La gráfica contiene una clique de tamaño 3.

Por lo tanto:

$$
\omega(G)=3
$$

---

## Número cromático

El **número cromático** es la cantidad mínima de colores necesarios para colorear los vértices de una gráfica de manera que vértices adyacentes reciban colores distintos.

$$
\chi(G)
$$

Por ejemplo:

```text
A ----- B
 \     /
   \ /
    C
```

requiere tres colores distintos:

$$
\chi(G)=3
$$

---

## Cuello (Girth)

El **cuello** de una gráfica es la longitud del ciclo más corto que contiene.

$$
g(G)
$$

Por ejemplo:

```text
0 --- 1
|     |
|     |
3 --- 2
```

tiene:

$$
g(G)=4
$$

---

# ⚙️ Algoritmos utilizados

## Clique máxima

Se utiliza una variante de **MAXCLIQUE2**, inspirado en el Algoritmo 4.19 del libro de Kreher & Stinson, basada en:

- Backtracking
- Branch and Bound
- Coloración glotona para acotar
- Exploración de vértices por grado descendente

---

## Número cromático

El número cromático se calcula mediante:

- Backtracking
- Ruptura de simetría
- Branch and Bound
- Ordenamiento por grado descendente

Además, se aprovecha la relación:

$$
\omega(G)\leq\chi(G)
$$

para utilizar el número de clan como cota inferior inicial.

---

## Cuello

El cuello se calcula mediante búsquedas BFS desde cada vértice.

Antes de la búsqueda:

- Se eliminan iterativamente vértices de grado menor que 2.
- Si se detecta una clique de tamaño al menos 3, entonces se concluye inmediatamente:

$$
g(G)=3
$$

sin necesidad de explorar el resto de la gráfica.

---

# 🔬 Relación entre los parámetros

La biblioteca aprovecha relaciones clásicas entre los parámetros:

$$
\omega(G)\leq\chi(G)
$$

y

$$
\omega(G)\geq 3
\Longrightarrow
g(G)=3
$$

lo que permite realizar podas y optimizaciones durante los cálculos.

---

# 🛠 Dependencias

- Python 3.10+
- NetworkX

Instalación manual:

```bash
pip install networkx
```

---

# 🤝 Contribuciones

Las contribuciones son bienvenidas.

Para contribuir:

```bash
git fork
git checkout -b nueva-funcionalidad
git commit -m "Agregar nueva funcionalidad"
git push origin nueva-funcionalidad
```

Posteriormente abre un Pull Request.

---

# 📄 Licencia

Este proyecto se distribuye bajo la licencia MIT.

---

# 👨‍💻 Autores
Parra Pérez Jared Israel
Ortega Zempoaltecatlc Orlando
Cobos Vera Cristo Tristán
