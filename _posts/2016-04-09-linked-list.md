---
title:  "Linked List"
date:   2016-04-06 05:14:00
categories: ['Data Structures']
tags: ['Data Structures']
---

{% include toc title="Index" %}

# Three types of Linked List
1. Singly Linked List
2. Doubly Linked list
3. Circular Linked List

## Singly Linked List
* Head is the starting point
* Can traverse only in one direction
* copy head into a runner and work with the runner. **Never** modify head

```java
class Node<V> {
    public V dataObject;
    Node next;
}
```

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

## Singly LinkedList Challenges

### Traversal accross all elements
```java
 Node runner = head;//head
 while (runner != null){
 // Obtain the dataObject and perform operation on it
 runner = runner.next;
}
```

##### Add at the front of the List
```java
head = new Node(value, head);
```

##### Add at an 'index'
{% gist nitinkc/66e6ca32e3c6faf4b1fc4cec5472b7de %}

##### Add a node at the end of a Linked List

{% gist nitinkc/1a7981081dbdeacfda37bfaeca1caaae %}

##### Linked List Iteration
{% gist nitinkc/4e97df8926c80696a67ba8ae8ca87b08 %}

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
