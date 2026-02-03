---
title: Recursion
date: 2026-01-16 13:05:00
categories:
- Algorithms
tags:
- Recursion
---

{% include toc title="Index" %}


> If a problem is asked to be solved without using loops (for or while), then recursion is the way to go.

```java
void printReverseLinkedList(ListNode head){
  if(head == null)
    return;
    
    printReverseLinkedList(head.next);
    System.out.println(head.data);
}
```

## Steps to thinking Recursively
- A thought on base cases :
  - identify a condition where no further recursive calls are needed?
  - What is the smallest input for which the problem can be solved trivially?
  - What is the simplest version of the problem that can be solved directly without recursion?


**Step 1** : Base condition
- Be mindful of the if-else conditions in the base case
- Try to achieve the simplest base case possible
```java
//Count number of 7's in a number

//This is more verbose and keeps one smaller case. there is even more smaller sub case
if(n/10 == 0){//Last remaining digit
    if(n%10 == 7)
      return 1;
    else
      return 0;
}

// Can also be written as
        
if(n == 0) //Exhausting the digits
    return 0;
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

## Math based Recursion
### Factorial
```java
public int factorial(int n) {
  if(n == 1)
    return 1;
  
  return n* factorial(n-1);
}
```

### Fibonacci
- fib(0) = 0, fib(1) = 1
- `  if(n == 0 || n == 1)` is equivalent to `if(n <= 1)`
```java
public int fibonacci(int n) {
  //base condition
  if(n == 0 || n == 1)
    return n;
  
  return fibonacci(n-1) + fibonacci(n-2);
}
```

### Power of a number

- `if(n == 1) return base;` or `if(n == 0) return 1;` for n>=0
```java
// for n >1 always condition
public int powerN(int base, int n) {
  if(n == 1)
    return base;

  return base*powerN(base,n-1);
}
```

- when negative exponents are allowed
```java
if(n == 0) return 1;

  if(n > 0)
    return x*myPow(x,n-1);
  else
    return myPow(x,n+1)/x;
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

### Digit based Recursion
- mod (%) by 10 yields the rightmost digit (126 % 10 is 6).
- while divide (/) by 10 removes the rightmost digit (126 / 10 is 12).

