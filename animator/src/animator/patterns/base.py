"""Base pattern abstract class and AnimationStep dataclass."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, Generator, Optional

from ..core.animation import Animation
from ..core.canvas import Canvas
from ..renderers.base import BaseRenderer
from ..config import AnimationConfig


@dataclass
class AnimationStep:
    """Represents a single step in an animation."""

    state: Dict[str, Any]  # Visual state for renderer
    caption: str = ""  # Optional caption text
    duration_ms: Optional[int] = None  # Optional custom duration
    is_pause: bool = False  # Whether this is a pause frame


class BasePattern(ABC):
    """
    Abstract base class for pattern animators.

    Patterns define WHAT steps to animate. They yield AnimationStep
    objects that describe the visual state at each frame.
    """

    def __init__(
        self,
        renderer: BaseRenderer,
        config: Optional[AnimationConfig] = None,
    ):
        self.renderer = renderer
        self.config = config or AnimationConfig()

    @abstractmethod
    def get_steps(self, data: Any, **kwargs) -> Generator[AnimationStep, None, None]:
        """
        Generate animation steps for the pattern.

        Args:
            data: Input data for the algorithm
            **kwargs: Pattern-specific parameters

        Yields:
            AnimationStep objects describing each frame
        """
        pass

    def create_animation(self, data: Any, **kwargs) -> Animation:
        """Create a complete animation from the pattern."""
        animation = Animation(self.config)

        width, height = self.renderer.calculate_dimensions(data)
        # Add space for caption
        height += 50

        for step in self.get_steps(data, **kwargs):
            canvas = Canvas(width, height, self.config.background_color)
            self.renderer.render(canvas, data, step.state)

            if step.caption:
                canvas.draw_text(
                    width // 2, height - 25, step.caption,
                    color="#374151", font_size=14
                )

            if step.is_pause:
                animation.add_pause_frame(
                    canvas.get_image(), step.duration_ms or 1500
                )
            else:
                animation.add_frame(canvas.get_image(), step.duration_ms)

        return animation

    @property
    @abstractmethod
    def name(self) -> str:
        """Pattern name for CLI and registry."""
        pass

    @property
    def description(self) -> str:
        """Pattern description."""
        return ""
