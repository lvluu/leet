"""Matrix/grid renderer for island and matrix traversal problems."""

from typing import Any, Dict, List, Optional, Set, Tuple

from .base import BaseRenderer
from ..core.canvas import Canvas
from ..config import ColorScheme


class MatrixRenderer(BaseRenderer):
    """
    Renders 2D grids/matrices with:
    - Cell coloring based on value and state
    - Current cell highlighting
    - Visited cells
    - Direction arrows for traversal
    """

    def __init__(
        self,
        cell_size: int = 45,
        cell_gap: int = 2,
        color_scheme: Optional[ColorScheme] = None,
    ):
        super().__init__(color_scheme)
        self.cell_size = cell_size
        self.cell_gap = cell_gap
        self._positions: List[List[Tuple[int, int]]] = []

        # Matrix-specific colors
        self.water_color = "#BFDBFE"  # Light blue for water (0)
        self.land_color = "#86EFAC"   # Light green for land (1)
        self.visiting_color = "#FDE68A"  # Yellow for currently visiting
        self.visited_color = "#34D399"   # Darker green for visited land

    def calculate_dimensions(self, data: List[List[Any]]) -> Tuple[int, int]:
        """Calculate canvas dimensions for the matrix."""
        if not data or not data[0]:
            return 400, 400

        rows = len(data)
        cols = len(data[0])

        width = cols * (self.cell_size + self.cell_gap) - self.cell_gap + 100
        height = rows * (self.cell_size + self.cell_gap) - self.cell_gap + 120
        return width, height

    def render(
        self, canvas: Canvas, data: List[List[Any]], state: Dict[str, Any]
    ) -> None:
        """
        Render matrix with visual state.

        State keys:
            - current: Tuple (row, col) - current cell
            - visited: Set of (row, col) tuples - visited cells
            - frontier: Set of (row, col) tuples - cells in queue/stack
            - component: Set of (row, col) - current connected component
            - highlights: Dict of (row, col) -> color
        """
        if not data or not data[0]:
            return

        rows = len(data)
        cols = len(data[0])

        start_x = 50
        start_y = 50

        self._positions = []

        # Draw row indices
        for r in range(rows):
            y = start_y + r * (self.cell_size + self.cell_gap) + self.cell_size // 2
            canvas.draw_text(start_x - 25, y, str(r), color="#6B7280", font_size=12)

        # Draw column indices
        for c in range(cols):
            x = start_x + c * (self.cell_size + self.cell_gap) + self.cell_size // 2
            canvas.draw_text(x, start_y - 20, str(c), color="#6B7280", font_size=12)

        # Draw cells
        for r in range(rows):
            row_positions = []
            for c in range(cols):
                x = start_x + c * (self.cell_size + self.cell_gap)
                y = start_y + r * (self.cell_size + self.cell_gap)
                cx = x + self.cell_size // 2
                cy = y + self.cell_size // 2
                row_positions.append((cx, cy))

                fill = self._get_cell_color(data[r][c], (r, c), state)
                outline = self.colors.border

                # Highlight current cell with thicker border
                border_width = 3 if (r, c) == state.get("current") else 1

                canvas.draw_rounded_rect(
                    x, y, self.cell_size, self.cell_size,
                    radius=4, fill=fill, outline=outline
                )

                # Draw cell value
                val = data[r][c]
                text_color = self.colors.text if val else "#64748B"
                canvas.draw_text(cx, cy, str(val), color=text_color, font_size=14)

            self._positions.append(row_positions)

        # Draw queue if present
        queue = state.get("queue", [])
        if queue:
            self._draw_queue(canvas, queue, canvas.width)

    def _get_cell_color(
        self, value: Any, pos: Tuple[int, int], state: Dict[str, Any]
    ) -> str:
        """Determine cell color based on value and state."""
        highlights = state.get("highlights", {})
        if pos in highlights:
            return highlights[pos]

        if pos == state.get("current"):
            return self.visiting_color

        if pos in state.get("frontier", set()):
            return self.colors.node_frontier

        if pos in state.get("visited", set()):
            return self.visited_color

        if pos in state.get("component", set()):
            return self.visited_color

        # Default: water vs land
        return self.land_color if value == 1 else self.water_color

    def _draw_queue(self, canvas: Canvas, queue: List[Tuple[int, int]], width: int) -> None:
        """Draw queue contents."""
        y = 20
        x = 50

        canvas.draw_text(x, y, "Queue:", color=self.colors.text, font_size=12, anchor="lm")

        x += 50
        for pos in queue[:8]:  # Show max 8 items
            text = f"({pos[0]},{pos[1]})"
            canvas.draw_rounded_rect(x, y - 10, 40, 20, radius=4,
                                    fill=self.colors.node_frontier, outline=self.colors.border)
            canvas.draw_text(x + 20, y, text, color=self.colors.text, font_size=10)
            x += 45

        if len(queue) > 8:
            canvas.draw_text(x + 10, y, f"...+{len(queue) - 8}", color="#6B7280", font_size=10)

    def get_element_position(self, data: List[List[Any]], pos: Tuple[int, int]) -> Tuple[int, int]:
        """Get center position of a cell."""
        r, c = pos
        if self._positions and 0 <= r < len(self._positions) and 0 <= c < len(self._positions[r]):
            return self._positions[r][c]
        raise IndexError(f"Invalid position {pos}")
