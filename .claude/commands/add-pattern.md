# Add Pattern Documentation

Add new DSA pattern documentation with animations.

## Instructions

When the user wants to add documentation for a new pattern:

1. **Identify the pattern** from COURSE.md - check which chapter/pattern they want to document

2. **Check existing animations** by running:
   ```bash
   cd animator && uv run animator list
   ```

3. **Create or update the pattern documentation** in `docs/<pattern-name>/`:
   - `introduction.md` - Pattern overview, when to use, complexity
   - Include embedded animations where relevant

4. **Generate animations if needed**:
   - If animations don't exist for this pattern, consider adding them to the animator
   - Add new scenarios to `animator/src/animator/scenarios/registry.py`
   - Generate with: `cd animator && uv run animator generate-all --output-dir ../docs/.gitbook/assets/animations`

5. **Embed animations** in the markdown using:
   ```markdown
   ![Description](../.gitbook/assets/animations/<pattern>/<animation>.gif)
   ```

6. **Update docs/SUMMARY.md** to include the new pages in the sidebar navigation

## Available Animation Patterns

Current renderers support:
- **Arrays**: sliding window, two pointers, binary search, monotonic stack
- **Trees**: level order, preorder, inorder, postorder traversal
- **Graphs**: BFS, DFS traversal
- **Matrices**: island counting, flood fill

## Pattern to Animation Mapping

| Pattern | Animation Scenarios |
|---------|---------------------|
| sliding-window | sliding_window_fixed, sliding_window_dynamic |
| two-pointers | two_pointers_opposite, two_pointers_same, two_pointers_fast_slow |
| modified-binary-search | binary_search_classic, binary_search_first, binary_search_rotated |
| tree-breadth-first-search | tree_level_order |
| tree-depth-first-search | tree_preorder, tree_inorder, tree_postorder |
| graphs | graph_bfs, graph_dfs |
| island | island_count_bfs, island_count_dfs, island_flood_fill |
| monotonic-stack | monotonic_next_greater, monotonic_next_smaller |

## Example Usage

User: "Add docs for the Two Heaps pattern"

Response should:
1. Check if two-heaps animations exist (they don't yet)
2. Create `docs/two-heaps/introduction.md` with pattern explanation
3. If animating heaps: add HeapRenderer and TwoHeapsPattern to animator
4. Generate animations and embed in docs
5. Update SUMMARY.md
