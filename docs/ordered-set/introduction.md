# Introduction to Ordered Set Pattern

An **Ordered Set** (or Sorted Container) maintains elements in sorted order while supporting efficient insertion, deletion, and range queries. In Python, this is typically implemented using `sortedcontainers.SortedList` or balanced BST structures.

## Visual Example

### Ordered Set Operations
![Ordered set](../assets/ordered-set/ordered_set.gif)

Elements stay sorted after each insertion. Binary search enables O(log n) lookups, and we can efficiently find predecessors, successors, and range queries.

## When to Use

- Need elements in sorted order at all times.
- Frequent insertions/deletions with order maintenance.
- Finding predecessor/successor of a value.
- Range queries (elements between X and Y).
- Sliding window with sorted access.
- Problems requiring "next smaller/larger" dynamically.

## Operations Complexity

| Operation | SortedList | TreeSet (Java) |
|-----------|------------|----------------|
| Insert | O(log n) | O(log n) |
| Delete | O(log n) | O(log n) |
| Search | O(log n) | O(log n) |
| Index access | O(log n) | O(log n) |
| Min/Max | O(1) | O(log n) |
| Range query | O(log n + k) | O(log n + k) |

## Python: sortedcontainers

```python
from sortedcontainers import SortedList

sl = SortedList([3, 1, 4, 1, 5])
# sl = [1, 1, 3, 4, 5] (automatically sorted)

sl.add(2)           # [1, 1, 2, 3, 4, 5]
sl.remove(1)        # [1, 2, 3, 4, 5] (removes first occurrence)
sl.discard(10)      # No error if not found

# Binary search
sl.bisect_left(3)   # 2 (index where 3 would go, left of existing)
sl.bisect_right(3)  # 3 (index after existing 3s)

# Index access
sl[0]               # 1 (minimum)
sl[-1]              # 5 (maximum)
sl[2]               # 3 (element at index 2)

# Range
sl.irange(2, 4)     # Iterator for elements in [2, 4]
```

## Short Examples — Python

### Setup (install sortedcontainers)

```bash
pip install sortedcontainers
```

### Containment Checking with Ranges

```python
from sortedcontainers import SortedList

def contains_nearby_almost_duplicate(nums: list[int], k: int, t: int) -> bool:
    """
    Check if there are two indices i, j where:
    - |i - j| <= k (within window)
    - |nums[i] - nums[j]| <= t (values close)
    """
    if t < 0:
        return False

    sl = SortedList()

    for i, num in enumerate(nums):
        # Find position where num would be inserted
        pos = sl.bisect_left(num)

        # Check neighbors within range [num - t, num + t]
        # Check element at pos (>= num)
        if pos < len(sl) and sl[pos] - num <= t:
            return True
        # Check element at pos - 1 (< num)
        if pos > 0 and num - sl[pos - 1] <= t:
            return True

        sl.add(num)

        # Maintain window of size k
        if i >= k:
            sl.remove(nums[i - k])

    return False
```

### My Calendar (Non-overlapping intervals)

```python
from sortedcontainers import SortedList

class MyCalendar:
    def __init__(self):
        self.events = SortedList()

    def book(self, start: int, end: int) -> bool:
        # Find where this event would go
        idx = self.events.bisect_right((start, end))

        # Check overlap with previous event
        if idx > 0:
            prev_start, prev_end = self.events[idx - 1]
            if prev_end > start:
                return False

        # Check overlap with next event
        if idx < len(self.events):
            next_start, next_end = self.events[idx]
            if end > next_start:
                return False

        self.events.add((start, end))
        return True
```

### 132 Pattern

```python
from sortedcontainers import SortedList

def find132pattern(nums: list[int]) -> bool:
    """
    Find i < j < k where nums[i] < nums[k] < nums[j]
    """
    if len(nums) < 3:
        return False

    # min_left[i] = minimum value in nums[0:i]
    min_left = [float('inf')] * len(nums)
    for i in range(1, len(nums)):
        min_left[i] = min(min_left[i-1], nums[i-1])

    # Scan from right, maintaining sorted set of potential nums[k]
    sl = SortedList()

    for j in range(len(nums) - 1, 0, -1):
        # nums[i] = min_left[j], nums[j] = nums[j]
        # Need nums[k] where min_left[j] < nums[k] < nums[j]

        if nums[j] > min_left[j]:
            # Find smallest element > min_left[j]
            idx = sl.bisect_right(min_left[j])
            if idx < len(sl) and sl[idx] < nums[j]:
                return True

        sl.add(nums[j])

    return False
```

