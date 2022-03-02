---
title:  "Utility Methods"
date:   2021-11-06 02:42:00
categories: Algorithms
tags: [Algorithms]
---

{% include toc title="Index" %}

## Arrays, Lists and Collections Utility Classes

## Character

While comparing individual characters of a String, `Character.toLowerCase('C')` comes handy.

Note: To uniformaly handle even an odd length Strings, use While loop with the condition  `start < end` with pointers running from both end 

```java
private static Boolean isPalindrome(String word) {
    for (int i = 0, j = word.length()-1; i < j; i++,j--) {
        if(Character.toLowerCase(word.charAt(i)) != Character.toLowerCase(word.charAt(j)))
            return false;
    }
    return true;
}
```

Identify if a character is alphanumeric or Skipping punctuation marks `Character.isLetterOrDigit(str.charAt(i))`

```java
private static Boolean isStringPalindrome(String str) {
    int i = 0, j = str.length()-1;
    while (i < j) {
        //Skip punctuation marks
        while(!Character.isLetterOrDigit(str.charAt(i)) && i < j)
            i++;

        while(!Character.isLetterOrDigit(str.charAt(j)) && i < j)
            j--;

        if(Character.toLowerCase(str.charAt(i)) != Character.toLowerCase(str.charAt(j)))
            return false;
        i++;j--;
    }
    return true;
}
```

## String 

From String to char array

```java
String str = "Ramdom String";
char[] charArr = str.toCharArray();
```

From Char Array to String
```java
String newStr = new String(charArr);
```



### String to Int

```java
int digit = 0;
int x = str.charAt(i) - '0';//Subtracting '0' char is important

//12345 = 1*10^4 + 2*10^3 + 3*10^2 + 4*10^1 + 5*10^0;
digit = (int) (digit + (x* Math.pow(10,str.length()-1-i)));

//12345 = 1 -> 10+2 -> 120+3 -> 1230+4 -> 12340+5
digit = digit*10 + x;
```