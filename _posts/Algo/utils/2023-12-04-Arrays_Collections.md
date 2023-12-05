---
title:  "Arrays, List and Collections Class"
date:   2023-12-04 18:30:00
categories: Algorithms
tags: [Algorithms]
---
{% include toc title="Index" %}

# Array Syntax
[Refer All types of syntax](https://nitinkc.github.io/algorithms/array-syntax/)


### The Arrays Class - for Arrays

#### Arrays fill
{% gist nitinkc/8a955a843d2b383d88b7ca92997c627f %}

##### Arrays.asList & List.of

Arrays.asList accepts Wrapper Class array.
```java
//Accepts arrays of Integer, Character, String etc.
List<Integer> list = Arrays.asList(arr);
```

The `Arrays.asList()` method works with objects, **not primitive** types.

```java
// Create an array
String[] array = {"apple", "banana", "orange"};

// Convert array to ArrayList using Arrays.asList()
List<String> arrayList = new ArrayList<>(Arrays.asList(array));

int intArray[] = {1,2,3};
List<Integer> a = Arrays.asList(intArray);// FOR PRIMITIVES, DOES NOT WORK, change to INTEGER
        
List<Integer> b = List.of(1,2,3);//Immutable List

//Printing an ArrayList as ann Integer
Arrays.toString(a);//op: [1,2,3]
```

To convert primitive array into a list of Wrapper class (list of primitive class is not possible)

```java
int[] arr = {1, 2, 1, 3, 4, 5, 2, 1, 3, 4, 5, 6, 7, 8, 97, 1, 2};

 List<Integer> list = Arrays.stream(arr)// IntStream
                .boxed()// Stream<Integer>
                .collect(Collectors.toList());

list = IntStream.of(arr)//IntStream, Static Factory method
                .boxed()
                .collect(Collectors.toList());

Integer[] intAr = Arrays.stream(arr)// IntStream
                .boxed()// Stream<Integer>
                .toArray(Integer[]::new);

intAr = IntStream.of(arr)//IntStream, Static Factory method
                .boxed()
                .toArray(Integer[]::new);
```

```java
 char c[] = {'T','e','s','t'};

Character[] charArrBoxed = new String(c).chars()
                            .mapToObj(ch -> (char) ch)
                             .toArray(Character[]::new);
        
List<Character> characterList = new String(c).chars()
                .mapToObj(ch -> (char) ch)
                .collect(Collectors.toList());
```


### ArrayList to Array
```java
//Converting an ArrayList into Array
int[] result = a.toArray();
```

### Array sorting

[Sorting in Detail](https://nitinkc.github.io/java/sorting/)


Traditional Array can be sorted with sort method Arrays Utility Class.

##### Sorting an Array of primitives
```java
int[] arr = {4,5,3,8,2};
Arrays.sort(arr);
```

```java
//Sort takes array
int intArray[] = {4,5,3,8,2,71};

Arrays.sort(intArray);// Default Natural Sorting Order
Arrays.sort(integerArray, Comparator.reverseOrder());//Comparator can be used with a CLASS - Reverse sorting
        
String[] stringArray = {"one", "two", "three", "four"};
Arrays.sort(stringArray);
Arrays.sort(stringArray, Comparator.reverseOrder());
```

#### Sorting via list object

For list of type T, a comparator has to be defined.
```java
list.sort(Comparator
        .comparing(Data::getPopulation).reversed()
        .thenComparing(Data::getState)
        .thenComparing(Data::getCity));
```

```java
String[] array = {"apple", "banana", "orange"};
// Convert array to ArrayList using Arrays.asList()
List<String> arrayListString = new ArrayList<>(Arrays.asList(array));
arrayListString.sort(Comparator.naturalOrder());

List<Integer> arrayListInteger = Arrays.asList(4,5,3,8,2,71);
arrayListInteger.sort(Comparator.reverseOrder());
```

##### Sorting via Collections Class


```java
// Sort the List of Objects based on the Population
list.sort(Comparator
        .comparing(Data::getPopulation).reversed()
        .thenComparing(Data::getState)
        .thenComparing(Data::getCity));
        

//Comparator.nullsLast is null safe and takes care in case there is a null.
List<String> empList = list.stream()
        .sorted(Comparator.comparing(Employee::getSalary,Comparator.nullsLast(Comparator.naturalOrder())))
        .map(employee -> ...)
        .collect(Collectors.toList());
```

# The List Class

```java
list.sort(Comparator.naturalOrder());
list.sort(Comparator.naturalOrder());
list.stream().sorted(Comparator.comparing(s -> s.length()));

```
# Collection Class for List

```java
List<String> stringList = Arrays.asList("apple", null, null, "banana", "orange");
Collections.sort(stringList, Comparator.nullsFirst(Comparator.naturalOrder()));

List<String> stringList = Arrays.asList("apple","banana", "orange");
Collections.sort(stringList, Comparator
    .comparing(String::length)
    .thenComparing(Comparator.reverseOrder()));
```

