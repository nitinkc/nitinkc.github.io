---
title:  "Array Syntax"
date:   2022-01-03 01:30:00
categories: Algorithms
tags: [Algorithms]
---

### Points to keep in Mind
{% gist nitinkc/7bed7e03f3e21790c98353df6a921137 %}

### ArrayList
{% gist nitinkc/98b5adaf0ed85980472ec423237e9edd %}

### 1D Arrays
{% gist nitinkc/c2abeb754d1a64641b0149bc6d8f21ae %}

### 2D Arrays

A Rectangular 2D array has different no. of Rows and Columns (eg: 6X7)
{% gist nitinkc/d9ca95267cae73a9145d5e96ca7d8f22 %}


The Skewed 2D array need not have the same number of Columns each Row.
{% gist nitinkc/f828994bdaabbc55505c51096c3b7d0d %}

### The Arrays Class

```
Import java.util.ArrayList;

// Declaring an ArrayList
ArrayList<Integer> a = new ArrayList<Integer>;

//Inserting values
a.add(1); a.add(2); a.add(3);

//Printing an ArrayList as ann Integer
Arrays.toString(a);//op: [1,2,3]

//Converting an ArrayList into Array <ArrayList.toArray()>
a.toArray();
```

### String Methods (Most Important)
{% gist nitinkc/a91ab5df313cbd3e21b6ea71c30f993f %}

### Array vs Linked List
```java
 for (int i = 0; i < arr.length; i++){
      System.out.prinln(arr[i]);
 }

 for (ListNode runner = head; runner != null; runner = runner.next){
      System.out.println(runner.data);
 }
```