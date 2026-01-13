---
title: Algo Drills
date: 2023-12-18 18:27:00
categories:
- Algorithms
tags:
- Practice
---

{% include toc title="Index" %}

# Summary 
- mod (%) by 10 yields the rightmost digit (126 % 10 is 6).
- while divide (/) by 10 removes the rightmost digit (126 / 10 is 12).
- `parse` converts a String to a primitive type, while `valueOf` converts a String or primitive type to a Wrapper object.
- 

# Object Declarations in Java

## Array Declaration
```java
int[] a = new int[3]; // use [] for array instead of ()
int[] a = new int[] {1, 2, 3};
int[] b = {1, 2, 3}; // Same as above

// Declaring a Rectangular Matrix
String[][] arr = new String[6][7]; // 6 rows and 7 columns
// Iterating through the 2D array and assigning values
for (int i = 0; i < arr.length; i++) { // Loop through rows
    for (int j = 0; j < arr[i].length; j++) { // Loop through columns
        arr[i][j] = "-" + i + "_" + j; // Do something
    }
}
```

## ArrayList Declaration
```java
List<Integer> list = new ArrayList<>();
list.add(10);
list.get(0);
```

## LinkedList Declaration
```java
List<String> list = new LinkedList<>();
list.add("Hello");
list.add("World");
list.getFirst();
list.getLast();
list.removeFirst();
list.removeLast();
```

## Stack Declaration
```java
Stack<Integer> stack = new Stack<>();
stack.push(10);           // Add 10
stack.push(20);           // Add 20
System.out.println(stack.peek());  // 20 (top element)
stack.pop();              // Removes 20
System.out.println(stack.isEmpty()); // false
System.out.println(stack.size());   // 1
stack.clear();            // Clear the stack
```

## Queue Declaration
```java
Queue<Integer> queue = new LinkedList<>();
Deque<Integer> deque = new ArrayDeque<>(); // Doubly ended Queue

// Queue Methods
queue.add(10);        // Adds element to queue at the rear, throws an exception if the operation fails
queue.offer(20);      // Adds element to queue at the rear, returns false if the operation fails
queue.poll();         // Removes element from front
queue.peek();         // Retrieves front element
queue.size();         // Returns size
queue.clear();        // Clears queue

// Deque Methods
deque.addFirst(10);   // Adds element to front
deque.offerFirst(20); // Adds element to front
deque.removeLast();   // Removes element from back
deque.peekLast();     // Retrieves last element
deque.size();         // Returns size
deque.clear();        // Clears deque
```

## PriorityQueue (Heap) Declaration
```java
Queue<Integer> pq = new PriorityQueue<>();
pq.add(10);              // Add 10
pq.offer(20);            // Add 20
System.out.println(pq.peek());  // 10 (head of the queue)
pq.poll();               // Removes 10
System.out.println(pq.isEmpty()); // false
System.out.println(pq.size());   // 1
pq.clear();              // Clear the queue
```

## Set Declaration
```java
HashSet<Integer> set = new HashSet<>();
Set<String> treeSet = new TreeSet<>(Comparator.reverseOrder());
```

## Map Declaration
```java
Map<String, Integer> map = new HashMap<>();
Map<String, Integer> map = new TreeMap<>(Comparator.reverseOrder());

boolean containsValue = map.containsValue(3);
boolean containsKey = map.containsKey("Harry"); // returns true if the key is in the map, false otherwise

List<Integer> allValues = map.values(); // Returns a Collection view of the values contained in this map.
Set<String> allKeys = map.keySet(); // Returns a Set view of the keys contained in this map.

// Iterate over the map using entrySet()
for (Map.Entry<String, Integer> entry : map.entrySet()) {
    String key = entry.getKey();
    Integer value = entry.getValue();
}

// Iterate over the map using iterator
Iterator<String> itr = map.keySet().iterator(); // Returns iterator to all the keys
while (itr.hasNext()) {
    String key = itr.next();
    Integer value = map.get(key);
}
```

---

# String Parsing and Conversion in Java

## Strings to Primitives using `parse`

### `parseInt()` and `parseDouble()`
Used for parsing a **String** into a **primitive int or double**.
```java
int i = Integer.parseInt("12345");
int j = Integer.valueOf("1234").intValue(); // From String to Wrapper to Primitive
```

## Creating Wrapper Instances using `valueOf`

### `valueOf()`
Used to create instances of wrapper classes from a **String or primitive**.
```java
Integer fromPrimitiveInt = Integer.valueOf(25); // From primitive
Integer fromString = Integer.valueOf("90");   // From String
```

