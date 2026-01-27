"""Top K Elements pattern animations."""

import heapq
from typing import Generator, List, Optional

from .base import BasePattern, AnimationStep
from ..renderers.array_renderer import ArrayRenderer
from ..config import AnimationConfig, ColorScheme


class TopKPattern(BasePattern):
    """
    Animates Top K Elements pattern using min-heap.

    Shows:
    - Heap operations (push/pop)
    - Maintaining k largest elements
    - Final result
    """

    @property
    def name(self) -> str:
        return "top_k"

    @property
    def description(self) -> str:
        return "Top K elements using min-heap"

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
        k: int = 3,
    ) -> Generator[AnimationStep, None, None]:
        yield from self._top_k_steps(data, k)

    def _top_k_steps(
        self, nums: List[int], k: int
    ) -> Generator[AnimationStep, None, None]:
        """Animate finding top k largest elements."""
        min_heap = []

        yield AnimationStep(
            state={
                "nums": nums,
                "k": k,
                "heap": [],
                "current_idx": -1,
            },
            caption=f"Find top {k} largest using min-heap of size {k}",
        )

        for i, num in enumerate(nums):
            yield AnimationStep(
                state={
                    "nums": nums,
                    "k": k,
                    "heap": sorted(min_heap),
                    "current_idx": i,
                    "current_num": num,
                    "action": "considering",
                },
                caption=f"Consider {num}",
            )

            if len(min_heap) < k:
                heapq.heappush(min_heap, num)
                action_msg = f"Heap not full, add {num}"
            elif num > min_heap[0]:
                removed = heapq.heapreplace(min_heap, num)
                action_msg = f"{num} > {removed} (min), replace"
            else:
                action_msg = f"{num} <= {min_heap[0]} (min), skip"

            yield AnimationStep(
                state={
                    "nums": nums,
                    "k": k,
                    "heap": sorted(min_heap),
                    "current_idx": i,
                    "current_num": num,
                    "action": "processed",
                },
                caption=action_msg,
            )

        yield AnimationStep(
            state={
                "nums": nums,
                "k": k,
                "heap": sorted(min_heap, reverse=True),
                "current_idx": -1,
                "final": True,
            },
            caption=f"Top {k}: {sorted(min_heap, reverse=True)}",
            is_pause=True,
            duration_ms=1500,
        )

    def create_animation(self, data: List[int], k: int = 3, **kwargs):
        """Custom rendering for top k visualization."""
        from ..core.animation import Animation
        from ..core.canvas import Canvas

        animation = Animation(self.config)

        width = 500
        height = 320
        cell_w, cell_h = 40, 35

        for step in self._top_k_steps(data, k):
            canvas = Canvas(width, height, self.config.background_color)
            state = step.state

            nums = state.get("nums", [])
            heap = state.get("heap", [])
            current_idx = state.get("current_idx", -1)
            k_val = state.get("k", 3)

            # Title
            canvas.draw_text(width // 2, 20, f"Top {k_val} Elements Pattern", color="#374151", font_size=16)

            # Draw input array
            canvas.draw_text(width // 2, 50, "Input Array:", color="#6B7280", font_size=11)
            start_x = (width - len(nums) * cell_w) // 2
            y = 65

            for i, num in enumerate(nums):
                x = start_x + i * cell_w
                if i == current_idx:
                    fill = "#86EFAC"  # Green - current
                elif i < current_idx:
                    fill = "#D1D5DB"  # Gray - processed
                else:
                    fill = "#E5E7EB"  # Light - pending

                canvas.draw_rounded_rect(x, y, cell_w - 4, cell_h, radius=6, fill=fill, outline="#6B7280")
                canvas.draw_text(x + cell_w // 2 - 2, y + cell_h // 2, str(num), color="#1F2937", font_size=13)

            # Draw heap (min-heap showing k largest)
            canvas.draw_text(width // 2, 130, f"Min-Heap (size ≤ {k_val}):", color="#6B7280", font_size=11)

            heap_y = 150
            heap_start_x = (width - len(heap) * cell_w) // 2 if heap else width // 2 - 20

            if heap:
                for i, val in enumerate(heap):
                    x = heap_start_x + i * cell_w
                    fill = "#C7D2FE" if i == 0 else "#E0E7FF"  # Highlight min (root)
                    canvas.draw_rounded_rect(x, heap_y, cell_w - 4, cell_h, radius=6, fill=fill, outline="#4F46E5")
                    canvas.draw_text(x + cell_w // 2 - 2, heap_y + cell_h // 2, str(val), color="#1F2937", font_size=13)

                # Mark minimum
                canvas.draw_text(heap_start_x + cell_w // 2 - 2, heap_y + cell_h + 12, "min", color="#4F46E5", font_size=10)
            else:
                canvas.draw_text(width // 2, heap_y + 15, "(empty)", color="#9CA3AF", font_size=11)

            # Explanation
            canvas.draw_text(width // 2, 220, "Keep k largest: reject if ≤ min(heap)", color="#6B7280", font_size=10)

            # Caption
            if step.caption:
                canvas.draw_text(width // 2, height - 25, step.caption, color="#374151", font_size=12)

            if step.is_pause:
                animation.add_pause_frame(canvas.get_image(), step.duration_ms or 1500)
            else:
                animation.add_frame(canvas.get_image(), step.duration_ms)

        return animation
