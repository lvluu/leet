````markdown
# Introduction to Subsets Pattern

The Subsets pattern (sometimes called the *power set* pattern) is about generating **all combinations** of a collection.
It shows up whenever a problem asks for *all possible selections*, *all arrangements*, or *all ways to build* something.

A key point: the number of results is usually exponential.
- For $n$ distinct items, the number of subsets is $2^n$.
- For permutations, the number of results is $n!$.

When to use
- The problem asks for **all subsets / combinations / selections**.
- You see phrasing like “generate all”, “return all possible”, “all ways”, “find every…”.
- You can build the answer by making a sequence of **binary decisions** (include/exclude), or by choosing the **next element** from remaining options.

Common variants
- Subsets (power set): all combinations of elements.
- Subsets with duplicates: avoid duplicate subsets by sorting + skipping duplicates.
- Combinations with constraints: e.g., size $k$, sum == target.
- Permutations: all orderings of elements.
- String permutations by case: each letter branches into upper/lower.
- Balanced parentheses: build only valid sequences by tracking counts.
- “Different ways to evaluate”: recursively split expression (divide-and-combine).
- Structurally unique BSTs: count/generate BSTs (Catalan-number family).

Pattern recipe (classic subsets)

Option A: iterative expansion (BFS-style)
1. Start with a list containing the empty subset: `[[]]`.
2. For each element `x`:
   - Copy all existing subsets and append `x` to each copy.
   - Add those new subsets back into the list.

Option B: backtracking (DFS)
1. Keep a `path` (current subset).
2. At index `i`, branch:
   - include `nums[i]` in `path`
   - exclude `nums[i]`
3. When you reach the end, emit `path`.

Handling duplicates (Subsets II)
- Sort input.
- During iterative expansion, only extend the subsets created in the previous step when you see a duplicate.
- During DFS, skip duplicates at the same recursion depth.

Complexity
- Subsets (distinct):
  - Time: $O(n \cdot 2^n)$ (each subset copy can cost up to $n$)
  - Space: $O(n \cdot 2^n)$ for output
- Permutations:
  - Time: $O(n \cdot n!)$
  - Space: $O(n)$ recursion depth (plus output)

Short examples

Generate all subsets (iterative) — Python

```python
def subsets(nums):
    result = [[]]
    for x in nums:
        result += [curr + [x] for curr in result]
    return result
```

Subsets with duplicates (iterative) — Python

```python
def subsets_with_dup(nums):
    nums.sort()
    result = [[]]
    start = 0

    for i, x in enumerate(nums):
        # if current value is a duplicate, only extend subsets added in the previous step
        if i > 0 and nums[i] == nums[i - 1]:
            subset_range = result[start:]
        else:
            subset_range = result

        start = len(result)
        result += [curr + [x] for curr in subset_range]

    return result
```

Balanced parentheses (backtracking) — Python

```python
def generate_parentheses(n):
    result = []

    def dfs(path, open_count, close_count):
        if len(path) == 2 * n:
            result.append(path)
            return
        if open_count < n:
            dfs(path + "(", open_count + 1, close_count)
        if close_count < open_count:
            dfs(path + ")", open_count, close_count + 1)

    dfs("", 0, 0)
    return result
```

Problems to practice
- [Subsets](https://leetcode.com/problems/subsets/)
- [Subsets II](https://leetcode.com/problems/subsets-ii/)
- [Permutations](https://leetcode.com/problems/permutations/)
- [Letter Case Permutation](https://leetcode.com/problems/letter-case-permutation/)
- [Generate Parentheses](https://leetcode.com/problems/generate-parentheses/)
- [Different Ways to Add Parentheses](https://leetcode.com/problems/different-ways-to-add-parentheses/)
- [Unique Binary Search Trees](https://leetcode.com/problems/unique-binary-search-trees/)
- [Unique Binary Search Trees II](https://leetcode.com/problems/unique-binary-search-trees-ii/)
````
