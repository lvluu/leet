"""Stack renderer for visualizing stack operations."""

from typing import Any, Dict, List, Optional, Tuple

from .base import BaseRenderer
from ..core.canvas import Canvas
from ..config import ColorScheme


class StackRenderer(BaseRenderer):
    """
    Renders a stack visualization with:
    - Vertical stack display
    - Push/pop highlighting
    - Top pointer indicator
    """

    def __init__(
        self,
        cell_width: int = 60,
        cell_height: int = 35,
        max_visible: int = 8,
        color_scheme: Optional[ColorScheme] = None,
    ):
        super().__init__(color_scheme)
        self.cell_width = cell_width
        self.cell_height = cell_height
        self.max_visible = max_visible

    def calculate_dimensions(self, data: List[Any]) -> Tuple[int, int]:
        """Calculate canvas dimensions for the stack."""
        height = min(len(data), self.max_visible) * self.cell_height + 100
        width = self.cell_width + 100
        return max(width, 200), max(height, 200)

    def render(self, canvas: Canvas, data: List[Any], state: Dict[str, Any]) -> None:
        """
        Render stack with visual state.

        State keys:
            - pushing: Value being pushed (highlighted at top)
            - popping: Value being popped (highlighted, about to leave)
            - highlight_indices: Set of indices to highlight
        """
        x = 50
        base_y = canvas.height - 50

        # Draw stack base
        canvas.draw_line(
            x - 10, base_y + 5,
            x + self.cell_width + 10, base_y + 5,
            color=self.colors.border, width=3
        )

        # Draw "Stack" label
        canvas.draw_text(
            x + self.cell_width // 2, 20,
            "Stack", color=self.colors.text, font_size=14
        )

        if not data:
            canvas.draw_text(
                x + self.cell_width // 2, base_y - 20,
                "(empty)", color="#9CA3AF", font_size=12
            )
            return

        pushing = state.get("pushing")
        popping = state.get("popping")
        highlight_indices = state.get("highlight_indices", set())

        # Draw stack elements (bottom to top)
        visible_data = data[-self.max_visible:]
        for i, val in enumerate(visible_data):
            y = base_y - (i + 1) * self.cell_height

            # Determine fill color
            is_top = (i == len(visible_data) - 1)
            if is_top and popping is not None:
                fill = "#FCA5A5"  # Red for popping
            elif is_top and pushing is not None:
                fill = "#86EFAC"  # Green for pushing
            elif (len(data) - len(visible_data) + i) in highlight_indices:
                fill = self.colors.highlight
            elif is_top:
                fill = self.colors.current
            else:
                fill = self.colors.default

            canvas.draw_rounded_rect(
                x, y, self.cell_width, self.cell_height - 2,
                radius=4, fill=fill, outline=self.colors.border
            )
            canvas.draw_text(
                x + self.cell_width // 2, y + self.cell_height // 2 - 1,
                str(val), color=self.colors.text, font_size=14
            )

        # Draw top pointer
        top_y = base_y - len(visible_data) * self.cell_height
        canvas.draw_text(
            x + self.cell_width + 25, top_y + self.cell_height // 2,
            "← top", color=self.colors.pointer_left, font_size=12, anchor="lm"
        )

        # Show overflow indicator
        if len(data) > self.max_visible:
            canvas.draw_text(
                x + self.cell_width // 2, base_y - self.max_visible * self.cell_height - 15,
                f"... +{len(data) - self.max_visible} more",
                color="#9CA3AF", font_size=10
            )

    def get_element_position(self, data: List[Any], index: int) -> Tuple[int, int]:
        """Get position of stack element by index."""
        raise NotImplementedError("Stack positions are relative to render")
