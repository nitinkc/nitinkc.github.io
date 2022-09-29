---
# layout: static
title:  "Coding Hints"
date:   2021-10-30 21:55:00
categories: Algorithms
tags: [Algorithms]
---

{% include toc title="Index" %}

# Conding Hints

### 7 Step Process

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

##### Find a cycle in a Linked List (Recursively)

##### Find a cycle in a Linked List (Iteratively)


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

sadsad

##### Find BST Height

```java
int getHeight(BSTNode root){
    if root( == null )
        return 1;

    // Recursive calls
    return 1 + getHeight(root.left) + getHeight(root.right);
}
```


##### Binary Search

```java
int binarySearchRecursive(int[] arr, int start, int end, int value)
/* Base Case when start > end */

if (start > end)
   return -1;// value not found. Index = -1

int mid = (start + end) / 2;

if (arr[mid] < value)
    binarySearchRecursive(arr, mid + 1, end, value);
else if  (arr[mid] > value)
    binarySearchRecursive(arr, 0, mid - 1, value);   
else
    return mid;           
```



##### FizzBuzz Problem

Importacnce of placing if statements are tested here!!

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



### Tree Traversals

##### Inorder

```java
 /* Function for inorder traversal */
    public void inorder(BSTNode r)
    {
        if(r != null){
        inorder(r.left);
        System.out.print(r.data + " ");
        inorder(r.right);
        }
    }
```

##### PreOrder

```java
    /* Function for pre-order traversal */
    public void preorder(BSTNode r)
    {
       if(r != null){
           System.out.print(r.data + " ");
           preorder(r.left);
           preorder(r.right);
       }
    }
```

##### PostOrder

```java
    /* Function for postorder traversal */
    public void postorder(BSTNode r)
    {
         if(r != null){
           preorder(r.left);
           preorder(r.right);
           System.out.print(r.data + " ");
         }     
    }
```


### Test Cases

##### String

1. if null
2. if odd/even length
3. throw new IllegalArgumentException
4. String with all same character
5. String with special characters

##### Arrays

 1. if Null
 2. if arr.length == 0
 3. if arr.length > required size
