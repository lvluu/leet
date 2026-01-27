"""Topological Sort pattern animations."""

from collections import deque, defaultdict
from typing import Generator, List, Optional, Tuple

from .base import BasePattern, AnimationStep
from ..renderers.array_renderer import ArrayRenderer
from ..config import AnimationConfig, ColorScheme


class TopoSortPattern(BasePattern):
    """
    Animates Topological Sort using Kahn's Algorithm (BFS).

    Shows:
    - In-degree tracking
    - Processing zero in-degree nodes
    - Building sorted order
    """

    @property
    def name(self) -> str:
        return "topo_sort"

    @property
    def description(self) -> str:
        return "Topological Sort (Kahn's Algorithm)"

    def __init__(
        self,
        config: Optional[AnimationConfig] = None,
        color_scheme: Optional[ColorScheme] = None,
    ):
        renderer = ArrayRenderer(color_scheme=color_scheme)
        super().__init__(renderer, config)

    def get_steps(
        self,
        n: int,
        edges: List[Tuple[int, int]],
    ) -> Generator[AnimationStep, None, None]:
        yield from self._topo_sort_steps(n, edges)

    def _topo_sort_steps(
        self, n: int, edges: List[Tuple[int, int]]
    ) -> Generator[AnimationStep, None, None]:
        """Animate topological sort with Kahn's algorithm."""
        graph = defaultdict(list)
        in_degree = [0] * n

        for a, b in edges:
            graph[a].append(b)
            in_degree[b] += 1

        yield AnimationStep(
            state={
                "n": n,
                "edges": edges,
                "in_degree": in_degree[:],
                "queue": [],
                "result": [],
                "processing": None,
            },
            caption="Topological Sort: process nodes with in-degree 0",
        )

        queue = deque([i for i in range(n) if in_degree[i] == 0])
        result = []

        yield AnimationStep(
            state={
                "n": n,
                "edges": edges,
                "in_degree": in_degree[:],
                "queue": list(queue),
                "result": result[:],
                "processing": None,
            },
            caption=f"Initial queue (in-degree 0): {list(queue)}",
        )

        while queue:
            node = queue.popleft()

            yield AnimationStep(
                state={
                    "n": n,
                    "edges": edges,
                    "in_degree": in_degree[:],
                    "queue": list(queue),
                    "result": result[:],
                    "processing": node,
                },
                caption=f"Process node {node}",
            )

            result.append(node)

            for neighbor in graph[node]:
                in_degree[neighbor] -= 1

                yield AnimationStep(
                    state={
                        "n": n,
                        "edges": edges,
                        "in_degree": in_degree[:],
                        "queue": list(queue),
                        "result": result[:],
                        "processing": node,
                        "updating": neighbor,
                    },
                    caption=f"Decrement in-degree of {neighbor} to {in_degree[neighbor]}",
                )

                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

            yield AnimationStep(
                state={
                    "n": n,
                    "edges": edges,
                    "in_degree": in_degree[:],
                    "queue": list(queue),
                    "result": result[:],
                    "processing": None,
                },
                caption=f"Added {node} to result. Queue: {list(queue)}",
            )

        has_cycle = len(result) != n

        yield AnimationStep(
            state={
                "n": n,
                "edges": edges,
                "in_degree": in_degree[:],
                "queue": [],
                "result": result[:],
                "processing": None,
                "final": True,
                "has_cycle": has_cycle,
            },
            caption=f"Result: {result}" if not has_cycle else "Cycle detected! No valid ordering.",
            is_pause=True,
            duration_ms=1500,
        )

    def create_animation(self, n: int, edges: List[Tuple[int, int]], **kwargs):
        """Custom rendering for topological sort."""
        from ..core.animation import Animation
        from ..core.canvas import Canvas

        animation = Animation(self.config)

        width = 500
        height = 320

        for step in self._topo_sort_steps(n, edges):
            canvas = Canvas(width, height, self.config.background_color)
            state = step.state

            num_nodes = state.get("n", 0)
            in_degree = state.get("in_degree", [])
            queue = state.get("queue", [])
            result = state.get("result", [])
            processing = state.get("processing")
            updating = state.get("updating")

            # Title
            canvas.draw_text(width // 2, 20, "Topological Sort (Kahn's BFS)", color="#374151", font_size=16)

            # Draw nodes with in-degrees
            node_y = 70
            node_spacing = min(60, (width - 80) // num_nodes)
            start_x = (width - num_nodes * node_spacing) // 2 + node_spacing // 2

            canvas.draw_text(width // 2, 50, "Nodes (in-degree):", color="#6B7280", font_size=10)

            for i in range(num_nodes):
                x = start_x + i * node_spacing

                if i == processing:
                    fill = "#86EFAC"  # Green - processing
                elif i == updating:
                    fill = "#FDE68A"  # Yellow - updating
                elif i in result:
                    fill = "#D1D5DB"  # Gray - done
                elif i in queue:
                    fill = "#C7D2FE"  # Purple - in queue
                else:
                    fill = "#E5E7EB"

                canvas.draw_circle(x, node_y, 18, fill=fill, outline="#6B7280")
                canvas.draw_text(x, node_y, str(i), color="#1F2937", font_size=12)

                # In-degree below
                canvas.draw_text(x, node_y + 28, f"({in_degree[i]})", color="#6B7280", font_size=9)

            # Draw queue
            canvas.draw_text(width // 2, 130, f"Queue: {queue if queue else '(empty)'}", color="#4F46E5", font_size=12)

            # Draw result
            canvas.draw_text(width // 2, 160, "Result:", color="#6B7280", font_size=11)

            if result:
                result_start_x = (width - len(result) * 40) // 2
                for i, node in enumerate(result):
                    x = result_start_x + i * 40
                    canvas.draw_rounded_rect(x, 175, 36, 30, radius=6, fill="#A7F3D0", outline="#059669")
                    canvas.draw_text(x + 18, 190, str(node), color="#1F2937", font_size=12)

                    if i < len(result) - 1:
                        canvas.draw_text(x + 38, 190, "→", color="#9CA3AF", font_size=12)
            else:
                canvas.draw_text(width // 2, 190, "(building...)", color="#9CA3AF", font_size=11)

            # Caption
            if step.caption:
                canvas.draw_text(width // 2, height - 25, step.caption, color="#374151", font_size=11)

            if step.is_pause:
                animation.add_pause_frame(canvas.get_image(), step.duration_ms or 1500)
            else:
                animation.add_frame(canvas.get_image(), step.duration_ms)

        return animation
