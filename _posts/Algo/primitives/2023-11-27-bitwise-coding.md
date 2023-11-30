---
title:  "Bitwise Operators"
date:   2023-11-27 08:30:00
categories: ['Algorithms']
tags: ['Algorithms']
---

{% include toc title="Index" %}

**Bit representation**

```java
int x = 0b11101011;//Bit representation of an integer 235
System.out.println(Integer.toBinaryString(235));
```

**Extracts the LSB of a number**
```java
(number & 1)
```

**Unset the rightmost set bit** : flip the **least significant set bit** to 0
```java
`x & (x - 1)`
```

# Bitwise Operators
- `AND (&)`: 1 if both bits are 1; otherwise, it's 0. Product of zero with anything is a zero
- `OR (|)`: 1 if either of the bits is 1; otherwise, it's 0. behaves like an addition
- `XOR (^)`: The result is `1 | TRUE` if the bits are **different**; otherwise, for same bits it's 0.
- `NOT (~)`: Changes 1 to 0 and 0 to 1.
- `Left Shift (<<)`: Shifts th
    - This operator shifts the bits to the left.
    - The vacant positions on the right are filled with zeros.
    - It effectively **multiplies** the operand by 2 raised to the power of the right operand.
- NO `<<<`
- `Signed Right Shift (>>)`: Shifts the bits of the operand to the right by a specified number of positions.
    - It fills the vacant positions on the left with the sign bit (the leftmost bit) to preserve the sign of the number.
    - If the number is positive, it fills with 0, and if negative, it fills with 1.
    - **Divides** the number by 2
    - ```java
    int x = -8;//11111111111111111111111111111000
    int result = x >> 1; // result is -4, 11111111111111111111111111111100
   ```
- `Unsigned Right Shift (>>>)`
    - It fills the vacant positions on the left with zeros, regardless of the sign bit.
    - It is used for **logical right shifts**, and it treats the operand as an unsigned quantity.
    - ```java
      int x = -8;//11111111111111111111111111111000
      int result = x >>> 1; // result is 2147483644, 01111111111111111111111111111100
      ```

## XOR (Cancels each other)

- If 2 similar things are XOR'd, it will return False.
- XORing two identical numbers results in 0,
while XORing any number with 0 results in the same number.

The XOR operation returns `1` for bits that are different and `0` for bits that are the same.


Subtracting 1 from x flips the rightmost set bit and sets all the bits to its right to 1.
Performing the bitwise AND operation with x and x - 1 results in all bits being preserved except for the rightmost set bit, which becomes 0.
In other words, this operation effectively removes the rightmost (lowest-order) 1-bit in the binary representation of x.

### The XOR Trick

Same variables cancels the effect of each other if the bitwise XOR is used.

```java
// Use of XOR (both flags are boolean) - Exactly one is True
if (flag2 ^ flag4)
//is equivalent to
(flag2 && !flag4) || (!flag2 && flag4);
```

```java
// Works only with integer, in its native form, for others change it into its equivalent binary representation.
a = a^b;
b = a^b; //a^b^b yields a
a = a^b;//a^b^a = b(b is recently converted to a)
```

The logic is used for finding a unique element among duplicates (Stolen Drone problem (21) in Interview cake)

{% gist nitinkc/c2b08480ddf73b06f2ad1df65be5483d %}

## More Examples



1. **Finding Unique Numbers:** If you XOR all numbers in an array, duplicate numbers will cancel each other out,
   leaving you with the unique number. Use this trick to **find Unique numbers** in an Array with O(1) space and O(n) time complexity.'
    2. To find all uniques, use a **set** (On adding in set, if false, remove) as well, but it will use O(n) space and time complexity.

2. **Swapping Numbers:** You can swap two numbers using XOR without using a temporary variable: `a = a ^ b; b = a ^ b; a = a ^ b;`

3. **Finding Missing Number:** You can find a missing number in a sequence by XORing all numbers with the sequence from 1 to n. The result will be the missing number.



1. **Checking if a Number is Even or Odd:**
   ```java
   boolean isEven = (num & 1) == 0; // true if even, false if odd
   ```
   Explanation: In binary representation, even numbers have their least significant bit (LSB) set to 0, 
while odd numbers have it set to 1. 
Thus **extract the LSB** of the number and if the result is 0, the number is even; if it's 1, the number is odd.

2. **Swapping Two Numbers:**

   ```java
   a = a ^ b;
   b = a ^ b;
   a = a ^ b;
   ```

   Explanation: This code uses XOR to swap the values of `a` and `b` without using a temporary variable. 
When you XOR a value twice with the same number, it returns the original value (XOR is its own inverse). 
The sequence of operations effectively swaps the values of `a` and `b`.

3. **Finding the Missing Number:**

   ```java
   int findMissing(int[] nums) {
       int result = nums.length;
       for (int i = 0; i < nums.length; i++) {
           result ^= i ^ nums[i];
       }
       return result;
   }
   ```

   Explanation: This code finds the missing number in an array containing elements from 0 to n. 
It XORs each index `i` and corresponding value `nums[i]`, along with the indices themselves (0 to n-1), 
and finally with `n`. This effectively cancels out all the numbers that are present, leaving only the missing number.

4. **Counting Set Bits (1s) in an Integer:**

- `(x & 1)` can either be Zero or 1
- returns `1` if the Least Significant Bit (LSB) of `x` is 1 else `0`.

{% gist nitinkc/21506427325bbe9cad52867af3134ca0 %}

```java
if ((x & 1) == 1) {
    count++;
}
//can be replaced with
count += (x & 1);
```

**Brian Kernighan's algorithm**

```java
int countSetBits(int num) {
    int count = 0;
    while (num > 0) {
        num &= (num - 1);
        count++;
    }
    return count;
}
```

   Explanation: This code uses Brian Kernighan's algorithm to count the number of set bits (1s) in an integer.
In each iteration, it flips the **least significant set bit** to 0 by performing a bitwise AND operation with `num - 1`. 
This effectively counts and removes one set bit in each iteration.

5. **Finding Power of 2:**

   ```java
   boolean isPowerOf2(int num) {
       return (num & (num - 1)) == 0;
   }
   ```

   Explanation: This code checks if a number is a power of 2. A binary representation of a power of 2 has only one bit set. When you subtract 1 from a power of 2, all the lower bits are set to 1. Performing a bitwise AND with the original number and its decremented value will result in 0 if it's a power of 2.

6. **Toggle Nth Bit:**

   ```java
   int toggleNthBit(int num, int n) {
       return num ^ (1 << n);
   }
   ```

   Explanation: This code toggles the Nth bit of a number by performing a bitwise XOR with a number where only the Nth bit is set (achieved using left shift). This operation flips the value of the Nth bit while leaving other bits unchanged.

7. **Finding Maximum and Minimum:**

   ```java
   int max = b ^ ((a ^ b) & -(a < b ? 1 : 0));
   int min = a ^ ((a ^ b) & -(a < b ? 1 : 0));
   ```

   Explanation: These code snippets find the maximum and minimum of two numbers (`a` and `b`) using bitwise operations. The expression `(a < b ? 1 : 0)` evaluates to 1 if `a` is less than `b`, and 0 otherwise. The bitwise AND operation with `-1` (all bits set) or `0` (all bits cleared) determines whether the maximum or minimum value is selected.

These explanations should help clarify how each bitwise operation is being used and why these tricks are effective for solving specific problems. Remember that while these techniques might not be the most intuitive at first, they can provide efficient solutions to various coding challenges.

