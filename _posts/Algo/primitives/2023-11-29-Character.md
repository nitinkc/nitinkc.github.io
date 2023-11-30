---
title:  "Character Utility Class"
date:   2023-11-19 23:30:00
categories: Algorithms
tags: [Algorithms]
---

{% include toc title="Index" %}


Integer representation of a Character with 
- `Character.getNumericValue('A')`
- `'A' - 0` - Zero as an integer, works only for alphabets

```java
int intValueOfChar = 'A' - 0;//65

//Same can be achieved through the library method
int numericValue = Character.getNumericValue(c);
```

While comparing individual characters of a String, this comes handy.
```java
Character.toLowerCase('A')
``` 

Note: To evenly handle even an odd length Strings, use While loop with the condition  `start < end` with pointers running from both end

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


