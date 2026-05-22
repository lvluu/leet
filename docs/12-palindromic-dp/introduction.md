# Introduction to Palindromic Subsequence (Dynamic Programming)

The **Palindromic DP** pattern solves problems involving palindromes in strings using dynamic programming. Key problems include finding the longest palindromic subsequence, substring, counting palindromes, and minimum deletions to make a palindrome.

## Visual Example

### Longest Palindromic Subsequence DP Table
![Palindromic DP](../assets/palindromic-dp/palindrome_dp.gif)

`dp[i][j]` represents the length of the longest palindromic subsequence in `s[i:j+1]`. We fill the table diagonally, expanding from single characters to the full string.

## Key Insight

For a string `s[i..j]`:
- If `s[i] == s[j]`: Both characters can be part of the palindrome
- If `s[i] != s[j]`: Try excluding either end

## When to Use

- Longest palindromic subsequence (LPS).
- Longest palindromic substring.
- Count palindromic substrings.
- Minimum insertions/deletions to make palindrome.
- Palindrome partitioning.

## Pattern Recipe

1. **Define state**: `dp[i][j]` = answer for substring `s[i..j]`.
2. **Base case**: Single characters are palindromes of length 1.
3. **Transition**:
   - If `s[i] == s[j]`: Extend from inner substring
   - Else: Take best of excluding either end
4. **Fill order**: Diagonally (by length) or bottom-up.
5. **Answer**: `dp[0][n-1]` for full string.

## Complexity

- Time: $O(n^2)$ — filling n×n table
- Space: $O(n^2)$ for table, or $O(n)$ with optimization

## Short Examples — Python

### Longest Palindromic Subsequence (LPS)

```python
def longest_palindrome_subseq(s: str) -> int:
    n = len(s)
    dp = [[0] * n for _ in range(n)]

    # Base case: single characters
    for i in range(n):
        dp[i][i] = 1

    # Fill by increasing length
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1

            if s[i] == s[j]:
                dp[i][j] = dp[i+1][j-1] + 2
            else:
                dp[i][j] = max(dp[i+1][j], dp[i][j-1])

    return dp[0][n-1]

# Example: "bbbab" → 4 ("bbbb")
```

### Space-Optimized LPS

```python
def longest_palindrome_subseq_optimized(s: str) -> int:
    n = len(s)
    dp = [1] * n  # Current row
    prev = [0] * n  # Previous row

    for i in range(n - 2, -1, -1):
        prev, dp = dp, prev
        dp[i] = 1

        for j in range(i + 1, n):
            if s[i] == s[j]:
                dp[j] = prev[j-1] + 2
            else:
                dp[j] = max(prev[j], dp[j-1])

    return dp[n-1]
```

### Longest Palindromic Substring

```python
def longest_palindrome_substring(s: str) -> str:
    n = len(s)
    if n == 0:
        return ""

    # dp[i][j] = True if s[i:j+1] is palindrome
    dp = [[False] * n for _ in range(n)]
    start, max_len = 0, 1

    # Base: single characters
    for i in range(n):
        dp[i][i] = True

    # Base: two characters
    for i in range(n - 1):
        if s[i] == s[i+1]:
            dp[i][i+1] = True
            start, max_len = i, 2

    # Length 3 and above
    for length in range(3, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1

            if s[i] == s[j] and dp[i+1][j-1]:
                dp[i][j] = True
                start, max_len = i, length

    return s[start:start + max_len]

# Example: "babad" → "bab" or "aba"
```

### Expand Around Center (O(1) space for substring)

```python
def longest_palindrome_expand(s: str) -> str:
    def expand(left: int, right: int) -> str:
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left -= 1
            right += 1
        return s[left + 1:right]

    result = ""
    for i in range(len(s)):
        # Odd length palindrome
        odd = expand(i, i)
        if len(odd) > len(result):
            result = odd

        # Even length palindrome
        even = expand(i, i + 1)
        if len(even) > len(result):
            result = even

    return result
```

### Count Palindromic Substrings

```python
def count_palindromic_substrings(s: str) -> int:
    n = len(s)
    count = 0

    # Expand around each center
    for center in range(2 * n - 1):
        left = center // 2
        right = left + center % 2

        while left >= 0 and right < n and s[left] == s[right]:
            count += 1
            left -= 1
            right += 1

    return count

# Example: "aaa" → 6 ("a", "a", "a", "aa", "aa", "aaa")
```

### Minimum Deletions to Make Palindrome

```python
def min_deletions_palindrome(s: str) -> int:
    """
    Minimum deletions = len(s) - LPS length
    """
    return len(s) - longest_palindrome_subseq(s)

# Example: "abcda" → 2 (delete 'b' and 'c' → "ada")
```

### Minimum Insertions to Make Palindrome

```python
def min_insertions_palindrome(s: str) -> int:
    """
    Same as minimum deletions (insert what's missing).
    """
    return len(s) - longest_palindrome_subseq(s)
```

### Palindrome Partitioning (Minimum Cuts)

```python
def min_cut(s: str) -> int:
    n = len(s)

    # is_palindrome[i][j] = True if s[i:j+1] is palindrome
    is_palindrome = [[False] * n for _ in range(n)]
    for i in range(n):
        is_palindrome[i][i] = True
    for i in range(n - 1):
        is_palindrome[i][i+1] = (s[i] == s[i+1])
    for length in range(3, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            is_palindrome[i][j] = (s[i] == s[j] and is_palindrome[i+1][j-1])

    # dp[i] = min cuts for s[0:i+1]
    dp = list(range(n))  # Worst case: cut after each char

    for i in range(n):
        if is_palindrome[0][i]:
            dp[i] = 0
        else:
            for j in range(i):
                if is_palindrome[j+1][i]:
                    dp[i] = min(dp[i], dp[j] + 1)

    return dp[n-1]

# Example: "aab" → 1 (cut into "aa" | "b")
```

## Common Recurrences

| Problem | Recurrence |
|---------|------------|
| LPS Length | `dp[i][j] = dp[i+1][j-1] + 2` if match, else `max(dp[i+1][j], dp[i][j-1])` |
| Is Palindrome | `dp[i][j] = (s[i]==s[j]) and dp[i+1][j-1]` |
| Count Substrings | Expand from each center |
| Min Deletions | `n - LPS` |

## Common Pitfalls

- Wrong fill order (must fill shorter substrings first).
- Off-by-one errors with substring indices.
- Forgetting base cases for length 1 and 2.
- Confusing subsequence (non-contiguous) with substring (contiguous).

## Problems to Practice

- [Longest Palindromic Subsequence](https://leetcode.com/problems/longest-palindromic-subsequence/)
- [Longest Palindromic Substring](https://leetcode.com/problems/longest-palindromic-substring/)
- [Palindromic Substrings](https://leetcode.com/problems/palindromic-substrings/)
- [Minimum Insertion Steps to Make a String Palindrome](https://leetcode.com/problems/minimum-insertion-steps-to-make-a-string-palindrome/)
- [Palindrome Partitioning II](https://leetcode.com/problems/palindrome-partitioning-ii/)
