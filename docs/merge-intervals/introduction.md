# Introduction to Merge Intervals Pattern

The Merge Intervals pattern is used for problems that involve **intervals** (ranges like `[start, end]`) where you need to **merge overlaps**, **find intersections**, or **reason about schedules**.

The core idea is to bring the intervals into an order (usually by start time), then make a single pass while maintaining a “current” interval that you expand, emit, or split based on overlap.

When to use
- The input is a list of ranges (time blocks, indices, segments) and you need to combine or compare them.
- You’re asked to merge overlapping intervals, insert a new interval, or detect conflicts.
- You need results like “free time”, “minimum rooms”, or “combined utilization”.

Common variants
- Merge all overlaps: return a condensed set of disjoint intervals.
- Insert interval: add one interval into an existing schedule and re-merge.
- Intersections: find overlapping parts across two lists of intervals.
- Sweep line / events: convert `[start, end]` into `(+1 at start, -1 at end)` to compute concurrent load/rooms.

Pattern recipe (merge overlaps)
1. Sort intervals by `start` (and by `end` to break ties).
2. Initialize `merged` with the first interval.
3. For each next interval:
   - If it overlaps the last merged interval, extend the last interval’s end.
   - Otherwise, append it as a new disjoint interval.
4. Return `merged`.

Overlap rule
- Two intervals overlap if `next.start <= current.end` (for closed intervals).
- If the problem treats endpoints as non-overlapping (half-open intervals), you’ll use `next.start < current.end`.

Complexity
- Time: $O(n \log n)$ for sorting + $O(n)$ scan.
- Space: $O(n)$ for output (or $O(1)$ extra if modifying in-place).

Short examples

Merge overlapping intervals — Python

```python
def merge_intervals(intervals):
    if not intervals:
        return []

    intervals.sort(key=lambda x: (x[0], x[1]))
    merged = [intervals[0]]

    for start, end in intervals[1:]:
        last_start, last_end = merged[-1]
        if start <= last_end:
            merged[-1][1] = max(last_end, end)
        else:
            merged.append([start, end])

    return merged
```

Insert interval — Python

```python
def insert_interval(intervals, new_interval):
    result = []
    i = 0
    n = len(intervals)

    # 1) Add all intervals ending before new starts
    while i < n and intervals[i][1] < new_interval[0]:
        result.append(intervals[i])
        i += 1

    # 2) Merge all overlapping intervals into new_interval
    start, end = new_interval
    while i < n and intervals[i][0] <= end:
        start = min(start, intervals[i][0])
        end = max(end, intervals[i][1])
        i += 1

    result.append([start, end])

    # 3) Add the remaining intervals
    while i < n:
        result.append(intervals[i])
        i += 1

    return result
```

Problems to practice
- [Merge Intervals](https://leetcode.com/problems/merge-intervals/)
- [Insert Interval](https://leetcode.com/problems/insert-interval/)
- [Interval List Intersections](https://leetcode.com/problems/interval-list-intersections/)
- [Meeting Rooms](https://leetcode.com/problems/meeting-rooms/)
- [Meeting Rooms II](https://leetcode.com/problems/meeting-rooms-ii/) (often solved via sweep line or min-heap)
- [Minimum Number of Arrows to Burst Balloons](https://leetcode.com/problems/minimum-number-of-arrows-to-burst-balloons/)
