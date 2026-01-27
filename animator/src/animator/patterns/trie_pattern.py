"""Trie pattern animations."""

from typing import Generator, List, Optional, Dict, Any

from .base import BasePattern, AnimationStep
from ..renderers.array_renderer import ArrayRenderer
from ..config import AnimationConfig, ColorScheme


class TriePattern(BasePattern):
    """
    Animates Trie insert and search operations.

    Shows:
    - Building trie structure
    - Character-by-character traversal
    - Word completion markers
    """

    @property
    def name(self) -> str:
        return "trie"

    @property
    def description(self) -> str:
        return "Trie insert and search"

    def __init__(
        self,
        config: Optional[AnimationConfig] = None,
        color_scheme: Optional[ColorScheme] = None,
    ):
        renderer = ArrayRenderer(color_scheme=color_scheme)
        super().__init__(renderer, config)

    def get_steps(
        self,
        words: List[str],
    ) -> Generator[AnimationStep, None, None]:
        yield from self._trie_steps(words)

    def _trie_steps(
        self, words: List[str]
    ) -> Generator[AnimationStep, None, None]:
        """Animate trie construction."""
        trie: Dict[str, Any] = {}

        yield AnimationStep(
            state={
                "trie": {},
                "words": words,
                "current_word": None,
                "current_char_idx": -1,
                "inserted_words": [],
            },
            caption="Trie: prefix tree for efficient string operations",
        )

        inserted_words = []

        for word in words:
            node = trie

            for i, char in enumerate(word):
                yield AnimationStep(
                    state={
                        "trie": self._copy_trie(trie),
                        "words": words,
                        "current_word": word,
                        "current_char_idx": i,
                        "current_char": char,
                        "path": word[:i+1],
                        "inserted_words": inserted_words[:],
                    },
                    caption=f"Insert '{word}': traverse/create '{char}'",
                )

                if char not in node:
                    node[char] = {}
                node = node[char]

            node["#"] = True  # Mark end of word
            inserted_words.append(word)

            yield AnimationStep(
                state={
                    "trie": self._copy_trie(trie),
                    "words": words,
                    "current_word": word,
                    "current_char_idx": len(word),
                    "path": word,
                    "inserted_words": inserted_words[:],
                    "word_complete": True,
                },
                caption=f"Mark '{word}' as complete word",
            )

        yield AnimationStep(
            state={
                "trie": self._copy_trie(trie),
                "words": words,
                "current_word": None,
                "inserted_words": inserted_words[:],
                "final": True,
            },
            caption=f"Trie built with {len(words)} words",
            is_pause=True,
            duration_ms=1500,
        )

    def _copy_trie(self, trie: dict) -> dict:
        """Deep copy trie structure."""
        result = {}
        for k, v in trie.items():
            if k == "#":
                result[k] = v
            else:
                result[k] = self._copy_trie(v)
        return result

    def create_animation(self, words: List[str], **kwargs):
        """Custom rendering for trie visualization."""
        from ..core.animation import Animation
        from ..core.canvas import Canvas

        animation = Animation(self.config)

        width = 500
        height = 350

        for step in self._trie_steps(words):
            canvas = Canvas(width, height, self.config.background_color)
            state = step.state

            trie = state.get("trie", {})
            current_word = state.get("current_word")
            current_char_idx = state.get("current_char_idx", -1)
            path = state.get("path", "")
            inserted_words = state.get("inserted_words", [])

            # Title
            canvas.draw_text(width // 2, 20, "Trie (Prefix Tree)", color="#374151", font_size=16)

            # Draw current word being processed
            if current_word:
                canvas.draw_text(width // 2, 50, f"Inserting: {current_word}", color="#059669", font_size=12)

                # Show characters
                char_start_x = (width - len(current_word) * 30) // 2
                for i, char in enumerate(current_word):
                    x = char_start_x + i * 30
                    if i < current_char_idx:
                        fill = "#D1D5DB"  # Gray - done
                    elif i == current_char_idx:
                        fill = "#86EFAC"  # Green - current
                    else:
                        fill = "#E5E7EB"  # Light - pending

                    canvas.draw_rounded_rect(x, 65, 26, 28, radius=4, fill=fill, outline="#6B7280")
                    canvas.draw_text(x + 13, 79, char, color="#1F2937", font_size=13)

            # Draw trie structure (simplified visual)
            self._draw_trie(canvas, trie, width // 2, 120, path, 0)

            # Show inserted words
            if inserted_words:
                words_str = ", ".join(inserted_words)
                canvas.draw_text(width // 2, height - 50, f"Words: {words_str}", color="#6B7280", font_size=10)

            # Caption
            if step.caption:
                canvas.draw_text(width // 2, height - 20, step.caption, color="#374151", font_size=11)

            if step.is_pause:
                animation.add_pause_frame(canvas.get_image(), step.duration_ms or 1500)
            else:
                animation.add_frame(canvas.get_image(), step.duration_ms)

        return animation

    def _draw_trie(self, canvas, node: dict, x: int, y: int, highlight_path: str, depth: int, path_so_far: str = ""):
        """Recursively draw trie nodes."""
        if depth > 4:  # Limit depth for visualization
            return

        children = [(k, v) for k, v in node.items() if k != "#"]
        if not children:
            return

        spacing = max(60 // (depth + 1), 20)
        total_width = len(children) * spacing
        start_x = x - total_width // 2

        for i, (char, child) in enumerate(children):
            child_x = start_x + i * spacing + spacing // 2
            child_y = y + 50

            # Draw edge
            canvas.draw_line(x, y + 10, child_x, child_y - 10, "#9CA3AF", 1)

            # Check if this node is on the highlight path
            current_path = path_so_far + char
            is_highlighted = highlight_path.startswith(current_path) and len(current_path) <= len(highlight_path)

            # Draw node
            fill = "#86EFAC" if is_highlighted else "#E5E7EB"
            outline = "#059669" if is_highlighted else "#6B7280"

            is_end = child.get("#", False)
            if is_end:
                fill = "#FDE68A" if not is_highlighted else "#86EFAC"
                outline = "#F59E0B" if not is_highlighted else "#059669"

            canvas.draw_circle(child_x, child_y, 12, fill=fill, outline=outline)
            canvas.draw_text(child_x, child_y, char, color="#1F2937", font_size=11)

            # Recurse
            self._draw_trie(canvas, child, child_x, child_y, highlight_path, depth + 1, current_path)
