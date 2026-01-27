"""Scenario registry for pre-configured animations."""

import json
from dataclasses import dataclass
from typing import Callable, Dict, Iterator, Optional, Tuple

from ..core.animation import Animation
from ..config import AnimationConfig


@dataclass
class Scenario:
    """A pre-configured animation scenario."""

    name: str
    pattern: str
    description: str
    factory: Callable[[AnimationConfig, Optional[str]], Animation]


class ScenarioRegistry:
    """Registry for discovering and accessing animation scenarios."""

    _scenarios: Dict[str, Scenario] = {}

    @classmethod
    def register(cls, name: str, pattern: str, description: str = ""):
        """Decorator to register a scenario factory."""

        def decorator(func: Callable):
            cls._scenarios[name] = Scenario(
                name=name,
                pattern=pattern,
                description=description,
                factory=func,
            )
            return func

        return decorator

    @classmethod
    def get(cls, name: str) -> Optional[Scenario]:
        return cls._scenarios.get(name)

    @classmethod
    def all(cls) -> Iterator[Tuple[str, Scenario]]:
        yield from cls._scenarios.items()


# === Registered Scenarios ===


@ScenarioRegistry.register(
    "sliding_window_fixed",
    "sliding-window",
    "Fixed-size window sliding across array",
)
def sliding_window_fixed_scenario(
    config: AnimationConfig, data: Optional[str] = None
) -> Animation:
    from ..patterns.sliding_window import SlidingWindowPattern

    arr = [2, 1, 5, 1, 3, 2] if not data else json.loads(data)
    pattern = SlidingWindowPattern(config=config)
    return pattern.create_animation(arr, window_size=3, algorithm="fixed")


@ScenarioRegistry.register(
    "sliding_window_dynamic",
    "sliding-window",
    "Dynamic window that expands and contracts",
)
def sliding_window_dynamic_scenario(
    config: AnimationConfig, data: Optional[str] = None
) -> Animation:
    from ..patterns.sliding_window import SlidingWindowPattern

    arr = [1, 3, 2, 6, -1, 4, 1, 8, 2] if not data else json.loads(data)
    pattern = SlidingWindowPattern(config=config)
    return pattern.create_animation(arr, algorithm="dynamic")


@ScenarioRegistry.register(
    "sliding_window_max_sum",
    "sliding-window",
    "Find max sum subarray of size k",
)
def sliding_window_max_sum_scenario(
    config: AnimationConfig, data: Optional[str] = None
) -> Animation:
    from ..patterns.sliding_window import SlidingWindowPattern

    arr = [2, 3, 4, 1, 5] if not data else json.loads(data)
    pattern = SlidingWindowPattern(config=config)
    return pattern.create_animation(arr, window_size=2, algorithm="fixed")


# === Two Pointers Scenarios ===


@ScenarioRegistry.register(
    "two_pointers_opposite",
    "two-pointers",
    "Two pointers converging from ends (pair sum)",
)
def two_pointers_opposite_scenario(
    config: AnimationConfig, data: Optional[str] = None
) -> Animation:
    from ..patterns.two_pointers import TwoPointersPattern

    arr = [1, 2, 3, 4, 6] if not data else json.loads(data)
    pattern = TwoPointersPattern(config=config)
    return pattern.create_animation(arr, variant="opposite", target=6)


@ScenarioRegistry.register(
    "two_pointers_same",
    "two-pointers",
    "Same direction pointers (remove duplicates)",
)
def two_pointers_same_scenario(
    config: AnimationConfig, data: Optional[str] = None
) -> Animation:
    from ..patterns.two_pointers import TwoPointersPattern

    arr = [1, 1, 2, 2, 3, 4, 4, 5] if not data else json.loads(data)
    pattern = TwoPointersPattern(config=config)
    return pattern.create_animation(arr, variant="same")


@ScenarioRegistry.register(
    "two_pointers_fast_slow",
    "two-pointers",
    "Fast and slow pointers (find middle)",
)
def two_pointers_fast_slow_scenario(
    config: AnimationConfig, data: Optional[str] = None
) -> Animation:
    from ..patterns.two_pointers import TwoPointersPattern

    arr = [1, 2, 3, 4, 5, 6, 7] if not data else json.loads(data)
    pattern = TwoPointersPattern(config=config)
    return pattern.create_animation(arr, variant="fast_slow")


