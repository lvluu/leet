"""Animation class for managing frames and GIF export."""

from PIL import Image
from pathlib import Path
from typing import List, Optional

from ..config import AnimationConfig


class Animation:
    """
    Manages a sequence of frames and exports to GIF.
    """

    def __init__(self, config: Optional[AnimationConfig] = None):
        self.config = config or AnimationConfig()
        self.frames: List[Image.Image] = []
        self.frame_durations: List[int] = []

    def add_frame(self, image: Image.Image, duration_ms: Optional[int] = None) -> None:
        """Add a frame with optional custom duration."""
        self.frames.append(image)
        self.frame_durations.append(duration_ms or self.config.frame_duration_ms)

    def add_pause_frame(self, image: Image.Image, pause_ms: int = 1000) -> None:
        """Add a frame that pauses longer (for emphasis)."""
        self.add_frame(image, pause_ms)

    def export_gif(self, output_path: Path | str) -> Path:
        """Export frames to animated GIF."""
        if not self.frames:
            raise ValueError("No frames to export")

        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Convert RGBA to P mode with palette for better GIF support
        frames_p = []
        for frame in self.frames:
            # Convert to palette mode for GIF
            frame_rgb = frame.convert("RGB")
            frames_p.append(frame_rgb)

        frames_p[0].save(
            output_path,
            save_all=True,
            append_images=frames_p[1:],
            duration=self.frame_durations,
            loop=self.config.loop_count,
            optimize=True,
        )
        return output_path

    def clear(self) -> None:
        """Clear all frames."""
        self.frames.clear()
        self.frame_durations.clear()

    def __len__(self) -> int:
        return len(self.frames)
