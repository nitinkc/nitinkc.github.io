---
title:  "Array Problems"
date:   2016-11-25 20:20:00
categories: Algorithms
tags: [Algorithms]
---

{% include toc title="Index" %}

For Arrays, Strings and Lists
* For Array, length is a field - `array.length`
* For String, length is a method - `str.length()`
* List length is a method = `list.size()`

### Single Pointer Technique
- Iterate through left
- Iterate through RIGHT (
  - `int idx = (arr.length-1)`
  - `int idx = list.size()-1`
- Use an ADDITIONAL ARRAY of same size (Space complexity O(N), where N = size of the array
- Optimize the additional Array to use a single variable

### Two Pointer Technique


- One begins from left/start, other from the right end.
- The while 
```java
int left = 0, right = str.length() - 1;
while(left < right){
    left++;
    right--;
}
```

{% gist nitinkc/8a3eb81f7ccf93b013a2fe8455a04703 %}


##### Left pointer and Right pointer movements based on if condition.

{% gist nitinkc/00b4970b6d3d13d6b52c7c57cc06af41 %}


##### Find count of given Sum in all pairs in the Array

Checks :
  * if array size < 2, return 0;

Approach 1 : Greedy approach to test all the possible combinations exhaustively

{% gist nitinkc/27b6ac30958dcf7a2d37d30797442603 %}

Approach 2 : Two pointer Approach - Test only those possible combinations that makes sense

{% gist nitinkc/a084561f90c18fba94ae9aab66b2d72a %}


Approach 3 : Hash map and variant approach

{% gist nitinkc/216dfdbb277577d5285334cf82c6f626 %}


##### One Fast runner the other one runs slow.


### Left & Right Array approach

Create two temporary arrays, one left that takes computation of elements to the left, upto the current element. Same for Right array.

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


### Sliding Window Approach


