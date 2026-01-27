"""Prefix Sum pattern animations."""

from typing import Generator, List, Optional

from .base import BasePattern, AnimationStep
from ..renderers.array_renderer import ArrayRenderer
from ..config import AnimationConfig, ColorScheme


class PrefixSumPattern(BasePattern):
    """
    Animates Prefix Sum pattern.

    Shows:
    - Building prefix sum array
    - Range sum queries
    """

    @property
    def name(self) -> str:
        return "prefix_sum"

    @property
    def description(self) -> str:
        return "Prefix sum for range queries"

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
        yield from self._build_prefix_steps(data)

    def _build_prefix_steps(
        self, nums: List[int]
    ) -> Generator[AnimationStep, None, None]:
        """Animate building prefix sum array."""
        n = len(nums)
        prefix = [0] * (n + 1)

        yield AnimationStep(
            state={
                "nums": nums,
                "prefix": prefix[:],
                "current_idx": -1,
            },
            caption="Build prefix sum: prefix[i] = sum of nums[0:i]",
        )

        for i in range(n):
            prefix[i + 1] = prefix[i] + nums[i]

            yield AnimationStep(
                state={
                    "nums": nums,
                    "prefix": prefix[:],
                    "current_idx": i,
                    "formula": f"prefix[{i+1}] = prefix[{i}] + nums[{i}] = {prefix[i+1]}",
                },
                caption=f"prefix[{i+1}] = {prefix[i]} + {nums[i]} = {prefix[i+1]}",
            )

        # Show a range query example
        if n >= 3:
            i, j = 1, 3
            range_sum = prefix[j + 1] - prefix[i]

            yield AnimationStep(
                state={
                    "nums": nums,
                    "prefix": prefix[:],
                    "current_idx": -1,
                    "query_start": i,
                    "query_end": j,
                    "range_sum": range_sum,
                },
                caption=f"Query sum({i},{j}) = prefix[{j+1}] - prefix[{i}] = {prefix[j+1]} - {prefix[i]} = {range_sum}",
                is_pause=True,
                duration_ms=1500,
            )

    def create_animation(self, data: List[int], **kwargs):
        """Custom rendering for prefix sum visualization."""
        from ..core.animation import Animation
        from ..core.canvas import Canvas

        animation = Animation(self.config)

        width = 550
        height = 300
        cell_w, cell_h = 45, 35

        for step in self._build_prefix_steps(data):
            canvas = Canvas(width, height, self.config.background_color)
            state = step.state

            nums = state.get("nums", [])
            prefix = state.get("prefix", [])
            current_idx = state.get("current_idx", -1)
            query_start = state.get("query_start", -1)
            query_end = state.get("query_end", -1)

            # Title
            canvas.draw_text(width // 2, 20, "Prefix Sum Pattern", color="#374151", font_size=16)

            # Draw original array
            canvas.draw_text(70, 60, "nums:", color="#6B7280", font_size=11, anchor="rm")
            start_x = 80

            for i, num in enumerate(nums):
                x = start_x + i * cell_w
                if query_start <= i <= query_end:
                    fill = "#FDE68A"  # Yellow - query range
                elif i == current_idx:
                    fill = "#86EFAC"  # Green - current
                elif i < current_idx:
                    fill = "#D1D5DB"  # Gray - processed
                else:
                    fill = "#E5E7EB"

                canvas.draw_rounded_rect(x, 45, cell_w - 4, cell_h, radius=6, fill=fill, outline="#6B7280")
                canvas.draw_text(x + cell_w // 2 - 2, 45 + cell_h // 2, str(num), color="#1F2937", font_size=13)

                # Index
                canvas.draw_text(x + cell_w // 2 - 2, 45 + cell_h + 12, str(i), color="#9CA3AF", font_size=9)

            # Draw prefix array
            canvas.draw_text(70, 130, "prefix:", color="#6B7280", font_size=11, anchor="rm")

            for i, val in enumerate(prefix):
                x = start_x + i * cell_w
                if i == current_idx + 1 and current_idx >= 0:
                    fill = "#86EFAC"  # Green - just computed
                elif i <= current_idx + 1:
                    fill = "#C7D2FE"  # Light purple - computed
                else:
                    fill = "#F3F4F6"

                canvas.draw_rounded_rect(x, 115, cell_w - 4, cell_h, radius=6, fill=fill, outline="#4F46E5")
                canvas.draw_text(x + cell_w // 2 - 2, 115 + cell_h // 2, str(val), color="#1F2937", font_size=13)

                # Index
                canvas.draw_text(x + cell_w // 2 - 2, 115 + cell_h + 12, str(i), color="#9CA3AF", font_size=9)

            # Formula
            canvas.draw_text(width // 2, 190, "Formula: sum(i,j) = prefix[j+1] - prefix[i]", color="#6B7280", font_size=11)

            # Show range sum if query
            if query_start >= 0:
                range_sum = state.get("range_sum", 0)
                canvas.draw_rounded_rect(width // 2 - 80, 210, 160, 35, radius=8, fill="#FEF3C7", outline="#F59E0B")
                canvas.draw_text(width // 2, 227, f"Range sum = {range_sum}", color="#92400E", font_size=14)

            # Caption
            if step.caption:
                canvas.draw_text(width // 2, height - 20, step.caption, color="#374151", font_size=11)

            if step.is_pause:
                animation.add_pause_frame(canvas.get_image(), step.duration_ms or 1500)
            else:
                animation.add_frame(canvas.get_image(), step.duration_ms)

        return animation
