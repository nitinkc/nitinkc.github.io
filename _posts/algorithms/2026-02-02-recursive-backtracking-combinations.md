---
title: Recursive Backtracking - Combinations
date: 2026-02-03 13:05:00
categories:
- Algorithms
tags:
- Recursion
- Backtracking
---

{% include toc title="Index" %}

### Pattern 4: Combinations

```
Pick k elements from n, order doesn't matter
Key: Start from current index (avoid [1,2] and [2,1])
Branches: C(n,k)
```

What distinguishes a combination from a subset?
- Combinations always have a specified **size**, unlike subsets (which can be **any size**)
- We can think of combinations as **"subsets with constraints"**

**Decision** at each step (each level of the tree):
- Are we going to include a given element in our combination?
     
**Options** at each decision (branches from each node):
- Include element
- Don’t include element

Information we need to store along the way:
- The combination you’ve built so far
- The remaining elements to choose from
- **The remaining number of spots left to fill**


**Recursive case:**
- Choose: Pick an element in remaining.
- Explore: Try including and excluding the element and store resulting sets.
- Return the combined returned sets from **both inclusion and exclusion**.

**Base cases:**
- No more remaining elements to choose from → return empty set
- No more space in chosen (k is maxed out) → return set with chosen

### Example: Generate All Combinations of Size k


```java
import java.util.*;

public class CombinationGenerator {
    // Main method to generate all combinations of size k
    public static List<List<String>> generateCombinations(Set<String> masterSet, int k) {
        List<List<String>> result = new ArrayList<>();
        List<String> chosen = new ArrayList<>();
        listSubsetsRec(new ArrayList<>(masterSet), 0, k, chosen, result);
        return result;
    }
    
    // Recursive helper method
    private static void listSubsetsRec(List<String> masterList, int index, int size, 
                                       List<String> chosen, List<List<String>> result) {
        // Base case 1: Found a valid combination of size k
        if (size == 0) {
            result.add(new ArrayList<>(chosen)); // Add current combination to result
            return;
        }
        
        // Base case 2: Not enough elements remaining to fill the combination
        if (index == masterList.size()) {
            return;
        }
        
        String element = masterList.get(index);
        
        // Choice 1: Exclude the current element
        listSubsetsRec(masterList, index + 1, size, chosen, result);
        
        // Choice 2: Include the current element
        chosen.add(element);
        listSubsetsRec(masterList, index + 1, size - 1, chosen, result);
        chosen.remove(chosen.size() - 1); // Backtrack: undo the choice
    }
}
```

**Example Usage**:
```java
Set<String> masterSet = new HashSet<>(Arrays.asList("A", "B", "C", "D"));
int k = 2;
List<List<String>> allCombinations = CombinationGenerator.generateCombinations(masterSet, k);

// Output (all 2-combinations of {A, B, C, D}):
// [A, B]
// [A, C]
// [A, D]
// [B, C]
// [B, D]
// [C, D]
```

**Key Differences from Pseudocode → Java:**
1. **Size tracking**: Instead of decrementing `size` in the pseudocode, we pass `size - 1` to count down to 0
2. **Base cases**: We check both `size == 0` (found a combination) and `index == masterList.size()` (no more elements)
3. **No Set arithmetic**: Use index-based iteration instead of `set - element`
4. **Backtracking**: After exploring with the element included, we remove it from `chosen`
5. **Result collection**: Return `List<List<String>>` instead of printing

**Recursion Tree Example** for combinations of size 2 from {A, B, C}:
```
                    root(k=2)
                   /        \
            exclude A      include A
               /               \
          (k=2,idx=1)      (k=1,idx=1)
          /      \           /      \
     exclude B  include B  exclude B  include B
       /           \         /           \
   (k=2,idx=2)  [A,B]    (k=1,idx=2)  [A,B]
      /                      /
  exclude C              exclude C
    /                         /
(k=2,idx=3) ✓           (k=1,idx=3) ✓
           return [B,C]           return [A,C]
```

---
**Pseudocode**
```java
Set<Set<string>> combinationsRec(Set<String> remaining, int k, Set<String> chosen)
```


