# Graph Representations

How you store a graph matters for both performance and implementation simplicity.

The most common representations are:
- **Edge list**
- **Adjacency list**
- **Adjacency matrix**

Edge list
Store edges as a list of pairs (or triples if weighted):
- Unweighted: `(u, v)`
- Weighted: `(u, v, w)`

Pros
- Simple input format.
- Great when you just need to iterate edges (e.g., Kruskal, Bellman–Ford).

Cons
- Slow neighbor lookup: finding neighbors of `u` is $O(E)$.

Adjacency list (most common)
Map each node to a list of its neighbors.

Pros
- Fast neighbor iteration.
- Space efficient for sparse graphs.
- Standard for DFS/BFS.

Cons
- Checking if an edge exists is not $O(1)$ unless neighbors are stored in a set.

Python build examples

Undirected, unweighted adjacency list

```python
from collections import defaultdict

def build_undirected(n, edges):
    g = defaultdict(list)
    for u, v in edges:
        g[u].append(v)
        g[v].append(u)
    return g
```

Directed, unweighted adjacency list

```python
from collections import defaultdict

def build_directed(n, edges):
    g = defaultdict(list)
    for u, v in edges:
        g[u].append(v)
    return g
```

Weighted adjacency list

```python
from collections import defaultdict

def build_weighted_directed(n, edges):
    # edges: (u, v, w)
    g = defaultdict(list)
    for u, v, w in edges:
        g[u].append((v, w))
    return g
```

Adjacency matrix
Use a `V x V` matrix. For unweighted graphs, `matrix[u][v]` can be `True/False`.

Pros
- Fast edge existence check: $O(1)$.
- Helpful for dense graphs.

Cons
- Space: $O(V^2)$, often too big.

Complexity summary
- Edge list: space $O(E)$
- Adjacency list: space $O(V + E)$
- Adjacency matrix: space $O(V^2)$

Choosing the right representation
- Use adjacency list for most interview problems.
- Use adjacency matrix when:
  - graph is dense
  - you need very fast edge checks
  - `V` is small
- Use edge list when your algorithm is edge-centric (Kruskal, Bellman–Ford).

Problems to practice
- [Number of Provinces](https://leetcode.com/problems/number-of-provinces/) (often given as adjacency matrix)
- [Find if Path Exists in Graph](https://leetcode.com/problems/find-if-path-exists-in-graph/) (edge list → adjacency list)
- [Network Delay Time](https://leetcode.com/problems/network-delay-time/) (weighted adjacency list)