### `String.valueOf()`
Converts **primitives** and **char arrays** into Strings.
```java
String intAsString = String.valueOf(42); 
String doubleAsString = String.valueOf(3.14159);
String booleanAsString = String.valueOf(true);
String charArrayAsString = String.valueOf(new char[] {'H', 'e', 'l', 'l', 'o'});
```

## Key Differences

### Between `parse` and `valueOf`
- `parse`: Converts a **String** to a **primitive type**.
- `valueOf`: Converts a **String** or **primitive type** to a **Wrapper object**.

Read more about parse and valueOf

### Between `parse` and `format`
- **`parse`**: Converts a **String** to the data type of the class being parsed.
  ```java
  LocalDate startLocalDate = LocalDate.parse("2023-10-30"); // yyyy-MM-dd format by default
  ```
- **`format`**: Converts an **object** to a formatted **String**.
  ```java
  String formattedDate = startLocalDate.format(DateTimeFormatter.ofPattern("dd-MMM-YYYY"));
  ```

---

# 1D Array

- `a.length` is a field in array
- Declare simple array
  ```java
  int[] a = new int[3]; // use [] for array instead of ()
  int[] a = new int[] {1, 2, 3};
  int[] b = {1, 2, 3}; // Same as above
  ```

- Declare an ArrayList using `Arrays.asList()`
  ```java
  List<String> list = Arrays.asList("str1", "str2");
  ```

- Linearity vs circularity
  ```java
  arr[idx] = element; // Assign the element at the current index
  
  idx = idx + 1;      // Increment the index linearly until idx reaches arr.length - 1
  idx = (idx + 1) % arr.length;  // Increment the index circularly. The modulo operator ensures that idx wraps around to 0 when it reaches arr.length
  ```

---

# 2D Array
- Declare and Iterate through the 2D Array
  ```java
  // Declaring a Rectangular Matrix
  String[][] arr = new String[6][7]; // 6 rows and 7 columns
  
  // Iterating through the 2D array and assigning values
  for (int i = 0; i < arr.length; i++) { // Loop through rows
    for (int j = 0; j < arr[i].length; j++) { // Loop through columns
        arr[i][j] = "-" + i + "_" + j; // Do something
    }
  }
  ```

- Using List of List
  ```java
  // Declaring a 2D Matrix
  List<List<Integer>> list = new ArrayList<>();
  
  // Adding Elements into 2D ArrayList
  list.add(0, Arrays.asList(11, 12, 13));
  list.add(1, Arrays.asList(21, 22, 23));
  list.add(2, Arrays.asList(31, 32, 33));
  
  // Printing the Matrix using FOR Loop
  for (int i = 0; i < list.size(); i = i + 1) {
      for (int j = 0; j < list.get(i).size(); j = i + 1) {
          System.out.print(list.get(i).get(j) + "\t");
      }
      System.out.println();
  }
  ```

# The Arrays Class

### Initializing Arrays
```java
int size = 10; // any chosen size

// Primitive array: Initialized to False
boolean[] arr = new boolean[size];

// Wrapper class array: Initialized to False
Boolean[] array = new Boolean[size];
Arrays.fill(array, Boolean.FALSE);

// Primitive array: Initialized to 0
int[] intArr = new int[size];

// Wrapper class array: Initialized to 0
Integer[] wrapperIntArr = new Integer[size];
Arrays.fill(wrapperIntArr, Integer.valueOf(0));
```

### Copying and Comparing Arrays
```java
int[] original = {1, 2, 3, 4, 5};

// Copy array
int[] copy = Arrays.copyOf(original, original.length);

// Compare arrays
boolean areEqual = Arrays.equals(original, copy);
```

### Sorting Arrays
```java
String[] stringArr = new String[5];
Arrays.fill(stringArr, "Default Value"); // Initialize all elements
stringArr[2] = "Custom Value"; // Replacing specific elements

// Sorting the array
Arrays.sort(stringArr); // returns void, changes the original array
```

# Maps

### Contains Key or Value
```java
boolean containsValue = map.containsValue(3);
boolean containsKey = map.containsKey("Harry"); // returns true if the key is in the map, false otherwise
```

### getOrDefault
```java
Map<String, Integer> map = new HashMap<>();
for (String str : list) { // Considering a list of Strings
    // Use getOrDefault to fetch the current count (default to 0 if the key is not present)
    int count = map.getOrDefault(str, 0);
    map.put(str, count + 1); // Increment the count and update the map
}
```

