"""Backtracking pattern animations."""

from typing import Generator, List, Optional

from .base import BasePattern, AnimationStep
from ..renderers.array_renderer import ArrayRenderer
from ..config import AnimationConfig, ColorScheme


class BacktrackingPattern(BasePattern):
    """
    Animates Backtracking pattern for generating permutations/combinations.

    Shows:
    - Decision tree exploration
    - Backtracking (undoing choices)
    - Building solutions
    """

    @property
    def name(self) -> str:
        return "backtracking"

    @property
    def description(self) -> str:
        return "Backtracking for permutations"

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
        yield from self._permutation_steps(data)

    def _permutation_steps(
        self, nums: List[int]
    ) -> Generator[AnimationStep, None, None]:
        """Animate permutation generation with backtracking."""
        results = []
        path = []
        used = [False] * len(nums)

        yield AnimationStep(
            state={
                "nums": nums,
                "path": [],
                "used": used[:],
                "results": [],
                "action": "start",
            },
            caption="Generate permutations using backtracking",
        )

        def backtrack():
            if len(path) == len(nums):
                results.append(path[:])
                yield AnimationStep(
                    state={
                        "nums": nums,
                        "path": path[:],
                        "used": used[:],
                        "results": [r[:] for r in results],
                        "action": "found",
                    },
                    caption=f"Found permutation: {path}",
                )
                return

            for i in range(len(nums)):
                if used[i]:
                    continue

                # Make choice
                path.append(nums[i])
                used[i] = True

                yield AnimationStep(
                    state={
                        "nums": nums,
                        "path": path[:],
                        "used": used[:],
                        "results": [r[:] for r in results],
                        "action": "choose",
                        "chosen_idx": i,
                    },
                    caption=f"Choose {nums[i]} → path: {path}",
                )

                # Recurse
                yield from backtrack()

                # Backtrack
                removed = path.pop()
                used[i] = False

                yield AnimationStep(
                    state={
                        "nums": nums,
                        "path": path[:],
                        "used": used[:],
                        "results": [r[:] for r in results],
                        "action": "backtrack",
                        "removed": removed,
                    },
                    caption=f"Backtrack: remove {removed} → path: {path}",
                )

        yield from backtrack()

        yield AnimationStep(
            state={
                "nums": nums,
                "path": [],
                "used": [False] * len(nums),
                "results": [r[:] for r in results],
                "action": "complete",
                "final": True,
            },
            caption=f"All {len(results)} permutations found",
            is_pause=True,
            duration_ms=1500,
        )

    def create_animation(self, data: List[int], **kwargs):
        """Custom rendering for backtracking visualization."""
        from ..core.animation import Animation
        from ..core.canvas import Canvas

        animation = Animation(self.config)

        width = 500
        height = 350
        cell_w = 40

        for step in self._permutation_steps(data):
            canvas = Canvas(width, height, self.config.background_color)
            state = step.state

            nums = state.get("nums", [])
            path = state.get("path", [])
            used = state.get("used", [])
            results = state.get("results", [])
            action = state.get("action", "")

            # Title
            canvas.draw_text(width // 2, 20, "Backtracking Pattern", color="#374151", font_size=16)

            # Draw available numbers
            canvas.draw_text(width // 2, 50, "Available:", color="#6B7280", font_size=11)
            start_x = (width - len(nums) * cell_w) // 2

            for i, num in enumerate(nums):
                x = start_x + i * cell_w
                if used[i]:
                    fill = "#D1D5DB"  # Gray - used
                else:
                    fill = "#86EFAC"  # Green - available

                canvas.draw_rounded_rect(x, 65, cell_w - 4, 32, radius=6, fill=fill, outline="#6B7280")
                canvas.draw_text(x + cell_w // 2 - 2, 81, str(num), color="#1F2937", font_size=13)

            # Draw current path
            canvas.draw_text(width // 2, 115, "Current Path:", color="#6B7280", font_size=11)

            if path:
                path_start_x = (width - len(path) * cell_w) // 2
                for i, num in enumerate(path):
                    x = path_start_x + i * cell_w
                    fill = "#C7D2FE"  # Light purple
                    if action == "backtrack" and i == len(path) - 1:
                        fill = "#FECACA"  # Red - being removed

                    canvas.draw_rounded_rect(x, 130, cell_w - 4, 32, radius=6, fill=fill, outline="#4F46E5")
                    canvas.draw_text(x + cell_w // 2 - 2, 146, str(num), color="#1F2937", font_size=13)

                # Draw arrows between path elements
                for i in range(len(path) - 1):
                    x1 = path_start_x + i * cell_w + cell_w - 4
                    x2 = path_start_x + (i + 1) * cell_w
                    canvas.draw_text((x1 + x2) // 2, 146, "→", color="#9CA3AF", font_size=12)
            else:
                canvas.draw_text(width // 2, 146, "(empty)", color="#9CA3AF", font_size=11)

            # Draw action indicator
            action_colors = {
                "choose": "#059669",
                "backtrack": "#DC2626",
                "found": "#7C3AED",
            }
            if action in action_colors:
                canvas.draw_text(width // 2, 180, action.upper(), color=action_colors[action], font_size=12)

            # Draw found permutations
            canvas.draw_text(width // 2, 210, f"Found ({len(results)}):", color="#6B7280", font_size=11)

            if results:
                # Show last few results
                display_results = results[-4:] if len(results) > 4 else results
                results_str = "  ".join(str(r) for r in display_results)
                if len(results) > 4:
                    results_str = "... " + results_str
                canvas.draw_text(width // 2, 235, results_str, color="#4F46E5", font_size=11)

            # Caption
            if step.caption:
                canvas.draw_text(width // 2, height - 20, step.caption, color="#374151", font_size=11)

            if step.is_pause:
                animation.add_pause_frame(canvas.get_image(), step.duration_ms or 1500)
            else:
                animation.add_frame(canvas.get_image(), step.duration_ms)

        return animation
