---
title:  "Arrays"
date:   2016-11-25 20:20:00
categories: ['Data Structures']
tags: ['Data Structures']
---

{% include toc title="Index" %}

## Arrays Patterns

    1. Two Pointer Technique
       1. One Fast runner the other one runs slow.
       2. One begins from start, other from the end.

{% gist nitinkc/8a3eb81f7ccf93b013a2fe8455a04703 %}



##### Find count of given Sum in all pairs in the Array

Checks :

  * if array size < 2, return 0;

Approach 1 : Greedy approach to test all the possible combinations exhaustively

```java
// O(n^2)

 for (int i = 0; i < arr.length; i++){
    for (int j = i + 1; j < arr.lenght; j++){
        if (arr[i] + arr[j] == sum){
            count++;
        }
    }
 }
 return count;
```

Approach 2 : Two pointer Approach - Test only those possible combinations that makes sense

{% gist nitinkc/a084561f90c18fba94ae9aab66b2d72a %}


Approach 3 : Hash map and variant approach

{% gist nitinkc/216dfdbb277577d5285334cf82c6f626 %}


### Left & Right Array approach

Create two temporary arrays, one left that takes computation of elements to the left, upto the current element. Same for Right array.

##### Replace each element with the greatest element to the Right in an Array

[https://leetcode.com/problems/replace-elements-with-greatest-element-on-right-side/](https://leetcode.com/problems/replace-elements-with-greatest-element-on-right-side/)

{% gist nitinkc/c326860cffb8fc3cf2d87c193cc0a33d %}


##### Relace a number with product of all other without division

[https://leetcode.com/problems/product-of-array-except-self/](https://leetcode.com/problems/product-of-array-except-self/)

{% gist nitinkc/2f07a7eab2eaffc1609fbc7211eadb1a %}


##### Trapping Rain Water

[Trapping Rain Water Problem](https://leetcode.com/problems/trapping-rain-water/)

```java
left[i] = Math.max(left[i-1], arr[i]);
right[i] = math.max(right[i+1], arr[i]);
result = result + Math.min(left[i],right[i]) - arr[i];
```

{% gist nitinkc/ba5c2731c23b85a89eb5dd71636d01d0 %}
