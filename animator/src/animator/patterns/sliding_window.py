"""Sliding window pattern animations."""

from typing import Any, Generator, List, Optional

from .base import BasePattern, AnimationStep
from ..renderers.array_renderer import ArrayRenderer
from ..config import AnimationConfig, ColorScheme


class SlidingWindowPattern(BasePattern):
    """
    Animates sliding window algorithms on arrays.

    Supports:
    - Fixed-size windows
    - Dynamic/variable windows (expand/contract)
    """

    @property
    def name(self) -> str:
        return "sliding_window"

    @property
    def description(self) -> str:
        return "Sliding window technique on arrays"

    def __init__(
        self,
        config: Optional[AnimationConfig] = None,
        color_scheme: Optional[ColorScheme] = None,
    ):
        renderer = ArrayRenderer(color_scheme=color_scheme)
        super().__init__(renderer, config)

    def get_steps(
        self,
        data: List[Any],
        window_size: Optional[int] = None,
        algorithm: str = "fixed",
    ) -> Generator[AnimationStep, None, None]:
        """
        Generate sliding window animation steps.

        Args:
            data: Input array
            window_size: Fixed window size (for fixed algorithm)
            algorithm: "fixed" or "dynamic"
        """
        if algorithm == "fixed":
            yield from self._fixed_window_steps(data, window_size or 3)
        else:
            yield from self._dynamic_window_steps(data)

    def _fixed_window_steps(
        self, arr: List[int], k: int
    ) -> Generator[AnimationStep, None, None]:
        """Generate steps for fixed-size sliding window."""
        n = len(arr)

        # Initial state
        yield AnimationStep(
            state={"pointers": []},
            caption=f"Array of {n} elements, window size k={k}",
        )

        # Build initial window
        for i in range(min(k, n)):
            yield AnimationStep(
                state={
                    "window": (0, i),
                    "current": i,
                    "pointers": [
                        {"index": 0, "label": "L", "color": "#EF4444", "position": "below"},
                        {"index": i, "label": "R", "color": "#8B5CF6", "position": "below"},
                    ],
                },
                caption=f"Building window: add arr[{i}] = {arr[i]}",
            )

        if n <= k:
            yield AnimationStep(
                state={
                    "window": (0, n - 1),
                    "visited": set(range(n)),
                    "pointers": [
                        {"index": 0, "label": "L", "color": "#EF4444", "position": "below"},
                        {"index": n - 1, "label": "R", "color": "#8B5CF6", "position": "below"},
                    ],
                },
                caption="Window covers entire array!",
                is_pause=True,
            )
            return

        # Slide window
        for i in range(k, n):
            left = i - k + 1
            yield AnimationStep(
                state={
                    "window": (left, i),
                    "current": i,
                    "visited": set(range(left)),
                    "pointers": [
                        {"index": left, "label": "L", "color": "#EF4444", "position": "below"},
                        {"index": i, "label": "R", "color": "#8B5CF6", "position": "below"},
                    ],
                },
                caption=f"Slide: remove arr[{left-1}], add arr[{i}] = {arr[i]}",
            )

        # Final state
        yield AnimationStep(
            state={
                "window": (n - k, n - 1),
                "visited": set(range(n)),
                "pointers": [
                    {"index": n - k, "label": "L", "color": "#EF4444", "position": "below"},
                    {"index": n - 1, "label": "R", "color": "#8B5CF6", "position": "below"},
                ],
            },
            caption="Window traversal complete!",
            is_pause=True,
            duration_ms=1500,
        )

    def _dynamic_window_steps(
        self, arr: List[int]
    ) -> Generator[AnimationStep, None, None]:
        """Generate steps for dynamic sliding window (expand/contract)."""
        n = len(arr)
        left = 0

        yield AnimationStep(
            state={
                "pointers": [
                    {"index": 0, "label": "L", "color": "#EF4444", "position": "below"},
                    {"index": 0, "label": "R", "color": "#8B5CF6", "position": "below"},
                ],
            },
            caption="Initialize: left=0, right=0",
        )

        for right in range(n):
            # Expansion step
            yield AnimationStep(
                state={
                    "window": (left, right),
                    "current": right,
                    "pointers": [
                        {"index": left, "label": "L", "color": "#EF4444", "position": "below"},
                        {"index": right, "label": "R", "color": "#8B5CF6", "position": "below"},
                    ],
                },
                caption=f"Expand: right -> {right}, window=[{left}..{right}]",
            )

            # Simulate contraction every few steps for demo
            if right > 0 and right % 3 == 0 and left < right:
                left += 1
                yield AnimationStep(
                    state={
                        "window": (left, right),
                        "visited": set(range(left)),
                        "pointers": [
                            {"index": left, "label": "L", "color": "#EF4444", "position": "below"},
                            {"index": right, "label": "R", "color": "#8B5CF6", "position": "below"},
                        ],
                    },
                    caption=f"Contract: left -> {left}, window=[{left}..{right}]",
                )

        yield AnimationStep(
            state={
                "window": (left, n - 1),
                "visited": set(range(n)),
                "pointers": [
                    {"index": left, "label": "L", "color": "#EF4444", "position": "below"},
                    {"index": n - 1, "label": "R", "color": "#8B5CF6", "position": "below"},
                ],
            },
            caption="Traversal complete!",
            is_pause=True,
            duration_ms=1500,
        )
