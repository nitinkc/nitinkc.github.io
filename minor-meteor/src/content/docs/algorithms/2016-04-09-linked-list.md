---
title: Linked List
date: 2016-04-06 05:14:00
categories:
- Algorithms
tags:
- Data Structures
- Implementation
---

{% include toc title="Index" %}

# Three types of Linked List
1. Singly Linked List
2. Doubly Linked list
3. Circular Linked List

## Summary
* copy head into a runner and work with the runner. **Never** modify head

### Solving using Dummy List
If input list is not required to be maintained, just move it head instead of creating a runner
[https://leetcode.com/problems/merge-two-sorted-lists/](https://leetcode.com/problems/merge-two-sorted-lists/)

```java
ListNode dummy=new ListNode(0);// Create a dummy node and return the next node as head
ListNode finalList = dummy;

return finalList.next;//Avoiding the forst dummy node created
```

### Linked List Iteration
```java
 Node runner = head;//head
 while (runner != null){
     // Obtain the dataObject and perform operation on it
     runner = runner.next;
}
```
{% gist nitinkc/4e97df8926c80696a67ba8ae8ca87b08 %}

### Array vs Linked List
```java
 for (int i = 0; i < arr.length; i++){
      System.out.prinln(arr[i]);
 }

 for (ListNode runner = head; runner != null; runner = runner.next){
      System.out.println(runner.data);
 }
```

### Reaching the second last element and staying there

```java
// Reaching the second last element and staying there
while(runner.next.next != null){
  runner = runner.next;
}
```

## Singly Linked List
* Head is the starting point
* Can traverse only in one direction

##### Add at the front of the List
```java
head = new Node(value, head);
```
##### Reversing LinkedList
[https://leetcode.com/problems/reverse-linked-list/description/](https://leetcode.com/problems/reverse-linked-list/description/)

```java
Node reverse(Node head) {
    Node prev = null;
    Node current = head;
    Node next = null;
    while (current != null) {
        next = current.next;//Set the next first so the current can be referenced to the previous node
        current.next = prev;// Chaging -> to <- direction
        prev = current;//Move prev one step forward
        current = next;//Move current one step forward
    }
    head = prev;
    return head;
}
```

##### Cycle Detection:
Relative Speed Concept: If there is a cycle, the fast runner will **eventually** catch up to the slow runner. 
- think of a RACE between two runners on a circular track. The faster runner will eventually lap the slower runner, meaning they will be at the same point on the track at some time.
  - But maintain relative speed of the fast runner to be 2X the slow runner, so that they will meet at the same point in the cycle.
- If there is no cycle, the fast runner will reach the end of the list.
[https://leetcode.com/problems/linked-list-cycle/description/](https://leetcode.com/problems/linked-list-cycle/description/)

```java
boolean hasCycle(Node head) {
    if (head == null || head.next == null) 
      return false;
    Node slow = head, fast = head.next;
    while (fast != null && fast.next != null) {
        if (slow == fast) 
          return true;//cycle exists
        slow = slow.next;
        fast = fast.next.next;//2X speed of the slow runner
    }
    return false;
}
```

##### Add at an 'index'
{% gist nitinkc/66e6ca32e3c6faf4b1fc4cec5472b7de %}

##### Add a node at the end of a Linked List
{% gist nitinkc/1a7981081dbdeacfda37bfaeca1caaae %}

##### Set all nodes to 42
{% gist nitinkc/9aef8598074b343be5e85c4946c9c2b7 %}

##### Set Last node to 42
{% gist nitinkc/3a068e9a976ed17e8dd48fb0926cce5e %}

##### Set a given node to 42
{% gist nitinkc/0adc9cbca58a575ad8cdc7519c3fd0a1 %}

##### Find the max/min in a Linked List
{% gist nitinkc/743c96f56cadd8ad502d313e871a56b6 %}

##### Find the last index of a given number in a Linked List
{% gist nitinkc/e607f8b37d13eb2fbf4d9e6333f38869 %}

##### Count Duplicate
{% gist nitinkc/3376fda31d518cc1f1747bcd1135d0e7 %}

##### Delete from the end
{% gist nitinkc/b0021888f69349f08614edc484f7d050 %}

## Doubly Linked List

* Head is the starting point
* Can traverse only in **either** direction
* copy head into a runner and work with the runner. **Never** modify head

```java
class Node<V> {
    Node previous
    public V dataObject;
    Node next;
}
```

**Insertion:**
```java
class DoublyNode {
    int data;
    DoublyNode next, prev;
    DoublyNode(int d) { data = d; next = prev = null; }
}

class DoublyLinkedList {
    DoublyNode head;

    void insert(int data) {
        DoublyNode newNode = new DoublyNode(data);
        if (head == null) {
            head = newNode;
        } else {
            DoublyNode temp = head;
            while (temp.next != null) {
                temp = temp.next;
            }
            temp.next = newNode;
            newNode.prev = temp;
        }
    }
}
```

**Deletion:**
```java
void delete(DoublyNode head, DoublyNode del) {
    if (head == null || del == null) return;
    if (head == del) head = del.next;
    if (del.next != null) del.next.prev = del.prev;
    if (del.prev != null) del.prev.next = del.next;
    return;
}
```

**Reversal:**
```java
DoublyNode reverse(DoublyNode head) {
    DoublyNode temp = null;
    DoublyNode current = head;
    while (current != null) {
        temp = current.prev;
        current.prev = current.next;
        current.next = temp;
        current = current.prev;
    }
    if (temp != null) {
        head = temp.prev;
    }
    return head;
}
```

#### Circular Linked List
**Insertion:**
```java
class CircularNode {
    int data;
    CircularNode next;
    CircularNode(int d) { data = d; next = null; }
}

class CircularLinkedList {
    CircularNode head;

    insert(int data) {
        CircularNode newNode = new CircularNode(data);
        if (head == null) {
            head = newNode;
            newNode.next = head;
        } else {
            CircularNode temp = head;
            while (temp.next != head) {
                temp = temp.next;
            }
            temp.next = newNode;
            newNode.next = head;
        }
    }
}
```

**Deletion:**
```java
void delete(int key) {
    if (head == null) return;
    CircularNode temp = head, prev = null;
    if (head.data == key && head.next == head) {
        head = null;
        return;
    }
    if (head.data == key) {
        while (temp.next != head) {
            temp = temp.next;
        }
        temp.next = head.next;
        head = temp.next;
        return;
    }
    while (temp.next != head && temp.data != key) {
        prev = temp;
        temp = temp.next;
    }
    if (temp.data == key) {
        prev.next = temp.next;
    }
}
```

**Traversal:**
```java
void traverse() {
    if (head == null) return;
    CircularNode temp = head;
    do {
        System.out.print(temp.data + " ");
        temp = temp.next;
    } while (temp != head);
}
```

## Java Implementation of LinkedList

```java
import java.util.LinkedList;

// Creating a LinkedList
LinkedList<String> linkedList = new LinkedList<>();

// Adding elements to the LinkedList
linkedList.add("Apple");
linkedList.add("Banana");

// Adding elements at specific positions
linkedList.add(2, "Grape");//Index 2
linkedList.addFirst("Apricot");// Start of tje LinkedList
linkedList.addLast("Fig");// End of the linked List

// Getting elements by index
String secondElement = linkedList.get(1);

// Removing elements
linkedList.remove("Banana");
linkedList.remove(3);
```