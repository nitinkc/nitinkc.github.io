---
title:  "Syntax Reference"
date:   2021-10-30 21:55:00
categories: Algorithms
tags: [Algorithm Interviews]
---
# Reference for Coding Interviews


{% include toc title="Index" %}

### Points to keep in Mind

{% gist nitinkc/7bed7e03f3e21790c98353df6a921137 %}

### Boolean Logic (multiple if statements into switch)
{% gist nitinkc/96387a9700c9c58185a969ae48bfdc45 %}

### For Loop Traps
{% gist nitinkc/382798a984e00a732d86a12a6637e0a2 %}

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

## COLLECTIONS FRAMEWORK
```
Collection(I)
|
|---List
|      |----ArrayList
|      |----LinkedList
|      |----Vector---Stack      
|      
|----Set
|      |----HashSet----LinkedHashSet
|      |----TreeSet
|           
|----Queue
|      |----PriorityQueue(I) (Heap Representation in Java)
|      |----BlockingQueue
```

*[Collection API - PDF]({{ site.url }}/media/Collections.pdf)*.

[Collection Interface](http://blogs.bgsu.edu/nitinc/2017/02/11/collection/)

### For Each Loop (Read Only Loop)
{% gist nitinkc/606150a527983a417dd1c5b5d4926cf3 %}

### Iterator itr (for some collection)
{% gist nitinkc/78621758745aa25b11369999cc942120 %}

### ArrayList
{% gist nitinkc/98b5adaf0ed85980472ec423237e9edd %}

### SETS
Set takes only single instance of an element.

While adding an element into a set, a test of equality happens, to determine if the object being pushed already exist.
Thus override equals & hashCode methods in case of non primitive Objects

With Integer, no need to override hashCode() and equals()

With Tree set it will sort to DNSO
{% gist nitinkc/f98cd225bc3dd60b21368c56980ef006 %}

### Stacks
Stacks print in an [a, b, c] format from bottom  to top
{% gist nitinkc/df63e7d0bc54653a97f133233eca3925 %}

### Queues
Queues print in an [a, b, c] format from front to back
{% gist /nitinkc/9a3b529f8bad45a05ba20405bc975411 %}

### Heaps (Priority Queues in Java)
Heaps are represented using Priority Queue.

  * It gives O(1) seek time.
  * Does not permit null elements.
  * The elements are ordered according to their natural ordering, or by a Comparator provided at queue construction time.

METHDS :

 * 	add(E e) Inserts the specified element into this priority queue.
 *  offer(E e) Inserts the specified element into this priority queue
 *  poll() Retrieves and removes the head of this queue, or returns null if this queue is empty.

{% gist nitinkc/c187b0ee3462c34d3e7eae3597fd01da %}

### MAP (Not part of Collection Framework)

There are 3 classes that implements the Map interface

 **1.) HashMap**: (IMPLEMENTATION OF HASHTABLE) This is "the map", able to store key-value pairs, and able to find the value according to the key in O(1) if the hash function is perfect/good
 * PROBLEM: makes no guarantee about the order of iteration

 **2.) TreeMap**: it supports ordering --> natural ordering, compareTo() method or Comparator is important to be able to decide the order !!!

 **3.) LinkedHashMap**: it contains a doubly linked list connecting all the entries in the map
 * Unlike HashMap it preserves insertion-order
 * insertion order is not affected if a key is re-inserted into the map
 * IMPORTANT: they consume more memory than HashMap !!!

{% gist nitinkc/3b434410bca596c8fbeae64a0e7c2895 %}

### Binary Search Tree
"BST": a binary tree that is either:
* empty (null), or
* a root node R such that:
  1. every element of R's left subtree contains data "less than" R's data,
  2. every element of R's right subtree contains data "greater than" R's,
  3. R's left and right subtrees are also binary search trees.

BSTs store their elements insorted order, which is helpfulfor searching/sorting tasks.

{% gist /nitinkc/dbc98632abc89fb83119af50b2448300 %}


### The XOR Trick

Same variables cancels the effect of each other if the bitwise XOR is used.

```java
a = a^b;
b = a^b; //a^b^b yields a
a = a^b;//a^b^a = b(b is recently converted to a)
/* (Works only with integer, in its native form, for others change it into its equivalent binary representation) */

/*
The logic is used for finding a unique element among duplicates (Stolen Drone problem (21) in Interview cake)
*/

// Use of XOR (both flags are boolean)
if (flag2 ^ flag4)
//is equivalent to
(flag2 && !flag4) || (!flag2 && flag4);
```

### Reading, Parsing and Type Checking Command Line Inputs.
```java

/*Assuming 2 command line arguments <Nitin 29>*/

if (args.length == 0 || args.length > 2) {
     System.err.println("Incorrect Number of arguments passed");
     System.exit(-1);
  }
String name = args[0];
  int age = Integer.parseInt(args[1]);
```

### Running time of a method
```java
System.currentTimeMillis();//type long , from Jan 1 1970
System.nanoTime();
```

### Random
```java
import java.util.Random

Random generator = new Random(); //or new Random(123), 123 being the seed
generator.nextInt(5);//range 0 to 5, add 1 to get range 1 to 6 (dices)
/* Eg: int throw = generator.nextInt(6) + 1; */

generator.nextInt(); // 2^31 to 2^31 -1
generator.nextDouble();//Range: 0.0 to 1.1

```

## Java Input

### Key Board Input

```java
import java.util.Scanner;
 Scanner in = new Scanner(System.in);

 /* Input Problem occurs when a mix of int and strings are given
 The extra invocation is done to get rid of previous \n */
 int n = in.nextLine();
 in.nextLine(); //To avoid INPUT Problem
 String str = in.nextLine();

 in.nextLine();//reads entire line of in
 in.next();//next character upto but not including space

/* NO METHOD TO READ A SINGLE CHARACTER */
 char a = in.nextLine.charAt(0);
```

### File Input

```java
//Open the File
 File myFile = new File("/nitin/a.txt");
 Scanner in = new Scanner(myFile);
 //Instead of System.in, take the file to read

//Read from the File
 String str = in.nextLine();
//OR
 while (in.hasNext());
 System.out.println(in.nextLine());

//Close the File
 in.close();
```

## Output File Handling

### Writing text to File
```java
import java.io.PrintWriter;
 final String FILENAME = "nitin.txt";
//Surrounding with try catch!!
 PrintWriter output = new PrintWriter(FILENAME);

 output.println("Nitin"); output.println("Chaurasia");

//To avoid erasing files that already exist
 PrintWriter pw = new PrintWriter(new FileWriter("nitin.txt", true));
```

### Appending Text to file
```java
FileWriter fw = new FileWriter("Names.txt", true);
PrintWriter pw = new PrintWriter(fw);
//OR
PrintWriter pw = new PrintWriter(new FileWriter("Names.txt, true"));
```

### Reading Data from a file
```java
File myFile = new File("customer.txt");
Scanner ipFile = new Scanner(myFile); //instead of System.in
```
