"""Canvas wrapper around Pillow for drawing operations."""

from PIL import Image, ImageDraw, ImageFont
from typing import Optional
import math


class Canvas:
    """
    Wrapper around Pillow for consistent drawing operations.
    Provides high-level methods for common DSA visualization elements.
    """

    def __init__(self, width: int, height: int, background: str = "#FFFFFF"):
        self.width = width
        self.height = height
        self.image = Image.new("RGBA", (width, height), background)
        self.draw = ImageDraw.Draw(self.image)
        self._default_font: Optional[ImageFont.FreeTypeFont] = None

    def _get_font(self, size: int) -> ImageFont.FreeTypeFont:
        """Get a font at the specified size."""
        try:
            return ImageFont.truetype("arial.ttf", size)
        except OSError:
            try:
                return ImageFont.truetype("DejaVuSans.ttf", size)
            except OSError:
                return ImageFont.load_default()

    def draw_rect(
        self,
        x: int,
        y: int,
        w: int,
        h: int,
        fill: Optional[str] = None,
        outline: Optional[str] = None,
        width: int = 2,
    ) -> None:
        """Draw a rectangle."""
        self.draw.rectangle([x, y, x + w, y + h], fill=fill, outline=outline, width=width)

    def draw_rounded_rect(
        self,
        x: int,
        y: int,
        w: int,
        h: int,
        radius: int = 8,
        fill: Optional[str] = None,
        outline: Optional[str] = None,
    ) -> None:
        """Draw a rounded rectangle."""
        self.draw.rounded_rectangle(
            [x, y, x + w, y + h], radius=radius, fill=fill, outline=outline
        )

    def draw_circle(
        self,
        cx: int,
        cy: int,
        radius: int,
        fill: Optional[str] = None,
        outline: Optional[str] = None,
        width: int = 2,
    ) -> None:
        """Draw a circle centered at (cx, cy)."""
        self.draw.ellipse(
            [cx - radius, cy - radius, cx + radius, cy + radius],
            fill=fill,
            outline=outline,
            width=width,
        )

    def draw_line(
        self,
        x1: int,
        y1: int,
        x2: int,
        y2: int,
        color: str = "#000000",
        width: int = 2,
    ) -> None:
        """Draw a line from (x1, y1) to (x2, y2)."""
        self.draw.line([x1, y1, x2, y2], fill=color, width=width)

    def draw_arrow(
        self,
        x1: int,
        y1: int,
        x2: int,
        y2: int,
        color: str = "#000000",
        width: int = 2,
        head_size: int = 10,
    ) -> None:
        """Draw an arrow from (x1, y1) to (x2, y2)."""
        # Draw the line
        self.draw.line([x1, y1, x2, y2], fill=color, width=width)

        # Calculate arrow head
        angle = math.atan2(y2 - y1, x2 - x1)
        head_angle = math.pi / 6  # 30 degrees

        # Arrow head points
        left_x = x2 - head_size * math.cos(angle - head_angle)
        left_y = y2 - head_size * math.sin(angle - head_angle)
        right_x = x2 - head_size * math.cos(angle + head_angle)
        right_y = y2 - head_size * math.sin(angle + head_angle)

        self.draw.polygon(
            [(x2, y2), (left_x, left_y), (right_x, right_y)], fill=color
        )

    def draw_text(
        self,
        x: int,
        y: int,
        text: str,
        color: str = "#000000",
        font_size: int = 16,
        anchor: str = "mm",
    ) -> None:
        """
        Draw text at position.

        anchor: Pillow text anchor (mm = middle-middle, lt = left-top, etc.)
        """
        font = self._get_font(font_size)
        self.draw.text((x, y), text, fill=color, font=font, anchor=anchor)

    def draw_pointer_below(
        self, x: int, y: int, label: str, color: str, arrow_height: int = 20
    ) -> None:
        """Draw a pointer arrow with label below a position."""
        # Arrow pointing up
        self.draw_arrow(x, y + arrow_height, x, y + 5, color=color, head_size=8)
        # Label below arrow
        self.draw_text(x, y + arrow_height + 12, label, color=color, font_size=14)

    def draw_pointer_above(
        self, x: int, y: int, label: str, color: str, arrow_height: int = 20
    ) -> None:
        """Draw a pointer arrow with label above a position."""
        # Arrow pointing down
        self.draw_arrow(x, y - arrow_height, x, y - 5, color=color, head_size=8)
        # Label above arrow
        self.draw_text(x, y - arrow_height - 12, label, color=color, font_size=14)

    def get_image(self) -> Image.Image:
        """Return a copy of the current image."""
        return self.image.copy()
