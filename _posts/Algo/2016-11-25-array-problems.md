---
title:  "Array Problems"
date:   2016-11-25 20:20:00
categories: Algorithms
tags: [Algorithms]
---

{% include toc title="Index" %}

For Arrays, Strings and Lists
* For Array, **length** is a field - `array.length`
* For String, **length** is a method - `str.length()`
* List has a **size** method = `list.size()`

# Single Pointer Technique
- Iterate through LEFT
  - `int idx = 0`
- Iterate through RIGHT
    - `int idx = arr.length-1`
    - `int idx = list.size()-1`
- Use an ADDITIONAL ARRAY of same size (Space complexity O(N), where N = size of
  the array
- Optimize the additional Array to use a single variable

# Two Pointer Technique
- One begins from left/start, other from the right end.
- The while loop with `left < right`
  ```java
  int left = 0, right = str.length() - 1;
  while(left < right){
      left++;
      right--;
    }
  ```
- The for loop
  ```java
  for(int low = 0, high = s.length-1; low < high; low++,high--){
  ```
  
#### 2 pointer movements with/without if condition.
{% gist nitinkc/8a3eb81f7ccf93b013a2fe8455a04703 %}

[Container With Most Water](https://leetcode.com/problems/container-with-most-water/description/){:target="_blank"}
{% gist nitinkc/00b4970b6d3d13d6b52c7c57cc06af41 %}

#### 2-Sum Problem  

##### **count** of given Sum in all pairs in the Array

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

##### 2-Sum with indices to be returned
**Approach 3** : Hash map and variant approach
- 2-Sum problem with index to be returned
- [Two Sum](https://leetcode.com/problems/two-sum/description/)
- The array can't be sorted (`Arrays.sort`) as the index can't be changed
- Use a hashmap to keep track of the indices with the diff involved
{% gist nitinkc/e68ab190b3ae9babcb140cb02b0525b2 %}
- {% gist nitinkc/216dfdbb277577d5285334cf82c6f626 %}


### Search in Rotated Sorted Array
{% gist nitinkc/f0ac783652a74a2fdcdf91b0285da6f7 %}

### Left & Right Array approach
Create two temporary arrays, 
- one left that takes computation of elements to the left, upto the current element. 
- Same for Right array.

##### Replace each element with the greatest element to the Right in an Array
[https://leetcode.com/problems/replace-elements-with-greatest-element-on-right-side/](https://leetcode.com/problems/replace-elements-with-greatest-element-on-right-side/)

{% gist nitinkc/c326860cffb8fc3cf2d87c193cc0a33d %}

##### Replace a number with product of all other without division
[https://leetcode.com/problems/product-of-array-except-self/](https://leetcode.com/problems/product-of-array-except-self/)

{% gist nitinkc/2f07a7eab2eaffc1609fbc7211eadb1a %}

##### Trapping Rain Water

[Trapping Rain Water Problem](https://leetcode.com/problems/trapping-rain-water/)

```java
left[i] = Math.max(left[i-1], arr[i]);//arr[i] means including current element
right[i] = Math.max(right[i+1], arr[i]);
result = result + Math.min(left[i],right[i]) - arr[i];
```

{% gist nitinkc/ba5c2731c23b85a89eb5dd71636d01d0 %}

# Sliding Window Approach