### Traditional Map Update
```java
for (String str : namesList) {
    if (treeMap.containsKey(str)) {
        treeMap.put(str, map.get(str) + 1);
    } else {
        treeMap.put(str, 1);
    }
}
```

### Put Key-Value
```java
Map<Integer, Integer> map = new HashMap<>();
map.putIfAbsent(key, value);

map.put(1, 100); // Inserts the key-value pair (1, 100)
map.put(1, 200); // Updates the value associated with key 1 to 200, returns 100

map.putIfAbsent(1, 100); // Inserts the key-value pair (1, 100)
map.putIfAbsent(1, 200); // Does nothing because key 1 already exists, returns 100
```

### Remove from Map
```java
// Removes the key/value pair for this key if present. Does nothing if the key is not present.
map.remove(key); // Concurrent Modification Exception in a Loop
itr.remove(); // Used to avoid concurrent modification exception using an Iterator
```

### Map Iterator

#### Using `map.keySet().iterator()`
```java
Iterator<String> itr = map.keySet().iterator(); // Returns iterator to all the keys
while (itr.hasNext()) {
    String key = itr.next();
    Integer value = map.get(key);
}
```

#### Using `map.entrySet()`
```java
// Iterate over the map using entrySet()
for (Map.Entry<String, Integer> entry : map.entrySet()) {
    String key = entry.getKey();
    Integer value = entry.getValue();
}
```

### Map forEach
```java
treeMap.forEach((key, value) -> System.out.println(key + " -> " + value));
```

### TreeMap with Comparator

TreeMap keeps the **Default Natural Sorting Order** with **the Keys**
```java
Map<String, Integer> treeMap = new TreeMap<>(); // Default Natural Sorting Order
Map<String, Integer> treeMapReversed = new TreeMap<>(Comparator.reverseOrder());
Map<String, Integer> treeMapCustom = new TreeMap<>(Comparator.comparing(String::length)); // Custom key sorter

for (String name : namesList) { // From a list of Strings, put String as key
    treeMap.put(name, name.length());
}
```
---

# Character

### Primitive to Wrapper
```java
Character d = Character.valueOf('c'); // From primitive to Wrapper
```

### Get ASCII Value of a Character
```java
char myChar = 'a';
int asciiValue = myChar;
System.out.println("From type Casting " + asciiValue);
```

### Get Int from Char (with numerical value) using `-'0'`
```java
char charNum2 = '2';
int num2 = charNum2 - '0';
```

### Character Checks
```java
System.out.println(Character.isLetter('r')); // true 'r' is a letter
System.out.println(Character.isDigit('4')); // true
System.out.println(!Character.isLetterOrDigit('!')); // true : punctuation mark

System.out.println(Character.compare('1', '1')); // Compare character
```

### Int Array to Keep Char ASCII as Index and Array Value as Count
```java
int[] chars = new int[127]; // primitive int array initializes all the values with 0
char test = 'a';
chars[test]++;
chars['A']++;
System.out.println(Arrays.toString(chars)); // The value of Array at index = asciiVal of char is increased by 1
```

### Get Numeric Value from Character
```java
// Same can be achieved through the library method
// Returns unicode for characters from 10 to 35
System.out.println(Character.getNumericValue('A')); // DO NOT USE THIS
System.out.println(Character.getNumericValue(myChar));
System.out.println(Character.getNumericValue('1'));
/*
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ##1##, 0, 0, 0, 0, 0, 0, 
   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,##1##, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]        
  */ 
```

# String

### Basic Methods
```java
str1.equals(str2); // For Equality, DO NOT USE == (will compare objects)

str1.compareTo(str2);
// negative if str is "lexicographically" less than str2
// positive if str is "lexicographically" greater than str2
// ZERO if both strings are equal
```

### Check if Blank
```java
System.out.println(" ".isBlank()); // True -> Returns true if the string is empty or contains only white space
```

### Split
```java
// Cut the Strings from spaces into words
String[] words = strList.split(",");
```

### Trim and Strip
```java
String s = " Malgudi Days   ";
System.out.println(s.trim()); // Trimmed blank spaces with all leading and trailing space removed

System.out.println(s.strip()); // Strip is Unicode Aware
System.out.println(s.stripLeading());
System.out.println(s.stripTrailing());
```

### Contains
```java
String sentence = "Hello, world!";
// Check if the string contains a specific substring
boolean containsHello = sentence.contains("Hello");
```

