# Implementing Stack Data Structure

A stack can be implemented in multiple ways. The most common are:
- **Dynamic array / list-based stack** (fast and simple)
- **Linked-list-based stack** (useful when you want explicit node control)

The stack API
A minimal stack typically supports:
- `push(x)`
- `pop()`
- `peek()`
- `is_empty()`
- (optional) `size()`

Implementation 1: list-based stack (Python)

In Python, a plain list is a great stack:
- `append(x)` is `push`
- `pop()` is `pop`

```python
class Stack:
    def __init__(self):
        self._data = []

    def push(self, x):
        self._data.append(x)

    def pop(self):
        if not self._data:
            raise IndexError("pop from empty stack")
        return self._data.pop()

    def peek(self):
        if not self._data:
            raise IndexError("peek from empty stack")
        return self._data[-1]

    def is_empty(self) -> bool:
        return len(self._data) == 0

    def size(self) -> int:
        return len(self._data)
```

Notes
- Prefer `list.append` / `list.pop()` from the **end** for $O(1)$ amortized behavior.
- Avoid `insert(0, x)` / `pop(0)` for stack behavior; those are $O(n)$.

Complexity
- `push`: $O(1)$ amortized
- `pop`: $O(1)$ amortized
- `peek`: $O(1)$
- space: $O(n)$

Implementation 2: linked-list stack (Python)

A linked list stack keeps a pointer to the top node.

```python
class _Node:
    __slots__ = ("val", "next")

    def __init__(self, val, next=None):
        self.val = val
        self.next = next


class LinkedStack:
    def __init__(self):
        self._top = None
        self._size = 0

    def push(self, x):
        self._top = _Node(x, self._top)
        self._size += 1

    def pop(self):
        if self._top is None:
            raise IndexError("pop from empty stack")
        x = self._top.val
        self._top = self._top.next
        self._size -= 1
        return x

    def peek(self):
        if self._top is None:
            raise IndexError("peek from empty stack")
        return self._top.val

    def is_empty(self) -> bool:
        return self._top is None

    def size(self) -> int:
        return self._size
```

Complexity
- All operations are $O(1)$ worst-case.
- Space is $O(n)$, plus per-node overhead.

Common pitfalls
- Returning `None` on empty `pop()`/`peek()` can hide bugs; raising an error is clearer.
- Accidentally implementing a queue by popping from the front of a list (`pop(0)`) causes $O(n)$ operations.
- Storing values instead of indices in monotonic-stack problems can block you from computing spans/distances.

Quick usage example

```python
s = Stack()

s.push(10)
s.push(20)
assert s.peek() == 20
assert s.pop() == 20
assert s.pop() == 10
assert s.is_empty()
```

Problems to practice
- [Implement Stack using Queues](https://leetcode.com/problems/implement-stack-using-queues/)
- [Evaluate Reverse Polish Notation](https://leetcode.com/problems/evaluate-reverse-polish-notation/)
- [Simplify Path](https://leetcode.com/problems/simplify-path/)
- [Decode String](https://leetcode.com/problems/decode-string/)
