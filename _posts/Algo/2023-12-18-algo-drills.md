---
title: "Algo Drills"
date:  2023-12-18 18:27:00
categories: Algorithms
tags: [Algorithms]
---

{% include toc title="Index" %}

##### Primitive with parse

`parseInt` & `parseDouble`: Used for parsing a **String** to a **primitive int
or double**.

```java 
int i = Integer.parseInt("12345");
int j = Integer.valueOf("1234").intValue();//From String
int k = Integer.valueOf(23).intValue();
```

`String.valueOf()` converts every **primitive** and **char array** into String

##### Wrapper using valueOf

`valueOf` is Used for creating instances of wrapper classes from **String or
primitive** to Wrapper

```java
Integer fromPrimitiveInt = Integer.valueOf(25);//From String or primitive to Wrapper
Integer fromString = Integer.valueOf("90");
```

# Difference between parse and format

`parse` takes a string and returns the DataType of the Class being parsed, for
example, LocalDate.parse returns LocalDate

```java
LocalDate startLocalDate = LocalDate.parse("2023-10-30");//yyyy-mm-dd format by default
```

`format` returns a string from an object.
Eg:

```java
String format = startLocalDate.format(DateTimeFormatter.ofPattern("dd-MMM-YYYY"));
```

# Difference between parse and valueOf

