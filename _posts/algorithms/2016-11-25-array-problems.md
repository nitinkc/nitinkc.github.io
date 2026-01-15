---
title: Array Problems
date: 2016-11-25 20:20:00
categories:
- Algorithms
tags:
- Arrays
- Practice
- Interview
---

{% include toc title="Index" %}


### Points to keep in Mind

{% gist nitinkc/7bed7e03f3e21790c98353df6a921137 %}

<!-- ### ArrayList
{% gist nitinkc/98b5adaf0ed85980472ec423237e9edd %} -->

### Array List API

```java
list.add (10) // Appends the specified element to the end of this list. Returns boolean
list.add(3, 10) //Inserts at index 3 Shifts current and subsequent elements to the right (adds one to their indices)int indx =  list.indexOf(10) //index of the first occurrence of the element in the list, or -1 if this list does not contain the element.
int data = list.get(3) //Returns the element at the specified position in this list.
ListIterator listIterator() //Bi directional iterator

list.set(3, 10) //Replaces the element at the specified position .Returns the previous element 
        list.remove(3) //Removes the element at the specified position in this list.
list.remove(10) //Removes the first occurrence of the specified element from this list, if it is present.
```

### 1D Arrays

{% gist nitinkc/c2abeb754d1a64641b0149bc6d8f21ae %}

### 2D Array using primitive arrays

A Rectangular 2D array has different no. of Rows and Columns (eg: 6X7)

In both cases, the row and column count is

```java
int row = arr.length;
int col = arr[0].length;
```

{% gist nitinkc/d9ca95267cae73a9145d5e96ca7d8f22 %}

The Skewed 2D array need not have the same number of Columns each Row.
{% gist nitinkc/f828994bdaabbc55505c51096c3b7d0d %}

### 2D ArrayList

Square Matrix using Arraylist with a focus on Iteration

Row count is equal to the size of the entire List

```java
row = list.size();
```

Column count is individual sublist size

```java
col = list.get(i).size();
```

{% gist nitinkc/79da313a1da762bfc0c791a1f3843305 %}


# Array Syntax

### The Arrays Class - for Arrays

#### Arrays fill

{% gist nitinkc/8a955a843d2b383d88b7ca92997c627f %}

##### Arrays.asList & List.of

Arrays.asList accepts Wrapper Class array.

```java
//Accepts arrays of Integer, Character, String etc.
List<Integer> list = Arrays.asList(arr);
```

The `Arrays.asList()` method works with objects, **not primitive** types.

```java
// Create an array
String[] array = {"apple", "banana", "orange"};

// Convert array to ArrayList using Arrays.asList()
List<String> arrayList = new ArrayList<>(Arrays.asList(array));

int[] intArray = {1,2,3};
List<Integer> a = Arrays.asList(intArray);// FOR PRIMITIVES, DOES NOT WORK, change to INTEGER
        
List<Integer> b = List.of(1,2,3);//Immutable List

//Printing an ArrayList as ann Integer
Arrays.toString(a);//op: [1,2,3]
```

To convert primitive array into a list of Wrapper class (list of primitive class
is not possible)

```java
int[] arr = {1, 2, 1, 3, 4, 5, 2, 1, 3, 4, 5, 6, 7, 8, 97, 1, 2};

 List<Integer> list = Arrays.stream(arr)// IntStream
                .boxed()// Stream<Integer>
                .collect(Collectors.toList());

list = IntStream.of(arr)//IntStream, Static Factory method
                .boxed()
                .collect(Collectors.toList());

Integer[] intAr = Arrays.stream(arr)// IntStream
                .boxed()// Stream<Integer>
                .toArray(Integer[]::new);

intAr = IntStream.of(arr)//IntStream, Static Factory method
                .boxed()
                .toArray(Integer[]::new);
```

```java
 char[] c = {'T','e','s','t'};

Character[] charArrBoxed = new String(c).chars()
                            .mapToObj(ch -> (char) ch)
                             .toArray(Character[]::new);
        
List<Character> characterList = new String(c).chars()
                .mapToObj(ch -> (char) ch)
                .collect(Collectors.toList());
```

### ArrayList to Array

```java
//Converting an ArrayList into Array
int[] result = a.toArray();
```

### Array sorting

