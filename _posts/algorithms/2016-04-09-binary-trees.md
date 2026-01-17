---
title: Binary Trees (DFS & BFS)
date: 2016-04-06 05:14:00
categories:
- Algorithms
tags:
- Trees
- Data Structures
---

{% include toc title="Index" %}

### Summary
- ensures that the root is a branch (only one child)
```java
if(root.left != null || root.right != null){//Condition for non leaf node
  count++;
}
```
- {% gist /nitinkc/dbc98632abc89fb83119af50b2448300 %}

- For BFS (level order traversal) of a Tree, a Queue is used as intermediate data structure.
  - regular
    ```java
    Queue<TreeNode> q = new LinkedList<>();
    q.add(root);
    while(!q.isEmpty()){
    TreeNode temp = q.poll();
    if(temp.left == null && temp.right == null)
      count++;
  
    if(temp.left != null) q.add(temp.left);
    if(temp.right != null) q.add(temp.right);
    }
    ```
    
  - when somethings to be done at the same level (Level Order)
    ```java
    Queue<TreeNode> queue = new LinkedList<>();
    queue.add(root);//Begin with root
    while(!queue.isEmpty()){
      int size = queue.size();// number of nodes at current level
      for(int i = 0; i < size; i++){ // Only when all calculation is to be done in the same level. 
        TreeNode current = queue.poll();
        if(current.left != null) queue.add(current.left); //For BFS, first left, then right
        if(current.right != null) queue.add(current.right);
      }
    ....
    }
    ```

#### Tree Traversal
Three types of Depth First Search (DFS) Traversal.
- For Iterative traversal, a Stack is used as intermediate data structure.
- With Recursive Approach, recursion stack takes care

- InOrder (L,Root,R)
  ```java
  inOrder(root.left, list);
  list.add(root.data);
  inOrder(root.right,list);
  ```
- Pre order (Root,L,R)
  ```java
  list.add(root.data);
  preOrder(root.left, list);
  preOrder(root.right,list);
  ```
- Post Order (L,R,Root)
  ```java
  inOrder(root.left, list);
  inOrder(root.right,list);
  list.add(root.data);
  ```
- Level Order Traversal (Like BFS using a Queue - Iterative)
  {% gist nitinkc/042e93c55afab4bc7bafa9699a16073b %}

####  Binary Search Tree
"BST": a binary tree that is either:
* empty (null), or
* a root node R such that:
    1. every element of R's left subtree contains data "less than" R's data,
    2. every element of R's right subtree contains data "greater than" R's,
    3. R's left and right subtrees are also binary search trees.

BSTs store their elements in sorted order, which is helpful for searching/sorting tasks.
Storing each element in an array while traversing
{% gist nitinkc/ad0b3109163915d89db6f4b9e5e7cbbf %}

##### Binary Search

```java
int binarySearchRecursive(int[] arr, int start, int end, int value)
/* Base Case when start > end */

if (start > end)
   return -1;// value not found. Index = -1

int mid = (start + end) / 2;

if (arr[mid] < value) 
  return binarySearchRecursive(arr, mid + 1, end, value);
else if (arr[mid] > value) 
  return binarySearchRecursive(arr, 0, mid - 1, value);   
else 
  return mid;           
```


# Good Problems 
### Height of a Tree
{% gist nitinkc/5837831baee94bd7a6bbe0b58f050197 %}

### Find Level of a Given Node in a Binary Tree
{% gist nitinkc/00c46d469167c099679682c41e6b24e8 %}

### Print nodes at a level
Given a Tree and the depth/level, print all the nodes from left to right.
{% gist nitinkc/f34b9a1134477b0f1cbc22e777fab7e2 %}

### Print Leaves Nodes from Right to Left
{% gist nitinkc/5934eb3d94794c23106f38e17aaa61f1 %}

### Count all Leaf Nodes
[ Count all Leaf Nodes](https://www.codestepbystep.com/r/problem/view/java/collectionimpl/binarytrees/countLeaves)
{% gist nitinkc/e180867eb09c229d72ef3df06333401e %}

### Count Left Nodes
{% gist nitinkc/8ac5f8599a620d6e860228c15798f023 %}

### Number the nodes from top to bottom in Pre Order way.
[Problem Statement](https://practiceit.cs.washington.edu/problem/view/bjp5/chapter17/e11-numberNodes)
{% gist nitinkc/87f93c0ac63b4b5e8eaa51d9166b6585 %}

### Remove leaf node
{% gist nitinkc/cb357a5e77be6236be35afef0c398953 %}

### Count Empty Spots
{% gist nitinkc/619d22e2ae458a3f174b0297019e6fd5 %}

### Depth Sum
{% gist nitinkc/ffa2a55bdf2cd8eed9a041ff7a01c917 %}

#### Iterative
If you calculate the size of the queue, the current size has all elements at the same level
```java
int nodesAtLevel = q.size();
for(int i = 0; i < nodesAtLevel; i++){
    //Do something with the nodes at the same level
}
```

{% gist nitinkc/7515bd091884772b9bccb9b50d684d37 %}

### Complete to Level
[Problem Statement](https://www.codestepbystep.com/r/problem/view/java/collectionimpl/binarytrees/completeToLevel)

- Top-Down Approach
{% gist nitinkc/02752c3e1acf84cc9b1545a1054b2ff9 %}
- Recursive Approach
{% gist nitinkc/98430ec49742f659f36da37f765f9e62 %}
- Bottom-Up Approach
{% gist nitinkc/98430ec49742f659f36da37f765f9e62 %}

### Isomorphic Trees

```java
//base case,
if(root1 == null && root2 == null) return true;
//Cases like [1,null,2]
if(root1 == null || root2 == null) return false;

if(p.val != q.val) return false;

return (root1.val == root2.val) &&
        isIsomprphic(root1.left, root2.right) &&
        isIsomprphic(root1.right, root2.left)
```