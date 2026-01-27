"""Configuration and color scheme for animations."""

from dataclasses import dataclass


@dataclass
class AnimationConfig:
    """Global configuration for animation generation."""

    # Canvas settings
    width: int = 800
    height: int = 400
    background_color: str = "#FFFFFF"
    padding: int = 40

    # Animation timing
    frame_duration_ms: int = 500  # Default frame duration
    loop_count: int = 0  # 0 = infinite loop

    # Typography
    font_size: int = 16
    title_font_size: int = 20

    # Output
    output_dir: str = "docs/.gitbook/assets/animations"


@dataclass
class ColorScheme:
    """Color palette for consistent visualization."""

    # Base colors
    background: str = "#FFFFFF"
    text: str = "#1F2937"
    border: str = "#374151"

    # Array/data element colors
    default: str = "#E5E7EB"  # Gray - unprocessed
    current: str = "#3B82F6"  # Blue - current element
    visited: str = "#10B981"  # Green - processed/visited
    highlight: str = "#F59E0B"  # Amber - special highlight
    window: str = "#DBEAFE"  # Light blue - window background

    # Pointer colors
    pointer_left: str = "#EF4444"  # Red
    pointer_right: str = "#8B5CF6"  # Purple
    pointer_slow: str = "#06B6D4"  # Cyan
    pointer_fast: str = "#F97316"  # Orange

    # Graph/tree specific
    node_default: str = "#F3F4F6"
    node_visited: str = "#BBF7D0"
    node_frontier: str = "#FDE68A"
    edge_default: str = "#9CA3AF"
    edge_active: str = "#3B82F6"
