"""Island/matrix traversal pattern animations."""

from collections import deque
from typing import Any, Generator, List, Optional, Set, Tuple

from .base import BasePattern, AnimationStep
from ..renderers.matrix_renderer import MatrixRenderer
from ..config import AnimationConfig, ColorScheme


class IslandTraversalPattern(BasePattern):
    """
    Animates matrix traversal algorithms for island problems.

    Variants:
    - Number of islands (BFS)
    - Number of islands (DFS)
    - Flood fill
    """

    @property
    def name(self) -> str:
        return "island_traversal"

    @property
    def description(self) -> str:
        return "Island/matrix traversal patterns"

    def __init__(
        self,
        config: Optional[AnimationConfig] = None,
        color_scheme: Optional[ColorScheme] = None,
    ):
        renderer = MatrixRenderer(color_scheme=color_scheme)
        super().__init__(renderer, config)

    def get_steps(
        self,
        data: List[List[int]],
        variant: str = "count_bfs",
    ) -> Generator[AnimationStep, None, None]:
        """
        Generate island traversal animation steps.

        Args:
            data: 2D grid (1 = land, 0 = water)
            variant: "count_bfs", "count_dfs", "flood_fill"
        """
        if variant == "count_bfs":
            yield from self._count_islands_bfs(data)
        elif variant == "count_dfs":
            yield from self._count_islands_dfs(data)
        elif variant == "flood_fill":
            yield from self._flood_fill(data)

    def _count_islands_bfs(
        self, grid: List[List[int]]
    ) -> Generator[AnimationStep, None, None]:
        """Count islands using BFS."""
        if not grid or not grid[0]:
            return

        rows, cols = len(grid), len(grid[0])
        visited: Set[Tuple[int, int]] = set()
        island_count = 0

        yield AnimationStep(
            state={},
            caption="Count islands: Find connected components of 1s",
        )

        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == 1 and (r, c) not in visited:
                    # Found a new island
                    island_count += 1
                    queue = deque([(r, c)])
                    visited.add((r, c))
                    component: Set[Tuple[int, int]] = {(r, c)}

                    yield AnimationStep(
                        state={
                            "current": (r, c),
                            "visited": visited - {(r, c)},
                            "frontier": {(r, c)},
                            "queue": [(r, c)],
                        },
                        caption=f"Found island #{island_count} at ({r},{c})",
                    )

                    while queue:
                        cr, cc = queue.popleft()

                        yield AnimationStep(
                            state={
                                "current": (cr, cc),
                                "visited": visited - set(queue) - {(cr, cc)},
                                "frontier": set(queue),
                                "component": component,
                                "queue": list(queue),
                            },
                            caption=f"Process ({cr},{cc})",
                        )

                        # Check 4 directions
                        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                            nr, nc = cr + dr, cc + dc
                            if (
                                0 <= nr < rows
                                and 0 <= nc < cols
                                and grid[nr][nc] == 1
                                and (nr, nc) not in visited
                            ):
                                visited.add((nr, nc))
                                queue.append((nr, nc))
                                component.add((nr, nc))

                                yield AnimationStep(
                                    state={
                                        "current": (cr, cc),
                                        "visited": visited - set(queue),
                                        "frontier": set(queue),
                                        "component": component,
                                        "queue": list(queue),
                                    },
                                    caption=f"Add neighbor ({nr},{nc}) to queue",
                                )

                    yield AnimationStep(
                        state={
                            "visited": visited,
                            "component": component,
                        },
                        caption=f"Island #{island_count} complete, size={len(component)}",
                    )

        yield AnimationStep(
            state={"visited": visited},
            caption=f"Done! Total islands: {island_count}",
            is_pause=True,
            duration_ms=1500,
        )

    def _count_islands_dfs(
        self, grid: List[List[int]]
    ) -> Generator[AnimationStep, None, None]:
        """Count islands using DFS."""
        if not grid or not grid[0]:
            return

        rows, cols = len(grid), len(grid[0])
        visited: Set[Tuple[int, int]] = set()
        island_count = 0

        yield AnimationStep(
            state={},
            caption="Count islands using DFS",
        )

        def dfs(r: int, c: int, component: Set[Tuple[int, int]]) -> Generator[AnimationStep, None, None]:
            if (
                r < 0 or r >= rows or
                c < 0 or c >= cols or
                grid[r][c] == 0 or
                (r, c) in visited
            ):
                return

            visited.add((r, c))
            component.add((r, c))

            yield AnimationStep(
                state={
                    "current": (r, c),
                    "visited": visited - {(r, c)},
                    "component": component,
                },
                caption=f"DFS visit ({r},{c})",
            )

            # Explore 4 directions
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                yield from dfs(r + dr, c + dc, component)

        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == 1 and (r, c) not in visited:
                    island_count += 1
                    component: Set[Tuple[int, int]] = set()

                    yield AnimationStep(
                        state={
                            "current": (r, c),
                            "visited": visited.copy(),
                        },
                        caption=f"Found island #{island_count} at ({r},{c})",
                    )

                    yield from dfs(r, c, component)

                    yield AnimationStep(
                        state={
                            "visited": visited,
                            "component": component,
                        },
                        caption=f"Island #{island_count} complete, size={len(component)}",
                    )

        yield AnimationStep(
            state={"visited": visited},
            caption=f"Done! Total islands: {island_count}",
            is_pause=True,
            duration_ms=1500,
        )

    def _flood_fill(
        self, grid: List[List[int]]
    ) -> Generator[AnimationStep, None, None]:
        """Flood fill from center of grid."""
        if not grid or not grid[0]:
            return

        rows, cols = len(grid), len(grid[0])

        # Find a starting cell with value 1
        start = None
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == 1:
                    start = (r, c)
                    break
            if start:
                break

        if not start:
            yield AnimationStep(state={}, caption="No land to fill!")
            return

        visited: Set[Tuple[int, int]] = set()
        queue = deque([start])
        visited.add(start)

        yield AnimationStep(
            state={
                "current": start,
                "frontier": {start},
                "queue": [start],
            },
            caption=f"Flood fill from ({start[0]},{start[1]})",
        )

        while queue:
            r, c = queue.popleft()

            yield AnimationStep(
                state={
                    "current": (r, c),
                    "visited": visited - {(r, c)},
                    "frontier": set(queue),
                    "queue": list(queue),
                },
                caption=f"Fill ({r},{c})",
            )

            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nr, nc = r + dr, c + dc
                if (
                    0 <= nr < rows
                    and 0 <= nc < cols
                    and grid[nr][nc] == 1
                    and (nr, nc) not in visited
                ):
                    visited.add((nr, nc))
                    queue.append((nr, nc))

        yield AnimationStep(
            state={"visited": visited},
            caption=f"Flood fill complete! Filled {len(visited)} cells",
            is_pause=True,
            duration_ms=1500,
        )
