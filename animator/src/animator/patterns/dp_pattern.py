"""Dynamic Programming pattern animations (Knapsack, Fibonacci, etc.)."""

from typing import Generator, List, Optional, Tuple

from .base import BasePattern, AnimationStep
from ..renderers.array_renderer import ArrayRenderer
from ..config import AnimationConfig, ColorScheme


class KnapsackPattern(BasePattern):
    """
    Animates 0/1 Knapsack DP table filling.
    """

    @property
    def name(self) -> str:
        return "knapsack"

    @property
    def description(self) -> str:
        return "0/1 Knapsack DP"

    def __init__(
        self,
        config: Optional[AnimationConfig] = None,
        color_scheme: Optional[ColorScheme] = None,
    ):
        renderer = ArrayRenderer(color_scheme=color_scheme)
        super().__init__(renderer, config)

    def get_steps(
        self,
        weights: List[int],
        values: List[int],
        capacity: int,
    ) -> Generator[AnimationStep, None, None]:
        yield from self._knapsack_steps(weights, values, capacity)

    def _knapsack_steps(
        self, weights: List[int], values: List[int], capacity: int
    ) -> Generator[AnimationStep, None, None]:
        """Animate knapsack DP table construction."""
        n = len(weights)
        dp = [[0] * (capacity + 1) for _ in range(n + 1)]

        yield AnimationStep(
            state={
                "weights": weights,
                "values": values,
                "capacity": capacity,
                "dp": [row[:] for row in dp],
                "current_i": -1,
                "current_w": -1,
            },
            caption=f"0/1 Knapsack: {n} items, capacity {capacity}",
        )

        for i in range(1, n + 1):
            for w in range(capacity + 1):
                if weights[i-1] <= w:
                    dp[i][w] = max(
                        dp[i-1][w],
                        dp[i-1][w - weights[i-1]] + values[i-1]
                    )
                else:
                    dp[i][w] = dp[i-1][w]

                yield AnimationStep(
                    state={
                        "weights": weights,
                        "values": values,
                        "capacity": capacity,
                        "dp": [row[:] for row in dp],
                        "current_i": i,
                        "current_w": w,
                        "current_item_weight": weights[i-1],
                        "current_item_value": values[i-1],
                    },
                    caption=f"Item {i} (w={weights[i-1]}, v={values[i-1]}), capacity={w} → {dp[i][w]}",
                )

        yield AnimationStep(
            state={
                "weights": weights,
                "values": values,
                "capacity": capacity,
                "dp": [row[:] for row in dp],
                "current_i": -1,
                "current_w": -1,
                "final": True,
                "max_value": dp[n][capacity],
            },
            caption=f"Maximum value: {dp[n][capacity]}",
            is_pause=True,
            duration_ms=1500,
        )

    def create_animation(self, weights: List[int], values: List[int], capacity: int, **kwargs):
        """Custom rendering for knapsack DP table."""
        from ..core.animation import Animation
        from ..core.canvas import Canvas

        animation = Animation(self.config)

        width = 500
        height = 350
        cell_size = 32

        for step in self._knapsack_steps(weights, values, capacity):
            canvas = Canvas(width, height, self.config.background_color)
            state = step.state

            dp = state.get("dp", [])
            current_i = state.get("current_i", -1)
            current_w = state.get("current_w", -1)
            wts = state.get("weights", [])
            vals = state.get("values", [])

            # Title
            canvas.draw_text(width // 2, 20, "0/1 Knapsack DP Table", color="#374151", font_size=16)

            # Items info
            items_str = ", ".join(f"({w},{v})" for w, v in zip(wts, vals))
            canvas.draw_text(width // 2, 45, f"Items (w,v): {items_str}", color="#6B7280", font_size=10)

            # Draw DP table (limited view for space)
            n = len(dp)
            cap = len(dp[0]) if dp else 0

            # Limit display size
            max_display_cols = min(cap, 8)
            max_display_rows = min(n, 5)

            table_start_x = (width - (max_display_cols + 1) * cell_size) // 2
            table_start_y = 70

            # Column headers (capacity)
            for w in range(max_display_cols):
                x = table_start_x + (w + 1) * cell_size
                canvas.draw_text(x + cell_size // 2, table_start_y + cell_size // 2, str(w), color="#6B7280", font_size=10)

            # Row headers and cells
            for i in range(max_display_rows):
                y = table_start_y + (i + 1) * cell_size

                # Row header
                label = "0" if i == 0 else f"i{i}"
                canvas.draw_text(table_start_x + cell_size // 2, y + cell_size // 2, label, color="#6B7280", font_size=10)

                # Cells
                for w in range(max_display_cols):
                    x = table_start_x + (w + 1) * cell_size

                    fill = "#E5E7EB"
                    if i == current_i and w == current_w:
                        fill = "#86EFAC"  # Current cell
                    elif i < current_i or (i == current_i and w < current_w):
                        fill = "#C7D2FE"  # Computed

                    canvas.draw_rounded_rect(x, y, cell_size - 2, cell_size - 2, radius=3, fill=fill, outline="#9CA3AF")

                    if i < len(dp) and w < len(dp[i]):
                        canvas.draw_text(x + cell_size // 2 - 1, y + cell_size // 2 - 1, str(dp[i][w]), color="#1F2937", font_size=10)

            # Formula
            canvas.draw_text(width // 2, height - 60, "dp[i][w] = max(skip, take if fits)", color="#6B7280", font_size=10)

            # Caption
            if step.caption:
                canvas.draw_text(width // 2, height - 25, step.caption, color="#374151", font_size=11)

            if step.is_pause:
                animation.add_pause_frame(canvas.get_image(), step.duration_ms or 1500)
            else:
                animation.add_frame(canvas.get_image(), step.duration_ms)

        return animation


class FibonacciPattern(BasePattern):
    """
    Animates Fibonacci with memoization.
    """

    @property
    def name(self) -> str:
        return "fibonacci"

    @property
    def description(self) -> str:
        return "Fibonacci DP"

    def __init__(
        self,
        config: Optional[AnimationConfig] = None,
        color_scheme: Optional[ColorScheme] = None,
    ):
        renderer = ArrayRenderer(color_scheme=color_scheme)
        super().__init__(renderer, config)

    def get_steps(
        self,
        n: int,
    ) -> Generator[AnimationStep, None, None]:
        yield from self._fib_steps(n)

    def _fib_steps(self, n: int) -> Generator[AnimationStep, None, None]:
        """Animate fibonacci with tabulation."""
        dp = [0] * (n + 1)
        if n >= 1:
            dp[1] = 1

        yield AnimationStep(
            state={
                "n": n,
                "dp": dp[:],
                "current": -1,
            },
            caption=f"Fibonacci({n}) using tabulation",
        )

        for i in range(2, n + 1):
            dp[i] = dp[i-1] + dp[i-2]

            yield AnimationStep(
                state={
                    "n": n,
                    "dp": dp[:],
                    "current": i,
                    "prev1": i - 1,
                    "prev2": i - 2,
                },
                caption=f"dp[{i}] = dp[{i-1}] + dp[{i-2}] = {dp[i-1]} + {dp[i-2]} = {dp[i]}",
            )

        yield AnimationStep(
            state={
                "n": n,
                "dp": dp[:],
                "current": -1,
                "final": True,
            },
            caption=f"Fibonacci({n}) = {dp[n]}",
            is_pause=True,
            duration_ms=1500,
        )

    def create_animation(self, n: int, **kwargs):
        """Custom rendering for fibonacci."""
        from ..core.animation import Animation
        from ..core.canvas import Canvas

        animation = Animation(self.config)

        width = 500
        height = 250
        cell_w = 45

        for step in self._fib_steps(n):
            canvas = Canvas(width, height, self.config.background_color)
            state = step.state

            dp = state.get("dp", [])
            current = state.get("current", -1)
            prev1 = state.get("prev1", -1)
            prev2 = state.get("prev2", -1)

            # Title
            canvas.draw_text(width // 2, 25, "Fibonacci DP (Tabulation)", color="#374151", font_size=16)

            # Formula
            canvas.draw_text(width // 2, 55, "dp[i] = dp[i-1] + dp[i-2]", color="#6B7280", font_size=11)

            # Draw DP array (limited)
            display_count = min(len(dp), 10)
            start_x = (width - display_count * cell_w) // 2
            y = 85

            for i in range(display_count):
                x = start_x + i * cell_w

                if i == current:
                    fill = "#86EFAC"  # Green - current
                elif i == prev1 or i == prev2:
                    fill = "#FDE68A"  # Yellow - being used
                elif i < current or (current == -1 and state.get("final")):
                    fill = "#C7D2FE"  # Purple - computed
                else:
                    fill = "#E5E7EB"

                canvas.draw_rounded_rect(x, y, cell_w - 4, 35, radius=6, fill=fill, outline="#6B7280")
                canvas.draw_text(x + cell_w // 2 - 2, y + 17, str(dp[i]), color="#1F2937", font_size=13)

                # Index
                canvas.draw_text(x + cell_w // 2 - 2, y + 48, str(i), color="#9CA3AF", font_size=9)

            # Show computation arrows
            if current >= 2:
                # Arrows from prev1 and prev2 to current
                curr_x = start_x + current * cell_w + cell_w // 2
                prev1_x = start_x + prev1 * cell_w + cell_w // 2
                prev2_x = start_x + prev2 * cell_w + cell_w // 2

                canvas.draw_text(width // 2, 160, f"{dp[prev2]} + {dp[prev1]} = {dp[current]}", color="#059669", font_size=14)

            # Caption
            if step.caption:
                canvas.draw_text(width // 2, height - 25, step.caption, color="#374151", font_size=11)

            if step.is_pause:
                animation.add_pause_frame(canvas.get_image(), step.duration_ms or 1500)
            else:
                animation.add_frame(canvas.get_image(), step.duration_ms)

        return animation
