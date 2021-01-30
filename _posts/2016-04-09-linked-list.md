---
layout: post
title:  "Linked List"
date:   2016-04-06 05:14:00
categories: data structures
comments: true
disqus_identifier: A7655498-AB9E-40BF-A0D5-E5C6DE6BBF28
tags: [job interview, basic data structures]
published: false
---

### Linked List
```java
 LinkNode runner = front;//head
 while (runner.next != null){//Runner stops at the last node, else runner will end up pointing null!!
 runner = runner.next;
}
```

#### Add in the List

##### Add in the front
```java
front = new ListNode(value, front);
```

##### Add at 'index'
```java
if (index == 0)
front = new ListNode(value, front);
else{
ListNode runner = front;
for (int i = 0; i < index - 1; i++)//Stop at an index one before the desired
current = current.next;
}
current.next = new ListNode(value, current.next); //old current.next is assigned to the new node which in turn is assigned to current.next
```

##### Add in the end
```java
if (front == null)
  front = new ListNode(value, front);
else{
  ListNode runner = front;
  while (runner.next != null) // Go till the last node
      runner = runner.next;
  runner.next = new ListNode(value); //this constructor has .next as null
}
```

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
