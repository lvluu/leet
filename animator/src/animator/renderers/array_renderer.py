"""Array renderer with support for pointers, windows, and highlights."""

from typing import Any, Dict, List, Optional, Set, Tuple

from .base import BaseRenderer
from ..core.canvas import Canvas
from ..config import ColorScheme


class ArrayRenderer(BaseRenderer):
    """
    Renders arrays with support for:
    - Element highlighting (current, visited, special)
    - Pointers (left, right, slow, fast, custom)
    - Sliding windows (shaded regions)
    - Value display inside cells
    """

    def __init__(
        self,
        cell_width: int = 50,
        cell_height: int = 50,
        cell_gap: int = 4,
        show_indices: bool = True,
        color_scheme: Optional[ColorScheme] = None,
    ):
        super().__init__(color_scheme)
        self.cell_width = cell_width
        self.cell_height = cell_height
        self.cell_gap = cell_gap
        self.show_indices = show_indices
        self._positions: List[Tuple[int, int]] = []

    def calculate_dimensions(self, data: List[Any]) -> Tuple[int, int]:
        """Calculate canvas dimensions needed for the array."""
        n = len(data)
        width = n * (self.cell_width + self.cell_gap) - self.cell_gap + 100
        height = self.cell_height + 140  # Space for indices and pointers
        return width, height

    def render(self, canvas: Canvas, data: List[Any], state: Dict[str, Any]) -> None:
        """
        Render array with visual state.

        State keys:
            - window: tuple[int, int] - (left, right) indices for window shading
            - current: int - current element index
            - visited: Set[int] - set of visited indices
            - highlights: Dict[int, str] - index -> color for custom highlights
            - pointers: List[dict] - [{"index": i, "label": "L", "color": "#...", "position": "below"}]
        """
        n = len(data)
        start_x = 50
        start_y = 50

        self._positions = []

        # Draw window background if specified
        window = state.get("window")
        if window:
            left, right = window
            if 0 <= left <= right < n:
                wx = start_x + left * (self.cell_width + self.cell_gap) - 3
                wy = start_y - 3
                ww = (right - left + 1) * (self.cell_width + self.cell_gap) - self.cell_gap + 6
                wh = self.cell_height + 6
                canvas.draw_rounded_rect(
                    wx, wy, ww, wh, radius=8, fill=self.colors.window
                )

        # Draw cells
        for i, value in enumerate(data):
            x = start_x + i * (self.cell_width + self.cell_gap)
            y = start_y
            cx = x + self.cell_width // 2
            cy = y + self.cell_height // 2
            self._positions.append((cx, cy))

            # Determine cell color
            fill = self._get_cell_color(i, state)

            canvas.draw_rounded_rect(
                x, y, self.cell_width, self.cell_height,
                radius=6, fill=fill, outline=self.colors.border
            )
            canvas.draw_text(cx, cy, str(value), color=self.colors.text, font_size=18)

            # Draw index below
            if self.show_indices:
                canvas.draw_text(
                    cx, y + self.cell_height + 18, str(i),
                    color="#6B7280", font_size=12
                )

        # Draw pointers
        for pointer in state.get("pointers", []):
            self._draw_pointer(canvas, pointer, start_y)

    def _get_cell_color(self, index: int, state: Dict[str, Any]) -> str:
        """Determine the fill color for a cell based on state."""
        highlights = state.get("highlights", {})
        if index in highlights:
            return highlights[index]
        if index == state.get("current"):
            return self.colors.current
        if index in state.get("visited", set()):
            return self.colors.visited
        return self.colors.default

    def _draw_pointer(self, canvas: Canvas, pointer: dict, base_y: int) -> None:
        """Draw a pointer arrow with label."""
        idx = pointer.get("index", 0)
        if 0 <= idx < len(self._positions):
            cx, _ = self._positions[idx]
            label = pointer.get("label", "")
            color = pointer.get("color", self.colors.pointer_left)
            position = pointer.get("position", "below")

            if position == "below":
                pointer_y = base_y + self.cell_height + 35
                canvas.draw_pointer_below(cx, pointer_y, label, color)
            else:
                pointer_y = base_y - 10
                canvas.draw_pointer_above(cx, pointer_y, label, color)

    def get_element_position(self, data: List[Any], index: int) -> Tuple[int, int]:
        """Get the center position of an element."""
        if self._positions and 0 <= index < len(self._positions):
            return self._positions[index]
        raise IndexError(f"Invalid index {index}")