# === Binary Search Scenarios ===


@ScenarioRegistry.register(
    "binary_search_classic",
    "modified-binary-search",
    "Classic binary search in sorted array",
)
def binary_search_classic_scenario(
    config: AnimationConfig, data: Optional[str] = None
) -> Animation:
    from ..patterns.binary_search import BinarySearchPattern

    arr = [1, 3, 5, 7, 9, 11, 13, 15] if not data else json.loads(data)
    pattern = BinarySearchPattern(config=config)
    return pattern.create_animation(arr, target=9, variant="classic")


@ScenarioRegistry.register(
    "binary_search_first",
    "modified-binary-search",
    "Find first occurrence of target",
)
def binary_search_first_scenario(
    config: AnimationConfig, data: Optional[str] = None
) -> Animation:
    from ..patterns.binary_search import BinarySearchPattern

    arr = [1, 2, 2, 2, 3, 4, 5] if not data else json.loads(data)
    pattern = BinarySearchPattern(config=config)
    return pattern.create_animation(arr, target=2, variant="first_occurrence")


@ScenarioRegistry.register(
    "binary_search_rotated",
    "modified-binary-search",
    "Search in rotated sorted array",
)
def binary_search_rotated_scenario(
    config: AnimationConfig, data: Optional[str] = None
) -> Animation:
    from ..patterns.binary_search import BinarySearchPattern

    arr = [4, 5, 6, 7, 0, 1, 2] if not data else json.loads(data)
    pattern = BinarySearchPattern(config=config)
    return pattern.create_animation(arr, target=0, variant="rotated")


# === Tree Traversal Scenarios ===


@ScenarioRegistry.register(
    "tree_level_order",
    "tree-breadth-first-search",
    "Level order (BFS) tree traversal",
)
def tree_level_order_scenario(
    config: AnimationConfig, data: Optional[str] = None
) -> Animation:
    from ..patterns.tree_traversal import TreeTraversalPattern, build_tree

    tree = build_tree([1, 2, 3, 4, 5, 6, 7])
    pattern = TreeTraversalPattern(config=config)
    return pattern.create_animation(tree, variant="level_order")


@ScenarioRegistry.register(
    "tree_preorder",
    "tree-depth-first-search",
    "Pre-order DFS tree traversal",
)
def tree_preorder_scenario(
    config: AnimationConfig, data: Optional[str] = None
) -> Animation:
    from ..patterns.tree_traversal import TreeTraversalPattern, build_tree

    tree = build_tree([1, 2, 3, 4, 5, 6, 7])
    pattern = TreeTraversalPattern(config=config)
    return pattern.create_animation(tree, variant="preorder")


@ScenarioRegistry.register(
    "tree_inorder",
    "tree-depth-first-search",
    "In-order DFS tree traversal",
)
def tree_inorder_scenario(
    config: AnimationConfig, data: Optional[str] = None
) -> Animation:
    from ..patterns.tree_traversal import TreeTraversalPattern, build_tree

    tree = build_tree([1, 2, 3, 4, 5, 6, 7])
    pattern = TreeTraversalPattern(config=config)
    return pattern.create_animation(tree, variant="inorder")


@ScenarioRegistry.register(
    "tree_postorder",
    "tree-depth-first-search",
    "Post-order DFS tree traversal",
)
def tree_postorder_scenario(
    config: AnimationConfig, data: Optional[str] = None
) -> Animation:
    from ..patterns.tree_traversal import TreeTraversalPattern, build_tree

    tree = build_tree([1, 2, 3, 4, 5, 6, 7])
    pattern = TreeTraversalPattern(config=config)
    return pattern.create_animation(tree, variant="postorder")


# === Graph Traversal Scenarios ===


@ScenarioRegistry.register(
    "graph_bfs",
    "graphs",
    "BFS traversal on undirected graph",
)
def graph_bfs_scenario(
    config: AnimationConfig, data: Optional[str] = None
) -> Animation:
    from ..patterns.graph_traversal import GraphTraversalPattern

    graph = {
        0: [1, 2],
        1: [0, 3, 4],
        2: [0, 5],
        3: [1],
        4: [1, 5],
        5: [2, 4],
    }
    pattern = GraphTraversalPattern(config=config)
    return pattern.create_animation(graph, start=0, variant="bfs")


