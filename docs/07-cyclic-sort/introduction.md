# Introduction to Cyclic Sort Pattern

The Cyclic Sort pattern is an in-place technique for arrays containing numbers in a known, limited range (most commonly `1..n` or `0..n`).

The key idea is simple: **each value belongs to a specific index**. While scanning the array, if the current number is not in its correct position, swap it into place. This often turns seemingly $O(n \log n)$ sorting-based problems into clean $O(n)$ solutions.

When to use
- The array contains integers in a tight range like `1..n` or `0..n`.
- You need to find a **missing number**, **duplicate**, **corrupt pair**, or the **first missing positive**.
- You’re allowed to modify the array (in-place is the usual win).

Common variants
- `1..n` placement: value `x` should be at index `x - 1`.
- `0..n` placement: value `x` should be at index `x` (often with one missing).
- Duplicates present: you can’t always place everything perfectly; use mismatches to detect duplicates/missing.
- Multiple missing/duplicates: after placement, scan for indices where `nums[i] != i + 1`.

Pattern recipe (for `1..n`)
1. Set `i = 0`.
2. While `i < n`:
   - Let `correct = nums[i] - 1`.
   - If `nums[i]` is in range and `nums[i] != nums[correct]`, swap `nums[i]` with `nums[correct]`.
   - Otherwise, increment `i`.
3. After this pass, many problems become a simple scan for mismatches.

Why the `nums[i] != nums[correct]` check matters
- If duplicates exist, naive swapping can loop forever (you keep swapping identical values).
- The inequality check ensures every swap makes progress.

Complexity
- Time: $O(n)$ — each element is swapped at most once into its final position.
- Space: $O(1)$ extra space (besides output storage).

Short examples

Cyclic sort (`1..n`) — Python

```python
def cyclic_sort(nums):
    i = 0
    while i < len(nums):
        correct = nums[i] - 1
        if nums[i] != nums[correct]:
            nums[i], nums[correct] = nums[correct], nums[i]
        else:
            i += 1
    return nums
```

Find the missing number (`0..n`) — Python

```python
def missing_number(nums):
    i = 0
    n = len(nums)

    while i < n:
        correct = nums[i]
        # values are in [0..n], but index range is [0..n-1]
        if 0 <= correct < n and nums[i] != nums[correct]:
            nums[i], nums[correct] = nums[correct], nums[i]
        else:
            i += 1

    for idx, val in enumerate(nums):
        if val != idx:
            return idx

    return n
```

Find all missing numbers (`1..n`) — Python

```python
def find_all_missing(nums):
    i = 0
    while i < len(nums):
        correct = nums[i] - 1
        if 1 <= nums[i] <= len(nums) and nums[i] != nums[correct]:
            nums[i], nums[correct] = nums[correct], nums[i]
        else:
            i += 1

    missing = []
    for i, v in enumerate(nums):
        if v != i + 1:
            missing.append(i + 1)
    return missing
```

Problems to practice
- [Missing Number](https://leetcode.com/problems/missing-number/)
- [Find All Numbers Disappeared in an Array](https://leetcode.com/problems/find-all-numbers-disappeared-in-an-array/)
- [Find the Duplicate Number](https://leetcode.com/problems/find-the-duplicate-number/) (often solved without modifying; cyclic-sort variant exists)
- [Find All Duplicates in an Array](https://leetcode.com/problems/find-all-duplicates-in-an-array/)
- [Set Mismatch](https://leetcode.com/problems/set-mismatch/)
- [First Missing Positive](https://leetcode.com/problems/first-missing-positive/)
