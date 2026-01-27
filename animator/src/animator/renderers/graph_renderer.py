"""Graph renderer for visualizing graph traversals."""

import math
from typing import Any, Dict, List, Optional, Set, Tuple

from .base import BaseRenderer
from ..core.canvas import Canvas
from ..config import ColorScheme


class GraphRenderer(BaseRenderer):
    """
    Renders graphs with:
    - Node positioning (predefined or circular layout)
    - Directed/undirected edges
    - Node states (unvisited, frontier, visited, current)
    - Edge highlighting
    """

    def __init__(
        self,
        node_radius: int = 25,
        color_scheme: Optional[ColorScheme] = None,
    ):
        super().__init__(color_scheme)
        self.node_radius = node_radius
        self._positions: Dict[Any, Tuple[int, int]] = {}

    def calculate_dimensions(self, data: Dict[Any, List[Any]]) -> Tuple[int, int]:
        """Calculate canvas dimensions for the graph."""
        n = len(data)
        size = max(400, n * 80)
        return size, size

    def render(
        self,
        canvas: Canvas,
        data: Dict[Any, List[Any]],
        state: Dict[str, Any],
    ) -> None:
        """
        Render graph with visual state.

        Args:
            data: Adjacency list {node: [neighbors]}
            state: Visual state dict

        State keys:
            - current: Current node being processed
            - visited: Set of visited nodes
            - frontier: Set of frontier nodes (in queue/stack)
            - highlighted_edges: List of (from, to) tuples to highlight
            - positions: Optional dict of {node: (x, y)} for custom layout
            - directed: bool - whether to draw arrows (default False)
            - queue: List - current queue/stack contents
        """
        nodes = list(data.keys())
        if not nodes:
            return

        # Use provided positions or calculate circular layout
        positions = state.get("positions")
        if positions:
            self._positions = positions
        else:
            self._calculate_circular_layout(nodes, canvas.width, canvas.height)

        directed = state.get("directed", False)

        # Draw edges first
        self._draw_edges(canvas, data, state, directed)

        # Draw nodes
        self._draw_nodes(canvas, nodes, state)

        # Draw queue/stack if present
        queue = state.get("queue", [])
        if queue:
            self._draw_queue(canvas, queue, state.get("queue_label", "Queue"))

    def _calculate_circular_layout(
        self, nodes: List[Any], width: int, height: int
    ) -> None:
        """Calculate circular layout for nodes."""
        n = len(nodes)
        cx, cy = width // 2, height // 2
        radius = min(width, height) // 2 - 60

        for i, node in enumerate(nodes):
            angle = 2 * math.pi * i / n - math.pi / 2
            x = int(cx + radius * math.cos(angle))
            y = int(cy + radius * math.sin(angle))
            self._positions[node] = (x, y)

    def _draw_edges(
        self,
        canvas: Canvas,
        adj_list: Dict[Any, List[Any]],
        state: Dict[str, Any],
        directed: bool,
    ) -> None:
        """Draw edges between nodes."""
        highlighted = set(state.get("highlighted_edges", []))
        drawn = set()

        for node, neighbors in adj_list.items():
            if node not in self._positions:
                continue

            x1, y1 = self._positions[node]

            for neighbor in neighbors:
                if neighbor not in self._positions:
                    continue

                # For undirected graphs, only draw each edge once
                edge_key = (min(node, neighbor), max(node, neighbor)) if not directed else (node, neighbor)
                if not directed and edge_key in drawn:
                    continue
                drawn.add(edge_key)

                x2, y2 = self._positions[neighbor]

                # Check if edge is highlighted
                is_highlighted = (node, neighbor) in highlighted or (neighbor, node) in highlighted
                color = self.colors.edge_active if is_highlighted else self.colors.edge_default
                width = 3 if is_highlighted else 2

                if directed:
                    # Calculate arrow endpoint (stop at node boundary)
                    dx, dy = x2 - x1, y2 - y1
                    dist = math.sqrt(dx * dx + dy * dy)
                    if dist > 0:
                        ratio = (dist - self.node_radius - 5) / dist
                        end_x = int(x1 + dx * ratio)
                        end_y = int(y1 + dy * ratio)
                        canvas.draw_arrow(x1, y1, end_x, end_y, color, width)
                else:
                    canvas.draw_line(x1, y1, x2, y2, color, width)

    def _draw_nodes(
        self, canvas: Canvas, nodes: List[Any], state: Dict[str, Any]
    ) -> None:
        """Draw all nodes."""
        for node in nodes:
            if node not in self._positions:
                continue

            x, y = self._positions[node]
            fill = self._get_node_color(node, state)

            canvas.draw_circle(x, y, self.node_radius, fill=fill, outline=self.colors.border)
            canvas.draw_text(x, y, str(node), color=self.colors.text, font_size=16)

    def _get_node_color(self, node: Any, state: Dict[str, Any]) -> str:
        """Determine node color based on state."""
        if node == state.get("current"):
            return self.colors.current
        if node in state.get("frontier", set()):
            return self.colors.node_frontier
        if node in state.get("visited", set()):
            return self.colors.node_visited
        return self.colors.node_default

    def _draw_queue(self, canvas: Canvas, queue: List[Any], label: str) -> None:
        """Draw the current queue/stack contents."""
        y = 30
        x_start = 20

        canvas.draw_text(x_start, y, f"{label}:", color=self.colors.text, font_size=12, anchor="lm")

        x = x_start + 60
        for val in queue:
            canvas.draw_rounded_rect(x, y - 12, 28, 24, radius=4,
                                    fill=self.colors.node_frontier, outline=self.colors.border)
            canvas.draw_text(x + 14, y, str(val), color=self.colors.text, font_size=12)
            x += 32

    def get_element_position(self, data: Dict, node: Any) -> Tuple[int, int]:
        """Get position of a node."""
        if node in self._positions:
            return self._positions[node]
        raise KeyError(f"Node {node} not found")
