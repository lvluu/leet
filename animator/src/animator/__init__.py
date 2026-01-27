"""DSA Animation Generator for GitBook."""

from .config import AnimationConfig, ColorScheme
from .core import Animation, Canvas
from .patterns import BasePattern, AnimationStep, SlidingWindowPattern
from .renderers import BaseRenderer, ArrayRenderer
from .cli import main

__all__ = [
    "AnimationConfig",
    "ColorScheme",
    "Animation",
    "Canvas",
    "BasePattern",
    "AnimationStep",
    "SlidingWindowPattern",
    "BaseRenderer",
    "ArrayRenderer",
    "main",
]