[https://nitinkc.github.io/java/wrapper-class/](https://nitinkc.github.io/java/wrapper-class/)

# 1D Array

- `a.length` is a field in array
- Declare simple array

```java
int[] a = new int[3];//use [] for array instead of ()
int[] a = new int[] {1,2,3};
// Same as above
int[] b = {1,2,3};
```

- Declare an ArrayList using `Arrays.asList()`

```java
List<String> list = Arrays.asList("str1","str2");
```

- Linearity vs circularity

```java
arr[idx] = element; idx = idx+1; //Linear condition until the in = arr.lenght-1;
arr[idx] = element; idx = (idx+1) % arr.length;//Circularity
```

# 2D Array

Declare and Iterate through the 2D Array

```java
// Declaring a Rectangular Matrix
String[][] arr = new String[6][7];
int row = arr.length;// Row = 6
int col = arr[0].length; // Columns = 7
for (int i = 0; i < arr[0].length; i++) {
   for (int j = 0; j < arr[i].length; j++) {
        arr2[i][j] = "-" + i + "_" + j;
   }
}
```

using List of List

```java
// Declaring a 2D Matrix
List<List<Integer>> list = new ArrayList<>();

//Adding Elements into 2D ArrayList
list.add(0, Arrays.asList(11,12,13));
list.add(1, Arrays.asList(21,22,23));
list.add(2, Arrays.asList(31,32,33));

//Printing the Matrix using FOR Loop
for (int i = 0; i < list.size(); i = i + 1) {
    for (int j = 0; j < list.get(i).size(); j = j + 1) {
        System.out.print(list.get(i).get(j) + "\t");
    }
    System.out.println();
}
```

# Arrays

```java
int size = 10;//any chosen size
        
boolean[] arr = new boolean[size];//primitive array : Initialized to False

Boolean[] array = new Boolean[size];//Wrapper Class
Arrays.fill(array, Boolean.FALSE);//Initialize entire Array
```

# Maps

- contains key or value

```java
boolean containsValue = map.containsValue(3);
boolean containsKey = map.containsKey("Harry");// returns true if the key is in the map, false otherwise
```

- getOrDefault

```java
for (String str: list){
    map.put(str, map.getOrDefault(str,0) + 1);//count number of occurances
}
```

- Traditional

```java
for (String str: namesList) {
   if(treeMap.containsKey(str))
       treeMap.put(str, map.get(str) + 1);
   else
       treeMap.put(str,1);
}
```

- put key-value
    ```java
    Map<Integer,Integer> map = new HashMap<>();
    map.putIfAbsent(key, value);
    
    map.put(1, 100); //Inserts the key-value pair (1, 100)
    map.put(1, 200); //Updates the value associated with key 1 to 200, returns 100
    
    map.putIfAbsent(1, 100); //Inserts the key-value pair (1, 100)
    map.putIfAbsent(1, 200); //Does nothing because key 1 already exists, returns 100
    ```
- Remove from Map

```java
/* removes the key/value pair for this key if present. Does nothing if the key is not present. */
map.remove(key); //Concurrent Modification Exception in a Loop
itr.remove(); //used to avoid concurrent modification exception using an Iterator
```

### Map Iterator

- `map.keySet().iterator()`

```java
Iterator<String> itr = map.keySet().iterator();
while (itr.hasNext()) {
    String key = itr.next();
    Integer value = map.get(key);
}
```

- `map.entrySet()`

```java
// Iterate over the map using entrySet()
for (Map.Entry<String, Integer> entry : map.entrySet()) {
    String key = entry.getKey();
    Integer value = entry.getValue();
}
```

- map forEach - Takes in a BiConsumer (key,value)

```java
treeMap.forEach((name, length) -> System.out.println(name + ": " + length));
```

### TreeMap with Comparator

Tree map keeps the **Default Natural Sorting Order** with **the Keys**

```java
Map<String, Integer> treeMap = new TreeMap<>();//Default Natural Sorting Order
Map<String, Integer> treeMapReversed =new TreeMap<>(Comparator.reverseOrder());
Map<String, Integer> treeMapCustom = new TreeMap<>(Comparator.comparing(String::length));//Custom key sorter

for (String name : namesList) {//From a list of Strints, put String as key
    treeMap.put(name, name.length());
}
```

# Integer & Double

- to Wrapper Classes

```java
  Integer fromPrimitiveInt = Integer.valueOf(12);
  Integer fromString = Integer.valueOf("123");//NOT NULL SAFE
          
  Double fromPrimitiveInt = Double.valueOf(12.36);//From String or primitive to Wrapper
  Double fromString = Double.valueOf("90.25");
```

- to primitive Ints

```java
  //To Primitive Ints
  int i = Integer.parseInt("12345");//Parses strings into primitive int; From String to primitive
  int j = Integer.valueOf("1234").intValue();//From String or primitive to Wrapper
  int k =  Integer.valueOf(23).intValue();
  
  double i = Double.parseDouble("12345");//Parses strings into primitive int; From String to primitive
  double j = Double.valueOf("1234").doubleValue();//From String or primitive to Wrapper
  double k = Double.valueOf(23);
```

# Character

- primitive to Wrapper

```java
  Character d = Character.valueOf('c');//From primitive to Wrapper
```

- get ascii value from character

```java
  char myChar = 'a';
  int asciiValue = myChar;
  System.out.println("From type Casting "+asciiValue);
```

- `getNumericValue()` returns Integer value from character

```java
  // Same can be achieved through the library method
  //Returns unicode for characters from 10 to 35
  System.out.println(Character.getNumericValue('A'));//DO NOT USE THIS
  System.out.println(Character.getNumericValue(myChar));
  System.out.println(Character.getNumericValue('1'));
```

- get int from char with `-'0'`

```java
char charNum2 = '2';
int num2 = charNum2 - '0';
```

- `isLetterOrDigit()` checks for punctuation marks or

```java
  System.out.println(Character.isLetter('r'));
  System.out.println(Character.isDigit('4'));
  System.out.println(!Character.isLetterOrDigit('!'));//punctuation mark
          
  System.out.println(Character.compare('1','1'));//Compare character
```

- int array to keep char ascii as index and array value as count. Use of HashMap
  can be avoided to keep the count.
    - primitive int array initializes all the values with 0.

```java
int[] chars = new int[127];
char test = 'a';
chars[test]++;
chars['A']++;
System.out.println(Arrays.toString(chars));//The value of Array at index = asciiVal of char is increased by 1
/*
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ##1##, 0, 0, 0, 0, 0, 0, 
 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,##1##, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]        
*/] = new int[127];
char test = 'a';
chars[test]++;
chars['A']++;
System.out.println(Arrays.toString(chars));//The value of Array at index = asciiVal of char is increased by 1
/*
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ##1##, 0, 0, 0, 0, 0, 0, 
 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,##1##, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]        
*/
```

# String

- length(), equals() & str.compareTo("");

```java
  str1.equals(str2);//For Equality, DO NOT USE == (will compare objects)

  str1.compareTo(str2);
  // negative if str is "lexicographically" less than str2
  // positive if str is "lexicographically" greater than str2
  // ZERO is both strings are equal
```

- isBlank()
    ```java
    System.out.println(" ".isBlank());//True -> Returns true if the string is empty or contains only white space 
    ```
- split()

```java
    //Cut the Strings from spaces into a words
    String[] words = strList.split(",");
  ```

- trim() and strip()

```java
  String s = " Malgudi Days   ";
  
  System.out.println(s.trim());//Trimmed blank spaces with all leading and trailing space removed
  
  System.out.println(s.strip());//Strip is Unicode Aware
  System.out.println(s.stripLeading());
  System.out.println(s.stripTrailing());
 ```

- contains

```java
  String sentence = "Hello, world!";
  // Check if the string contains a specific substring
  boolean containsHello = sentence.contains("Hello");
```

- charAt & substring()
  ```java
  //returns a character at a given index i
  str.chatAt(i);
  str.substring(i,j);//index j not included
  str.substring(i);//from i till end
  ```

- indexOf & lastIndexOf
  ```java
  //2 if "er" begins from index 1, -1 if not Found
  str.indexOf("er");
  str.indexOf("er", 2); //start the search from index 2
  
  str.lastIndexOf("ew");//searches right to left
  str.lastIndexOf("ew", 5);//right to left, from index 5
  ```

- case change
  ```java
  str.toLowerCase();
  str.toUpperCase();
  ```

- compare & replace
  ```java
  System.out.println(str.replace("a","$$"));
  System.out.println(str.replace('e','*'));//Character Replace
  String str1 = str.replaceAll(" ", "" );//Replace All, takes RegEx
  ```

- String to Char Array to String
  ```java
  String str = "Pneumonia";
  char[] c = str.toLowerCase().toCharArray();
  Arrays.sort(c);//Returns a void
  
  String revStr = new String(c);
  ```

- Turn anything into String
  ```java
char c = 'C';
int d = 5;
Integer i = 5;
String newStr = String.valueOf(i));

char[] c = {'T','e','s','t'};
String newStr = String.valueOf(c);
```

# Sorting

All sorts (`Arrays.sort`, `listObj.sort`, `Collections.sort`)

- returns void
- changes the input array

### Arrays Sort

```java
int[] intArray = {4,5,3,8,2,71};
Arrays.sort(intArray);//Default Natural Sorting Order
Arrays.sort(intArray, Comparator.reverseOrder());//Reverse sorting
```

### List Sort

- `Comparator.nullsFirst()` or `Comparator.nullsLast()` can be used to
  accommodate null values.

```java
  List<Integer> list = Arrays.asList(null,4,5,null,3,8,2,71,null);
  list.sort(Comparator.nullsLast(Comparator.naturalOrder()));
  list.sort(Comparator.nullsFirst(Comparator.reverseOrder()));
  
  List<String> stringList = Arrays.asList("apple", "banana", "orange");
  stringList.sort(Comparator.comparing(String::length).reversed());
```

### Collections sort

- takes care of arranging the `null` values
-   ```java
    List<Integer> integerListWithNull = Arrays.asList(5, 6, null, 71, 2, 3);
    Collections.sort(integerListWithNull, Comparator.nullsLast(Comparator.naturalOrder()));
    Collections.sort(integerListWithoutNull, Collections.reverseOrder());
    
    List<String> stringList = Arrays.asList("apple","banana", "orange");
    Collections.sort(stringList, Comparator
                                      .comparing(String::length)
                                      .thenComparing(Comparator.reverseOrder()));
    ```

# Set

```java
List<String> namesList = Arrays.asList("Harry", "Hermione", "Ron","Harry", "Ron", "Ron", "Remus");
// Sorted values returned while iterating in TreeSet
Set<String> treeSet = new TreeSet<>(Comparator.reverseOrder());
treeSet.addAll(namesList);

// Ordering NOT guaranteed in HashSet
Set<Integer> set = new HashSet<Integer>();
```

- Add elements in a Set
  ```java
  /* Adds the element to the set and returns true if this set does not have this element.
  if the element already exist the call leaves the set unchanged and returns false*/
  set.add(value);
  //boolean add(E e);
  ```

- Find an element in a set
  ```java
  /* returns true if the key is in the map, false otherwise.*/
  set.contains(key);
  ```

- remove from Set
  ```java
  boolean remove(Object o)
  // Removes the specified element from this set if it is present. Returns true if this set contained the element
  set.remove(key);// Concurrent Modification Exception in a Loop
  itr.remove();// use of Iterator to avoid conc. modi. excep.
  ```

##### Set Iteration

```java
Iterator<String> itr = set.iterator();
while(itr.hasNext()){
    if(itr.next().length()%2 == 0){
        itr.remove();
    }
}
```

# Heap

- Declaring min and max heaps
  ```java
  // Primitive Types
  Queue<Integer> pq = new PriorityQueue<>();//Default Natural Sorting Order
  Queue<Integer> pq = new PriorityQueue<>(Comparator.naturalOrder());//Min Heap
  Queue<Integer> pq = new PriorityQueue<>(Comparator.reverseOrder());//Max Heap
  ```
- `poll()` to pop the element out
  ```java
  //Heap methods
  pq.offer(100);
  pq.poll();//pops the root of the heap
  ```
- Heap/Priority Queue of Type T
  ```java
  //For Type T
  Queue<Employee> heapMax = new PriorityQueue<>(Comparator.comparing(Employee::getAge)//If the employee age is same
                                                .thenComparing(Employee::getSalary));//Natural Sort Order
  ```

# Queue

* offer() Enqueue (add) elements to the queue****
* peek() Retrieves, but **does not remove**, the head of this queue, or returns
  null if this queue is empty.
* poll() Retrieves and removes **the head** of this queue, or returns null if
  this queue is empty.
* remove() Removes a single instance of the specified element from this queue,
  if it is present.
* element() Retrieves, but does not remove, the head of this queue, differs from
  peek -> throws an exception if queue is empty.

```java
// Declare a queue using LinkedList
Queue<String> queue = new LinkedList<>();

// Enqueue (add) elements to the queue
queue.offer("Apple");
queue.offer("Banana");
queue.offer("Orange");
```

# Stack

- push(E item): Pushes an item onto the top of the stack.
- pop(): Removes the object at the top of the stack and returns that object.
- peek(): Looks at the object at the top of the stack **without removing** it.
- empty(): Checks if the stack is empty.
- search(Object o): Searches for the specified object in the stack and returns
  its position.

```java
Stack<Integer> stack = new Stack<>();
stack.push(1); stack.push(2);stack.push(3);

System.out.println("Top element: " + stack.peek());  // Output: 3

while (!stack.empty()) {
    System.out.println("Popped element: " + stack.pop());
}

// This Does not work as stack.pop reduces the size of the stack each time
for (int i = 0; i < stack.size(); i++) {
    System.out.println(stack.pop());
}
```

# Math

- min & max
  ```java
  int maxNumber = Math.max(10, 20);
  float maxFloat = Math.max(15.5f, 12.7f);
  
  int minNumber = Math.min(10, 20);
  float minFloat = Math.min(15.5f, 12.7f);
  ```

- power and square root
  ```java
  double powerIntResult = Math.pow(2, 3);
  double powerFloatResult = Math.pow(2.5, 2);
  
  double sqrtResult = Math.sqrt(25);
  ```

- absolute
  ```java
  int absoluteIntValue = Math.abs(-5);
  float absoluteFloatValue = Math.abs(-8.9f);
  ```
- ceil and floor
  ```java
  double ceilIntResult = Math.ceil(5.3);
  float ceilFloatResult = (float) Math.ceil(5.3f);
  
  double floorIntResult = Math.floor(5.9);
  float floorFloatResult = (float) Math.floor(5.9f);
  ```

- log
  ```java
  double log10IntResult = Math.log10(1000);
  double log10FloatResult = Math.log10(1000.0f);
  double logResult = Math.log(Math.E); // Log base e of e is 1
  ```

# Bitwise

- `Left Shift (<<)`: Shifts the bits to the left by a specified number of
  positions (n) value << n.
    - The vacant positions on the right are filled with zeros.
    - it effectively **multiplies** the operand by `2^n`

- `Signed Right Shift (>>)`: Shifts the bits of the operand to the right by a
  specified number of positions.
    - It fills the vacant positions on the left with the sign bit (the leftmost
      bit) to preserve the sign of the number.
    - If the number is positive, it fills with 0, and if negative, it fills with
      1.
    - **Divides** the number by `2^n`

- `Unsigned Right Shift (>>>)`
    - It fills the vacant positions on the left with zeros, regardless of the
      sign bit.
    - It is used for **logical right shifts**, and it treats the operand as an
      unsigned quantity.
    - ALWAYS use this for the while loop, else infinite loop for negative
      numbers


- **Bit representation**
  ```java
  short x = 0b11101011;
  Integer.toBinaryString(235)
  ```
- **Negative number**
  ```java
  int positiveNum= 0b00101100;//44
  int twoScomplement = 0b11010100;
  ````
- **Extracts the LSB of a number**
  ```java
  (number & 1)
  ```
- **Clear/Unset the rightmost set bit**
  ```java
  x & (x - 1)
  ```

- **Extracts the rightmost set bit**
  ```java
  x & ~(x - 1)` isolates the rightmost 1-bit of y and sets all other bits to 0 
  ```
- **Set the Nth bit** Bitmask
  ```java
  1 << n
  ```
- **XOR #1 Cancels when same**
  ```java
  (x^x);//0
  (x^(~x));//-1
  ```
- **XOR #2 Adding Without Carrying**
  ```java
  ```
- **Parity = 1 When #1's Odd**
  ```java
  x = (x & (x-1));
  parity = (parity ^ 1);
  ```