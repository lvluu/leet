# Graph Traversal - Depth First Search (DFS)

**DFS** explores a graph by going as deep as possible before backtracking.

## Visual Example

![Graph DFS traversal](../.gitbook/assets/animations/graphs/graph_dfs.gif)

DFS is useful for:
- reachability (“can I get from A to B?”)
- connected components
- cycle detection
- topological sorting (with recursion stack / postorder in DAG)

When to use
- You need to explore all nodes in a component.
- You need to detect cycles (with variations for directed vs undirected).
- You’re doing recursive-style exploration (paths, backtracking).

Key idea: visited tracking
Graphs can contain cycles, so you must track `visited` to avoid infinite loops.

Pattern recipe (iterative)
1. Push a start node onto a stack.
2. While stack not empty:
   - pop a node
   - if unvisited, mark visited and push neighbors

Pattern recipe (recursive)
1. Mark current node visited.
2. Recurse into each unvisited neighbor.

Complexity
- Time: $O(V + E)$ (adjacency list)
- Space: $O(V)$ for visited + recursion/stack

Short examples

DFS (recursive) — Python

```python
def dfs_recursive(g, start):
    visited = set()

    def go(u):
        visited.add(u)
        for v in g[u]:
            if v not in visited:
                go(v)

    go(start)
    return visited
```

DFS (iterative) — Python

```python
def dfs_iterative(g, start):
    visited = set()
    st = [start]

    while st:
        u = st.pop()
        if u in visited:
            continue
        visited.add(u)
        for v in g[u]:
            if v not in visited:
                st.append(v)

    return visited
```

Connected components (undirected) — Python

```python
def count_components(n, g):
    visited = set()
    components = 0

    for i in range(n):
        if i in visited:
            continue
        components += 1
        st = [i]
        while st:
            u = st.pop()
            if u in visited:
                continue
            visited.add(u)
            for v in g[u]:
                if v not in visited:
                    st.append(v)

    return components
```

Notes on cycle detection
- Undirected: track `(node, parent)` during DFS.
- Directed: track a recursion stack / colors (white-gray-black).

Problems to practice
- [Number of Provinces](https://leetcode.com/problems/number-of-provinces/)
- [Find if Path Exists in Graph](https://leetcode.com/problems/find-if-path-exists-in-graph/)
- [Course Schedule](https://leetcode.com/problems/course-schedule/) (directed cycle detection)
- [Find Eventual Safe States](https://leetcode.com/problems/find-eventual-safe-states/)
