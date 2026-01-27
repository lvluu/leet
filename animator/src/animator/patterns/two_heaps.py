"""Two Heaps pattern animations."""

import heapq
from typing import Any, Generator, List, Optional

from .base import BasePattern, AnimationStep
from ..renderers.array_renderer import ArrayRenderer
from ..config import AnimationConfig, ColorScheme


class TwoHeapsPattern(BasePattern):
    """
    Animates Two Heaps pattern for finding running median.

    Shows:
    - Max-heap (lower half)
    - Min-heap (upper half)
    - Rebalancing operations
    - Median calculation
    """

    @property
    def name(self) -> str:
        return "two_heaps"

    @property
    def description(self) -> str:
        return "Two Heaps for running median"

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
    ) -> Generator[AnimationStep, None, None]:
        """
        Generate two heaps animation for running median.

        Args:
            data: Numbers to insert one by one
        """
        yield from self._running_median_steps(data)

    def _running_median_steps(
        self, nums: List[int]
    ) -> Generator[AnimationStep, None, None]:
        """Animate running median with two heaps."""
        # lower: max-heap (store negatives)
        # upper: min-heap
        lower: List[int] = []  # max-heap via negatives
        upper: List[int] = []  # min-heap

        yield AnimationStep(
            state={
                "lower": [],
                "upper": [],
                "current": None,
                "median": None,
            },
            caption="Two Heaps: max-heap (lower) + min-heap (upper)",
        )

        for num in nums:
            # Decide which heap to insert into
            if not lower or num <= -lower[0]:
                heapq.heappush(lower, -num)
                target = "lower"
            else:
                heapq.heappush(upper, num)
                target = "upper"

            lower_vals = sorted([-x for x in lower], reverse=True)
            upper_vals = sorted(upper)

            yield AnimationStep(
                state={
                    "lower": lower_vals,
                    "upper": upper_vals,
                    "current": num,
                    "target": target,
                    "median": None,
                },
                caption=f"Insert {num} → {'lower (max-heap)' if target == 'lower' else 'upper (min-heap)'}",
            )

            # Rebalance
            rebalanced = False
            if len(lower) > len(upper) + 1:
                val = -heapq.heappop(lower)
                heapq.heappush(upper, val)
                rebalanced = True
                move_val = val
                move_dir = "lower → upper"
            elif len(upper) > len(lower):
                val = heapq.heappop(upper)
                heapq.heappush(lower, -val)
                rebalanced = True
                move_val = val
                move_dir = "upper → lower"

            if rebalanced:
                lower_vals = sorted([-x for x in lower], reverse=True)
                upper_vals = sorted(upper)

                yield AnimationStep(
                    state={
                        "lower": lower_vals,
                        "upper": upper_vals,
                        "current": None,
                        "rebalance": move_val,
                        "median": None,
                    },
                    caption=f"Rebalance: move {move_val} from {move_dir}",
                )

            # Calculate median
            if len(lower) > len(upper):
                median = -lower[0]
            else:
                median = (-lower[0] + upper[0]) / 2

            lower_vals = sorted([-x for x in lower], reverse=True)
            upper_vals = sorted(upper)

            yield AnimationStep(
                state={
                    "lower": lower_vals,
                    "upper": upper_vals,
                    "current": None,
                    "median": median,
                },
                caption=f"Median = {median}" + (" (top of lower)" if len(lower) > len(upper) else " (avg of tops)"),
            )

        yield AnimationStep(
            state={
                "lower": sorted([-x for x in lower], reverse=True),
                "upper": sorted(upper),
                "current": None,
                "median": median,
                "final": True,
            },
            caption=f"Final median: {median}",
            is_pause=True,
            duration_ms=1500,
        )

    def create_animation(self, data: List[int], **kwargs):
        """Custom rendering for two heaps side by side."""
        from ..core.animation import Animation
        from ..core.canvas import Canvas

        animation = Animation(self.config)

        width = 500
        height = 350
        cell_w, cell_h = 40, 35

        lower: List[int] = []
        upper: List[int] = []

        for step in self._running_median_steps(data):
            canvas = Canvas(width, height, self.config.background_color)
            state = step.state

            lower_vals = state.get("lower", [])
            upper_vals = state.get("upper", [])
            current = state.get("current")
            median = state.get("median")
            target = state.get("target")
            rebalance = state.get("rebalance")

            # Title
            canvas.draw_text(width // 2, 20, "Two Heaps Pattern", color="#374151", font_size=16)

            # Draw lower heap (max-heap) on left
            lx = 80
            canvas.draw_text(lx + 50, 55, "Lower (max-heap)", color="#6366F1", font_size=12)

            for i, val in enumerate(lower_vals):
                y = 80 + i * cell_h
                fill = "#C7D2FE"  # Light indigo
                if current == val and target == "lower":
                    fill = "#86EFAC"  # Green - just inserted
                if rebalance == val:
                    fill = "#FDE68A"  # Yellow - being moved
                canvas.draw_rounded_rect(lx, y, cell_w * 2, cell_h - 4, radius=6, fill=fill, outline="#4F46E5")
                canvas.draw_text(lx + cell_w, y + cell_h // 2 - 2, str(val), color="#1F2937", font_size=14)

            if lower_vals:
                # Mark the top (max)
                canvas.draw_text(lx + cell_w * 2 + 15, 80 + cell_h // 2 - 2, "← max", color="#4F46E5", font_size=10, anchor="lm")

            # Draw upper heap (min-heap) on right
            rx = width - 160
            canvas.draw_text(rx + 50, 55, "Upper (min-heap)", color="#059669", font_size=12)

            for i, val in enumerate(upper_vals):
                y = 80 + i * cell_h
                fill = "#A7F3D0"  # Light green
                if current == val and target == "upper":
                    fill = "#86EFAC"  # Bright green - just inserted
                if rebalance == val:
                    fill = "#FDE68A"  # Yellow - being moved
                canvas.draw_rounded_rect(rx, y, cell_w * 2, cell_h - 4, radius=6, fill=fill, outline="#059669")
                canvas.draw_text(rx + cell_w, y + cell_h // 2 - 2, str(val), color="#1F2937", font_size=14)

            if upper_vals:
                # Mark the top (min)
                canvas.draw_text(rx + cell_w * 2 + 15, 80 + cell_h // 2 - 2, "← min", color="#059669", font_size=10, anchor="lm")

            # Draw center divider and invariant
            cx = width // 2
            canvas.draw_line(cx, 70, cx, 250, "#D1D5DB", 2)
            canvas.draw_text(cx, 265, "max(lower) ≤ min(upper)", color="#6B7280", font_size=10)

            # Draw median box
            if median is not None:
                canvas.draw_rounded_rect(cx - 60, 280, 120, 35, radius=8, fill="#FEF3C7", outline="#F59E0B")
                canvas.draw_text(cx, 297, f"Median: {median}", color="#92400E", font_size=14)

            # Draw caption
            if step.caption:
                canvas.draw_text(width // 2, height - 20, step.caption, color="#374151", font_size=12)

            if step.is_pause:
                animation.add_pause_frame(canvas.get_image(), step.duration_ms or 1500)
            else:
                animation.add_frame(canvas.get_image(), step.duration_ms)

        return animation
