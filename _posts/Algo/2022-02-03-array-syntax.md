---
title:  "Array Syntax"
date:   2022-02-03 01:30:00
categories: Algorithms
tags: [Algorithms]
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