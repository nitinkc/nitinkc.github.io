---
title:  "Utility Methods"
date:   2021-11-06 02:42:00
categories: Algorithms
tags: [Algorithms]
---

{% include toc title="Index" %}


## Character

While comparing individual characters of a String, this comes handy.
```java
Character.toLowerCase('A')
``` 

Note: To uniformaly handle even an odd length Strings, use While loop with the condition  `start < end` with pointers running from both end 

{% gist nitinkc/677d996fd8fab0b033c8339e4fe6ae6d %}


Identify if a character is alphanumeric or Skipping punctuation marks 
```java
Character.isLetterOrDigit(str.charAt(i))
```
{% gist nitinkc/eb96b7d58398b277e97e8df6b6f22e0a %}

```java
char c = '9';
Character.isDigit(c)//True
c = 'S';
Character.isLetter(c)
```


## String 

##### From String to char array

```java
String str = "Ramdom String";
char[] charArr = str.toCharArray();
```

##### From Char Array to String
```java
String newStr = new String(charArr);
```

##### Turn anything into String
```java
char c = 'C';
int d = 5;
Integer i = 5;
String newStr = String.valueOf(i));

char c[] = {'T','e','s','t'};
String newStr = String.valueOf(c);
```

##### String to Int

```java
int digit = 0;
int x = str.charAt(i) - '0';//Subtracting '0' char is important

//12345 = 1*10^4 + 2*10^3 + 3*10^2 + 4*10^1 + 5*10^0;
digit = (int) (digit + (x* Math.pow(10,str.length()-1-i)));

//12345 = 1 -> 10+2 -> 120+3 -> 1230+4 -> 12340+5
digit = digit*10 + x;
```

##### Integer

```java 
int i = Integer.parseInt("12345");
Integer x = Integer.valueOf("67");
int j = Integer.valueOf("1234").intValue();
```

##### String Joining

```java
 // No more Off-By-One Issue
String combinedString = String.join(", ", list));

String combinedString = list.stream()
            .map(String::toUpperCase)
            .collect(Collectors.joining(" && ");
```


## Optional ofNullable
Instead of using then else statement, use of optional can be handy

```java
Optional.ofNullable(str1).orElse(str2)
```

## Math

```java
int temp = Math.min(height[left],height[right]) * (right - left);

```

## Arrays

#### Arrays fill
{% gist nitinkc/8a955a843d2b383d88b7ca92997c627f %}

Arrays.asList accepts Wrapper Class array.
```java
//Accepts arrays of Integer, Character, String etc.
List<Integer> list = Arrays.asList(arr);
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

## Sorting Arrays

##### Sorting an Array of primitives
```java
int[] arr = {4,5,3,8,2};
Arrays.sort(arr);
```

### Sorting List

For list of type T, a comparator has to be defined.
```java
list.sort(Comparator
        .comparing(Data::getPopulation).reversed()
        .thenComparing(Data::getState)
        .thenComparing(Data::getCity));
```

For list of primitive type, use

```java
list.sort(Comparator.naturalOrder());


```java
Collections.sort();
```

## Collectors.toMap

Collectors is a utility Class just like Collections.


```java
public static <T, K, U>
    Collector<T, ?, Map<K,U>> toMap(Function<? super T, ? extends K> keyMapper,
                                    Function<? super T, ? extends U> valueMapper)
```


### Boolean

```java
String str = "undefined";
//Handles null, str can be True, true to pass
Boolean.valueOf(str)
```