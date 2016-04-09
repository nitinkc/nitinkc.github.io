---
layout: static
title:  "Coding"
---
# Reference for Coding Interviews

## Contents
{:.no_toc}

* Will be replaced with the ToC, excluding the "Contents" header
{:toc}
---

### Points to keep in Mind

```java
//length is a field in Arrays
int[] nums => nums.length;

//length is a method in String
String str => str.length();

//length is called size() in arrayList
ArrayList<Integer> a => a.size();
```

### Boolean Logic (multiple if statements into switch)
```java
if (a > b && (a-b) >= 2){
    return true;
}

//is equivalent to

return (a > b && (a-b) >= 2);
```

### For Loop Traps
```java
int arr[] = new int[8];

// Check for the Boundry conditions
for (int i = 0; i < arr.length; i = i+2){
    System.out.println(i);  
   } // if length = 8, loop will run 0,2,4,6.... 8 is never included.

// Start the Pointer from an index ahead and check the previous
for (int i = 1; i < num.length; i++) //NOTICE : i < num.length
  if (num[i-1] == num[i]) 
    return true;

// Start the Pointer from index 0 and check the next
for (int i = 0; i < num.length - 1; i++) // NOTICE : i < num.length -1
  if (num[i] == num[i+1]) 
    return true;

//Prints alphabets from 'a' to 'z' 
for (char i = 'a'; i <= 'z'; i++){ 
  System.out.println(i); 
}
```

### 1D Arrays

```java

//Single Line Declaration. NO () IS USED
int[] a = new int[3]; 

//Split Line Declaration
int[] a;
a = new int[3]; //notice []. NOT () to be used

a.length ; //Length is a "field" in Array, while a method in Strings

// Declaration and Initialization
int[] a = new int[] {1,2,3};

// Same as above
int[] b = {1,2,3};

//Converting array to ArrayList (arr is standard array)
ArrayList<E> arrayList = Arrays.asList(arr);

//Printing Arrays as String using Arrays utility
System.out.println(Arrays.toString(num));

//Testing if a value exists in an Array
boolean result = Arrays.asList(arr).contains("a");// returns boolean true/false
```

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

### String Functions (Most Important)
```java
+ ⇒ concatenation

//returns a character at a given index i
str.chatAt(i);

//Method in String, Field in Arrays;
str.length(); 

//index j not included
str.substring(i,j);

//from i till end 
//str.substring(i,str.length());
str.substring(i);

//For Equality 
str.equals();//DO NOT USE == (will compare objects)

//2 if "er" begins from index 1, -1 if not Found
str.indexOf("er");

str.indexOf("er", 2); //start the search from index 2

str.lastIndexOf("ew");//searches right to left

str.lastIndexOf("ew", 5);//right to left, from index 5

str.toLowerCase();
str.toUpperCase();

str.compareTo("");
str.replace("old","new");

//Cut the Strings from spaces into a words
String[] ransomWords = ransom.split(" ");

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

### Array vs Linked List
```java
 for (int i = 0; i < arr.length; i++){
      System.out.prinln(arr[i]);
 }

 for (ListNode runner = head; runner != null; runner = runner.next){
      System.out.println(runner.data);
 }
```

### Linked List
```java
 LinkNode runner = front;//head
 while (runner.next != null){//Runner stops at the last node, else runner will end up pointing null!!
 runner = runner.next;
}
```

#### Add in the List

##### Add in the front
```java
front = new ListNode(value, front);
```

##### Add at 'index'
```java
if (index == 0)
front = new ListNode(value, front);
else{
ListNode runner = front;
for (int i = 0; i < index - 1; i++)//Stop at an index one before the desired
current = current.next;
}
current.next = new ListNode(value, current.next); //old current.next is assigned to the new node which in turn is assigned to current.next
```

##### Add in the end
```java
if (front == null)
  front = new ListNode(value, front);
else{
  ListNode runner = front;
  while (runner.next != null) // Go till the last node
      runner = runner.next;
  runner.next = new ListNode(value); //this constructor has .next as null
}
```

### For Each Loop (Read Only Loop)
```java
//Eg: Read as "for g in Grades of type Double"
Set<Double> grades = new HashSet<Double>();
for (double g: grades){
   System.out.println(g);
 }
```

### Iterator itr (for some collection)
```java
Iterator itr = c.iterator();
 itr.remove(i);
 itr.hasNext();
 itr.next();
```

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

### HashMap
```java
Map<String, Integer> ret = new HashMap<String, Integer>();
for (int key : map.keySet()){
ret.put(map.get(key),key);
}
```

### ArrayList
```java
// Declaration (Child of List Interface)

ArrayList<Integer> list = new ArrayList<Integer>();
List<Integer> list = new ArrayList<Integer>();// Polymorphic 

// Insert element
for (int i = 0; i < list.size(); i++){
  list.add(i);
  list.get(i);
}

// Common methods
list.add(value);
list.add(index, value);
list.set(index. value);
list.clear();
list.indexOf(value);
list.lastIndexOf();
list.toString();
list.toArray();
```

### HASHMAP (IMPLEMENTATION OF HASHTABLE)
```java
Map<String, Integer> ret = new HashMap<String, Integer>();
  for (int key : map.keySet()){
  ret.put(map.get(key),key);
}
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

##### Insert Java Code
{% highlight java linenos %}
{% endhighlight %}
