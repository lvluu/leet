"""Graph traversal pattern animations (BFS and DFS)."""

from collections import deque
from typing import Any, Dict, Generator, List, Optional, Set

from .base import BasePattern, AnimationStep
from ..renderers.graph_renderer import GraphRenderer
from ..config import AnimationConfig, ColorScheme


class GraphTraversalPattern(BasePattern):
    """
    Animates graph traversal algorithms.

    Variants:
    - BFS (Breadth-First Search)
    - DFS (Depth-First Search)
    """

    @property
    def name(self) -> str:
        return "graph_traversal"

    @property
    def description(self) -> str:
        return "Graph traversal patterns (BFS/DFS)"

    def __init__(
        self,
        config: Optional[AnimationConfig] = None,
        color_scheme: Optional[ColorScheme] = None,
    ):
        renderer = GraphRenderer(color_scheme=color_scheme)
        super().__init__(renderer, config)

    def get_steps(
        self,
        data: Dict[Any, List[Any]],
        start: Any,
        variant: str = "bfs",
    ) -> Generator[AnimationStep, None, None]:
        """
        Generate graph traversal animation steps.

        Args:
            data: Adjacency list {node: [neighbors]}
            start: Starting node
            variant: "bfs" or "dfs"
        """
        if variant == "bfs":
            yield from self._bfs_steps(data, start)
        elif variant == "dfs":
            yield from self._dfs_steps(data, start)

    def _bfs_steps(
        self, graph: Dict[Any, List[Any]], start: Any
    ) -> Generator[AnimationStep, None, None]:
        """Breadth-First Search traversal."""
        visited: Set[Any] = set()
        queue = deque([start])
        visited.add(start)
        result: List[Any] = []

        yield AnimationStep(
            state={
                "current": start,
                "frontier": {start},
                "queue": [start],
                "queue_label": "Queue",
            },
            caption=f"BFS: Start from node {start}",
        )

        while queue:
            node = queue.popleft()
            result.append(node)

            yield AnimationStep(
                state={
                    "current": node,
                    "visited": visited - {node},
                    "frontier": set(queue),
                    "queue": list(queue),
                    "queue_label": "Queue",
                },
                caption=f"Dequeue and process node {node}",
            )

            for neighbor in graph.get(node, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

                    yield AnimationStep(
                        state={
                            "current": node,
                            "visited": visited - set(queue) - {node},
                            "frontier": set(queue),
                            "highlighted_edges": [(node, neighbor)],
                            "queue": list(queue),
                            "queue_label": "Queue",
                        },
                        caption=f"Discover neighbor {neighbor}, add to queue",
                    )

            # Mark current as fully visited
            yield AnimationStep(
                state={
                    "visited": visited - set(queue),
                    "frontier": set(queue),
                    "queue": list(queue),
                    "queue_label": "Queue",
                },
                caption=f"Node {node} fully processed",
            )

        yield AnimationStep(
            state={"visited": visited},
            caption=f"BFS complete! Order: {result}",
            is_pause=True,
            duration_ms=1500,
        )

    def _dfs_steps(
        self, graph: Dict[Any, List[Any]], start: Any
    ) -> Generator[AnimationStep, None, None]:
        """Depth-First Search traversal using stack."""
        visited: Set[Any] = set()
        stack = [start]
        result: List[Any] = []

        yield AnimationStep(
            state={
                "frontier": {start},
                "queue": [start],
                "queue_label": "Stack",
            },
            caption=f"DFS: Start from node {start}",
        )

        while stack:
            node = stack.pop()

            if node in visited:
                continue

            visited.add(node)
            result.append(node)

            yield AnimationStep(
                state={
                    "current": node,
                    "visited": visited - {node},
                    "frontier": set(stack),
                    "queue": list(stack),
                    "queue_label": "Stack",
                },
                caption=f"Pop and visit node {node}",
            )

            # Add unvisited neighbors to stack (reverse order for standard DFS)
            for neighbor in reversed(graph.get(node, [])):
                if neighbor not in visited:
                    stack.append(neighbor)

                    yield AnimationStep(
                        state={
                            "current": node,
                            "visited": visited,
                            "frontier": set(stack),
                            "highlighted_edges": [(node, neighbor)],
                            "queue": list(stack),
                            "queue_label": "Stack",
                        },
                        caption=f"Push neighbor {neighbor} to stack",
                    )

        yield AnimationStep(
            state={"visited": visited},
            caption=f"DFS complete! Order: {result}",
            is_pause=True,
            duration_ms=1500,
        )