[Sorting in Detail](https://nitinkc.github.io/java/sorting/)

Traditional Array can be sorted with sort method Arrays Utility Class.

##### Sorting an Array of primitives

```java
int[] arr = {4,5,3,8,2};
Arrays.sort(arr);
```

```java
//Sort takes array
int[] intArray = {4,5,3,8,2,71};

Arrays.sort(intArray);// Default Natural Sorting Order
Arrays.sort(integerArray, Comparator.reverseOrder());//Comparator can be used with a CLASS - Reverse sorting
        
String[] stringArray = {"one", "two", "three", "four"};
Arrays.sort(stringArray);
Arrays.sort(stringArray, Comparator.reverseOrder());
```

#### Sorting via list object

For list of type T, a comparator has to be defined.

```java
list.sort(Comparator
        .comparing(Data::getPopulation).reversed()
        .thenComparing(Data::getState)
        .thenComparing(Data::getCity));
```

```java
String[] array = {"apple", "banana", "orange"};
// Convert array to ArrayList using Arrays.asList()
List<String> arrayListString = new ArrayList<>(Arrays.asList(array));
arrayListString.sort(Comparator.naturalOrder());

List<Integer> arrayListInteger = Arrays.asList(4,5,3,8,2,71);
arrayListInteger.sort(Comparator.reverseOrder());
```

##### Sorting via Collections Class

```java
// Sort the List of Objects based on the Population
list.sort(Comparator
        .comparing(Data::getPopulation).reversed()
        .thenComparing(Data::getState)
        .thenComparing(Data::getCity));
        

//Comparator.nullsLast is null safe and takes care in case there is a null.
List<String> empList = list.stream()
        .sorted(Comparator.comparing(Employee::getSalary,Comparator.nullsLast(Comparator.naturalOrder())))
        .map(employee -> ...)
        .collect(Collectors.toList());
```

# The List Class

```java
list.sort(Comparator.naturalOrder());
list.sort(Comparator.naturalOrder());
list.stream().sorted(Comparator.comparing(s -> s.length()));

```

# Collection Class for List

```java
List<String> stringList = Arrays.asList("apple", null, null, "banana", "orange");
Collections.sort(stringList, Comparator.nullsFirst(Comparator.naturalOrder()));

List<String> stringList = Arrays.asList("apple","banana", "orange");
Collections.sort(stringList, Comparator
    .comparing(String::length)
    .thenComparing(Comparator.reverseOrder()));
```

---- 

For Arrays, Strings and Lists
* For Array, **length** is a field - `array.length`
* For String, **length** is a method - `str.length()`
* List has a **size** method = `list.size()`
* `List<int[]> list= new ArrayList<>()` List of pairs.
  * `list.sort((a,b) -> a[0] - b[0])` Sort ascending. sorting by descending , use `b[0] - a[0]`

```java
int[] a = new int[3]; // use [] for array instead of ()
int[] a = new int[] {1, 2, 3};
int[] b = {1, 2, 3}; // Same as above
```

# Single Pointer Technique
- Iterate through LEFT
  - `int idx = 0`
- Iterate through RIGHT
    - `int idx = arr.length-1`
    - `int idx = list.size()-1`
- Use an ADDITIONAL ARRAY of same size (Space complexity O(N), where N = size of the array
- Optimize the additional Array to use a single variable

# Two Pointer Technique
**Summary:**
  - problems that deals with "pairs of elements" that runs in linear time
  - One begins from left/start, other from the right end.
  - The while loop with `left < right`
    ```java
    int left = 0, right = str.length() - 1;
    while(left < right){
        left++;
        right--;
      }
    ```
  - The for loop : DO NOT PREFER
    ```java
    for(int low = 0, high = s.length-1; low < high; low++,high--){
    ```
  
#### 2 pointer movements - opposite direction
{% gist nitinkc/8a3eb81f7ccf93b013a2fe8455a04703 %}

##### Container with most water
length is the diff in indices and height is the min of the 2 values
`area = (rt-lt) * Math.min(heights[lt], heights[rt]);`
[Container With Most Water](https://leetcode.com/problems/container-with-most-water/description/){:target="_blank"}
{% gist nitinkc/00b4970b6d3d13d6b52c7c57cc06af41 %}

##### 2-Sum Problem - **count** of given Sum in all pairs in the Array

**Checks**
```java
if (array size < 2)
    return 0;
```

**Approach 1** : Greedy approach to test all the possible combinations exhaustively
{% gist nitinkc/27b6ac30958dcf7a2d37d30797442603 %}

**Approach 2** : Two pointer Approach - Test only those possible combinations that
makes sense
{% gist nitinkc/a084561f90c18fba94ae9aab66b2d72a %}

**2-Sum with indices to be returned**

**Approach 3** : Hash map and variant approach
- 2-Sum problem with index to be returned
- [Two Sum](https://leetcode.com/problems/two-sum/description/){:target="_blank"}
- The array can't be sorted (`Arrays.sort`) as the index can't be changed
- Use a hashmap to keep track of the indices with the diff involved
{% gist nitinkc/e68ab190b3ae9babcb140cb02b0525b2 %}
- {% gist nitinkc/216dfdbb277577d5285334cf82c6f626 %}

##### Search in Rotated Sorted Array
{% gist nitinkc/f0ac783652a74a2fdcdf91b0285da6f7 %}

#### 2 pointer movements - same direction


# Left & Right Array approach
Create two temporary arrays, 
- one left that takes computation of elements to the left, upto the current element. 
- Same for Right array.

##### Replace each element with the greatest element to the Right in an Array
[replace-elements-with-greatest-element-on-right-side](https://leetcode.com/problems/replace-elements-with-greatest-element-on-right-side/){:target="_blank"}

{% gist nitinkc/c326860cffb8fc3cf2d87c193cc0a33d %}

##### Replace a number with product of all other without division
[product-of-array-except-self/](https://leetcode.com/problems/product-of-array-except-self/){:target="_blank"}

{% gist nitinkc/2f07a7eab2eaffc1609fbc7211eadb1a %}

##### Trapping Rain Water
[Trapping Rain Water Problem](https://leetcode.com/problems/trapping-rain-water/){:target="_blank"}

```java
left[i] = Math.max(left[i-1], arr[i]);//arr[i] means including current element
right[i] = Math.max(right[i+1], arr[i]);
result = result + Math.min(left[i],right[i]) - arr[i];
```

{% gist nitinkc/ba5c2731c23b85a89eb5dd71636d01d0 %}

# Sliding Window Approach

### Fixed-size sliding window
`i + windowSize <= arr.length` takes care of out of bounds

```java
for(int lt = 0; lt < nums.length; lt++){
  for(int rt = lt+1; rt <= Math.min(nums.length-1, lt+k); rt++){

```

Approach A — naive: **O(n * windowSize)** where n = array length
```java
// Naive fixed-size window: recompute sum for each window
int windowSize = 3;
for (int i = 0; i + windowSize <= arr.length; i++) {
    int sum = 0;
    for (int j = i; j < i + windowSize; j++) {
        sum += arr[j];
    }
}
```

Approach B — optimized using running sum (classic sliding window): **O(n)**

```java
// Optimized: maintain running sum, add new element and remove outgoing element
int windowSize = 3;
if (windowSize <= arr.length){
    int windowSum = 0;
    // initial window
    for (int i = 0; i < windowSize; i++) 
      windowSum += arr[i];

    for (int i = k; i < arr.length; i++) {
        windowSum += arr[i];           // include new element
        windowSum -= arr[i - k];       // exclude old element
    }
}
```

Notes:
- Use the optimized approach whenever possible — it's O(n).
- Fixed-size sliding window works well for aggregations (sum, max with deque, average).

### Variable-size sliding window

Variable-size windows expand and shrink to satisfy a condition (e.g., reach at least a target sum, or keep number of distinct characters under a limit). The general pattern:

1. Expand the right end (extend window) until the condition is met.
2. When condition is satisfied, optionally record/update answer, then shrink the left end to try to find a smaller/shorter window that still satisfies the condition.

Common example 1 — Minimum-length subarray with sum >= target (positive numbers):

Problem: given positive integers array and target S, find the minimal length of a contiguous subarray with sum >= S.

Java solution (O(n)):

```java
int minSubarrayLen(int target, int[] nums) {
    int n = nums.length;
    int left = 0, sum = 0, minLen = Integer.MAX_VALUE;
    for (int right = 0; right < n; right++) {
        sum += nums[right];
        // shrink from left while condition is satisfied
        while (sum >= target) {
            minLen = Math.min(minLen, right - left + 1);
            sum -= nums[left++];
        }
    }
    return (minLen == Integer.MAX_VALUE) ? 0 : minLen;
}
```
Complexity: O(n) because each element is added and removed at most once.

Common example 2 — Longest subarray with sum <= k (non-negative numbers):

When all numbers are non-negative, you can expand right and shrink left when sum > k. This yields O(n).

Java:

```java
int longestSubarrayAtMostK(int[] nums, int k) {
    int left = 0, sum = 0, best = 0;
    for (int right = 0; right < nums.length; right++) {
        sum += nums[right];
        while (sum > k && left <= right) {
            sum -= nums[left++];
        }
        // now sum <= k
        best = Math.max(best, right - left + 1);
    }
    return best;
}
```

Notes and edge-cases:
- Variable-size sliding window usually requires non-negative numbers when using the simple expand/shrink pattern (because with negatives the monotonicity breaks — sum can go down when you expand).
- For problems with allowed negatives, consider prefix sums + data structures (multiset, balanced tree) or divide-and-conquer.
- For problems finding maximum/minimum with window, a deque (monotonic queue) is common: it keeps candidates for max/min in O(1) amortized per element.

Monotonic deque example — sliding window maximum (fixed-size):

```java
// sliding window maximum using deque (indices)
int[] maxSlidingWindow(int[] nums, int k) {
    if (k == 0) return new int[0];
    int n = nums.length;
    Deque<Integer> dq = new ArrayDeque<>(); // stores indices
    int[] res = new int[n - k + 1];
    for (int i = 0; i < n; i++) {
        // remove indices out of window
        while (!dq.isEmpty() && dq.peekFirst() <= i - k) dq.pollFirst();
        // remove smaller values from the back
        while (!dq.isEmpty() && nums[dq.peekLast()] < nums[i]) dq.pollLast();
        dq.offerLast(i);
        if (i >= k - 1) res[i - k + 1] = nums[dq.peekFirst()];
    }
    return res;
}
```

Summary / quick checklist:
- Fixed-size: prefer running-sum / deque approach (O(n)).
- Variable-size: use expand-then-shrink pattern; ensure input properties (e.g., non-negative) hold.
- If negatives present or constraints break monotonicity, fall back to prefix-sum + binary search or other DS.

### Small practice exercises
- Compute all window sums of size k (implement both naive and optimized).
- Find minimum-length subarray with sum >= S.
- Sliding window maximum using deque.
