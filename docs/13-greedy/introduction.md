# Introduction to Greedy Algorithms

A **Greedy Algorithm** makes the locally optimal choice at each step, hoping to find a global optimum. It never reconsiders previous decisions—once a choice is made, it's final.

## Visual Example

### Activity Selection (Greedy by End Time)
![Greedy activity selection](../assets/greedy/greedy_activity.gif)

To maximize non-overlapping activities, always pick the one that **ends earliest**—this leaves maximum room for future activities.

## When to Use

Greedy works when the problem has:

1. **Greedy Choice Property**: A locally optimal choice leads to a globally optimal solution.
2. **Optimal Substructure**: An optimal solution contains optimal solutions to subproblems.

Common greedy scenarios:
- Interval scheduling (meeting rooms, activity selection)
- Huffman encoding
- Minimum spanning trees (Prim's, Kruskal's)
- Shortest paths (Dijkstra's)
- Coin change (with specific denominations)
- Fractional knapsack

## When NOT to Use

Greedy fails when local optima don't lead to global optima:
- **0/1 Knapsack**: Must use DP (can't take fractions)
- **Coin change with arbitrary denominations**: e.g., coins [1, 3, 4], amount 6 → greedy gives [4,1,1] but optimal is [3,3]
- **Longest path in graph**: Greedy can get stuck

## Pattern Recipe

1. **Identify the greedy choice**: What local decision seems best?
2. **Prove it works** (or trust the pattern for known problems).
3. **Sort** the input if needed (by end time, deadline, ratio, etc.).
4. **Iterate** and make greedy choices, updating state.
5. **Return** the result.

## Complexity

- Usually $O(n \log n)$ due to sorting
- Sometimes $O(n)$ if no sorting needed

## Short Examples — Python

### Activity Selection (Maximum Non-overlapping Intervals)

```python
def max_activities(activities: list[tuple[int, int]]) -> int:
    # Sort by end time
    activities.sort(key=lambda x: x[1])

    count = 0
    last_end = float('-inf')

    for start, end in activities:
        if start >= last_end:  # Non-overlapping
            count += 1
            last_end = end

    return count

# Example: [(1,3), (2,4), (3,5), (0,6), (5,7)] → 3
# Select: (1,3), (3,5), (5,7)
```

### Minimum Meeting Rooms (Interval Partitioning)

```python
import heapq

def min_meeting_rooms(intervals: list[list[int]]) -> int:
    if not intervals:
        return 0

    intervals.sort(key=lambda x: x[0])  # Sort by start
    heap = []  # Track end times of ongoing meetings

    for start, end in intervals:
        if heap and heap[0] <= start:
            heapq.heappop(heap)  # Reuse room
        heapq.heappush(heap, end)

    return len(heap)  # Number of rooms needed
```

### Jump Game (Can Reach End?)

```python
def can_jump(nums: list[int]) -> bool:
    max_reach = 0

    for i, jump in enumerate(nums):
        if i > max_reach:
            return False  # Can't reach this index
        max_reach = max(max_reach, i + jump)

    return True

# Example: [2,3,1,1,4] → True
# Example: [3,2,1,0,4] → False
```

### Gas Station Circuit

```python
def can_complete_circuit(gas: list[int], cost: list[int]) -> int:
    total_tank = 0
    current_tank = 0
    start = 0

    for i in range(len(gas)):
        total_tank += gas[i] - cost[i]
        current_tank += gas[i] - cost[i]

        if current_tank < 0:
            start = i + 1  # Reset start
            current_tank = 0

    return start if total_tank >= 0 else -1
```

### Fractional Knapsack

```python
def fractional_knapsack(
    capacity: int,
    items: list[tuple[int, int]]  # (value, weight)
) -> float:
    # Sort by value/weight ratio (descending)
    items.sort(key=lambda x: x[0] / x[1], reverse=True)

    total_value = 0.0

    for value, weight in items:
        if capacity >= weight:
            total_value += value
            capacity -= weight
        else:
            # Take fraction
            total_value += value * (capacity / weight)
            break

    return total_value
```

## Greedy Proof Techniques

1. **Exchange Argument**: Show that swapping a non-greedy choice with a greedy one doesn't worsen the solution.
2. **Stays Ahead**: Show the greedy solution is at least as good as any other at every step.
3. **Structural**: Show the greedy choice must be part of some optimal solution.

## Common Pitfalls

- Assuming greedy works without verification (it often doesn't!).
- Wrong sorting criteria (e.g., sorting by start time instead of end time).
- Not handling ties correctly.
- Forgetting edge cases (empty input, single element).

## Greedy vs Dynamic Programming

| Aspect | Greedy | DP |
|--------|--------|-----|
| Approach | Local optimal choice | Explore all subproblems |
| Revisits | Never | Stores and reuses |
| Speed | Usually faster | Can be slower |
| Correctness | Only for specific problems | Always correct |

## Problems to Practice

- [Jump Game](https://leetcode.com/problems/jump-game/)
- [Jump Game II](https://leetcode.com/problems/jump-game-ii/)
- [Gas Station](https://leetcode.com/problems/gas-station/)
- [Meeting Rooms II](https://leetcode.com/problems/meeting-rooms-ii/)
- [Non-overlapping Intervals](https://leetcode.com/problems/non-overlapping-intervals/)
- [Task Scheduler](https://leetcode.com/problems/task-scheduler/)
- [Partition Labels](https://leetcode.com/problems/partition-labels/)
- [Minimum Number of Arrows to Burst Balloons](https://leetcode.com/problems/minimum-number-of-arrows-to-burst-balloons/)
