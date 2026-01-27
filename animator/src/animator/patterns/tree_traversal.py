"""Tree traversal pattern animations (BFS and DFS)."""

from collections import deque
from typing import Any, Generator, List, Optional, Set

from .base import BasePattern, AnimationStep
from ..renderers.tree_renderer import TreeRenderer, TreeNode
from ..config import AnimationConfig, ColorScheme


class TreeTraversalPattern(BasePattern):
    """
    Animates tree traversal algorithms.

    Variants:
    - Level order (BFS)
    - Pre-order (DFS)
    - In-order (DFS)
    - Post-order (DFS)
    """

    @property
    def name(self) -> str:
        return "tree_traversal"

    @property
    def description(self) -> str:
        return "Tree traversal patterns (BFS/DFS)"

    def __init__(
        self,
        config: Optional[AnimationConfig] = None,
        color_scheme: Optional[ColorScheme] = None,
    ):
        renderer = TreeRenderer(color_scheme=color_scheme)
        super().__init__(renderer, config)

    def get_steps(
        self,
        data: TreeNode,
        variant: str = "level_order",
    ) -> Generator[AnimationStep, None, None]:
        """
        Generate tree traversal animation steps.

        Args:
            data: Root node of the tree
            variant: "level_order", "preorder", "inorder", "postorder"
        """
        if variant == "level_order":
            yield from self._level_order_steps(data)
        elif variant == "preorder":
            yield from self._preorder_steps(data)
        elif variant == "inorder":
            yield from self._inorder_steps(data)
        elif variant == "postorder":
            yield from self._postorder_steps(data)

    def _level_order_steps(
        self, root: TreeNode
    ) -> Generator[AnimationStep, None, None]:
        """Level order (BFS) traversal."""
        if not root:
            return

        visited: Set[Any] = set()
        queue = deque([root])

        yield AnimationStep(
            state={
                "frontier": {root.val},
                "queue": [root.val],
            },
            caption="Level Order: Start BFS with root in queue",
        )

        result: List[Any] = []

        while queue:
            level_size = len(queue)
            level_values = []

            for _ in range(level_size):
                node = queue.popleft()

                yield AnimationStep(
                    state={
                        "current": node.val,
                        "visited": visited.copy(),
                        "frontier": {n.val for n in queue},
                        "queue": [n.val for n in queue],
                    },
                    caption=f"Process node {node.val}",
                )

                visited.add(node.val)
                level_values.append(node.val)
                result.append(node.val)

                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)

                if node.left or node.right:
                    yield AnimationStep(
                        state={
                            "visited": visited.copy(),
                            "frontier": {n.val for n in queue},
                            "queue": [n.val for n in queue],
                        },
                        caption=f"Added children to queue: {[n.val for n in queue]}",
                    )

        yield AnimationStep(
            state={"visited": visited},
            caption=f"Complete! Order: {result}",
            is_pause=True,
            duration_ms=1500,
        )

    def _preorder_steps(
        self, root: TreeNode
    ) -> Generator[AnimationStep, None, None]:
        """Pre-order DFS traversal (root -> left -> right)."""
        visited: Set[Any] = set()
        result: List[Any] = []

        yield AnimationStep(
            state={"frontier": {root.val} if root else set()},
            caption="Pre-order DFS: Visit root, then left, then right",
        )

        def traverse(node: TreeNode) -> Generator[AnimationStep, None, None]:
            if not node:
                return

            # Visit current node first
            yield AnimationStep(
                state={
                    "current": node.val,
                    "visited": visited.copy(),
                },
                caption=f"Visit {node.val} (pre-order: process before children)",
            )

            visited.add(node.val)
            result.append(node.val)

            yield AnimationStep(
                state={
                    "visited": visited.copy(),
                    "frontier": {node.left.val} if node.left else set(),
                },
                caption=f"Visited {node.val}, go left",
            )

            # Then left subtree
            yield from traverse(node.left)

            # Then right subtree
            if node.right:
                yield AnimationStep(
                    state={
                        "visited": visited.copy(),
                        "frontier": {node.right.val},
                    },
                    caption=f"Left done, go right from {node.val}",
                )
            yield from traverse(node.right)

        if root:
            yield from traverse(root)

        yield AnimationStep(
            state={"visited": visited},
            caption=f"Pre-order complete: {result}",
            is_pause=True,
            duration_ms=1500,
        )

    def _inorder_steps(
        self, root: TreeNode
    ) -> Generator[AnimationStep, None, None]:
        """In-order DFS traversal (left -> root -> right)."""
        visited: Set[Any] = set()
        result: List[Any] = []

        yield AnimationStep(
            state={"frontier": {root.val} if root else set()},
            caption="In-order DFS: Left, then root, then right",
        )

        def traverse(node: TreeNode) -> Generator[AnimationStep, None, None]:
            if not node:
                return

            # First go left
            if node.left:
                yield AnimationStep(
                    state={
                        "visited": visited.copy(),
                        "frontier": {node.left.val},
                        "current": node.val,
                    },
                    caption=f"At {node.val}, go left first",
                )
            yield from traverse(node.left)

            # Then visit current
            yield AnimationStep(
                state={
                    "current": node.val,
                    "visited": visited.copy(),
                },
                caption=f"Visit {node.val} (in-order: after left subtree)",
            )

            visited.add(node.val)
            result.append(node.val)

            # Then go right
            if node.right:
                yield AnimationStep(
                    state={
                        "visited": visited.copy(),
                        "frontier": {node.right.val},
                    },
                    caption=f"Now go right from {node.val}",
                )
            yield from traverse(node.right)

        if root:
            yield from traverse(root)

        yield AnimationStep(
            state={"visited": visited},
            caption=f"In-order complete: {result}",
            is_pause=True,
            duration_ms=1500,
        )

    def _postorder_steps(
        self, root: TreeNode
    ) -> Generator[AnimationStep, None, None]:
        """Post-order DFS traversal (left -> right -> root)."""
        visited: Set[Any] = set()
        result: List[Any] = []

        yield AnimationStep(
            state={"frontier": {root.val} if root else set()},
            caption="Post-order DFS: Left, right, then root",
        )

        def traverse(node: TreeNode) -> Generator[AnimationStep, None, None]:
            if not node:
                return

            # First go left
            if node.left:
                yield AnimationStep(
                    state={
                        "visited": visited.copy(),
                        "frontier": {node.left.val},
                    },
                    caption=f"At {node.val}, go left first",
                )
            yield from traverse(node.left)

            # Then go right
            if node.right:
                yield AnimationStep(
                    state={
                        "visited": visited.copy(),
                        "frontier": {node.right.val},
                    },
                    caption=f"At {node.val}, go right",
                )
            yield from traverse(node.right)

            # Finally visit current
            yield AnimationStep(
                state={
                    "current": node.val,
                    "visited": visited.copy(),
                },
                caption=f"Visit {node.val} (post-order: after both children)",
            )

            visited.add(node.val)
            result.append(node.val)

        if root:
            yield from traverse(root)

        yield AnimationStep(
            state={"visited": visited},
            caption=f"Post-order complete: {result}",
            is_pause=True,
            duration_ms=1500,
        )


def build_tree(values: List[Optional[int]]) -> Optional[TreeNode]:
    """Build a tree from level-order list (None for missing nodes)."""
    if not values or values[0] is None:
        return None

    root = TreeNode(values[0])
    queue = deque([root])
    i = 1

    while queue and i < len(values):
        node = queue.popleft()

        if i < len(values) and values[i] is not None:
            node.left = TreeNode(values[i])
            queue.append(node.left)
        i += 1

        if i < len(values) and values[i] is not None:
            node.right = TreeNode(values[i])
            queue.append(node.right)
        i += 1

    return root
