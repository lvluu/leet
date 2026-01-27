"""Tree renderer for binary trees with node states."""

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Set, Tuple

from .base import BaseRenderer
from ..core.canvas import Canvas
from ..config import ColorScheme


@dataclass
class TreeNode:
    """Tree node for rendering."""
    val: Any
    left: Optional['TreeNode'] = None
    right: Optional['TreeNode'] = None


class TreeRenderer(BaseRenderer):
    """
    Renders binary trees with:
    - Node highlighting (current, visited, frontier)
    - Level indication
    - Edge highlighting
    - Queue/stack visualization
    """

    def __init__(
        self,
        node_radius: int = 22,
        level_height: int = 65,
        min_horizontal_gap: int = 15,
        color_scheme: Optional[ColorScheme] = None,
    ):
        super().__init__(color_scheme)
        self.node_radius = node_radius
        self.level_height = level_height
        self.min_horizontal_gap = min_horizontal_gap
        self._node_positions: Dict[int, Tuple[int, int]] = {}

    def calculate_dimensions(self, root: TreeNode) -> Tuple[int, int]:
        """Calculate canvas dimensions for the tree."""
        if not root:
            return 400, 200

        depth = self._get_depth(root)
        max_width = (2 ** depth) * (self.node_radius * 2 + self.min_horizontal_gap)
        height = depth * self.level_height + self.node_radius * 2 + 100
        return max(max_width, 400), height

    def render(self, canvas: Canvas, root: TreeNode, state: Dict[str, Any]) -> None:
        """
        Render tree with visual state.

        State keys:
            - current: node value being processed
            - visited: Set of visited node values
            - frontier: Set of frontier node values (queue/stack)
            - level_highlight: int - highlight specific level
            - highlighted_edges: List[tuple] - edges to highlight
            - queue: List - current queue contents (for BFS visualization)
        """
        if not root:
            return

        self._node_positions.clear()
        width, _ = self.calculate_dimensions(root)

        # Calculate positions
        self._calculate_positions(root, width // 2, 50, width // 4)

        # Draw edges first
        self._draw_edges(canvas, root, state)

        # Draw nodes
        self._draw_nodes(canvas, root, state)

        # Draw queue/stack if present
        queue = state.get("queue", [])
        if queue:
            self._draw_queue(canvas, queue, width)

    def _calculate_positions(
        self, node: TreeNode, x: int, y: int, x_offset: int
    ) -> None:
        """Calculate positions for all nodes."""
        if not node:
            return

        self._node_positions[id(node)] = (x, y)

        next_offset = max(x_offset // 2, self.node_radius + 5)
        if node.left:
            self._calculate_positions(node.left, x - x_offset, y + self.level_height, next_offset)
        if node.right:
            self._calculate_positions(node.right, x + x_offset, y + self.level_height, next_offset)

    def _draw_edges(self, canvas: Canvas, node: TreeNode, state: Dict[str, Any]) -> None:
        """Draw edges between nodes."""
        if not node:
            return

        x, y = self._node_positions[id(node)]
        highlighted = state.get("highlighted_edges", [])

        for child in [node.left, node.right]:
            if child:
                cx, cy = self._node_positions[id(child)]
                edge_key = (node.val, child.val)
                color = self.colors.edge_active if edge_key in highlighted else self.colors.edge_default
                canvas.draw_line(
                    x, y + self.node_radius,
                    cx, cy - self.node_radius,
                    color, width=2
                )
                self._draw_edges(canvas, child, state)

    def _draw_nodes(self, canvas: Canvas, node: TreeNode, state: Dict[str, Any]) -> None:
        """Draw all nodes."""
        if not node:
            return

        x, y = self._node_positions[id(node)]
        fill = self._get_node_color(node.val, state)

        canvas.draw_circle(x, y, self.node_radius, fill=fill, outline=self.colors.border)
        canvas.draw_text(x, y, str(node.val), color=self.colors.text, font_size=16)

        self._draw_nodes(canvas, node.left, state)
        self._draw_nodes(canvas, node.right, state)

    def _get_node_color(self, val: Any, state: Dict[str, Any]) -> str:
        """Determine node color based on state."""
        if val == state.get("current"):
            return self.colors.current
        if val in state.get("frontier", set()):
            return self.colors.node_frontier
        if val in state.get("visited", set()):
            return self.colors.node_visited
        return self.colors.node_default

    def _draw_queue(self, canvas: Canvas, queue: List[Any], width: int) -> None:
        """Draw the current queue contents."""
        if not queue:
            return

        y = 20
        x_start = width - 150

        canvas.draw_text(x_start, y, "Queue:", color=self.colors.text, font_size=12, anchor="lm")

        x = x_start + 50
        for val in queue:
            canvas.draw_rounded_rect(x, y - 12, 24, 24, radius=4,
                                    fill=self.colors.node_frontier, outline=self.colors.border)
            canvas.draw_text(x + 12, y, str(val), color=self.colors.text, font_size=12)
            x += 28

    def _get_depth(self, node: TreeNode) -> int:
        """Get tree depth."""
        if not node:
            return 0
        return 1 + max(self._get_depth(node.left), self._get_depth(node.right))

    def get_element_position(self, data: TreeNode, node_id: int) -> Tuple[int, int]:
        """Get position of a node by its id()."""
        if node_id in self._node_positions:
            return self._node_positions[node_id]
        raise KeyError(f"Node {node_id} not found")
