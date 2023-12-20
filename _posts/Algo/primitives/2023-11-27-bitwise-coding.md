---
title:  "Bitwise Operators"
date:   2023-11-27 08:30:00
categories: ['Algorithms']
tags: ['Algorithms']
---

{% include toc title="Index" %}

# Summary

| **Concept**                           | **Code Snippet**                                                              | **Mnemonic**                                                                                                                                |
|:--------------------------------------|:------------------------------------------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------|
| **Bit representation**                | `short x = 0b11101011;`<br>`Integer.toBinaryString(235)`                      |                                                                                                                                             |
| **Negative number**                   | `int positiveNum= 0b00101100;//44`<br>`int twoScomplement = 0b11010100;`      | 2's complement $$ (X' = \text{invert}(X) + 1) $$  <br>**Flip all the bits after the First 1 from LSB (rightmost Setbit), Go Left to Right** |
| **Extracts the LSB of a number**      | `(number & 1)`                                                                |                                                                                                                                             |
| **Clear/Unset the rightmost set bit** | `x & (x - 1)`                                                                 | Clear the **Least Significant Set Bit**                                                                                                     |
| **Extracts the rightmost set bit**    | `x & ~(x - 1)` isolates the rightmost 1-bit of y and sets all other bits to 0 |                                                                                                            |
| **Set the Nth bit** Bitmask           | `1 << n`                                                                      | Set the **Nth Bit**                                                                                                                         |
| **XOR #1 Cancels when same**          | `(x^x);//0` <br> `(x^(~x));//-1`                                              |                                                                                                                                             |
| **XOR #2 Adding Without Carrying**    |                                                                               | **Ex**clude **OR** -> `Add excluding Carry`                                                                                                 |
| **Parity = 1 When #1's Odd**          | `x = (x & (x-1));` <br> `parity = (parity ^ 1);`                              | Parity = 1 When #1's Odd                                                                                                                    |

### **Bit representation**

- ```java
  short x = 0b11101011;//Bit representation of an integer 235
  System.out.println(Integer.toBinaryString(235));//Converts the 16 bit short to 32 bit int
  ```
- `short` is `16-bit signed integer` - from $$ 2^{16} = -32,768 \text{ to 32,767 (inclusive)} $$
- `int` is `32-bit signed integer`. The size of an int in Java is fixed at 32 bits. (regardless of the underlying hardware architecture)
- `long` is `64-bit signed integer` in Java.

### **Negative number**