#### Sum of digits in a number
```java
public int sumDigits(int n) {
  if(n/10 == 0)
    return n;
  
  return n%10 + sumDigits(n/10);
}
```
#### Count 7s in a number
[https://codingbat.com/prob/p101409](https://codingbat.com/prob/p101409)
```java
public int count7(int n) {
  if(n == 0)
    return 0;
  
  if(n%10 == 7)
    return 1 + count7(n/10);
  return count7(n/10);
}
```

**Note:** The verbose version with `if(n/10 == 0)` also works but is unnecessarily complex. Prefer the simpler condition.

## Strings
Think of chatAt(index) and substring(start,end)/substring(start)

Count x in a string

### Navigate through the beginning
- str.charAt(0) gives the leftmost character of the string
- str.substring(1) removes the leftmost character from the string
  ```java
  public int countX(String str) {
    if (str.length() == 0) 
      return 0;
    
    if (str.charAt(0) == 'x')
       return 1+countX(str.substring(1,str.length()));
    return countX(str.substring(1));
  }
  ```

### Navigate through the end
  - str.charAt(str.length()-1) gives the rightmost character of the string
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

### Navigating through both ends
(https://codingbat.com/prob/p137918)[https://codingbat.com/prob/p137918]

```java
public String parenBit(String str) {
  if(str.charAt(0) !='(' )
    return parenBit(str.substring(1));

  if(str.charAt(str.length()-1)!=')')
    return parenBit(str.substring(0, str.length()-1));

  return str;
}
```

### 2 separate base cases, sequencing matters
[https://codingbat.com/prob/p118182](https://codingbat.com/prob/p118182)
```java
public boolean strCopies(String str, String sub, int n) {
  if(n==0) return true;

  if(str.length() < sub.length())
    return false;
  
  if(str.substring(0,sub.length()).equals(sub))
    return strCopies(str.substring(1),sub,n-1);
    
  return strCopies(str.substring(1),sub,n);
}
```
## Quick Reference: Base Cases for All Problem Types

| **Category**   | **Problem Type**           | **Input**    | **Base Case**                     | **Return**               | **Key Insight**                         |
|:---------------|:---------------------------|:-------------|:----------------------------------|:-------------------------|:----------------------------------------|
| **Math**       | Factorial                  | `n`          | `n == 1` or `n == 0`              | `1`                      | Stop at identity element                |
| **Math**       | Fibonacci                  | `n`          | `n == 0 \|\| n == 1`              | `n`                      | Two seed values                         |
| **Math**       | Power                      | `base, n`    | `n == 0`                          | `1`                      | Any number to power 0 is 1              |
| **Math**       | Power (negative)           | `x, n`       | `n == 0`                          | `1`                      | Handle signs separately after base case |
| **Math**       | Sum 1 to n                 | `n`          | `n == 0`                          | `0`                      | Identity for addition                   |
| **Counting**   | Bunny ears (static)        | `bunnies`    | `bunnies == 0`                    | `0`                      | No bunnies = no ears                    |
| **Counting**   | Bunny ears (conditional)   | `bunnies`    | `bunnies == 0`                    | `0`                      | Works for both even/odd branches        |
| **Digits**     | Sum digits                 | `n`          | `n/10 == 0` or `n == 0`           | `n` or `0`               | Simplest: just `n == 0` → `0`           |
| **Digits**     | Count specific digit       | `n`          | `n/10 == 0`                       | `n%10 == target ? 1 : 0` | Extract last digit directly             |
| **String**     | Count single char          | `str`        | `str.length() == 0`               | `0`                      | Empty string has count 0                |
| **String**     | Find size > 1 pattern      | `str`        | `str.length() < pattern.length()` | `0`                      | Can't match if string too short         |
| **String**     | Count pairs (offset)       | `str`        | `str.length() <= 2`               | `0`                      | Need 3+ chars minimum                   |
| **Array**      | Search/Count (index-based) | `arr, index` | `index >= arr.length`             | `0` or `false`           | Out of bounds = base case               |
| **Array**      | Check element              | `arr, index` | `index >= arr.length`             | `false`                  | Not found if exhausted                  |
| **Tree**       | Any traversal              | `node`       | `node == null`                    | `void` (stop)            | Null reference = leaf boundary          |
| **LinkedList** | Any traversal              | `head`       | `head == null`                    | `void` (stop)            | Null = end of list                      |

**Key Patterns:**
- **Numbers (n):** Usually `n == 0` or `n == 1` depending on identity element
- **Strings (s):** Always `length == 0` or `length < target_pattern_length`
- **Arrays/Index:** Always `index >= array.length`
- **Trees/LinkedLists:** Always `node == null`


```
### Strings with size > 1
- count hi
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

### Count Substring occurrences
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

### [Count pairs](https://codingbat.com/prob/p154048)
```java
public int countPairs(String str) {
  if(str.length() <= 2) return 0;//A minimum of 2 chars are needed
  
  if(str.charAt(0) == str.charAt(2))
    return 1 + countPairs(str.substring(1));
  
  return countPairs(str.substring(1));
}
```

## Where Sequence matters

```java
List<Integer> list = new ArrayList<>();

public List<Integer> inorderTraversal(TreeNode root) {
    //Inorder = Left-Root-Right
    inorder(root);
    return list;
}

private void inorder(TreeNode root){
    if(root==null){
        return;
    }

    inorder(root.left);//inorderTraversal(root.left);
    list.add(root.val);
    inorderTraversal(root.right);

}
```

## Array
**Simple rule for arrays:** Use `if(index >= arr.length)` as base case. This avoids verbose checks like checking `length == index+1` or examining the array bounds redundantly.

Why this works:
- `index >= arr.length` catches both empty arrays and exhausted indices
- Single, clear condition before processing the current element
- No need to bundle element checks with the boundary check

### Check if array contains 6
```java
public boolean array6(int[] nums, int index) {
  if(index >= nums.length)
    return false;

  if(nums[index] == 6)
    return true;
    
  return array6(nums, index+1);
}
```

### Count occurrences of 11 in array
```java
public int array11(int[] nums, int index) {
  if(index >= nums.length)
    return 0;

  if(nums[index] == 11)
    return 1 + array11(nums, index+1);
    
  return array11(nums, index+1);
}

```

## Conversion from Recursion to Iteration for DP
- Identify the base cases and initialize them in a dp array(usually one larger than input size).
- Identify the recurrence relation and fill the dp array iteratively using nested loops if needed.
- Return the final result from the dp array.



## Quick Reference: Base Cases for All Problem Types

| **Category** | **Problem Type** | **Input** | **Base Case** | **Return** | **Key Insight** |
|---|---|---|---|---|---|
| **Math** | Factorial | `n` | `n == 1` or `n == 0` | `1` | Stop at identity element |
| **Math** | Fibonacci | `n` | `n == 0 \|\| n == 1` | `n` | Two seed values |
| **Math** | Power | `base, n` | `n == 0` | `1` | Any number to power 0 is 1 |
| **Math** | Power (negative) | `x, n` | `n == 0` | `1` | Handle signs separately after base case |
| **Math** | Sum 1 to n | `n` | `n == 0` | `0` | Identity for addition |
| **Counting** | Bunny ears (static) | `bunnies` | `bunnies == 0` | `0` | No bunnies = no ears |
| **Counting** | Bunny ears (conditional) | `bunnies` | `bunnies == 0` | `0` | Works for both even/odd branches |
| **Digits** | Sum digits | `n` | `n/10 == 0` or `n == 0` | `n` or `0` | Simplest: just `n == 0` → `0` |
| **Digits** | Count specific digit | `n` | `n/10 == 0` | `n%10 == target ? 1 : 0` | Extract last digit directly |
| **String** | Count single char | `str` | `str.length() == 0` | `0` | Empty string has count 0 |
| **String** | Find size > 1 pattern | `str` | `str.length() < pattern.length()` | `0` | Can't match if string too short |
| **String** | Count pairs (offset) | `str` | `str.length() <= 2` | `0` | Need 3+ chars minimum |
| **Array** | Search/Count (index-based) | `arr, index` | `index >= arr.length` | `0` or `false` | Out of bounds = base case |
| **Array** | Check element | `arr, index` | `index >= arr.length` | `false` | Not found if exhausted |
| **Tree** | Any traversal | `node` | `node == null` | `void` (stop) | Null reference = leaf boundary |
| **LinkedList** | Any traversal | `head` | `head == null` | `void` (stop) | Null = end of list |

**Key Patterns:**
- **Numbers (n):** Usually `n == 0` or `n == 1` depending on identity element
- **Strings (s):** Always `length == 0` or `length < target_pattern_length`
- **Arrays/Index:** Always `index >= array.length`
- **Trees/LinkedLists:** Always `node == null`

