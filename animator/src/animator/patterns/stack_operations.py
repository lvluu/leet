"""Stack operations pattern animations."""

from typing import Any, Generator, List, Optional

from .base import BasePattern, AnimationStep
from ..renderers.array_renderer import ArrayRenderer
from ..config import AnimationConfig, ColorScheme


class StackOperationsPattern(BasePattern):
    """
    Animates basic stack operations (push/pop).

    Shows stack as a vertical structure with operations.
    """

    @property
    def name(self) -> str:
        return "stack_operations"

    @property
    def description(self) -> str:
        return "Stack push/pop operations (LIFO)"

    def __init__(
        self,
        config: Optional[AnimationConfig] = None,
        color_scheme: Optional[ColorScheme] = None,
    ):
        # Use array renderer but we'll customize the visualization
        renderer = ArrayRenderer(color_scheme=color_scheme)
        super().__init__(renderer, config)

    def get_steps(
        self,
        data: List[Any],
        operations: Optional[List[tuple]] = None,
    ) -> Generator[AnimationStep, None, None]:
        """
        Generate stack operation animation steps.

        Args:
            data: Initial values to push (or empty)
            operations: List of ("push", val) or ("pop",) tuples
        """
        if operations is None:
            # Default: push all data then pop all
            operations = [("push", x) for x in data] + [("pop",) for _ in data]

        yield from self._stack_operations(operations)

    def _stack_operations(
        self, operations: List[tuple]
    ) -> Generator[AnimationStep, None, None]:
        """Animate a sequence of stack operations."""
        stack: List[Any] = []

        yield AnimationStep(
            state={
                "highlights": {},
                "pointers": [],
            },
            caption="Stack: Last In, First Out (LIFO)",
        )

        for op in operations:
            if op[0] == "push":
                val = op[1]
                stack.append(val)

                # Show the push operation
                highlights = {i: "#E5E7EB" for i in range(len(stack) - 1)}
                highlights[len(stack) - 1] = "#86EFAC"  # Green for new element

                yield AnimationStep(
                    state={
                        "highlights": highlights,
                        "pointers": [
                            {"index": len(stack) - 1, "label": "top", "color": "#10B981", "position": "above"},
                        ],
                    },
                    caption=f"Push({val}) → stack = {stack}",
                )

            elif op[0] == "pop":
                if not stack:
                    yield AnimationStep(
                        state={"highlights": {}},
                        caption="Pop() → Stack is empty!",
                    )
                    continue

                val = stack[-1]

                # Show element about to be popped
                highlights = {i: "#E5E7EB" for i in range(len(stack) - 1)}
                highlights[len(stack) - 1] = "#FCA5A5"  # Red for element being removed

                yield AnimationStep(
                    state={
                        "highlights": highlights,
                        "pointers": [
                            {"index": len(stack) - 1, "label": "pop", "color": "#EF4444", "position": "above"},
                        ],
                    },
                    caption=f"Pop() → removing {val}",
                )

                stack.pop()

                # Show state after pop
                if stack:
                    highlights = {i: "#E5E7EB" for i in range(len(stack))}
                    highlights[len(stack) - 1] = "#3B82F6"  # Blue for new top
                    yield AnimationStep(
                        state={
                            "highlights": highlights,
                            "pointers": [
                                {"index": len(stack) - 1, "label": "top", "color": "#3B82F6", "position": "above"},
                            ],
                        },
                        caption=f"After pop: stack = {stack}",
                    )
                else:
                    yield AnimationStep(
                        state={"highlights": {}},
                        caption="Stack is now empty",
                    )

        yield AnimationStep(
            state={
                "highlights": {i: "#10B981" for i in range(len(stack))},
                "pointers": [{"index": len(stack) - 1, "label": "top", "color": "#10B981", "position": "above"}] if stack else [],
            },
            caption=f"Final stack: {stack}" if stack else "Stack empty",
            is_pause=True,
            duration_ms=1500,
        )

    def create_animation(self, data: List[Any], **kwargs):
        """Override to show stack vertically."""
        from ..core.animation import Animation
        from ..core.canvas import Canvas

        operations = kwargs.get("operations")
        if operations is None:
            operations = [("push", x) for x in data] + [("pop",) for _ in data]

        animation = Animation(self.config)

        # Calculate max stack size for canvas
        max_size = 0
        current = 0
        for op in operations:
            if op[0] == "push":
                current += 1
                max_size = max(max_size, current)
            elif op[0] == "pop" and current > 0:
                current -= 1

        cell_w, cell_h = 60, 40
        width = 300
        height = max(max_size * cell_h + 150, 250)

        stack: List[Any] = []

        for step in self._stack_operations(operations):
            canvas = Canvas(width, height, self.config.background_color)

            # Parse current stack from caption
            if "stack = [" in step.caption:
                import re
                match = re.search(r'stack = \[(.*?)\]', step.caption)
                if match:
                    content = match.group(1)
                    if content:
                        stack = [int(x.strip()) for x in content.split(',')]
                    else:
                        stack = []
            elif "Stack is now empty" in step.caption or "Stack empty" in step.caption:
                stack = []

            # Draw stack title
            canvas.draw_text(width // 2, 25, "Stack (LIFO)", color="#374151", font_size=16)

            # Draw stack container
            base_x = (width - cell_w) // 2
            base_y = height - 80

            # Draw base line
            canvas.draw_line(base_x - 10, base_y + 5, base_x + cell_w + 10, base_y + 5, "#374151", 3)

            # Draw stack elements from bottom to top
            highlights = step.state.get("highlights", {})
            for i, val in enumerate(stack):
                y = base_y - (i + 1) * cell_h

                fill = highlights.get(i, "#E5E7EB")
                canvas.draw_rounded_rect(base_x, y, cell_w, cell_h - 4, radius=6, fill=fill, outline="#374151")
                canvas.draw_text(base_x + cell_w // 2, y + cell_h // 2 - 2, str(val), color="#1F2937", font_size=16)

            # Draw top pointer
            if stack:
                pointers = step.state.get("pointers", [])
                for ptr in pointers:
                    idx = ptr.get("index", len(stack) - 1)
                    if 0 <= idx < len(stack):
                        y = base_y - (idx + 1) * cell_h + cell_h // 2
                        color = ptr.get("color", "#3B82F6")
                        label = ptr.get("label", "")
                        canvas.draw_text(base_x + cell_w + 30, y, f"← {label}", color=color, font_size=12, anchor="lm")

            # Draw caption
            if step.caption:
                canvas.draw_text(width // 2, height - 30, step.caption, color="#374151", font_size=12)

            if step.is_pause:
                animation.add_pause_frame(canvas.get_image(), step.duration_ms or 1500)
            else:
                animation.add_frame(canvas.get_image(), step.duration_ms)

        return animation
