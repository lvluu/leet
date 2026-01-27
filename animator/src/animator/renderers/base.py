"""Base renderer abstract class."""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Tuple

from ..core.canvas import Canvas
from ..config import ColorScheme


class BaseRenderer(ABC):
    """
    Abstract base class for data structure renderers.

    Renderers are responsible for HOW to draw a data structure.
    They don't know about animation steps - they just render state.
    """

    def __init__(self, color_scheme: Optional[ColorScheme] = None):
        self.colors = color_scheme or ColorScheme()

    @abstractmethod
    def calculate_dimensions(self, data: Any) -> Tuple[int, int]:
        """Calculate required canvas dimensions for the data."""
        pass

    @abstractmethod
    def render(self, canvas: Canvas, data: Any, state: Dict[str, Any]) -> None:
        """
        Render the data structure onto the canvas.

        Args:
            canvas: The drawing canvas
            data: The data structure to render
            state: Visual state (highlights, pointers, visited nodes, etc.)
        """
        pass

    def get_element_position(self, data: Any, index: Any) -> Tuple[int, int]:
        """Get the center position of an element for pointer drawing."""
        raise NotImplementedError("Subclass must implement for pointer support")
