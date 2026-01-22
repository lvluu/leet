# Introduction to Stack

A **stack** is a linear data structure that follows **LIFO** (Last In, First Out): the most recently added element is the first one removed.

You can think of it like a stack of plates:
- You *push* a plate onto the top.
- You *pop* a plate from the top.
- You can *peek* at the top plate without removing it.

Stacks show up constantly in algorithms because they naturally model:
- **Nested structures** (parentheses, XML/HTML tags)
- **Backtracking** (undo operations, DFS)
- **Monotonic behavior** (next greater element, stock span)

When to use
- You need to process items in *reverse* order of arrival.
- You need to match pairs with nesting (e.g., `()[]{}`).
- You need to maintain a monotonic structure (increasing/decreasing) while scanning.
- You need to simulate recursion / manage call frames explicitly.

Common variants
- Simple stack: supports `push`, `pop`, `peek`.
- Min stack / max stack: can return current min/max in $O(1)$.
- Monotonic stack: maintains increasing or decreasing values/indices.
- Two-stack techniques:
  - Implement a queue using two stacks.
  - Evaluate expressions (operator stack + operand stack).

Core operations
- `push(x)`: add to the top
- `pop()`: remove and return the top
- `peek()`: return the top without removing
- `is_empty()`: whether stack has no items
- (optional) `size()`: number of elements

Complexity
- Typical time: $O(1)$ per operation (`push`, `pop`, `peek`).
- Space: $O(n)$ for $n$ stored elements.

Short examples

Valid parentheses (stack of opening brackets) — Python

```python
def is_valid_parentheses(s: str) -> bool:
    pairs = {')': '(', ']': '[', '}': '{'}
    stack = []

    for ch in s:
        if ch in pairs.values():
            stack.append(ch)
        elif ch in pairs:
            if not stack or stack.pop() != pairs[ch]:
                return False
        else:
            # ignore or handle invalid characters as needed
            return False

    return not stack
```

Next greater element (monotonic decreasing stack of indices) — Python

```python
def next_greater(nums):
    res = [-1] * len(nums)
    st = []  # indices, nums[st] is strictly decreasing

    for i, x in enumerate(nums):
        while st and nums[st[-1]] < x:
            res[st.pop()] = x
        st.append(i)

    return res
```

Pattern recipe: monotonic stack (next greater style)
1. Decide whether you want the stack to be monotonic increasing or decreasing.
2. Store **indices** when you need distances/ranges; store **values** when you only need comparisons.
3. While the current element breaks monotonicity, pop and resolve answers for popped items.
4. Push the current element/index.

Problems to practice
- [Valid Parentheses](https://leetcode.com/problems/valid-parentheses/)
- [Min Stack](https://leetcode.com/problems/min-stack/)
- [Daily Temperatures](https://leetcode.com/problems/daily-temperatures/)
- [Next Greater Element I](https://leetcode.com/problems/next-greater-element-i/)
- [Largest Rectangle in Histogram](https://leetcode.com/problems/largest-rectangle-in-histogram/)
