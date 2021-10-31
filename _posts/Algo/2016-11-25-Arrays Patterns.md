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
