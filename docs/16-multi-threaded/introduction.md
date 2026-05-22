# Introduction to Multi-threaded Pattern

The **Multi-threaded** pattern covers concurrent programming techniques for solving problems that benefit from parallel execution. This includes thread synchronization, parallel algorithms, and concurrent data structure access.

## Visual Example

### Parallel Tree Traversal
![Multi-threaded execution](../assets/multi-threaded/parallel_execution.gif)

Multiple threads can process independent subtrees simultaneously. Synchronization ensures correctness when combining results.

## Key Concepts

### Thread vs Process
- **Thread**: Lightweight, shares memory with other threads
- **Process**: Heavyweight, isolated memory space

### Concurrency vs Parallelism
- **Concurrency**: Managing multiple tasks (may interleave)
- **Parallelism**: Executing multiple tasks simultaneously (requires multiple cores)

## When to Use

- CPU-bound tasks that can be divided (tree/graph traversal).
- I/O-bound tasks (parallel API calls, file reads).
- Producer-consumer scenarios.
- Problems explicitly asking for concurrent solutions.
- Embarrassingly parallel problems (independent subproblems).

## Python Threading Basics

```python
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

# Basic thread
def worker(name):
    print(f"Thread {name} running")

thread = threading.Thread(target=worker, args=("A",))
thread.start()
thread.join()  # Wait for completion

# Thread pool
with ThreadPoolExecutor(max_workers=4) as executor:
    futures = [executor.submit(worker, i) for i in range(4)]
    for future in as_completed(futures):
        result = future.result()
```

## Synchronization Primitives

| Primitive | Use Case |
|-----------|----------|
| Lock/Mutex | Mutual exclusion (one thread at a time) |
| Semaphore | Limit concurrent access (N threads) |
| Condition | Wait for specific condition |
| Event | Signal between threads |
| Barrier | Wait for all threads to reach point |

## Short Examples — Python

### Same Tree (Parallel Comparison)

```python
from concurrent.futures import ThreadPoolExecutor

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def is_same_tree_parallel(p: TreeNode, q: TreeNode) -> bool:
    if not p and not q:
        return True
    if not p or not q or p.val != q.val:
        return False

    with ThreadPoolExecutor(max_workers=2) as executor:
        left_future = executor.submit(is_same_tree_parallel, p.left, q.left)
        right_future = executor.submit(is_same_tree_parallel, p.right, q.right)

        return left_future.result() and right_future.result()
```

### Invert Binary Tree (Parallel)

```python
from concurrent.futures import ThreadPoolExecutor

def invert_tree_parallel(root: TreeNode) -> TreeNode:
    if not root:
        return None

    with ThreadPoolExecutor(max_workers=2) as executor:
        left_future = executor.submit(invert_tree_parallel, root.left)
        right_future = executor.submit(invert_tree_parallel, root.right)

        root.left = right_future.result()
        root.right = left_future.result()

    return root
```

### Producer-Consumer Pattern

```python
import threading
from queue import Queue

def producer(queue: Queue, items: list):
    for item in items:
        queue.put(item)
        print(f"Produced: {item}")
    queue.put(None)  # Sentinel to signal completion

def consumer(queue: Queue, results: list):
    while True:
        item = queue.get()
        if item is None:
            break
        results.append(item * 2)  # Process item
        print(f"Consumed: {item}")

queue = Queue()
results = []

prod_thread = threading.Thread(target=producer, args=(queue, [1, 2, 3, 4, 5]))
cons_thread = threading.Thread(target=consumer, args=(queue, results))

prod_thread.start()
cons_thread.start()

prod_thread.join()
cons_thread.join()

print(results)  # [2, 4, 6, 8, 10]
```

### Thread-Safe Counter (with Lock)

```python
import threading

class ThreadSafeCounter:
    def __init__(self):
        self.count = 0
        self.lock = threading.Lock()

    def increment(self):
        with self.lock:
            self.count += 1

    def get(self) -> int:
        with self.lock:
            return self.count

# Usage
counter = ThreadSafeCounter()

def worker():
    for _ in range(1000):
        counter.increment()

threads = [threading.Thread(target=worker) for _ in range(10)]
for t in threads:
    t.start()
for t in threads:
    t.join()

print(counter.get())  # 10000
```

