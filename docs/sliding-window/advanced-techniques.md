# Advanced Sliding Window Techniques

This guide covers more advanced applications of the sliding window pattern, including character replacement, permutation matching, and minimum window problems.

## 1. Character Replacement Problems

These problems involve allowing a limited number of character changes to maximize a window property.

### Longest Substring with Same Letters after K Replacements

**Problem**: Given a string, find the length of the longest substring with the same letters after replacing at most `k` characters.

**Strategy**: Track the frequency of characters in the window. The number of replacements needed = window_size - max_frequency. When this exceeds `k`, shrink the window.

```python
def length_of_longest_substring(s, k):
    char_freq = {}
    left = 0
    max_len = 0
    max_repeat_count = 0
    
    for right in range(len(s)):
        char_freq[s[right]] = char_freq.get(s[right], 0) + 1
        max_repeat_count = max(max_repeat_count, char_freq[s[right]])
        
        # If replacements needed > k, shrink window
        if (right - left + 1) - max_repeat_count > k:
            char_freq[s[left]] -= 1
            left += 1
        
        max_len = max(max_len, right - left + 1)
    
    return max_len
```

**JavaScript implementation**:

```javascript
function lengthOfLongestSubstring(s, k) {
  const charFreq = new Map();
  let left = 0;
  let maxLen = 0;
  let maxRepeatCount = 0;
  
  for (let right = 0; right < s.length; right++) {
    charFreq.set(s[right], (charFreq.get(s[right]) || 0) + 1);
    maxRepeatCount = Math.max(maxRepeatCount, charFreq.get(s[right]));
    
    if ((right - left + 1) - maxRepeatCount > k) {
      charFreq.set(s[left], charFreq.get(s[left]) - 1);
      left++;
    }
    
    maxLen = Math.max(maxLen, right - left + 1);
  }
  
  return maxLen;
}
```

## 2. Permutation Matching

Finding if a permutation of a pattern exists as a substring in a larger string.

### Permutation in a String

**Problem**: Given strings `s1` and `s2`, return true if `s2` contains a permutation of `s1`.

**Strategy**: Use a fixed-size window equal to `s1.length`. Track character frequencies and compare with the pattern.

```python
def check_inclusion(s1, s2):
    if len(s1) > len(s2):
        return False
    
    s1_freq = {}
    window_freq = {}
    
    for char in s1:
        s1_freq[char] = s1_freq.get(char, 0) + 1
    
    left = 0
    matched = 0
    
    for right in range(len(s2)):
        right_char = s2[right]
        if right_char in s1_freq:
            window_freq[right_char] = window_freq.get(right_char, 0) + 1
            if window_freq[right_char] == s1_freq[right_char]:
                matched += 1
        
        if right >= len(s1):
            left_char = s2[left]
            if left_char in s1_freq:
                if window_freq[left_char] == s1_freq[left_char]:
                    matched -= 1
                window_freq[left_char] -= 1
            left += 1
        
        if matched == len(s1_freq):
            return True
    
    return False
```

## 3. Minimum Window Problems

Finding the smallest window that satisfies a condition.

### Smallest Window Containing Substring

**Problem**: Find the minimum window in string `s` that contains all characters of string `t`.

**Strategy**: Expand window to find a valid solution, then contract to minimize it.

```python
def min_window(s, t):
    if not s or not t:
        return ""
    
    target_freq = {}
    for char in t:
        target_freq[char] = target_freq.get(char, 0) + 1
    
    required = len(target_freq)
    formed = 0
    window_freq = {}
    
    left = 0
    min_len = float('inf')
    min_left = 0
    
    for right in range(len(s)):
        char = s[right]
        window_freq[char] = window_freq.get(char, 0) + 1
        
        if char in target_freq and window_freq[char] == target_freq[char]:
            formed += 1
        
        while left <= right and formed == required:
            # Update result if this window is smaller
            if right - left + 1 < min_len:
                min_len = right - left + 1
                min_left = left
            
            # Try to shrink window
            char = s[left]
            window_freq[char] -= 1
            if char in target_freq and window_freq[char] < target_freq[char]:
                formed -= 1
            left += 1
    
    return "" if min_len == float('inf') else s[min_left:min_left + min_len]
```