### Longest Continuous Subarray (with limit)

```python
from sortedcontainers import SortedList

def longest_subarray(nums: list[int], limit: int) -> int:
    """
    Find longest subarray where max - min <= limit
    """
    sl = SortedList()
    left = 0
    result = 0

    for right, num in enumerate(nums):
        sl.add(num)

        # Shrink window if constraint violated
        while sl[-1] - sl[0] > limit:
            sl.remove(nums[left])
            left += 1

        result = max(result, right - left + 1)

    return result

# Example: [8,2,4,7], limit=4 → 2 (subarray [2,4])
```

### Count of Range Sum

```python
from sortedcontainers import SortedList

def count_range_sum(nums: list[int], lower: int, upper: int) -> int:
    """
    Count subarrays with sum in [lower, upper].
    Uses prefix sums: sum(i,j) = prefix[j+1] - prefix[i]
    """
    prefix = [0]
    for num in nums:
        prefix.append(prefix[-1] + num)

    sl = SortedList()
    count = 0

    for p in prefix:
        # Count prefix sums where: lower <= p - x <= upper
        # i.e., p - upper <= x <= p - lower
        left = sl.bisect_left(p - upper)
        right = sl.bisect_right(p - lower)
        count += right - left

        sl.add(p)

    return count
```

### Sliding Window Median (Alternative to Two Heaps)

```python
from sortedcontainers import SortedList

def median_sliding_window(nums: list[int], k: int) -> list[float]:
    sl = SortedList(nums[:k])
    result = []

    for i in range(k, len(nums) + 1):
        # Calculate median
        if k % 2:
            result.append(float(sl[k // 2]))
        else:
            result.append((sl[k // 2 - 1] + sl[k // 2]) / 2)

        # Slide window
        if i < len(nums):
            sl.remove(nums[i - k])
            sl.add(nums[i])

    return result
```

## When to Use Ordered Set vs Alternatives

| Problem Type | Best Choice |
|--------------|-------------|
| Static sorted data | Regular list + sort |
| Frequent insertions + sorted access | Ordered Set |
| Only need min/max | Heap |
| Range queries + updates | Ordered Set or Segment Tree |
| Predecessor/successor queries | Ordered Set |

## Common Pitfalls

- Using regular list with repeated sorting (O(n log n) per operation).
- Forgetting `sortedcontainers` needs installation (`pip install`).
- Confusing `bisect_left` vs `bisect_right`.
- Not handling duplicates correctly (SortedList allows duplicates).

## Alternative: Manual BST (for interviews without libraries)

```python
class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None
        self.count = 1  # For duplicates

# Or use bisect module with list (O(n) insert/delete)
import bisect

class SimpleSortedList:
    def __init__(self):
        self.data = []

    def add(self, x):
        bisect.insort(self.data, x)  # O(n) due to shift

    def remove(self, x):
        idx = bisect.bisect_left(self.data, x)
        if idx < len(self.data) and self.data[idx] == x:
            self.data.pop(idx)  # O(n)
```

## Problems to Practice

- [Contains Duplicate III](https://leetcode.com/problems/contains-duplicate-iii/)
- [My Calendar I](https://leetcode.com/problems/my-calendar-i/)
- [My Calendar II](https://leetcode.com/problems/my-calendar-ii/)
- [132 Pattern](https://leetcode.com/problems/132-pattern/)
- [Sliding Window Median](https://leetcode.com/problems/sliding-window-median/)
- [Longest Continuous Subarray](https://leetcode.com/problems/longest-continuous-subarray-with-absolute-diff-less-than-or-equal-to-limit/)
- [Count of Range Sum](https://leetcode.com/problems/count-of-range-sum/)
