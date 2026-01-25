# Introduction to Tree Depth First Search Pattern

**Tree Depth First Search (Tree DFS)** explores a tree by going as deep as possible before backtracking.

You’ll usually see DFS implemented in two ways:
- **Recursion** (most readable)
- **Explicit stack** (avoids recursion depth limits)

DFS is a great fit when problems ask about:
- **root-to-leaf paths**
- **path constraints** (sum, sequence, max/min along a path)
- **subtree computations** (aggregate results from children)

When to use
- You need to explore **all paths** from root to leaves.
- You need to compute a value that depends on children (post-order style).
- You need to check existence of a path satisfying a condition.
- You need to produce/collect paths or combinations along a traversal.

Common variants
- Pre-order (node → left → right): good for building paths top-down.
- In-order (left → node → right): common with BSTs.
- Post-order (left → right → node): common for bottom-up aggregation.
- “Backtracking DFS”: maintain a path list, add/remove as recursion enters/exits.

Pattern recipe (path-based DFS)
1. Start DFS from the root with a path/state.
2. Update the current state (e.g., add node value to path sum).
3. If you reached a leaf, check/record the result.
4. Recurse into children.
5. Undo state changes when returning (backtrack) if you’re using a shared mutable structure.

Complexity
- Time: $O(n)$ — visits each node once.
- Space:
  - recursion depth: $O(h)$ where $h$ is tree height
  - plus any path storage/output you keep

Short examples

Binary Tree Path Sum (existence) — Python

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def has_path_sum(root, target):
    if not root:
        return False

    target -= root.val

    if not root.left and not root.right:
        return target == 0

    return has_path_sum(root.left, target) or has_path_sum(root.right, target)
```

All root-to-leaf paths — Python

```python
def all_paths(root):
    res = []

    def dfs(node, path):
        if not node:
            return

        path.append(node.val)

        if not node.left and not node.right:
            res.append(path.copy())
        else:
            dfs(node.left, path)
            dfs(node.right, path)

        path.pop()  # backtrack

    dfs(root, [])
    return res
```

Iterative DFS (explicit stack) — Python

```python
def preorder_iterative(root):
    if not root:
        return []

    res = []
    st = [root]

    while st:
        node = st.pop()
        res.append(node.val)

        # push right first so left is processed first
        if node.right:
            st.append(node.right)
        if node.left:
            st.append(node.left)

    return res
```

Problems to practice
- [Path Sum](https://leetcode.com/problems/path-sum/)
- [Path Sum II](https://leetcode.com/problems/path-sum-ii/)
- [Binary Tree Paths](https://leetcode.com/problems/binary-tree-paths/)
- [Diameter of Binary Tree](https://leetcode.com/problems/diameter-of-binary-tree/)
- [Path Sum III](https://leetcode.com/problems/path-sum-iii/)
