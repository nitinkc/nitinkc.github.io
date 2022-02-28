---
title:  "Utility Methods"
date:   2021-11-06 02:42:00
categories: Algorithms
tags: [Algorithms]
---

{% include toc title="Index" %}

## Arrays, Lists and Collections Utility Classes

## Character Utility Class

```java
Character.toLowerCase(word.charAt(i))

private static Boolean isPalindrome(String word) {
    for (int i = 0, j = word.length()-1; i < j; i++,j--) {
        if(Character.toLowerCase(word.charAt(i)) != Character.toLowerCase(word.charAt(j)))
            return false;
    }
    return true;
}
```

//Skip punctuation marks
while(!Character.isLetterOrDigit(str.charAt(i)) && i < j)
    i++;

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