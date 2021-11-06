---
# layout: static
title:  "Searching"
date:   2021-04-16 01:25:00
categories: Algorithms
tags: [Algorithms]
---

# Searching

Liner Search :

Binary Search : O(log n). n,n/2,n/4,n/8,....

Pre processing over head. Elements need to be in sorted order.

Pick the middle element and match if the element is the requested element, else check if the mid is > or < than the requested element. based on that recursively call the binary search.

```java
public boolean binarySearch(int[] arr, int x){

    int mid = arr.length/2;

    if (arr[mid] == x)
        return true;
    else if(arr[mid] > x)
        binarySearch(arr,x)
    else if(arr[mid] < x)
        binarySearch()
}

int mid = l + (h-l)/2
```