### Parallel Merge Sort

```python
from concurrent.futures import ThreadPoolExecutor

def parallel_merge_sort(arr: list, depth: int = 0, max_depth: int = 2) -> list:
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2

    if depth < max_depth:
        with ThreadPoolExecutor(max_workers=2) as executor:
            left_future = executor.submit(parallel_merge_sort, arr[:mid], depth + 1, max_depth)
            right_future = executor.submit(parallel_merge_sort, arr[mid:], depth + 1, max_depth)
            left = left_future.result()
            right = right_future.result()
    else:
        # Sequential at deeper levels (thread overhead not worth it)
        left = parallel_merge_sort(arr[:mid], depth + 1, max_depth)
        right = parallel_merge_sort(arr[mid:], depth + 1, max_depth)

    return merge(left, right)

def merge(left: list, right: list) -> list:
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result
```

### BST Iterator (Thread-Safe)

```python
import threading

class BSTIterator:
    def __init__(self, root: TreeNode):
        self.stack = []
        self.lock = threading.Lock()
        self._push_left(root)

    def _push_left(self, node: TreeNode):
        while node:
            self.stack.append(node)
            node = node.left

    def next(self) -> int:
        with self.lock:
            node = self.stack.pop()
            self._push_left(node.right)
            return node.val

    def has_next(self) -> bool:
        with self.lock:
            return len(self.stack) > 0
```

### Parallel Web Requests

```python
from concurrent.futures import ThreadPoolExecutor, as_completed
import urllib.request

def fetch_url(url: str) -> tuple[str, str]:
    try:
        response = urllib.request.urlopen(url, timeout=5)
        return url, response.read()[:100].decode()
    except Exception as e:
        return url, str(e)

urls = [
    "https://example.com",
    "https://httpbin.org/get",
    "https://jsonplaceholder.typicode.com/posts/1"
]

with ThreadPoolExecutor(max_workers=3) as executor:
    future_to_url = {executor.submit(fetch_url, url): url for url in urls}

    for future in as_completed(future_to_url):
        url, result = future.result()
        print(f"{url}: {result[:50]}...")
```

## Common Pitfalls

### Race Conditions
```python
# BAD - Race condition
count = 0
def increment():
    global count
    count += 1  # Not atomic!

# GOOD - Use lock
lock = threading.Lock()
def safe_increment():
    global count
    with lock:
        count += 1
```

### Deadlock
```python
# BAD - Potential deadlock
def transfer(from_acc, to_acc, amount):
    with from_acc.lock:
        with to_acc.lock:  # If another thread locks in opposite order = deadlock
            pass

# GOOD - Consistent lock ordering
def safe_transfer(acc1, acc2, amount):
    first, second = sorted([acc1, acc2], key=id)
    with first.lock:
        with second.lock:
            pass
```

## Python GIL Note

Python's Global Interpreter Lock (GIL) means only one thread executes Python bytecode at a time. Threading helps with:
- I/O-bound tasks (waiting for network, disk)
- Calling C extensions that release GIL

For CPU-bound parallelism, use:
- `multiprocessing` module
- NumPy (releases GIL for array operations)
- `concurrent.futures.ProcessPoolExecutor`

## Thread Safety Checklist

- [ ] Protect shared mutable state with locks
- [ ] Use thread-safe data structures (Queue, etc.)
- [ ] Avoid shared state when possible
- [ ] Use consistent lock ordering to prevent deadlocks
- [ ] Consider using higher-level abstractions (ThreadPoolExecutor)

## Problems to Practice

- [Print in Order](https://leetcode.com/problems/print-in-order/)
- [Print FooBar Alternately](https://leetcode.com/problems/print-foobar-alternately/)
- [Building H2O](https://leetcode.com/problems/building-h2o/)
- [The Dining Philosophers](https://leetcode.com/problems/the-dining-philosophers/)
- [Fizz Buzz Multithreaded](https://leetcode.com/problems/fizz-buzz-multithreaded/)
- [Web Crawler Multithreaded](https://leetcode.com/problems/web-crawler-multithreaded/)
