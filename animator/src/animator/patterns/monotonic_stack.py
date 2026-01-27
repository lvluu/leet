"""Monotonic stack pattern animations."""

from typing import Any, Generator, List, Optional

from .base import BasePattern, AnimationStep
from ..renderers.array_renderer import ArrayRenderer
from ..config import AnimationConfig, ColorScheme


class MonotonicStackPattern(BasePattern):
    """
    Animates monotonic stack algorithms.

    Variants:
    - Next greater element
    - Next smaller element
    """

    @property
    def name(self) -> str:
        return "monotonic_stack"

    @property
    def description(self) -> str:
        return "Monotonic stack for next greater/smaller element"

    def __init__(
        self,
        config: Optional[AnimationConfig] = None,
        color_scheme: Optional[ColorScheme] = None,
    ):
        renderer = ArrayRenderer(color_scheme=color_scheme)
        super().__init__(renderer, config)

    def get_steps(
        self,
        data: List[int],
        variant: str = "next_greater",
    ) -> Generator[AnimationStep, None, None]:
        """
        Generate monotonic stack animation steps.

        Args:
            data: Input array
            variant: "next_greater" or "next_smaller"
        """
        if variant == "next_greater":
            yield from self._next_greater_steps(data)
        elif variant == "next_smaller":
            yield from self._next_smaller_steps(data)

    def _next_greater_steps(
        self, arr: List[int]
    ) -> Generator[AnimationStep, None, None]:
        """Find next greater element for each position."""
        n = len(arr)
        result = [-1] * n
        stack: List[int] = []  # Stack of indices

        yield AnimationStep(
            state={},
            caption="Find next greater element for each position",
        )

        for i in range(n):
            yield AnimationStep(
                state={
                    "current": i,
                    "highlights": {j: "#FDE68A" for j in stack},
                    "pointers": [
                        {"index": i, "label": "i", "color": "#3B82F6", "position": "below"},
                    ],
                },
                caption=f"Process arr[{i}] = {arr[i]}, stack indices: {stack}",
            )

            # Pop elements smaller than current
            while stack and arr[stack[-1]] < arr[i]:
                j = stack.pop()
                result[j] = arr[i]

                yield AnimationStep(
                    state={
                        "current": i,
                        "highlights": {
                            **{k: "#FDE68A" for k in stack},
                            j: "#10B981",  # Found answer
                        },
                        "pointers": [
                            {"index": i, "label": "i", "color": "#3B82F6", "position": "below"},
                            {"index": j, "label": "pop", "color": "#10B981", "position": "above"},
                        ],
                    },
                    caption=f"Pop idx {j}: arr[{j}]={arr[j]} < {arr[i]}, next greater = {arr[i]}",
                )

            # Push current index
            stack.append(i)
            yield AnimationStep(
                state={
                    "current": i,
                    "highlights": {j: "#FDE68A" for j in stack},
                    "pointers": [
                        {"index": i, "label": "push", "color": "#8B5CF6", "position": "below"},
                    ],
                },
                caption=f"Push index {i} onto stack",
            )

        # Remaining elements have no greater element
        yield AnimationStep(
            state={
                "highlights": {j: "#EF4444" for j in stack},
                "visited": set(range(n)) - set(stack),
            },
            caption=f"Remaining in stack have no next greater: {[arr[j] for j in stack]}",
        )

        yield AnimationStep(
            state={"visited": set(range(n))},
            caption=f"Result: {result}",
            is_pause=True,
            duration_ms=1500,
        )

    def _next_smaller_steps(
        self, arr: List[int]
    ) -> Generator[AnimationStep, None, None]:
        """Find next smaller element for each position."""
        n = len(arr)
        result = [-1] * n
        stack: List[int] = []

        yield AnimationStep(
            state={},
            caption="Find next smaller element for each position",
        )

        for i in range(n):
            yield AnimationStep(
                state={
                    "current": i,
                    "highlights": {j: "#FDE68A" for j in stack},
                    "pointers": [
                        {"index": i, "label": "i", "color": "#3B82F6", "position": "below"},
                    ],
                },
                caption=f"Process arr[{i}] = {arr[i]}, stack: {stack}",
            )

            # Pop elements greater than current
            while stack and arr[stack[-1]] > arr[i]:
                j = stack.pop()
                result[j] = arr[i]

                yield AnimationStep(
                    state={
                        "current": i,
                        "highlights": {
                            **{k: "#FDE68A" for k in stack},
                            j: "#10B981",
                        },
                        "pointers": [
                            {"index": i, "label": "i", "color": "#3B82F6", "position": "below"},
                            {"index": j, "label": "pop", "color": "#10B981", "position": "above"},
                        ],
                    },
                    caption=f"Pop idx {j}: arr[{j}]={arr[j]} > {arr[i]}, next smaller = {arr[i]}",
                )

            stack.append(i)
            yield AnimationStep(
                state={
                    "current": i,
                    "highlights": {j: "#FDE68A" for j in stack},
                    "pointers": [
                        {"index": i, "label": "push", "color": "#8B5CF6", "position": "below"},
                    ],
                },
                caption=f"Push index {i}",
            )

        yield AnimationStep(
            state={
                "highlights": {j: "#EF4444" for j in stack},
                "visited": set(range(n)) - set(stack),
            },
            caption=f"Remaining have no next smaller: {[arr[j] for j in stack]}",
        )

        yield AnimationStep(
            state={"visited": set(range(n))},
            caption=f"Result: {result}",
            is_pause=True,
            duration_ms=1500,
        )
