# Introduction to Two Heaps Pattern

The Two Heaps pattern solves problems where you need to continuously reason about the **middle** of a dataset (median, k-th boundary) or dynamically split values into a **lower half** and an **upper half**.

You maintain:
- a **max-heap** for the *lower* half (so you can quickly get the largest of the smaller values)
- a **min-heap** for the *upper* half (so you can quickly get the smallest of the larger values)

The heaps are kept **balanced** (sizes differ by at most 1), which makes the median or boundary element available in $O(1)$ after each update.

When to use
- You need a running median / dynamic median after each insertion.
- You need to support “add a number” and “query median” (streaming data).
- You need to maintain two groups with a natural split (e.g., “small vs large”) and frequently query the boundary.
- You need a sliding window median (two heaps + lazy deletion bookkeeping).

Core invariants
- All values in `lower` (max-heap) are `<=` all values in `upper` (min-heap).
- `len(lower)` is either equal to `len(upper)` or exactly one larger (common choice).

Pattern recipe (running median)
1. Insert the number into one heap:
   - If the number is `<= max(lower)`, push to `lower`.
   - Else push to `upper`.
2. Rebalance sizes so `abs(len(lower) - len(upper)) <= 1`.
   - If `lower` is too big, move its top to `upper`.
   - If `upper` is too big, move its top to `lower`.
3. Compute median:
   - If odd count, median is `top(lower)` (or whichever heap you keep larger).
   - If even count, median is the average of `top(lower)` and `top(upper)`.

Complexity
- Insert: $O(\log n)$
- Rebalance: $O(\log n)$ (one move)
- Query median/boundary: $O(1)$
- Space: $O(n)$

Short example (running median) — Python

```python
import heapq

class MedianFinder:
    def __init__(self):
        # lower: max-heap implemented via negatives
        self.lower = []
        # upper: min-heap
        self.upper = []

    def add_num(self, num: int) -> None:
        if not self.lower or num <= -self.lower[0]:
            heapq.heappush(self.lower, -num)
        else:
            heapq.heappush(self.upper, num)

        # rebalance
        if len(self.lower) > len(self.upper) + 1:
            heapq.heappush(self.upper, -heapq.heappop(self.lower))
        elif len(self.upper) > len(self.lower):
            heapq.heappush(self.lower, -heapq.heappop(self.upper))

    def find_median(self) -> float:
        if len(self.lower) > len(self.upper):
            return float(-self.lower[0])
        return (-self.lower[0] + self.upper[0]) / 2.0
```

Common pitfalls
- Forgetting to rebalance after every insertion.
- Violating the ordering invariant (`max(lower) <= min(upper)`).
- Sliding window median requires *removals*; typical solutions use “lazy deletion” maps + cleanup loops to discard invalid heap tops.
- Handling even-sized median carefully (integer vs float division).

Problems to practice
- [Find Median from Data Stream](https://leetcode.com/problems/find-median-from-data-stream/)
- [Sliding Window Median](https://leetcode.com/problems/sliding-window-median/) (two heaps + lazy deletion)
- [IPO (Maximize Capital)](https://leetcode.com/problems/ipo/) (often taught as two heaps: one by required capital, one by profits)
- [Find Right Interval](https://leetcode.com/problems/find-right-interval/) (commonly solved with heaps or sorting + binary search)
