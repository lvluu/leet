"""Modified binary search pattern animations."""

from typing import Any, Generator, List, Optional

from .base import BasePattern, AnimationStep
from ..renderers.array_renderer import ArrayRenderer
from ..config import AnimationConfig, ColorScheme


class BinarySearchPattern(BasePattern):
    """
    Animates binary search algorithms.

    Variants:
    - Classic binary search
    - Search for boundary (first/last occurrence)
    - Search in rotated array
    """

    @property
    def name(self) -> str:
        return "binary_search"

    @property
    def description(self) -> str:
        return "Modified binary search techniques"

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
        target: int,
        variant: str = "classic",
    ) -> Generator[AnimationStep, None, None]:
        """
        Generate binary search animation steps.

        Args:
            data: Sorted input array
            target: Value to search for
            variant: "classic", "first_occurrence", "rotated"
        """
        if variant == "classic":
            yield from self._classic_binary_search(data, target)
        elif variant == "first_occurrence":
            yield from self._first_occurrence_search(data, target)
        elif variant == "rotated":
            yield from self._rotated_array_search(data, target)

    def _classic_binary_search(
        self, arr: List[int], target: int
    ) -> Generator[AnimationStep, None, None]:
        """Classic binary search."""
        n = len(arr)
        left, right = 0, n - 1
        eliminated = set()

        yield AnimationStep(
            state={
                "pointers": [
                    {"index": left, "label": "L", "color": "#EF4444", "position": "below"},
                    {"index": right, "label": "R", "color": "#8B5CF6", "position": "below"},
                ],
            },
            caption=f"Binary search for {target} in sorted array",
        )

        while left <= right:
            mid = (left + right) // 2

            yield AnimationStep(
                state={
                    "window": (left, right),
                    "current": mid,
                    "visited": eliminated.copy(),
                    "pointers": [
                        {"index": left, "label": "L", "color": "#EF4444", "position": "below"},
                        {"index": mid, "label": "M", "color": "#3B82F6", "position": "above"},
                        {"index": right, "label": "R", "color": "#8B5CF6", "position": "below"},
                    ],
                },
                caption=f"mid = {mid}, arr[mid] = {arr[mid]}",
            )

            if arr[mid] == target:
                yield AnimationStep(
                    state={
                        "highlights": {mid: "#10B981"},
                        "visited": eliminated.copy(),
                        "pointers": [
                            {"index": mid, "label": "Found!", "color": "#10B981", "position": "below"},
                        ],
                    },
                    caption=f"Found {target} at index {mid}!",
                    is_pause=True,
                    duration_ms=1500,
                )
                return
            elif arr[mid] < target:
                # Eliminate left half
                for i in range(left, mid + 1):
                    eliminated.add(i)
                yield AnimationStep(
                    state={
                        "visited": eliminated.copy(),
                        "pointers": [
                            {"index": mid + 1, "label": "L", "color": "#EF4444", "position": "below"},
                            {"index": right, "label": "R", "color": "#8B5CF6", "position": "below"},
                        ],
                    },
                    caption=f"arr[mid]={arr[mid]} < {target}, search right half",
                )
                left = mid + 1
            else:
                # Eliminate right half
                for i in range(mid, right + 1):
                    eliminated.add(i)
                yield AnimationStep(
                    state={
                        "visited": eliminated.copy(),
                        "pointers": [
                            {"index": left, "label": "L", "color": "#EF4444", "position": "below"},
                            {"index": mid - 1, "label": "R", "color": "#8B5CF6", "position": "below"},
                        ],
                    },
                    caption=f"arr[mid]={arr[mid]} > {target}, search left half",
                )
                right = mid - 1

        yield AnimationStep(
            state={"visited": set(range(n))},
            caption=f"{target} not found in array!",
            is_pause=True,
            duration_ms=1500,
        )

    def _first_occurrence_search(
        self, arr: List[int], target: int
    ) -> Generator[AnimationStep, None, None]:
        """Find first occurrence of target."""
        n = len(arr)
        left, right = 0, n - 1
        result = -1
        eliminated = set()

        yield AnimationStep(
            state={
                "pointers": [
                    {"index": left, "label": "L", "color": "#EF4444", "position": "below"},
                    {"index": right, "label": "R", "color": "#8B5CF6", "position": "below"},
                ],
            },
            caption=f"Find FIRST occurrence of {target}",
        )

        while left <= right:
            mid = (left + right) // 2

            yield AnimationStep(
                state={
                    "window": (left, right),
                    "current": mid,
                    "visited": eliminated.copy(),
                    "highlights": {result: "#10B981"} if result >= 0 else {},
                    "pointers": [
                        {"index": left, "label": "L", "color": "#EF4444", "position": "below"},
                        {"index": mid, "label": "M", "color": "#3B82F6", "position": "above"},
                        {"index": right, "label": "R", "color": "#8B5CF6", "position": "below"},
                    ],
                },
                caption=f"mid = {mid}, arr[mid] = {arr[mid]}",
            )

            if arr[mid] == target:
                result = mid
                # Continue searching left for earlier occurrence
                for i in range(mid, right + 1):
                    eliminated.add(i)
                yield AnimationStep(
                    state={
                        "visited": eliminated.copy(),
                        "highlights": {result: "#10B981"},
                        "pointers": [
                            {"index": left, "label": "L", "color": "#EF4444", "position": "below"},
                            {"index": mid - 1, "label": "R", "color": "#8B5CF6", "position": "below"},
                        ],
                    },
                    caption=f"Found at {mid}, but check left for earlier occurrence",
                )
                right = mid - 1
            elif arr[mid] < target:
                for i in range(left, mid + 1):
                    eliminated.add(i)
                left = mid + 1
            else:
                for i in range(mid, right + 1):
                    eliminated.add(i)
                right = mid - 1

        if result >= 0:
            yield AnimationStep(
                state={
                    "highlights": {result: "#10B981"},
                    "visited": eliminated.copy(),
                    "pointers": [
                        {"index": result, "label": "First!", "color": "#10B981", "position": "below"},
                    ],
                },
                caption=f"First occurrence of {target} at index {result}",
                is_pause=True,
                duration_ms=1500,
            )
        else:
            yield AnimationStep(
                state={"visited": set(range(n))},
                caption=f"{target} not found!",
                is_pause=True,
            )

    def _rotated_array_search(
        self, arr: List[int], target: int
    ) -> Generator[AnimationStep, None, None]:
        """Search in rotated sorted array."""
        n = len(arr)
        left, right = 0, n - 1

        yield AnimationStep(
            state={
                "pointers": [
                    {"index": left, "label": "L", "color": "#EF4444", "position": "below"},
                    {"index": right, "label": "R", "color": "#8B5CF6", "position": "below"},
                ],
            },
            caption=f"Search {target} in rotated sorted array",
        )

        while left <= right:
            mid = (left + right) // 2

            yield AnimationStep(
                state={
                    "window": (left, right),
                    "current": mid,
                    "pointers": [
                        {"index": left, "label": "L", "color": "#EF4444", "position": "below"},
                        {"index": mid, "label": "M", "color": "#3B82F6", "position": "above"},
                        {"index": right, "label": "R", "color": "#8B5CF6", "position": "below"},
                    ],
                },
                caption=f"mid={mid}, arr[mid]={arr[mid]}",
            )

            if arr[mid] == target:
                yield AnimationStep(
                    state={
                        "highlights": {mid: "#10B981"},
                        "pointers": [
                            {"index": mid, "label": "Found!", "color": "#10B981", "position": "below"},
                        ],
                    },
                    caption=f"Found {target} at index {mid}!",
                    is_pause=True,
                    duration_ms=1500,
                )
                return

            # Determine which half is sorted
            if arr[left] <= arr[mid]:
                # Left half is sorted
                if arr[left] <= target < arr[mid]:
                    yield AnimationStep(
                        state={
                            "window": (left, mid - 1),
                            "pointers": [
                                {"index": left, "label": "L", "color": "#EF4444", "position": "below"},
                                {"index": mid - 1, "label": "R", "color": "#8B5CF6", "position": "below"},
                            ],
                        },
                        caption=f"Left sorted [{arr[left]}..{arr[mid]}], target in left half",
                    )
                    right = mid - 1
                else:
                    yield AnimationStep(
                        state={
                            "window": (mid + 1, right),
                            "pointers": [
                                {"index": mid + 1, "label": "L", "color": "#EF4444", "position": "below"},
                                {"index": right, "label": "R", "color": "#8B5CF6", "position": "below"},
                            ],
                        },
                        caption=f"Left sorted, but target in right half",
                    )
                    left = mid + 1
            else:
                # Right half is sorted
                if arr[mid] < target <= arr[right]:
                    yield AnimationStep(
                        state={
                            "window": (mid + 1, right),
                            "pointers": [
                                {"index": mid + 1, "label": "L", "color": "#EF4444", "position": "below"},
                                {"index": right, "label": "R", "color": "#8B5CF6", "position": "below"},
                            ],
                        },
                        caption=f"Right sorted [{arr[mid]}..{arr[right]}], target in right half",
                    )
                    left = mid + 1
                else:
                    yield AnimationStep(
                        state={
                            "window": (left, mid - 1),
                            "pointers": [
                                {"index": left, "label": "L", "color": "#EF4444", "position": "below"},
                                {"index": mid - 1, "label": "R", "color": "#8B5CF6", "position": "below"},
                            ],
                        },
                        caption=f"Right sorted, but target in left half",
                    )
                    right = mid - 1

        yield AnimationStep(
            state={},
            caption=f"{target} not found in array!",
            is_pause=True,
            duration_ms=1500,
        )
