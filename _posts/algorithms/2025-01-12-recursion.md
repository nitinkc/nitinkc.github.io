---
title: Recursion
date: 2025-01-12 13:05:00
categories:
- Algorithms
tags:
- Algorithms
---

{% include toc title="Index" %}

**Step 1** : Base condition
- Be mindful of the if-else conditions in the base case
```java
if(n/10 == 0){
    if(n%10 == 7)
      return 1;
    else
      return 0;
}
```

**Step 2** : Recurrence Relation 
Multiple flavors 
- `n* factorial(n-1)`
  - `2+bunnyEars(bunnies-1)`
- `fibonacci(n-1) + fibonacci(n-2)`
- `n%10 + sumDigits(n/10)`
```java
binarySearch(arr,lt,rt,target);
```


### Factorial
```java
public int factorial(int n) {
  if(n == 1)
    return 1;
  
  return n* factorial(n-1);
}
```

### Fibonacci
```java
public int fibonacci(int n) {
  //base condition
  if(n == 0 || n == 1)
    return n;
  
  return fibonacci(n-1) + fibonacci(n-2);
}
```

### Power of a number
```java
public int powerN(int base, int n) {
  if(n == 1)
    return base;

  return base*powerN(base,n-1);
}
```

### Sum to n
```java
public int triangle(int n) {//sum of n numbers upto n
  //base case
  if(n == 0)
    return 0;
  
  return n+triangle(n-1);
}
```

### Bunny Ears

#### Each bunny has 2 ears
```java
public int bunnyEars(int bunnies) {
  //Base Condition
  
  if(bunnies == 0)
    return 0;
    
  return 2+bunnyEars(bunnies-1);
}
```

#### Odd bunnies have 2 ears, even bunnies have 3 ears
[https://codingbat.com/prob/p107330](https://codingbat.com/prob/p107330)
```java
public int bunnyEars2(int bunnies) {
  if(bunnies == 0)
    return 0;
  
  if(bunnies %2 == 0){//even
    return 3+bunnyEars2(bunnies-1);
  } else {
    return 2+bunnyEars2(bunnies-1);
  }
}
```
# Numbers
- mod (%) by 10 yields the rightmost digit (126 % 10 is 6).
- while divide (/) by 10 removes the rightmost digit (126 / 10 is 12).

### Sum of digits in a number

```java
public int sumDigits(int n) {
  if(n/10 == 0)
    return n;
  
  int sum = 0;
  return n%10 + sumDigits(n/10);
}
```

[https://codingbat.com/prob/p101409](https://codingbat.com/prob/p101409)
```java
public int count7(int n) {
  if(n/10 == 0){
    if(n%10 == 7)
      return 1;
    else
      return 0;
  }
  if(n%10 == 7)
    return 1 + count7(n/10);
  return count7(n/10);
}
```
# Strings
- Navigate through the end
  - str.substring(0, str.length()-1) removes the rightmost character from the string
    - substring(start, end) includes the start index but **excludes** the end index
```java
public int countX(String str) {
  if(str.length() == 0)
    return 0;
  
  if(str.charAt(str.length()-1) == 'x')
    return 1+countX(str.substring(0, str.length()-1));
  return countX(str.substring(0, str.length()-1));
}
```
- Navigate through the beginning
  - str.substring(1) removes the leftmost character from the string
  - str.charAt(0) gives the leftmost character of the string
```java
public int countX(String str) {
  if (str.length() == 0) 
    return 0;
  
  if (str.charAt(0) == 'x')
     return 1+countX(str.substring(1,str.length()));
  return countX(str.substring(1,str.length()));
}
```

## Strings of size 2
```java
public int countHi(String str) {
  if(str.length() <= 1)
    return 0;
    
  if(str.substring(0,2).equals("hi"))
    return 1 + countHi(str.substring(2));
    
  return countHi(str.substring(1));
}
```
- count 11
```java
public int count11(String str) {
  if(str.length() < 2)
    return 0;
  
  if(str.substring(0,2).equals("11"))
    return 1+count11(str.substring(2));
  return count11(str.substring(1));  
}
```

###
[https://codingbat.com/prob/p186177](https://codingbat.com/prob/p186177)
```java
public int strCount(String str, String sub) {
  if(str.length() < sub.length())
    return 0;
    
  if(str.substring(0,sub.length()).equals(sub))
    return 1+strCount(str.substring(sub.length()),sub);//ensuring no overlapping
  return strCount(str.substring(1),sub);//ensuring all possible scenarios
}
```

# Array

```java
public boolean array6(int[] nums, int index) {
  if(nums.length == 0)
    return false;
    
  if(nums.length == index+1){
    if(nums[index] == 6)
      return true;
    return false;
  }

  if(nums[index] == 6)
    return true || array6(nums, index+1);;
    
  return array6(nums, index+1);
}
```