**Java implementation**:

```java
public String minWindow(String s, String t) {
    if (s.length() == 0 || t.length() == 0) {
        return "";
    }
    
    Map<Character, Integer> targetFreq = new HashMap<>();
    for (char c : t.toCharArray()) {
        targetFreq.put(c, targetFreq.getOrDefault(c, 0) + 1);
    }
    
    int required = targetFreq.size();
    int formed = 0;
    Map<Character, Integer> windowFreq = new HashMap<>();
    
    int left = 0, minLen = Integer.MAX_VALUE, minLeft = 0;
    
    for (int right = 0; right < s.length(); right++) {
        char c = s.charAt(right);
        windowFreq.put(c, windowFreq.getOrDefault(c, 0) + 1);
        
        if (targetFreq.containsKey(c) && 
            windowFreq.get(c).intValue() == targetFreq.get(c).intValue()) {
            formed++;
        }
        
        while (left <= right && formed == required) {
            if (right - left + 1 < minLen) {
                minLen = right - left + 1;
                minLeft = left;
            }
            
            char leftChar = s.charAt(left);
            windowFreq.put(leftChar, windowFreq.get(leftChar) - 1);
            if (targetFreq.containsKey(leftChar) && 
                windowFreq.get(leftChar) < targetFreq.get(leftChar)) {
                formed--;
            }
            left++;
        }
    }
    
    return minLen == Integer.MAX_VALUE ? "" : s.substring(minLeft, minLeft + minLen);
}
```

## 4. Subarray Product Problems

Dealing with products instead of sums requires careful handling of zeros and negative numbers.

### Subarrays with Product Less than Target

**Problem**: Find the count of contiguous subarrays where the product of all elements is less than a target value.

**Strategy**: Use a dynamic window. For each position of `right`, count all valid subarrays ending at `right`.

```python
def num_subarray_product_less_than_k(nums, k):
    if k <= 1:
        return 0
    
    product = 1
    left = 0
    count = 0
    
    for right in range(len(nums)):
        product *= nums[right]
        
        while product >= k:
            product //= nums[left]
            left += 1
        
        # All subarrays ending at right
        count += right - left + 1
    
    return count
```

## Key Insights

1. **Window state tracking**: Use appropriate data structures (maps, sets, counters) to maintain window state efficiently.

2. **Optimization trick**: In some problems (like character replacement), you don't need to update `max_repeat_count` when shrinking—it's okay if it's stale because we only care about larger windows.

3. **Counting subarrays**: When asked for count, remember that a window of size `n` contains `n` subarrays ending at the right pointer.

4. **Two conditions**: Some problems require satisfying two conditions simultaneously (e.g., substring with K distinct chars AND max frequency).

5. **Edge cases**: Always check for empty inputs, k=0 or k>n, negative numbers (for product problems).

## Practice Problems

- [Longest Substring with Same Letters after Replacement](https://leetcode.com/problems/longest-repeating-character-replacement/) (hard)
- [Longest Subarray with Ones after Replacement](https://leetcode.com/problems/max-consecutive-ones-iii/) (hard)
- [Permutation in a String](https://leetcode.com/problems/permutation-in-string/) (hard)
- [String Anagrams](https://leetcode.com/problems/find-all-anagrams-in-a-string/) (hard)
- [Smallest Window containing Substring](https://leetcode.com/problems/minimum-window-substring/) (hard)
- [Words Concatenation](https://leetcode.com/problems/substring-with-concatenation-of-all-words/) (hard)
- [Subarrays with Product Less than a Target](https://leetcode.com/problems/subarray-product-less-than-k/) (hard)