@ScenarioRegistry.register(
    "graph_dfs",
    "graphs",
    "DFS traversal on undirected graph",
)
def graph_dfs_scenario(
    config: AnimationConfig, data: Optional[str] = None
) -> Animation:
    from ..patterns.graph_traversal import GraphTraversalPattern

    graph = {
        0: [1, 2],
        1: [0, 3, 4],
        2: [0, 5],
        3: [1],
        4: [1, 5],
        5: [2, 4],
    }
    pattern = GraphTraversalPattern(config=config)
    return pattern.create_animation(graph, start=0, variant="dfs")


# === Island/Matrix Traversal Scenarios ===


@ScenarioRegistry.register(
    "island_count_bfs",
    "island",
    "Count islands using BFS",
)
def island_count_bfs_scenario(
    config: AnimationConfig, data: Optional[str] = None
) -> Animation:
    from ..patterns.island_traversal import IslandTraversalPattern

    grid = [
        [1, 1, 0, 0, 0],
        [1, 1, 0, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 0, 1, 1],
    ]
    pattern = IslandTraversalPattern(config=config)
    return pattern.create_animation(grid, variant="count_bfs")


@ScenarioRegistry.register(
    "island_count_dfs",
    "island",
    "Count islands using DFS",
)
def island_count_dfs_scenario(
    config: AnimationConfig, data: Optional[str] = None
) -> Animation:
    from ..patterns.island_traversal import IslandTraversalPattern

    grid = [
        [1, 1, 0, 0, 0],
        [1, 1, 0, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 0, 1, 1],
    ]
    pattern = IslandTraversalPattern(config=config)
    return pattern.create_animation(grid, variant="count_dfs")


@ScenarioRegistry.register(
    "island_flood_fill",
    "island",
    "Flood fill algorithm",
)
def island_flood_fill_scenario(
    config: AnimationConfig, data: Optional[str] = None
) -> Animation:
    from ..patterns.island_traversal import IslandTraversalPattern

    grid = [
        [1, 1, 1, 0, 0],
        [1, 0, 1, 0, 0],
        [1, 1, 1, 0, 0],
        [0, 0, 0, 0, 0],
    ]
    pattern = IslandTraversalPattern(config=config)
    return pattern.create_animation(grid, variant="flood_fill")


# === Monotonic Stack Scenarios ===


@ScenarioRegistry.register(
    "monotonic_next_greater",
    "monotonic-stack",
    "Next greater element using monotonic stack",
)
def monotonic_next_greater_scenario(
    config: AnimationConfig, data: Optional[str] = None
) -> Animation:
    from ..patterns.monotonic_stack import MonotonicStackPattern

    arr = [4, 5, 2, 10, 8] if not data else json.loads(data)
    pattern = MonotonicStackPattern(config=config)
    return pattern.create_animation(arr, variant="next_greater")


@ScenarioRegistry.register(
    "monotonic_next_smaller",
    "monotonic-stack",
    "Next smaller element using monotonic stack",
)
def monotonic_next_smaller_scenario(
    config: AnimationConfig, data: Optional[str] = None
) -> Animation:
    from ..patterns.monotonic_stack import MonotonicStackPattern

    arr = [4, 5, 2, 10, 8] if not data else json.loads(data)
    pattern = MonotonicStackPattern(config=config)
    return pattern.create_animation(arr, variant="next_smaller")


# === Stack Operations Scenarios ===


@ScenarioRegistry.register(
    "stack_push_pop",
    "stack",
    "Stack push and pop operations (LIFO)",
)
def stack_push_pop_scenario(
    config: AnimationConfig, data: Optional[str] = None
) -> Animation:
    from ..patterns.stack_operations import StackOperationsPattern

    values = [3, 7, 1, 9, 4] if not data else json.loads(data)
    operations = [("push", x) for x in values] + [("pop",) for _ in range(3)]
    pattern = StackOperationsPattern(config=config)
    return pattern.create_animation(values, operations=operations)


# === Two Heaps Scenarios ===


@ScenarioRegistry.register(
    "two_heaps_median",
    "two-heaps",
    "Running median using two heaps",
)
def two_heaps_median_scenario(
    config: AnimationConfig, data: Optional[str] = None
) -> Animation:
    from ..patterns.two_heaps import TwoHeapsPattern

    nums = [3, 1, 5, 4, 2] if not data else json.loads(data)
    pattern = TwoHeapsPattern(config=config)
    return pattern.create_animation(nums)
