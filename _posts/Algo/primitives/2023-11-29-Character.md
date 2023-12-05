---
title:  "Character Utility Class"
date:   2023-11-19 23:30:00
categories: Algorithms
tags: [Algorithms]
---

{% include toc title="Index" %}

- `int asciiValue = (int) 'A'`
  - `'A' - 0` - Zero as an integer, works only for alphabets, returns ASCII values of the alphabet
    - ```java
        int intValueOfChar = 'A' - 0;//65 
      ```
- Integer representation of a integer Character with int casting or subtraction with character 0
- `int x = '9' - '0';` is used to convert a character representing a digit to its corresponding integer value. 
  - In ASCII, the characters '0' to '9' are represented by consecutive values (48 to 57, respectively).
  - If c is '0', then c - '0' evaluates to 48 - 48, resulting in 0.
  - If c is '1', then c - '0' evaluates to 49 - 48, resulting in 1.
  - If c is '2', then c - '0' evaluates to 50 - 48, resulting in 2
- `int x = Character.getNumericValue(c);` does the same as above


### Character.getNumericValue()
Use only for numerical characters to get the int value from character
{% gist nitinkc/5d0e5275e9d726f9011eb2106ec467cc %}

### Character.toLowerCase()
While comparing individual characters of a String, this comes handy.
```java
Character.toLowerCase('A')
``` 

Note: To evenly handle even an odd length Strings, use While loop with the condition  `start < end` with pointers running from both end
{% gist nitinkc/677d996fd8fab0b033c8339e4fe6ae6d %}

### Character.isLetterOrDigit()
Identify if a character is alphanumeric or **Skipping punctuation marks**
```java
Character.isLetterOrDigit(str.charAt(i))
```
{% gist nitinkc/eb96b7d58398b277e97e8df6b6f22e0a %}

### isLetter() & OrDigit()
```java
char c = '9';
Character.isDigit(c);//True
c = 'S';
Character.isLetter(c).//True
```


