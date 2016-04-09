---
layout: static
title:  "Coding Hints"
---

# 7 Step Process

Before jumping into the Coding  
 1. Method Signature (Understand the problem statement)
 2. Some examples (test cases) to understand the edge cases
 3. Brainstorming 
 4. (Talking the problem and bring some approach)
 5. Find the Data structure and Algorithm to be used
 6. Write Code (use paper or whiteboard)
 7. Test for more test cases to avoid edge cases and 


##### Queue using two Stacks

One Stack to hold values, the second one to hold the poped values from one

```java
private Stack<Integer> main = new Stack<Integer>();
private Stack<Integer> temp = new Stack<Integer>();

//O(1) operation
public void enque(int item){
    main.push(item);
}

public int deque(){
    int ret;
    if (main.size() >= 1){
        while(main.size == 1){
            temp.push(main.pop());//put the value into the temp Stack
        }
        ret = main.pop(); // retain the value to return
    }
    // Reset the array for further processing (or interchange the stacks)
    while(temp.size() > 0){
        main.push(temp.pop());
    }

    /* Interchanging the Stack
        private Stack<Integer> interchange = null;
        interchange = main;
        main = temp; //Main to set to the filled Stack
        temp = interchange;
    */

    return ret;
}
```

##### Reverse a Linked List (Iteratively and Recursively)

```java
public void reverseList(Node head){
    Node curr = head;
    Node runner = curr.next;

    while (runner.next != null){
        Node temp = curr;
        temp = runner.next;
        head = head.next;
        runner.next = temp;
    }
}
```

##### Find a cycle in a Linked List (Iteratively and Recursively)

##### Find a cycle in a Linked List (Iteratively and Recursively)


##### UnCoupled Integer in an Array. 

O(n) Space and O(n) time Complexity in a set

```java
Set<Integer> unique = new HashSet<Integer>();

for (int i : arr){ // iterating the array
    if (unique.add(i)){
        //do nothing
    } else {
        unique.remove(i);
    }
}
```

O(1) Space and O(n) time complexity in XOR Approach

```java
int xor = 0;

for (int i = 0; i < arr.length; arr++){
    xor = xor^arr[i]; // Keeps only unique numbers
}

return xor;
```


##### Balanced Parenthesis

Push on opener and pop on closers.

```java
Stack<Character> stack = new Stack<Integer>(); 
for (int i = 0; i < str.length(); i++){
    char curr = str.charAt(i);

    // Push on Openers
    if ( curr == '(' || curr = '[' || curr = '{' ){
        temp.push();
    } else { // pop on SIMILAR closers
        // ALSO CHECK IF SIMIAR IS COMING OUT
        char top = stack.peek();//top element of stack 
        if ( (curr == '(' && top == ')') || 
             (curr == '{' && top == '}') ||
             (curr == '[' && top == ']')
            ){
                stack.pop();
            }
    }
}
```


##### Find count of given Sum in all pairs in the Array 

Checks : 

  * if array size < 2, return 0;

Greedy approach to test all the possible combinations exhaustively

```java
// O(n^2)

 for (int i = 0; i < arr.length; i++){
    for (int j = i + 1; j < arr.lenght; j++){
        if (arr[i] + arr[j] == sum){
            count++;
        }
    }
 }
 return count;
```

Test only those possible combinations that makes sense

``` java
// Two pointer Approach
/* Sort the Array First in Ascending Order [O(nLog(n))] */
int left = 0, right = arr.length -  1;
while (left < right){
    if (arr[left] + arr[right] > sum){//Right is heavier
        right--;
    } else if (arr[left] + arr[right] < sum){ // Left is lighter
        left ++
    } else { // Sum is equal
        count++;
    }
}
return count;
```
