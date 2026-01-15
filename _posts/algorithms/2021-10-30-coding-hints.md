---
title: Coding Hints
date: 2021-10-30 21:55:00
categories:
- Algorithms
tags:
- Programming
---

{% include toc title="Index" %}

# Coding Hints

##### Queue using two Stacks

One Stack to hold values, the second one to hold the poped values from one

```java
private Stack<Integer> main = new Stack<Integer>();
private final Stack<Integer> temp = new Stack<Integer>();

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

##### Balanced Parenthesis

Push on opener and pop on closers.

```java
/* If the String is odd lenght, the return false*/
  Stack<Character> stack = new Stack<>();
    for (int i = 0; i < str.length(); i++) {
        char curr = str.charAt(i);

        // Push on Openers
        if (curr == '(' || curr == '[' || curr == '{') {
            stack.push(curr);
        } else { // pop on similar CLOSURES
            // ALSO CHECK IF SIMIAR IS COMING OUT
            char top = stack.peek();//top element of stack
            //System.out.println(top);
            if (    ((top == '(') && (curr == ')')) ||
                    ((top == '{') && (curr == '}')) ||
                    ((top == '[') && (curr == ']'))
                    ) {
                stack.pop();
            } else {
                return false;
            }
        }
    }
        // return (stack.empty());
        return true;
```

##### Find minimum in a Stack

Maintain 2 Stacks, One internally for keeping track of the Max/Min Stack

## Recursion based


##### FizzBuzz Problem

Importance of placing if statements are tested here!!

```java
public String fizzString2(int n) {

    /* Important to check for 3 & 5 first else test cases fails.
     * Other if statements passes the if test, leaving this one unexecuted)  */
    //if (n%3 == 0 && n%5 == 0)
    if(n%15 == 0)//Same as above
        return "FizzBuzz!";
    if (n%3 == 0)
        return "Fizz!";
    if (n%5 == 0)
        return "Buzz!";  
}
```