### charAt and substring()
```java
// returns a character at a given index i
str.charAt(i);
str.substring(i, j); // index j not included
str.substring(i); // from i till end
```

### indexOf and lastIndexOf
```java
// 2 if "er" begins from index 1, -1 if not Found
str.indexOf("er");
str.indexOf("er", 2); // start the search from index 2

str.lastIndexOf("ew"); // searches right to left
str.lastIndexOf("ew", 5); // right to left, from index 5
```

### Case Change
```java
str.toLowerCase();
str.toUpperCase();
```

### Compare and Replace
```java
System.out.println(str.replace("a", "$$"));
System.out.println(str.replace('e', '*')); // Character Replace
String str1 = str.replaceAll(" ", ""); // Replace All, takes RegEx
```

### String to Char Array to String
```java
String str = "Pneumonia";
char[] c = str.toLowerCase().toCharArray();
Arrays.sort(c); // Returns void

String revStr = new String(c);
```

### Turn Anything into String
```java
char c = 'C';
int d = 5;
Integer i = 5;
String newStr = String.valueOf(i);

char[] cArr = {'T', 'e', 's', 't'};
String newStrFromArray = String.valueOf(cArr);
```

# Sorting
All sorts - `Arrays.sort`, `listObj.sort`, `Collections.sort`
- returns void
- changes the input array

### Arrays Sort
```java
int[] intArray = {4, 5, 3, 8, 2, 71};
Arrays.sort(intArray); // Default Natural Sorting Order
Arrays.sort(intArray, Comparator.reverseOrder()); // Reverse sorting
```

### ListObject Sort
`Comparator.nullsFirst()` or `Comparator.nullsLast()` can be used to accommodate null values.
```java
List<Integer> list = Arrays.asList(null, 4, 5, null, 3, 8, 2, 71, null);
list.sort(Comparator.nullsLast(Comparator.naturalOrder())); // Output: [2, 3, 4, 5, 8, 71, null, null, null]
list.sort(Comparator.nullsFirst(Comparator.reverseOrder())); // Output: [null, null, null, 71, 8, 5, 4, 3, 2]

List<String> stringList = Arrays.asList("apple", "banana", "orange");
stringList.sort(Comparator.comparing(String::length).reversed()); // Output: [banana, orange, apple] (since "banana" and "orange" have 6 characters, and "apple" has 5)
```

### Collections Sort
```java
List<Integer> integerListWithNull = Arrays.asList(5, 6, null, 71, 2, 3);
Collections.sort(integerListWithNull, Comparator.nullsLast(Comparator.naturalOrder())); // Output: [2, 3, 5, 6, 71, null]
Collections.sort(integerListWithoutNull, Collections.reverseOrder()); // Output: [71, 6, 5, 3, 2]

List<String> stringList = Arrays.asList("apple", "banana", "orange");
Collections.sort(stringList, Comparator.comparing(String::length)
                                       .thenComparing(Comparator.reverseOrder()));
// Output: [banana, orange, apple] 
// "banana" and "orange" have the same length (6), but "orange" is lexicographically after "banana".
```
---

# Set

### Creating Sets
```java
List<String> namesList = Arrays.asList("Harry", "Hermione", "Ron", "Harry", "Ron", "Ron", "Remus");

// Sorted values returned while iterating in TreeSet
Set<String> treeSet = new TreeSet<>(Comparator.reverseOrder());
treeSet.addAll(namesList); // Output: [Ron, Remus, Hermione, Harry]

// Ordering NOT guaranteed in HashSet
Set<Integer> hashSet = new HashSet<>();
hashSet.addAll(namesList); // Output: (Unordered, but no duplicates, e.g., [Hermione, Remus, Harry, Ron])
```

### Add Elements to a Set
```java
// boolean add(E e);
/* Adds the element to the set and returns true if this set does not have this element.
if the element already exists, the call leaves the set unchanged and returns false */
set.add(value);
```

### Find an Element in a Set
```java
/* Returns true if the key is in the set, false otherwise. */
set.contains(key);
```

### Remove from Set
```java
boolean remove(Object o);
// Removes the specified element from this set if it is present. Returns true if this set contained the element
set.remove(key); // Concurrent Modification Exception in a Loop
itr.remove(); // Use of Iterator to avoid concurrent modification exception
```

### Set Iteration
```java
Iterator<String> itr = set.iterator();
while (itr.hasNext()) {
    if (itr.next().length() % 2 == 0) {
        itr.remove();
    }
}
```

# Queue

