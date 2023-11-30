---
title:  "Bitwise Operators"
date:   2023-11-27 08:30:00
categories: ['Coding']
tags: ['Coding']
---

**Bit representation**

```java
int x = 0b11101011;//Bit representation of an integer 235   
```

# Checking the LSB of a number to be 1

`(x & 1)` can eityher be Zero or 1 
- returns `1` if the Least Significant Bit (LSB) of `x` is 1 else `0`.

{% gist nitinkc/21506427325bbe9cad52867af3134ca0 %}

```java
if ((x & 1) == 1) {
    count++;
}
```
can be replaced with 

```java
count += (x & 1);
```


XOR 

The XOR operation returns `1` for bits that are different and `0` for bits that are the same.

The expression x & (x - 1) is a bitwise operation commonly used to unset the rightmost set bit (1) in the binary representation of the integer x. Here's how it works:

Subtracting 1 from x flips the rightmost set bit and sets all the bits to its right to 1.
Performing the bitwise AND operation with x and x - 1 results in all bits being preserved except for the rightmost set bit, which becomes 0.
In other words, this operation effectively removes the rightmost (lowest-order) 1-bit in the binary representation of x. 