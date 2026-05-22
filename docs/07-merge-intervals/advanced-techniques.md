# Advanced Merge Intervals Techniques

This guide covers advanced applications of the Merge Intervals pattern, including sweep line/event counting, min-heap scheduling, and common edge cases.

## 1. Endpoint Semantics (Closed vs Half-open)

A frequent source of bugs is whether two intervals that “touch” at an endpoint should be merged.

- Closed intervals `[a, b]` overlap when `next.start <= current.end`.
- Half-open intervals `[a, b)` overlap when `next.start < current.end`.

Always confirm which model the problem uses (meeting times often behave like half-open; many LeetCode interval problems behave like closed).

## 2. Sweep Line / Event Counting

Instead of merging intervals directly, you can convert them into **events** and scan from left to right.

### Meeting Rooms II (minimum number of rooms)

**Problem**: Given meeting intervals, find the minimum number of rooms required.

**Idea**: Create events `(time, +1)` for meeting start and `(time, -1)` for meeting end. Sort events; the maximum prefix sum is the answer.

**Tie-breaking matters**
- If an end time and start time are the same, process **end before start** to avoid counting them as overlapping.

```python
def min_meeting_rooms(intervals):
    events = []
    for start, end in intervals:
        events.append((start, 1))
        events.append((end, -1))

    # end (-1) comes before start (+1) at the same time
    events.sort(key=lambda x: (x[0], x[1]))

    rooms = 0
    max_rooms = 0
    for _, delta in events:
        rooms += delta
        max_rooms = max(max_rooms, rooms)

    return max_rooms
```

### Maximum CPU Load (maximum overlap “weight”)

**Problem**: Each interval has a load; find the maximum total load at any time.

**Idea**: Events become `(time, +load)` and `(time, -load)`; scan and track max prefix sum.

```python
def max_cpu_load(jobs):
    events = []
    for start, end, load in jobs:
        events.append((start, load))
        events.append((end, -load))

    # same tie-breaking principle: end before start
    events.sort(key=lambda x: (x[0], x[1]))

    current = 0
    best = 0
    for _, delta in events:
        current += delta
        best = max(best, current)

    return best
```

## 3. Min-Heap Scheduling (Track Active Intervals)

A min-heap is useful when you need to manage “currently active” intervals and remove the earliest-finishing ones.

### Meeting Rooms II (heap approach)

**Idea**: Sort by start time. Keep a min-heap of end times for active meetings.

- If the earliest ending meeting ends before the next starts, reuse that room (pop).
- Push the new meeting’s end.
- Heap size is the room count.

```python
import heapq

def min_meeting_rooms_heap(intervals):
    if not intervals:
        return 0

    intervals.sort(key=lambda x: x[0])
    ends = []  # min-heap of end times

    for start, end in intervals:
        if ends and ends[0] <= start:
            heapq.heappop(ends)
        heapq.heappush(ends, end)

    return len(ends)
```

### Employee Free Time

**Idea**: Merge multiple employees’ schedules (k lists of sorted intervals), then find gaps between the merged busy times.

Common approaches:
- Flatten all intervals, sort, merge, then scan gaps.
- Use a min-heap over the heads of k sorted lists to do a k-way merge (better when k lists are large).

## 4. Greedy “One-pass after sort” Tricks

Some interval problems reduce to choosing as many non-overlapping intervals as possible or minimizing resources.

### Minimum Number of Arrows to Burst Balloons

**Idea**: Sort by end coordinate; greedily shoot an arrow at the current end. If the next balloon starts after that point, you need a new arrow.

```python
def find_min_arrows(points):
    if not points:
        return 0

    points.sort(key=lambda x: x[1])
    arrows = 1
    arrow_pos = points[0][1]

    for start, end in points[1:]:
        if start > arrow_pos:
            arrows += 1
            arrow_pos = end

    return arrows
```

## 5. Common Pitfalls & Checklist

1. Sorting key: most merge problems require sorting by `start` (sometimes by `end`).
2. Endpoint semantics: decide `<=` vs `<` for overlap.
3. In-place edits: be careful if you mutate the input list/interval objects.
4. Large coordinates: use integer-safe comparisons (no floating point).
5. Output format: some problems want inclusive endpoints, some want merged busy times vs free times.

## Practice Problems

- [Meeting Rooms II](https://leetcode.com/problems/meeting-rooms-ii/)
- [Employee Free Time](https://leetcode.com/problems/employee-free-time/)
- [Minimum Number of Arrows to Burst Balloons](https://leetcode.com/problems/minimum-number-of-arrows-to-burst-balloons/)
- [Car Pooling](https://leetcode.com/problems/car-pooling/) (classic sweep line)
- [My Calendar I](https://leetcode.com/problems/my-calendar-i/) (overlap detection)
