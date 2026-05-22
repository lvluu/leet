# Hash Maps: Advanced Techniques

This page collects a few high-leverage hash map patterns that show up repeatedly in interview problems.

## 1) Prefix sum + hash map

This is the most important “advanced” hash map technique.

Idea
- Convert range/subarray questions into a relationship between two prefix sums.
- Use a map to remember prefix sums you’ve seen (counts or earliest indices).

### A) Count subarrays with sum = K

Let `prefix[i]` be sum of `nums[0..i]`. A subarray `(j+1..i)` sums to `k` if:

$$
prefix[i] - prefix[j] = k \Rightarrow prefix[j] = prefix[i] - k
$$

So for each prefix value `p`, the number of valid subarrays ending here is the count of `(p - k)` seen so far.

Python

```python
def subarray_sum_equals_k(nums, k):
    count = 0
    prefix = 0
    freq = {0: 1}  # empty prefix

    for x in nums:
        prefix += x
        count += freq.get(prefix - k, 0)
        freq[prefix] = freq.get(prefix, 0) + 1

    return count
```

Common pitfalls
- You must seed `freq[0] = 1`, otherwise subarrays starting at index `0` are missed.

### B) Longest subarray with sum = K

Instead of counts, store the **earliest index** where each prefix sum appears.

```python
def longest_subarray_sum_k(nums, k):
    first = {0: -1}
    prefix = 0
    best = 0

    for i, x in enumerate(nums):
        prefix += x
        if prefix not in first:
            first[prefix] = i
        j = first.get(prefix - k)
        if j is not None:
            best = max(best, i - j)

    return best
```

Rule of thumb
- Store earliest occurrence to maximize length.

## 2) Hash map + sliding window (frequency maps)

Many sliding-window problems are fundamentally “hash map problems” because the window validity depends on counts.

Typical template
- Expand `right`, update counts.
- While invalid, shrink from `left`, update counts.
- Track best answer.

Example: longest substring with at most K distinct

```python
def longest_k_distinct(s: str, k: int) -> int:
    freq = {}
    left = 0
    best = 0

    for right, ch in enumerate(s):
        freq[ch] = freq.get(ch, 0) + 1

        while len(freq) > k:
            c = s[left]
            freq[c] -= 1
            if freq[c] == 0:
                del freq[c]
            left += 1

        best = max(best, right - left + 1)

    return best
```

## 3) Grouping / bucketing

When you need to group items by an attribute, use a map:
- `signature -> list`
- `category -> running aggregate`

Examples
- Group anagrams: `sorted(word)` or 26-count signature as key.
- Group by domain / user / date: `key -> list of events`.

Note
- Sorting strings costs $O(m \log m)$. For fixed alphabets, a 26-count tuple key is $O(m)$.

## 4) Set/map for “seen states”

Use a set (or map) to prevent revisiting states:
- Detect duplicates.
- Graph/DFS/BFS visited tracking.
- Cycle detection for sequences (e.g., “Happy Number”).

## 5) Choosing the right key

Good keys are:
- Immutable (hashable)
- Minimal (avoid storing huge objects)
- Comparable by value (not identity)

Common key patterns
- Tuples for coordinates: `(r, c)`
- Canonical forms: normalized strings, sorted pairs, reduced fractions
- Counters as tuples for fixed alphabets

Problems to practice
- [Subarray Sum Equals K](https://leetcode.com/problems/subarray-sum-equals-k/)
- [Binary Subarrays With Sum](https://leetcode.com/problems/binary-subarrays-with-sum/)
- [Continuous Subarray Sum](https://leetcode.com/problems/continuous-subarray-sum/) (prefix sum mod)
- [Group Anagrams](https://leetcode.com/problems/group-anagrams/)
- [Longest Substring with At Most K Distinct Characters](https://leetcode.com/problems/longest-substring-with-at-most-k-distinct-characters/)
