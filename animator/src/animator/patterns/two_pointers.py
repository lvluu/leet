"""Two pointers pattern animations."""

from typing import Any, Generator, List, Optional

from .base import BasePattern, AnimationStep
from ..renderers.array_renderer import ArrayRenderer
from ..config import AnimationConfig, ColorScheme


class TwoPointersPattern(BasePattern):
    """
    Animates two pointer techniques.

    Variants:
    - Opposite direction (converging from ends)
    - Same direction
    - Fast and slow pointers
    """

    @property
    def name(self) -> str:
        return "two_pointers"

    @property
    def description(self) -> str:
        return "Two pointer techniques on arrays"

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
        variant: str = "opposite",
        target: Optional[int] = None,
    ) -> Generator[AnimationStep, None, None]:
        """
        Generate two pointers animation steps.

        Args:
            data: Input array
            variant: "opposite", "same", or "fast_slow"
            target: Target sum (for opposite direction variant)
        """
        if variant == "opposite":
            yield from self._opposite_direction_steps(data, target or 10)
        elif variant == "same":
            yield from self._same_direction_steps(data)
        elif variant == "fast_slow":
            yield from self._fast_slow_steps(data)

    def _opposite_direction_steps(
        self, arr: List[int], target: int
    ) -> Generator[AnimationStep, None, None]:
        """Two sum on sorted array - pointers converging from ends."""
        n = len(arr)
        left, right = 0, n - 1

        yield AnimationStep(
            state={
                "pointers": [
                    {"index": left, "label": "L", "color": "#EF4444", "position": "below"},
                    {"index": right, "label": "R", "color": "#8B5CF6", "position": "below"},
                ],
            },
            caption=f"Find two numbers that sum to {target}",
        )

        visited = set()
        found = False

        while left < right:
            current_sum = arr[left] + arr[right]

            yield AnimationStep(
                state={
                    "highlights": {left: "#FDE68A", right: "#FDE68A"},
                    "visited": visited.copy(),
                    "pointers": [
                        {"index": left, "label": "L", "color": "#EF4444", "position": "below"},
                        {"index": right, "label": "R", "color": "#8B5CF6", "position": "below"},
                    ],
                },
                caption=f"arr[{left}] + arr[{right}] = {arr[left]} + {arr[right]} = {current_sum}",
            )

            if current_sum == target:
                yield AnimationStep(
                    state={
                        "highlights": {left: "#10B981", right: "#10B981"},
                        "visited": visited.copy(),
                        "pointers": [
                            {"index": left, "label": "L", "color": "#10B981", "position": "below"},
                            {"index": right, "label": "R", "color": "#10B981", "position": "below"},
                        ],
                    },
                    caption=f"Found! arr[{left}] + arr[{right}] = {target}",
                    is_pause=True,
                    duration_ms=1500,
                )
                found = True
                break
            elif current_sum < target:
                visited.add(left)
                left += 1
                yield AnimationStep(
                    state={
                        "visited": visited.copy(),
                        "pointers": [
                            {"index": left, "label": "L", "color": "#EF4444", "position": "below"},
                            {"index": right, "label": "R", "color": "#8B5CF6", "position": "below"},
                        ],
                    },
                    caption=f"Sum {current_sum} < {target}, move left pointer right",
                )
            else:
                visited.add(right)
                right -= 1
                yield AnimationStep(
                    state={
                        "visited": visited.copy(),
                        "pointers": [
                            {"index": left, "label": "L", "color": "#EF4444", "position": "below"},
                            {"index": right, "label": "R", "color": "#8B5CF6", "position": "below"},
                        ],
                    },
                    caption=f"Sum {current_sum} > {target}, move right pointer left",
                )

        if not found:
            yield AnimationStep(
                state={"visited": set(range(n))},
                caption="No pair found!",
                is_pause=True,
            )

    def _same_direction_steps(
        self, arr: List[int]
    ) -> Generator[AnimationStep, None, None]:
        """Remove duplicates from sorted array - same direction pointers."""
        n = len(arr)
        if n == 0:
            return

        slow = 0

        yield AnimationStep(
            state={
                "pointers": [
                    {"index": 0, "label": "slow", "color": "#06B6D4", "position": "below"},
                    {"index": 0, "label": "fast", "color": "#F97316", "position": "above"},
                ],
            },
            caption="Remove duplicates: slow tracks unique elements",
        )

        for fast in range(1, n):
            yield AnimationStep(
                state={
                    "current": fast,
                    "highlights": {slow: "#06B6D4"},
                    "pointers": [
                        {"index": slow, "label": "slow", "color": "#06B6D4", "position": "below"},
                        {"index": fast, "label": "fast", "color": "#F97316", "position": "above"},
                    ],
                },
                caption=f"Compare arr[{slow}]={arr[slow]} with arr[{fast}]={arr[fast]}",
            )

            if arr[fast] != arr[slow]:
                slow += 1
                yield AnimationStep(
                    state={
                        "current": fast,
                        "highlights": {slow: "#10B981"},
                        "visited": set(range(slow)),
                        "pointers": [
                            {"index": slow, "label": "slow", "color": "#06B6D4", "position": "below"},
                            {"index": fast, "label": "fast", "color": "#F97316", "position": "above"},
                        ],
                    },
                    caption=f"Different! Move slow to {slow}",
                )

        yield AnimationStep(
            state={
                "visited": set(range(slow + 1)),
                "pointers": [
                    {"index": slow, "label": "slow", "color": "#10B981", "position": "below"},
                ],
            },
            caption=f"Done! {slow + 1} unique elements",
            is_pause=True,
            duration_ms=1500,
        )

    def _fast_slow_steps(
        self, arr: List[int]
    ) -> Generator[AnimationStep, None, None]:
        """Fast and slow pointer demonstration."""
        n = len(arr)
        slow, fast = 0, 0

        yield AnimationStep(
            state={
                "pointers": [
                    {"index": slow, "label": "slow", "color": "#06B6D4", "position": "below"},
                    {"index": fast, "label": "fast", "color": "#F97316", "position": "above"},
                ],
            },
            caption="Fast pointer moves 2x speed of slow pointer",
        )

        while fast < n - 1:
            slow += 1
            fast = min(fast + 2, n - 1)

            yield AnimationStep(
                state={
                    "highlights": {slow: "#06B6D4", fast: "#F97316"},
                    "pointers": [
                        {"index": slow, "label": "slow", "color": "#06B6D4", "position": "below"},
                        {"index": fast, "label": "fast", "color": "#F97316", "position": "above"},
                    ],
                },
                caption=f"slow={slow}, fast={fast}",
            )

        yield AnimationStep(
            state={
                "highlights": {slow: "#10B981"},
                "pointers": [
                    {"index": slow, "label": "middle", "color": "#10B981", "position": "below"},
                ],
            },
            caption=f"Slow pointer at middle: index {slow}",
            is_pause=True,
            duration_ms=1500,
        )
