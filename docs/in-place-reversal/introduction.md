# Introduction to In-place Reversal of a Linked List Pattern

The **In-place Reversal of a Linked List** pattern focuses on reversing pointers inside a linked list without allocating additional data structures.

Instead of copying values into an array/stack, you **re-wire** `next` pointers as you traverse.

When to use
- You need to reverse an entire linked list or a portion of it.
- You’re asked to reverse nodes in groups (e.g., every $k$ nodes).
- The constraints suggest **$O(1)$ extra space**, and mutating the list is allowed.

Common variants
- Reverse the whole list.
- Reverse a sub-list between positions `p` and `q`.
- Reverse nodes in groups of size `k`.
- Reverse alternating groups of size `k`.
- Rotate a list (often uses partial reversal or careful pointer rewiring).

Pattern recipe (reverse a segment)
1. Walk the list to reach the node just **before** the segment you want to reverse.
2. Reverse the pointers inside the segment using the standard 3-pointer technique:
   - `prev`, `current`, `next`.
3. Reconnect:
   - The node before the segment → new head of reversed segment.
   - The tail of the reversed segment → the node after the segment.

Core reversal loop
- Keep a `prev` pointer.
- Iteratively move `current.next` to point to `prev`.
- Advance all pointers forward.

Complexity
- Time: $O(n)$ — each node is processed a constant number of times.
- Space: $O(1)$ extra space.

Short examples

Reverse a linked list (Python)

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def reverse_list(head: ListNode | None) -> ListNode | None:
    prev = None
    current = head

    while current:
        nxt = current.next
        current.next = prev
        prev = current
        current = nxt

    return prev
```

Reverse a sub-list from position `p` to `q` (1-indexed) — Python

```python
def reverse_sub_list(head: ListNode | None, p: int, q: int) -> ListNode | None:
    if not head or p == q:
        return head

    current, prev = head, None

    # 1) Skip first p-1 nodes
    for _ in range(p - 1):
        prev = current
        current = current.next

    # current is now at p
    last_node_of_first_part = prev
    last_node_of_sub_list = current

    # 2) Reverse nodes between p and q
    nxt = None
    for _ in range(q - p + 1):
        nxt = current.next
        current.next = prev
        prev = current
        current = nxt

    # 3) Connect with the first part
    if last_node_of_first_part:
        last_node_of_first_part.next = prev
    else:
        head = prev

    # 4) Connect with the remaining part
    last_node_of_sub_list.next = current

    return head
```

Reverse nodes in groups of size `k` (outline) — Python

```python
def reverse_k_group(head: ListNode | None, k: int) -> ListNode | None:
    if k <= 1 or not head:
        return head

    dummy = ListNode(0, head)
    group_prev = dummy

    while True:
        # Find the kth node from group_prev
        kth = group_prev
        for _ in range(k):
            kth = kth.next
            if not kth:
                return dummy.next

        group_next = kth.next

        # Reverse the group
        prev, current = group_next, group_prev.next
        while current != group_next:
            nxt = current.next
            current.next = prev
            prev = current
            current = nxt

        # Connect group_prev to new head of this group
        tmp = group_prev.next  # becomes the tail after reversal
        group_prev.next = kth
        group_prev = tmp
```

Problems to practice
- [Reverse Linked List](https://leetcode.com/problems/reverse-linked-list/)
- [Reverse Linked List II](https://leetcode.com/problems/reverse-linked-list-ii/)
- [Reverse Nodes in k-Group](https://leetcode.com/problems/reverse-nodes-in-k-group/)
- [Rotate List](https://leetcode.com/problems/rotate-list/)
- [Palindrome Linked List](https://leetcode.com/problems/palindrome-linked-list/) (often reverses the second half)

