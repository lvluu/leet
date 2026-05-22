# Types of Graph

Graphs can be classified in several useful ways. Recognizing the type early helps you choose the right traversal and algorithm.

Directed vs undirected
- **Undirected**: an edge `(u, v)` means you can travel both ways.
- **Directed**: an edge `u → v` allows travel only from `u` to `v`.

Clues in problems
- “friends”, “connected”, “two-way roads” → likely **undirected**
- “prerequisite”, “depends on”, “follow”, “one-way roads” → likely **directed**

Weighted vs unweighted
- **Unweighted**: all edges have equal cost (usually treated as cost 1).
- **Weighted**: edges have costs (distance, time, price).

Rule of thumb
- Shortest path in **unweighted** graphs: BFS.
- Shortest path in **weighted** graphs:
  - non-negative weights: Dijkstra
  - negative weights: Bellman–Ford (and detect negative cycles)

Simple vs multigraph
- **Simple graph**: no parallel edges and no self-loops.
- **Multigraph**: multiple edges can exist between the same nodes.

Most interview problems assume a simple graph unless stated otherwise.

Connected vs disconnected
- A graph may have multiple **connected components**.
- Many tasks require iterating all nodes and starting a traversal from each unvisited node.

Cyclic vs acyclic
- **Cyclic**: contains at least one cycle.
- **Acyclic**:
  - For undirected graphs: a connected acyclic graph is a **tree**.
  - For directed graphs: an acyclic directed graph is a **DAG**.

Why it matters
- Cycle detection strategies differ between directed and undirected graphs.
- DAGs enable topological ordering and DP on graphs.

DAG (Directed Acyclic Graph)
A DAG has no directed cycles.

Common DAG use cases
- course prerequisites
- build systems / dependency graphs
- scheduling

Bipartite graphs
A graph is **bipartite** if vertices can be colored with two colors so that no edge connects same-colored vertices.

Common use cases
- “two groups” constraints
- matching problems
- checking odd cycles (a graph is bipartite iff it has no odd-length cycle)

Trees as a special case
A tree is an undirected graph with:
- connected
- acyclic
- exactly `V - 1` edges

Short examples

Detect graph type hints (conceptual)
- If input is an edge list without direction, assume undirected.
- If edges are ordered pairs or described as “from/to”, assume directed.

Problems to practice
- [Course Schedule](https://leetcode.com/problems/course-schedule/) (directed cycle detection)
- [Find if Path Exists in Graph](https://leetcode.com/problems/find-if-path-exists-in-graph/) (undirected reachability)
- [Is Graph Bipartite?](https://leetcode.com/problems/is-graph-bipartite/)
- [Redundant Connection](https://leetcode.com/problems/redundant-connection/) (cycle in undirected)
- [Find Eventual Safe States](https://leetcode.com/problems/find-eventual-safe-states/) (directed graph)
