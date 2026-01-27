"""Bitwise XOR pattern animations."""

from typing import Generator, List, Optional

from .base import BasePattern, AnimationStep
from ..renderers.array_renderer import ArrayRenderer
from ..config import AnimationConfig, ColorScheme


class XORPattern(BasePattern):
    """
    Animates XOR pattern for finding single number.

    Shows:
    - XOR operations step by step
    - Binary representation
    - Result accumulation
    """

    @property
    def name(self) -> str:
        return "xor_pattern"

    @property
    def description(self) -> str:
        return "XOR operations for finding unique element"

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
        yield from self._single_number_steps(data)

    def _single_number_steps(
        self, nums: List[int]
    ) -> Generator[AnimationStep, None, None]:
        """Animate XOR for single number problem."""
        result = 0

        yield AnimationStep(
            state={
                "nums": nums,
                "current_idx": -1,
                "result": result,
                "result_binary": bin(result)[2:].zfill(8),
            },
            caption="XOR all numbers: duplicates cancel (a^a=0)",
        )

        for i, num in enumerate(nums):
            yield AnimationStep(
                state={
                    "nums": nums,
                    "current_idx": i,
                    "current_num": num,
                    "current_binary": bin(num)[2:].zfill(8),
                    "result": result,
                    "result_binary": bin(result)[2:].zfill(8),
                    "operation": "before",
                },
                caption=f"Current: {num} (binary: {bin(num)[2:]})",
            )

            result ^= num

            yield AnimationStep(
                state={
                    "nums": nums,
                    "current_idx": i,
                    "current_num": num,
                    "result": result,
                    "result_binary": bin(result)[2:].zfill(8),
                    "operation": "after",
                },
                caption=f"Result XOR {num} = {result}",
            )

        yield AnimationStep(
            state={
                "nums": nums,
                "current_idx": -1,
                "result": result,
                "result_binary": bin(result)[2:].zfill(8),
                "final": True,
            },
            caption=f"Single number: {result}",
            is_pause=True,
            duration_ms=1500,
        )

    def create_animation(self, data: List[int], **kwargs):
        """Custom rendering for XOR visualization."""
        from ..core.animation import Animation
        from ..core.canvas import Canvas

        animation = Animation(self.config)

        width = 500
        height = 300
        cell_w, cell_h = 45, 35

        for step in self._single_number_steps(data):
            canvas = Canvas(width, height, self.config.background_color)
            state = step.state

            nums = state.get("nums", [])
            current_idx = state.get("current_idx", -1)
            result = state.get("result", 0)
            result_binary = state.get("result_binary", "00000000")

            # Title
            canvas.draw_text(width // 2, 20, "XOR Pattern - Single Number", color="#374151", font_size=16)

            # Draw array
            start_x = (width - len(nums) * cell_w) // 2
            y = 60

            for i, num in enumerate(nums):
                x = start_x + i * cell_w
                if i == current_idx:
                    fill = "#86EFAC"  # Green - current
                elif i < current_idx:
                    fill = "#D1D5DB"  # Gray - processed
                else:
                    fill = "#E5E7EB"  # Light - pending

                canvas.draw_rounded_rect(x, y, cell_w - 4, cell_h, radius=6, fill=fill, outline="#6B7280")
                canvas.draw_text(x + cell_w // 2 - 2, y + cell_h // 2, str(num), color="#1F2937", font_size=14)

            # Draw current number binary
            if current_idx >= 0:
                current_binary = state.get("current_binary", "")
                if current_binary:
                    canvas.draw_text(width // 2, 120, f"Current: {current_binary}", color="#059669", font_size=12)

            # Draw result
            canvas.draw_text(width // 2, 160, "Result (XOR accumulator):", color="#374151", font_size=12)

            # Result binary visualization
            bit_start_x = (width - 8 * 30) // 2
            for i, bit in enumerate(result_binary):
                x = bit_start_x + i * 30
                fill = "#FDE68A" if bit == "1" else "#F3F4F6"
                canvas.draw_rounded_rect(x, 180, 26, 30, radius=4, fill=fill, outline="#9CA3AF")
                canvas.draw_text(x + 13, 195, bit, color="#1F2937", font_size=14)

            # Result decimal
            canvas.draw_text(width // 2, 230, f"Decimal: {result}", color="#4F46E5", font_size=16)

            # Caption
            if step.caption:
                canvas.draw_text(width // 2, height - 25, step.caption, color="#374151", font_size=12)

            if step.is_pause:
                animation.add_pause_frame(canvas.get_image(), step.duration_ms or 1500)
            else:
                animation.add_frame(canvas.get_image(), step.duration_ms)

        return animation