is represented in $$ \textbf {2's complement} X′ = invert(X) + 1 $$
- ```java
    int y = -2;//11111111111111111111111111111110 -> 32 bit
    int x = -8;//11111111111111111111111111111000
    x = x >> 1; //Divide by 2 -> -4, 11111111111111111111111111111100
    x = x << 1;//Multiply by 2
   ```

### **Extracts the LSB of a number**
- ```java
  (number & 1)
  ```

### **Clear/Unset the rightmost set bit** :
- flip the **least significant set bit** to 0
-turns the Rightmost 1, from LSB, to zero
- ```java
  `x & (x - 1)`
  ```
- Subtracting 1 from x flips the rightmost set bit and sets all the bits to its right to 1.
- Performing the bitwise AND operation with x and x - 1 results in all bits being preserved except for the rightmost set bit, which becomes 0.
In other words, this operation effectively removes the rightmost (lowest-order) 1-bit in the binary representation of x.

### **Extracts the rightmost set bit** :
- extracts the Rightmost 1, from LSB,without changing it.
- ```java
  x & ~(x - 1)
  ```

### **the Nth bit is set**
Bit mask technique
```java
1 << n //Set the nth bit from LSB, to be used as bit mask

int number = 10;
int n = 2;      // Set the 2nd bit from LSB (0-based index)
        
// Using bitwise OR to set the nth bit from LSB
int result = number | (1 << n);
```
sets the 2nd bit (0-based index) from the least significant bit (LSB) of the number 10. 
- The `1 << n` expression creates a mask with only the nth bit set, 
- the bitwise OR operation combines this mask with the original number, setting the specified n<sup>th</sup> bit.

### **XOR Trick(Cancels each other Or Adding Without Carrying)**
- XOR is essentially an addition operation without carrying over to the next bit
- Same variables cancels the effect.
- If 2 similar objects are XOR'd, it returns `0|False`. 
  - XORing **two identical numbers results in 0**. `8^8 = 0`
- XORing any number with 0 results in the same number.`a^0 = a`
- XORing two integers gives **the sum without carry**. 
  - trick used in bitwise addition
- **Mnemonic** : **Ex**clude **OR** -> OR is Addition, thus XOR is `Adding Without Carrying`
```java
// Use of XOR (both flags are boolean) and Exactly one is True
if (flag1 ^ flag2)
//is equivalent to
(flag1 && !flag2) || (!flag1 && flag2);
```

The logic is used for finding a unique element among duplicates (Stolen Drone problem (21) in Interview cake)

{% gist nitinkc/c2b08480ddf73b06f2ad1df65be5483d %}

# Bitwise Operators

Truth Table

|  A  | B  | A & B | A \| B | A ^ B |  ¬A  | 
|:---:|:--:|:-----:|:------:|:-----:|:----:|
|  0  | 0  |   0   |   0    |   0   |  1   | 
|  0  | 1  |   0   |   1    |   1   |  1   | 
|  1  | 0  |   0   |   1    |   1   |  0   | 
|  1  | 1  |   1   |   1    |   0   |  0   | 


- `NOT (~)`: Changes 1 to 0 and 0 to 1.
- `AND (&)`: 1 if both bits are 1; otherwise, it's 0. Product of zero with anything is a zero
- `OR (|)`: 1 if either of the bits is 1; otherwise, it's 0. behaves like an addition
- `XOR (^)`: If the bits are **different**, the result is `1 | TRUE` ; otherwise, for same bits it's 0.
    ```java
    int x = -13;
    System.out.println(x^x);//0
    System.out.println(x^(~x));//-1
    ```
  
##### `Left Shift (<<)`
- Shifts the bits to the left by a specified number of positions (n) `value << n`.
- The vacant positions on the right are filled with zeros.
- it effectively **multiplies** the operand by $$ {2^n} $$.
- x = x << 32; with an int variable x, this will result in x being assigned the value 0. 
  - This is because the bits that are shifted beyond the 32nd position will be discarded, and the result will be 0.
- If you try to left-shift an int value x by 33 bits (x << 33), it will be equivalent to a left shift by (33 % 32) bits, which is 1 bit.
  ```java
    int x = 5;
    x = x << 33;
    System.out.println(x); // Outputs 10

    // Explanation: 5 in binary is 0000 0000 0000 0000 0000 0000 0000 0101
    // Left-shifting by 33 bits effectively becomes a left shift by 1 bit:
    // 0000 0000 0000 0000 0000 0000 0000 1010, which is 10 in decimal.
    }
    ```
  
NO UNSIGNED LEFT SHIFT `<<<`
{: .notice--info}

##### `Signed Right Shift (>>)`
- Shifts the bits of the operand to the right by a specified number of positions.
- It fills the vacant positions on the left with the sign bit (the leftmost bit) to preserve the sign of the number.
- If the number is positive, it fills with 0, and if negative, it fills with 1.
- **Divides** the number by $$ {2^n} $$.

```java
 int x = -8;//11111111111111111111111111111000
 int result = x >> 1; // result is -4, 11111111111111111111111111111100
```

##### `Unsigned Right Shift (>>>)`
- It fills the vacant positions on the left with zeros, regardless of the sign bit.
- It is used for **logical right shifts**, and it treats the operand as an unsigned quantity.
- ALWAYS use this for the while loop, else infinite loop for negative numbers

```java
int x = -8;//11111111111111111111111111111000
int result = x >>> 1; // result is 2147483644, 01111111111111111111111111111100
while (x != 0) {
    //Some Logic
    x = x >>> 1;//Use Unsigned Right Shift for negative numbers, else infinite loop for negative numbers
}
```

# Examples

### **Checking if a Number is Even or Odd:**
   ```java
   boolean isEven = (num & 1) == 0; // true if even, false if odd
   ```
   **Explanation**: In binary representation, even numbers have their least significant bit (LSB) set to 0, 
while odd numbers have it set to 1. 
Thus **extract the LSB** of the number and if the result is 0, the number is even; if it's 1, the number is odd.

### **Swapping Two Numbers:**

```java
// Works only with integer, in its native form, for others change it into its equivalent binary representation.
a = a^b;
b = a^b; //a^b^b yields a
a = a^b;//a^b^a = b(b is recently converted to a)
```
   **Explanation**: This code uses XOR to swap the values of `a` and `b` without using a temporary variable. 
When you XOR a value twice with the same number, it returns the original value (XOR is its own inverse). 
The sequence of operations effectively swaps the values of `a` and `b`.

### **Finding the Missing Number:**

   ```java
   int findMissing(int[] nums) {
       int result = nums.length;
       for (int i = 0; i < nums.length; i++) {
           result ^= i ^ nums[i];
       }
       return result;
   }
   ```
   **Explanation**: This code finds the missing number in an array containing elements from 0 to n. 
It XORs each index `i` and corresponding value `nums[i]`, along with the indices themselves (0 to n-1), 
and finally with `n`. This effectively cancels out all the numbers that are present, leaving only the missing number.

### **Counting Set Bits (1s) in an Integer:**

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

   **Explanation**: This code uses Brian Kernighan's algorithm to count the number of set bits (1s) in an integer.
In each iteration, it flips the **least significant set bit** to 0 by performing a bitwise AND operation with `num - 1`. 
This effectively counts and removes one set bit in each iteration.

### **Finding Power of 2:**

   ```java
   boolean isPowerOf2(int num) {
       return (num & (num - 1)) == 0;
   }
   ```

   **Explanation**: checks if a number is a power of 2. A binary representation of a power of 2 has only one bit set. When you subtract 1 from a power of 2, all the lower bits are set to 1. Performing a bitwise AND with the original number and its decremented value will result in 0 if it's a power of 2.

### **Toggle Nth Bit:**
   ```java
   int toggleNthBit(int num, int n) {
       return num ^ (1 << n);
   }
   ```
   **Explanation**: toggles the Nth bit of a number by performing a bitwise XOR with a number 
   **where only the Nth bit is set** (achieved using left shift). This operation flips the value of the Nth bit while leaving other bits unchanged.

### **Finding Maximum and Minimum:**
   ```java
   int max = b ^ ((a ^ b) & -(a < b ? 1 : 0));
   int min = a ^ ((a ^ b) & -(a < b ? 1 : 0));
   ```
   **Explanation**: The expression `(a < b ? 1 : 0)` evaluates to 1 if `a` is less than `b`, and 0 otherwise. 
   The bitwise AND operation with `-1` (all bits set) or `0` (all bits cleared) determines whether the maximum or minimum value is selected.

### **Parity = 1 When #1's Odd**
```java
 while (x != 0){
   x = (short) (x & (x-1));//Changes the 1 from LSB to zero, and count
   count++;//Either count the number of 1's and see if its even or odd.
   parity = (short) (parity ^ 1);//Keep flipping the parity, when even its 0, when odd, its 1
}
```

### **Adding two numbers bitwise**
- Get the Carry Bit with AND`&` operator
- Get the sum without carry with XOR`^`
- Take the Carry to the next Left bit (from LSB)
- **Mnemonic** : `Add  1 Right 2 Left`
  {% gist nitinkc/008921af628eb9efee46420cdd94c5e5 %}

### **Multiplying 2 numbers in Binary**

{% gist nitinkc/f2029ae09d2ed8862638893bf5c6e8dc %}

```markdown
11     (3 in decimal)
×  10  (2 in decimal)
------
 00  (This is 11 multiplied by the rightmost bit of 0)
11x   (This is 11 multiplied by the leftmost bit of 0, shifted one position to the left)
------
110    (6 in decimal)
```


|  Iteration   |   num1 (binary)   |  num2 (binary)   |   result (binary)   | Operation                                                  |
|:------------:|:-----------------:|:----------------:|:-------------------:|:-----------------------------------------------------------|
|      1       |        11         |        10        |          0          | Check LSB of num1 (11) (1 & 1) == 1 (True)                 |
|              |                   |                  |                     | - result = add(result, num2) = add(0, 10) = 10             |
|              |                   |                  |                     | - Right shift num1 (num1 >>>= 1) => num1 = 01 (binary)     |
|              |                   |                  |                     | - Left shift num2 (num2 <<= 1) => num2 = 100 (binary)      |
| -----------  | ----------------  | ---------------  | ------------------  | -----------------------------------------------            |
|      2       |         1         |       100        |         10          | Check LSB of num1 (01) (1 & 1) == 1 (True)                 |
|              |                   |                  |                     | - result = add(result, num2) = add(10, 100) = 110          |
|              |                   |                  |                     | - Right shift num1 (num1 >>= 1) => num1 = 00 (binary)      |
|              |                   |                  |                     | - Left shift num2 (num2 <<= 1) => num2 = 1000 (binary)     |
| -----------  | ----------------  | ---------------  | ------------------  | -----------------------------------------------            |
|      3       |         0         |       1000       |         110         | Check LSB (0 & 1) == 0 (False)                             |
|              |                   |                  |                     | - No addition in this iteration                            |
|              |                   |                  |                     | - Right shift num1 (num1 >>= 1) => num1 = 0 (binary)       |
|              |                   |                  |                     | - Left shift num2 (num2 <<= 1) => num2 = 10000 (binary)    |
| -----------  | ----------------  | ---------------  | ------------------  | -----------------------------------------------            |
|    Final     |         0         |      10000       |         110         | Algorithm terminates : num1 becomes 0  `while (num1 != 0)` |


