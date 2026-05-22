# Introduction to Hash Tables (Hash Maps)

A **hash table** (often called a **hash map**, **dictionary**, or **hashtable**) stores **key → value** pairs and supports fast lookup, insert, and delete.

At a high level:
- A **hash function** converts a key into an array index (a “bucket”).
- Keys that map to the same bucket cause a **collision**, handled by chaining (lists) or open addressing.
- When the table gets “too full” (high **load factor**), it **resizes** and rehashes entries.

In interview problems, you typically use a hash map to trade a bit of memory for a big speedup.

When to use
- You need **fast membership tests**: “Have I seen this before?”
- You need **counts/frequencies** of elements (characters, numbers, words).
- You need to map items to **latest index / first index / best-so-far value**.
- You want to detect duplicates or maintain a **running set** of visited states.
- You need to solve problems like Two Sum in $O(n)$.

Common variants
- Frequency map: `value -> count`
- Index map: `value -> index` (often first seen or last seen)
- Set: `value -> True` (or use a real set)
- Multi-map: `key -> list of values` (grouping)

Pattern recipes

1) Frequency counting
1. Create a map `count`.
2. For each item `x`: `count[x] += 1`.
3. Use the map to compute the answer (max frequency, first unique, etc.).

2) “Seen so far” / complement lookup (Two Sum style)
1. Create a map from value to index.
2. For each `x` at index `i`, compute `need = target - x`.
3. If `need` exists in the map, you found a pair; otherwise store `x -> i`.

3) Track best/earliest occurrence
1. Keep a map from key to earliest index/value.
2. Update the answer using the stored occurrence before overwriting.

Complexity
- Average time: $O(1)$ per `get`/`set`/`delete` (amortized).
- Worst-case time: $O(n)$ (pathological collisions), but most standard libraries mitigate this.
- Space: $O(n)$ for $n$ stored keys.

Short examples

Two Sum (value -> index) — Python

```python
def two_sum(nums, target):
    seen = {}  # value -> index
    for i, x in enumerate(nums):
        need = target - x
        if need in seen:
            return [seen[need], i]
        seen[x] = i
    return None
```

First non-repeating character (frequency map) — Python

```python
def first_unique_char(s: str) -> int:
    freq = {}
    for ch in s:
        freq[ch] = freq.get(ch, 0) + 1

    for i, ch in enumerate(s):
        if freq[ch] == 1:
            return i
    return -1
```

Group anagrams (signature -> list of strings) — Python

```python
def group_anagrams(strs):
    groups = {}
    for word in strs:
        key = "".join(sorted(word))
        groups.setdefault(key, []).append(word)
    return list(groups.values())
```

Common pitfalls
- Using a mutable key type (e.g., a list) as a key—keys must be hashable/immutable.
- Forgetting collisions exist conceptually (even if your language hides them).
- Off-by-one with “earliest/last index” maps; decide up front whether to store first or last.

Problems to practice
- [Two Sum](https://leetcode.com/problems/two-sum/)
- [First Unique Character in a String](https://leetcode.com/problems/first-unique-character-in-a-string/)
- [Valid Anagram](https://leetcode.com/problems/valid-anagram/)
- [Group Anagrams](https://leetcode.com/problems/group-anagrams/)
- [Ransom Note](https://leetcode.com/problems/ransom-note/)
- [Subarray Sum Equals K](https://leetcode.com/problems/subarray-sum-equals-k/) (prefix sum + map)
