"""Union Find pattern animations."""

from typing import Generator, List, Optional, Tuple

from .base import BasePattern, AnimationStep
from ..renderers.array_renderer import ArrayRenderer
from ..config import AnimationConfig, ColorScheme


class UnionFindPattern(BasePattern):
    """
    Animates Union Find (Disjoint Set Union) operations.

    Shows:
    - Union operations
    - Find with path compression
    - Connected components
    """

    @property
    def name(self) -> str:
        return "union_find"

    @property
    def description(self) -> str:
        return "Union Find for disjoint sets"

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
        yield from self._union_find_steps(n, edges)

    def _union_find_steps(
        self, n: int, edges: List[Tuple[int, int]]
    ) -> Generator[AnimationStep, None, None]:
        """Animate union find operations."""
        parent = list(range(n))
        rank = [0] * n

        def find(x: int) -> int:
            if parent[x] != x:
                parent[x] = find(parent[x])  # Path compression
            return parent[x]

        yield AnimationStep(
            state={
                "parent": parent[:],
                "n": n,
                "edges": edges,
                "current_edge": None,
                "components": n,
            },
            caption=f"Union Find: {n} nodes, each is its own set",
        )

        components = n

        for i, (a, b) in enumerate(edges):
            yield AnimationStep(
                state={
                    "parent": parent[:],
                    "n": n,
                    "edges": edges,
                    "current_edge": (a, b),
                    "edge_idx": i,
                    "action": "considering",
                    "components": components,
                },
                caption=f"Union({a}, {b}): find roots",
            )

            root_a = find(a)
            root_b = find(b)

            if root_a != root_b:
                # Union by rank
                if rank[root_a] < rank[root_b]:
                    parent[root_a] = root_b
                elif rank[root_a] > rank[root_b]:
                    parent[root_b] = root_a
                else:
                    parent[root_b] = root_a
                    rank[root_a] += 1

                components -= 1
                action_msg = f"Merged: root({a})={root_a}, root({b})={root_b}"
            else:
                action_msg = f"Already connected (same root: {root_a})"

            yield AnimationStep(
                state={
                    "parent": parent[:],
                    "n": n,
                    "edges": edges,
                    "current_edge": (a, b),
                    "edge_idx": i,
                    "action": "done",
                    "components": components,
                    "root_a": root_a,
                    "root_b": root_b,
                },
                caption=action_msg,
            )

        yield AnimationStep(
            state={
                "parent": parent[:],
                "n": n,
                "edges": edges,
                "current_edge": None,
                "components": components,
                "final": True,
            },
            caption=f"Final: {components} connected component(s)",
            is_pause=True,
            duration_ms=1500,
        )

    def create_animation(self, n: int, edges: List[Tuple[int, int]], **kwargs):
        """Custom rendering for union find visualization."""
        from ..core.animation import Animation
        from ..core.canvas import Canvas

        animation = Animation(self.config)

        width = 500
        height = 320

        for step in self._union_find_steps(n, edges):
            canvas = Canvas(width, height, self.config.background_color)
            state = step.state

            parent = state.get("parent", [])
            num_nodes = state.get("n", 0)
            current_edge = state.get("current_edge")
            components = state.get("components", num_nodes)

            # Title
            canvas.draw_text(width // 2, 20, "Union Find Pattern", color="#374151", font_size=16)

            # Draw nodes in a row
            node_y = 80
            node_spacing = min(60, (width - 100) // num_nodes)
            start_x = (width - num_nodes * node_spacing) // 2 + node_spacing // 2

            # Group nodes by their root
            roots = {}
            for i in range(num_nodes):
                root = parent[i]
                # Find actual root
                while parent[root] != root:
                    root = parent[root]
                if root not in roots:
                    roots[root] = []
                roots[root].append(i)

            # Assign colors to components
            colors = ["#C7D2FE", "#A7F3D0", "#FDE68A", "#FECACA", "#E9D5FF", "#CFFAFE"]

            node_colors = {}
            for idx, (root, members) in enumerate(roots.items()):
                color = colors[idx % len(colors)]
                for member in members:
                    node_colors[member] = color

            # Draw nodes
            node_positions = {}
            for i in range(num_nodes):
                x = start_x + i * node_spacing
                node_positions[i] = (x, node_y)

                fill = node_colors.get(i, "#E5E7EB")
                outline = "#6B7280"

                # Highlight current edge nodes
                if current_edge and i in current_edge:
                    outline = "#059669"
                    fill = "#86EFAC"

                canvas.draw_circle(x, node_y, 18, fill=fill, outline=outline)
                canvas.draw_text(x, node_y, str(i), color="#1F2937", font_size=12)

            # Draw parent array
            canvas.draw_text(width // 2, 130, "Parent Array:", color="#6B7280", font_size=11)

            arr_start_x = (width - num_nodes * 40) // 2
            for i in range(num_nodes):
                x = arr_start_x + i * 40

                fill = "#E5E7EB"
                if current_edge and i in current_edge:
                    fill = "#86EFAC"

                canvas.draw_rounded_rect(x, 145, 36, 30, radius=4, fill=fill, outline="#6B7280")
                canvas.draw_text(x + 18, 160, str(parent[i]), color="#1F2937", font_size=12)

                # Index label
                canvas.draw_text(x + 18, 185, str(i), color="#9CA3AF", font_size=9)

            # Draw parent pointers (edges in tree)
            for i in range(num_nodes):
                if parent[i] != i:
                    x1, y1 = node_positions[i]
                    x2, y2 = node_positions[parent[i]]
                    # Draw arrow pointing to parent
                    canvas.draw_line(x1, y1 - 20, x2, y2 + 20, "#9CA3AF", 1)

            # Components count
            canvas.draw_text(width // 2, 220, f"Components: {components}", color="#4F46E5", font_size=14)

            # Current operation
            if current_edge:
                a, b = current_edge
                canvas.draw_text(width // 2, 245, f"Processing edge: ({a}, {b})", color="#059669", font_size=11)

            # Caption
            if step.caption:
                canvas.draw_text(width // 2, height - 20, step.caption, color="#374151", font_size=11)

            if step.is_pause:
                animation.add_pause_frame(canvas.get_image(), step.duration_ms or 1500)
            else:
                animation.add_frame(canvas.get_image(), step.duration_ms)

        return animation
