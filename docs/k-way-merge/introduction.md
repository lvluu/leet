# Introduction to K-way Merge Pattern

The **K-way Merge** pattern efficiently merges K sorted arrays (or lists) into a single sorted output using a min-heap. Instead of merging pairs repeatedly, we track the smallest element across all K lists simultaneously.

## Visual Example

### Merging K Sorted Lists
![K-way merge](../assets/k-way-merge/k_way_merge.gif)

A min-heap holds one element from each list. We repeatedly:
1. Extract the minimum (smallest across all lists)
2. Add it to the result
3. Push the next element from that same list

## When to Use

- Merge K sorted arrays or linked lists.
- Find the K-th smallest element across multiple sorted sources.
- Find the smallest range covering elements from K lists.
- External sorting (merging sorted chunks from disk).
- Any problem involving multiple sorted sequences.

## Core Insight

The heap always contains **at most K elements** (one from each list), so operations are $O(\log k)$ instead of $O(\log n)$.

## Pattern Recipe

1. **Initialize** a min-heap with the first element from each list (store value + list index + element index).
2. **While heap is not empty**:
   - Pop the minimum element
   - Add it to result
   - If that list has more elements, push the next one
3. **Return** the merged result.

## Complexity

- Time: $O(n \log k)$ where n = total elements across all lists
- Space: $O(k)$ for the heap (plus $O(n)$ for output)

## Short Examples — Python

### Merge K Sorted Lists (Linked Lists)

```python
import heapq
from typing import Optional

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def merge_k_lists(lists: list[Optional[ListNode]]) -> Optional[ListNode]:
    min_heap = []

    # Add first node from each list
    for i, node in enumerate(lists):
        if node:
            heapq.heappush(min_heap, (node.val, i, node))

    dummy = ListNode(0)
    current = dummy

    while min_heap:
        val, i, node = heapq.heappop(min_heap)
        current.next = node
        current = current.next

        if node.next:
            heapq.heappush(min_heap, (node.next.val, i, node.next))

    return dummy.next
```

### Merge K Sorted Arrays

```python
import heapq

def merge_k_arrays(arrays: list[list[int]]) -> list[int]:
    min_heap = []
    result = []

    # (value, array_index, element_index)
    for i, arr in enumerate(arrays):
        if arr:
            heapq.heappush(min_heap, (arr[0], i, 0))

    while min_heap:
        val, arr_idx, elem_idx = heapq.heappop(min_heap)
        result.append(val)

        # Push next element from same array
        if elem_idx + 1 < len(arrays[arr_idx]):
            next_val = arrays[arr_idx][elem_idx + 1]
            heapq.heappush(min_heap, (next_val, arr_idx, elem_idx + 1))

    return result

# Example:
# [[1, 4, 7], [2, 5, 8], [3, 6, 9]] → [1, 2, 3, 4, 5, 6, 7, 8, 9]
```

### K-th Smallest in M Sorted Lists

```python
import heapq

def kth_smallest(arrays: list[list[int]], k: int) -> int:
    min_heap = []

    for i, arr in enumerate(arrays):
        if arr:
            heapq.heappush(min_heap, (arr[0], i, 0))

    count = 0
    while min_heap:
        val, arr_idx, elem_idx = heapq.heappop(min_heap)
        count += 1

        if count == k:
            return val

        if elem_idx + 1 < len(arrays[arr_idx]):
            next_val = arrays[arr_idx][elem_idx + 1]
            heapq.heappush(min_heap, (next_val, arr_idx, elem_idx + 1))

    return -1  # k is larger than total elements
```

### Smallest Range Covering K Lists

```python
import heapq
from math import inf

def smallest_range(nums: list[list[int]]) -> list[int]:
    min_heap = []
    current_max = -inf

    # Initialize with first element from each list
    for i, arr in enumerate(nums):
        heapq.heappush(min_heap, (arr[0], i, 0))
        current_max = max(current_max, arr[0])

    best_range = [-inf, inf]

    while len(min_heap) == len(nums):
        current_min, arr_idx, elem_idx = heapq.heappop(min_heap)

        # Update best range
        if current_max - current_min < best_range[1] - best_range[0]:
            best_range = [current_min, current_max]

        # Add next element from same list
        if elem_idx + 1 < len(nums[arr_idx]):
            next_val = nums[arr_idx][elem_idx + 1]
            heapq.heappush(min_heap, (next_val, arr_idx, elem_idx + 1))
            current_max = max(current_max, next_val)

    return best_range
```

## Common Pitfalls

- Forgetting to track which list each element came from.
- Not handling empty lists in the input.
- For linked lists in Python, you need a tiebreaker (list index) since `ListNode` isn't comparable.
- Off-by-one errors when checking if a list has more elements.

## Comparison with Divide & Conquer

| Approach | Time | When to Use |
|----------|------|-------------|
| K-way Merge (Heap) | $O(n \log k)$ | General case, streaming |
| Divide & Conquer | $O(n \log k)$ | When K is very large |
| Merge pairs iteratively | $O(nk)$ | Simple but slower |

## Problems to Practice

- [Merge k Sorted Lists](https://leetcode.com/problems/merge-k-sorted-lists/)
- [Kth Smallest Element in a Sorted Matrix](https://leetcode.com/problems/kth-smallest-element-in-a-sorted-matrix/)
- [Smallest Range Covering Elements from K Lists](https://leetcode.com/problems/smallest-range-covering-elements-from-k-lists/)
- [Find K Pairs with Smallest Sums](https://leetcode.com/problems/find-k-pairs-with-smallest-sums/)
