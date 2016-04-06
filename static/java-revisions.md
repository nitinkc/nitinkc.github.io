---
layout: post
title:  "Java Coding Revisions"
date:   2016-04-04 18:31:00
---

# Reference for Coding Interviews


#### Inserting Gist
{% gist nitinkc/bbf28d84627c186972e3f34b903e9698 %}

# hghjghvjhghjghj
{% highlight java linenos %}
{% endhighlight %}

int[] nums => nums.length;
String str => str.length();
ArrayList<Integer> a => a.size();

# Boolean Logic (if statement, switch)
```java
return (a > b && (a-b) >= 2);
         is equivalent to
if (a > b && (a-b) >= 2){         
    return true;
}```

### For Loop Traps

for (int i = 0; i < arr.length; i = i+2){ ...} // if lenght = 9, loop will run 0,2,4,6.. 8 is never included.
for (int i = 1; i < num.length; i++) if (num[i-1] == num[i]) return true;
for (int i = 0; i < num.length - 1; i++) if (num[i] == num[i+1]) return true;
for (char i = 'a'; i <= 'z'; i++){ sout(i); //Prints alphabets from 'a' to 'z' }
Arrays

int[] a;
a = new int[3]; //notice []. NOT () to be used
int[] a = new int[3]; //single line declaration
a.length ; //Length is a "field" in Array, while a method in Strings
int[] a = new int[] {1,2,3};
int[] b = {1,2,3};
sysout(Arrays.toString(num));
###The Arrays Class

Import java.util.ArrayList;

ArrayList<Integer> b = new ArrayList<Integer>;
Arrays.toString(a);//o/p [1,2,3]
Arrays.asList(a);
Arrays.asList.contains("a");//boolean true/false

### String Functions (Most Important)

+ ⇒ concatenation
str.chatAt(i);
str.length(); //Method in String, Field in Arrays;
str.substring(i,j);//j not included
str.substring(i);//from i till end str.substring(i,str.length());String Index begins from ZERO, thus lenght = max Index + 1
For Equality str.equals();//DO NOT USE == (will compare objects)
str.indexOf("er");//2 if "er" begins from index 1, -1 if not Found
str.indexOf("er", 2); //start the search from index 2
str.lastIndexOf("ew");//searches right to left
str.lastIndexOf("ew", 5);//right to left, from index 5
str.toLowerCase() / str.toUpperCase()
str.compareTo("");
str.replace("old","new");
String[] ransomWords = ransom.split(" ");//Cut the Strings from spaces into a words

## Java Input

#### Key Board Input

{% highlight java linenos %}
import java.util.Scanner;
Scanner in = new Scanner(System.in);
 int n = in.nextLine();
 in.nextLine(); //To avoid INPUT Problem
 String str = in.nextLine();
/* Input Problem occurs when a mix of int and strings are given
 The extra invocation is done to get rid of previous \n

16\n 1000\n Joe\n
/n Extra in.nextLine()
 in.nextInt; //reads next integer
 in.nextDouble();
 in.nextLine();//reads entire line of in
 in.next();//next character upto but not including space
/* NO METHOD TO READ A SINGLE CHARACTER */
 char a = in.nextLine.charAt(0);
 {% endhighlight %}

#### File Input

{% highlight java linenos %}
//Open the File
File myFile = new File("/nitin/a.txt");
 Scanner in = new Scanner(myFile; //Instead of System.in, take the file to read
//Read from the File
 String str = in.nextLine();
//OR
 while (in.hasNext());
 System.out.println(in.nextLine());
 //Close the File
 in.close();
{% endhighlight %}

## Output File Handling

#### Writing text to File
{% highlight java linenos %}
import java.io.PrintWriter;
 final String FILENAME = "nitin.txt";
//Surrounding with try catch!! OR
 PrintWriter output = new PrintWriter(FILENAME);
 PrintWriter output = new PrintWriter("nitin.txt");
output.println("Nitin"); output.println("Chaurasia");
//To avoid erasing files that already exist
 PrintWriter pw = new PrintWriter(new FileWriter("nitin.txt", true));
 {% endhighlight %}


#### Appending Text to file
{% highlight java linenos %}
FileWriter fw = new FileWriter("Names.txt", true);
PrintWriter pw = new PrintWriter(fw);

OR

PrintWriter pw = new PrintWriter(new FileWriter("Names.txt, true"));
Reading Data from a file

File myFile = new File("customer.txt");
Scanner ipFile = new Scanner(myFile); //instead of System.in
{% endhighlight %}

## Reading, Parsing and Type Checking Command Line Inputs.

/*Assuming 2 command line arguments <Nitin 29>*/

if (args.length == 0 || args.length > 2) {
     System.err.println("Incorrect Number of arguments passed");
     System.exit(-1);
  }
String name = args[0];
  int age = Integer.parseInt(args[1]);
Running time of a method

System.currentTimeMillis();//type long , from Jan 1 1970
System.nanoTime();

## Random
{% highlight java linenos %}

import java.util.Random

Random generator = new Random(); //or new Random(123), 123 being the seed
generator.nextInt(5);//range 0 to 5, add 1 to get range 1 to 6 (dices)
generator.nextInt(); // 2^31 to 2^31 -1
generator.nextDouble();//Range: 0.0 to 1.1
Eg: int throw = generator.nextInt(6) + 1;
{% endhighlight %}

## Array and Linked List

Capture

 for (int i = 0; i < arr.length; i++){
      System.out.prinln(arr[i]);
 }
 for (ListNode runner = head; runner != null; runner = runner.next){
      System.out.println(runner.data);
 }
Linked List

 LinkNode runner = front;//head
 while (runner.next != null){//Runner stops at the last node, else runner will end up pointing null!!
 runner = runner.next;
Add in the List

Add in the front
front = new ListNode(value, front);

Add at 'index'
if (index == 0)
front = new ListNode(value, front);
else{
ListNode runner = front;
for (int i = 0; i < index - 1; i++)//Stop at an index one before the desired
current = current.next;
}
current.next = new ListNode(value, current.next); //old current.next is assigned to the new node which in turn is assigned to current.next
Add in the end

if (front == null)
  front = new ListNode(value, front);
else{
  ListNode runner = front;
  while (runner.next != null) // Go till the last node
      runner = runner.next;
  runner.next = new ListNode(value); //this constructor has .next as null  
}
For Each Loop (Read Only Loop)

for (type name : collection){
 }
Eg: Set<Double> grades = new HashSet<Double>();
for (double g: grades){
   System.out.println(g);
 }
Iterator itr (for some collection)

Iterator itr = c.iterator();
 itr.remove(i);
 itr.hasNext();
 itr.next();
The XOR Trick

Same variables cancels the effect of each other if the bitwise XOR is used.

a = a^b;
b = a^b; //a^b^b yields a
a = a^b;//a^b^a = b(b is recently converted to a)
(Works only with integer, in its native form, for others change it into its equivalent binary representation)
The logic is used for finding a unique element among duplicates (Stolen Drone problem (21) in Interview cake)

Use of XOR (both flags are boolean)

if (flag2 ^ flag4)
is equivalent to
(flag2 && !flag4) || (!flag2 && flag4);

HashMap

Map<String, Integer> ret = new HashMap<String, Integer>();
for (int key : map.keySet()){
ret.put(map.get(key),key);
}

ArrayList

Declaration (Child of List Interface)

ArrayList<Integer> list = new ArrayList<Integer>();
List<Integer> list = new ArrayList<Integer>();

Insert element
for (int i = 0; i < list.size(); i++){
list.add(i);
list.get(i);
}

Common methods
add(value), add(index, value)
set(index. value)
clear()
indexOf(value)
lastIndexOf()
toString(), toArray();

HASHMAP (IMPLEMENTATION OF HASHTABLE)

Map<String, Integer> ret = new HashMap<String, Integer>();
for (int key : map.keySet()){
ret.put(map.get(key),key);