### Queue Methods
* `offer()`: Enqueue (add) elements to the queue
* `peek()`: Retrieves, but **does not remove**, the head of this queue, or returns null if this queue is empty.
* `poll()`: Retrieves and removes **the head** of this queue, or returns null if this queue is empty.
* `remove()`: Removes a single instance of the specified element from this queue, if it is present.
* `element()`: Retrieves, but does not remove, the head of this queue; differs from `peek()` -> throws an exception if queue is empty.

```java
// Declare a queue using LinkedList
Queue<String> queue = new LinkedList<>();

// Enqueue (add) elements to the queue
queue.offer("Apple");
queue.offer("Banana");
queue.offer("Orange");
```

## Heap

### Declaring Min and Max Heaps
```java
// Primitive Types
Queue<Integer> pq = new PriorityQueue<>(); // Default Natural Sorting Order
Queue<Integer> pq = new PriorityQueue<>(Comparator.naturalOrder()); // Min Heap
Queue<Integer> pq = new PriorityQueue<>(Comparator.reverseOrder()); // Max Heap

Queue<int[]> heap = new PriorityQueue<>((a, b) -> a[0] - b[0]);//Min heap, increasing order
Queue<int[]> heap = new PriorityQueue<>((int[] a, int[] b) -> b[0] - a[0]);//Max heap, decreasing order

//Heap/Priority Queue of Type T
Queue<Employee> heapMax = new PriorityQueue<>(Comparator.comparing(Employee::getAge) // If the employee age is same
                                                .thenComparing(Employee::getSalary)); // Natural Sort Order
```

### Heap Methods
```java
// Heap methods
pq.offer(100);
pq.poll(); // Pops the root of the heap
```

# Stack

### Stack Methods
* `push(E item)`: Pushes an item onto the top of the stack.
* `pop()`: Removes the object at the top of the stack and returns that object.
* `peek()`: Looks at the object at the top of the stack **without removing** it.
* `empty()`: Checks if the stack is empty.
* `search(Object o)`: Searches for the specified object in the stack and returns its position.

```java
Stack<Integer> stack = new Stack<>();
stack.push(1);
stack.push(2);
stack.push(3);

System.out.println("Top element: " + stack.peek());  // Output: 3

while (!stack.empty()) {
    System.out.println("Popped element: " + stack.pop());
}

// This does not work as stack.pop reduces the size of the stack each time
for (int i = 0; i < stack.size(); i++) {
    System.out.println(stack.pop());
}
```

# Math

### Min and Max
```java
int maxNumber = Math.max(10, 20);
float maxFloat = Math.max(15.5f, 12.7f);

int minNumber = Math.min(10, 20);
float minFloat = Math.min(15.5f, 12.7f);
```

### Power and Square Root
```java
double powerIntResult = Math.pow(2, 3);
double powerFloatResult = Math.pow(2.5, 2);

double sqrtResult = Math.sqrt(25);
```

### Absolute Value
```java
int absoluteIntValue = Math.abs(-5);
float absoluteFloatValue = Math.abs(-8.9f);
```

### Ceil and Floor
```java
double ceilIntResult = Math.ceil(5.3);
float ceilFloatResult = (float) Math.ceil(5.3f);

double floorIntResult = Math.floor(5.9);
float floorFloatResult = (float) Math.floor(5.9f);
```

### Logarithm
```java
double log10IntResult = Math.log10(1000);
double log10FloatResult = Math.log10(1000.0f);
double logResult = Math.log(Math.E); // Log base e of e is 1
```

# Bitwise

### Left Shift (<<)
Shifts the bits to the left by a specified number of positions (n) value << n.
- The vacant positions on the right are filled with zeros.
- It effectively **multiplies** the operand by `2^n`.

### Signed Right Shift (>>)
Shifts the bits of the operand to the right by a specified number of positions.
- It fills the vacant positions on the left with the sign bit (the leftmost bit) to preserve the sign of the number.
- If the number is positive, it fills with 0, and if negative, it fills with 1.
- **Divides** the number by `2^n`.

### Unsigned Right Shift (>>>)
- It fills the vacant positions on the left with zeros, regardless of the sign bit.
- It is used for **logical right shifts**, and it treats the operand as an unsigned quantity.
- ALWAYS use this for the while loop, else infinite loop for negative numbers.

### Bit Representation
```java
short x = 0b11101011;
Integer.toBinaryString(235);
```

### Negative Number Representation
```java
int positiveNum = 0b00101100; // 44
int twoScomplement = 0b11010100;
```

### Extracts the LSB of a Number
```java
(number & 1);
```

### Clear/Unset the Rightmost Set Bit
```java
x & (x - 1);
```

### Extracts the Rightmost Set Bit
```java
x & ~(x - 1); // Isolates the rightmost 1-bit of y and sets all other bits to 0
```

### Set the Nth Bit (Bitmask)
```java
1 << n;
```

### XOR #1 Cancels When Same
```java
(x ^ x); // 0
(x ^ (~x)); // -1
```

### XOR #2 Adding Without Carrying
```java
// Example usage
```

### Parity = 1 When #1's Odd
```java
x = (x & (x - 1));
parity = (parity ^ 1);
```

---

# Boolean Logic

Using switch statements instead of multiple if statements:

{% gist nitinkc/96387a9700c9c58185a969ae48bfdc45 %}

---

# For Loop Traps

```java
// If length = 9, loop will run 0, 2, 4, 6... 8 is never included
for (int i = 0; i < arr.length; i = i + 2) { ... }

// Compare current with previous
for (int i = 1; i < num.length; i++) {
    if (num[i - 1] == num[i]) return true;
}

// Compare current with next
for (int i = 0; i < num.length - 1; i++) {
    if (num[i] == num[i + 1]) return true;
}

// Print alphabets from 'a' to 'z'
for (char i = 'a'; i <= 'z'; i++) {
    System.out.println(i);
}
```

{% gist nitinkc/382798a984e00a732d86a12a6637e0a2 %}

---

# Command Line Arguments

Reading, parsing, and type checking command line inputs:

```java
// Assuming 2 command line arguments: <Name> <Age>
if (args.length == 0 || args.length > 2) {
    System.err.println("Incorrect Number of arguments passed");
    System.exit(-1);
}

String name = args[0];
int age = Integer.parseInt(args[1]);
```

---

# Running Time Measurement

```java
// Get current time in milliseconds (from Jan 1, 1970)
long startTime = System.currentTimeMillis();
// ... code to measure ...
long endTime = System.currentTimeMillis();
System.out.println("Time taken: " + (endTime - startTime) + " ms");

// For more precise measurements, use nanoTime
long startNano = System.nanoTime();
// ... code to measure ...
long endNano = System.nanoTime();
System.out.println("Time taken: " + (endNano - startNano) + " ns");
```

---

# Random Numbers

```java
import java.util.Random;

// Math.random() - returns a double [0.0, 1.0)
double randomValue = Math.random();
System.out.println("Random value: " + randomValue);

// Using Random class
Random generator = new Random(); // or new Random(123) with seed
int diceThrow = generator.nextInt(6) + 1; // Range 1 to 6 (dice)

generator.nextInt(); // Range: -2^31 to 2^31 - 1
generator.nextDouble(); // Range: 0.0 to 1.0
```

---

# Java Input and Output

## Keyboard Input

```java
import java.util.Scanner;

Scanner in = new Scanner(System.in);

/* Input Problem: Mix of int and strings
   Extra invocation to get rid of previous \n */
int n = in.nextInt();
in.nextLine(); // To avoid INPUT Problem - consume the newline
String str = in.nextLine();

in.nextLine(); // Reads entire line
in.next(); // Reads next character up to (but not including) space

/* NO METHOD TO READ A SINGLE CHARACTER */
char a = in.nextLine().charAt(0);
```

## File Input

```java
import java.io.File;
import java.util.Scanner;

// Open the File
File myFile = new File("/path/to/file.txt");
Scanner in = new Scanner(myFile);

// Read from the File
String str = in.nextLine();

// OR read all lines
while (in.hasNext()) {
    System.out.println(in.nextLine());
}

// Close the File
in.close();
```

## File Output

### Writing Text to File
```java
import java.io.PrintWriter;
import java.io.FileWriter;

final String FILENAME = "output.txt";

// Overwrite mode (surrounding with try-catch recommended)
PrintWriter output = new PrintWriter(FILENAME);
output.println("Line 1");
output.println("Line 2");
output.close();

// Append mode (to avoid erasing existing files)
PrintWriter pw = new PrintWriter(new FileWriter("output.txt", true));
pw.println("Appended line");
pw.close();
```

### Appending Text to File
```java
FileWriter fw = new FileWriter("Names.txt", true);
PrintWriter pw = new PrintWriter(fw);
pw.println("Appended content");
pw.close();

// OR in one line
PrintWriter pw = new PrintWriter(new FileWriter("Names.txt", true));
```