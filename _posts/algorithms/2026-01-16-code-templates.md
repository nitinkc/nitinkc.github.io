---
title: Code templates
date: 2026-01-16 1:06:00
categories:
- Algorithms
tags:
- Algorithms 
---

# Common Interview Patterns

### Boolean Logic with Switch
{% gist nitinkc/96387a9700c9c58185a969ae48bfdc45 %}

### For Loop Edge Cases
{% gist nitinkc/382798a984e00a732d86a12a6637e0a2 %}

## Two pointers: one input, opposite ends

```java
int left = 0;
int right = arr.length - 1;

while (left < right) {
    // do some logic here with left and right
    if (CONDITION) {
        left++;
    } else {
        right--;
    }
}
```

## Two pointers: two inputs, exhaust both

```java
public int fn(int[] arr1, int[] arr2) {
    int i = 0, j = 0, ans = 0;

    while (i < arr1.length && j < arr2.length) {
        // do some logic here
        if (CONDITION) {
            i++;
        } else {
            j++;
        }
    }

    while (i < arr1.length) {
        // do logic
        i++;
    }

    while (j < arr2.length) {
        // do logic
        j++;
    }

    return ans;
}
```

## Sliding window

```java
public int fn(int[] arr) {
    int left = 0, ans = 0, curr = 0;

    for (int right = 0; right < arr.length; right++) {
        // do logic here to add arr[right] to curr

        while (WINDOW_CONDITION_BROKEN) {
            // remove arr[left] from curr
            left++;
        }

        // update ans
    }

    return ans;
}
```

## Linked list: fast and slow pointer

```java
public int fn(ListNode head) {
    ListNode slow = head;
    ListNode fast = head;
    int ans = 0;

    while (fast != null && fast.next != null) {
        // do logic
        slow = slow.next;
        fast = fast.next.next;
    }

    return ans;
}
```

## Binary tree: DFS (recursive)

```java
public int dfs(TreeNode root) {
    if (root == null) {
        return 0;
    }

    int ans = 0;
    // do logic
    dfs(root.left);
    dfs(root.right);
    return ans;
}
```

## Binary tree: DFS (iterative)

```java
public int dfs(TreeNode root) {
    Stack<TreeNode> stack = new Stack<>();
    stack.push(root);
    int ans = 0;

    while (!stack.empty()) {
        TreeNode node = stack.pop();
        // do logic
        if (node.left != null) {
            stack.push(node.left);
        }
        if (node.right != null) {
            stack.push(node.right);
        }
    }

    return ans;
}
```

## Binary tree: BFS
```java
public int fn(TreeNode root) {
  Queue<TreeNode> queue = new LinkedList<>();
  queue.add(root);
  int ans = 0;

  while (!queue.isEmpty()) {
    int currentLength = queue.size();
    // do logic for current level

    for (int i = 0; i < currentLength; i++) {
      TreeNode node = queue.remove();
      // do logic
      if (node.left != null) {
        queue.add(node.left);
      }
      if (node.right != null) {
        queue.add(node.right);
      }
    }
  }

  return ans;
}
```

## Binary search


```java
public int fn(int[] arr, int target) {
    int left = 0;
    int right = arr.length - 1;
    while (left <= right) {
        int mid = left + (right - left) / 2;
        if (arr[mid] == target) {
            // do something
            return mid;
        }
        if (arr[mid] > target) {
            right = mid - 1;
        } else {
            left = mid + 1;
        }
    }

    // left is the insertion point
    return left;
}
```

## Binary search: duplicate elements, left-most insertion point

```java
public int fn(int[] arr, int target) {
    int left = 0;
    int right = arr.length;
    while (left < right) {
        int mid = left + (right - left) / 2;
        if (arr[mid] >= target) {
            right = mid;
        } else {
            left = mid + 1;
        }
    }

    return left;
}
```

## Binary search: for greedy problems

If looking for a minimum:


```java
public int fn(int[] arr) {
    int left = MINIMUM_POSSIBLE_ANSWER;
    int right = MAXIMUM_POSSIBLE_ANSWER;
    while (left <= right) {
        int mid = left + (right - left) / 2;
        if (check(mid)) {
            right = mid - 1;
        } else {
            left = mid + 1;
        }
    }

    return left;
}

public boolean check(int x) {
    // this function is implemented depending on the problem
    return BOOLEAN;
}
```

## Graph: DFS (recursive)

For the graph templates, assume the nodes are numbered from 0 to n - 1 and the graph is given as an adjacency list. Depending on the problem, you may need to convert the input into an equivalent adjacency list before using the templates.

```java
Set<Integer> seen = new HashSet<>();

public int fn(int[][] graph) {
    seen.add(START_NODE);
    return dfs(START_NODE, graph);
}

public int dfs(int node, int[][] graph) {
    int ans = 0;
    // do some logic
    for (int neighbor: graph[node]) {
        if (!seen.contains(neighbor)) {
            seen.add(neighbor);
            ans += dfs(neighbor, graph);
        }
    }

    return ans;
}
```

## Graph: DFS (iterative)

```java
public int fn(int[][] graph) {
    Stack<Integer> stack = new Stack<>();
    Set<Integer> seen = new HashSet<>();
    stack.push(START_NODE);
    seen.add(START_NODE);
    int ans = 0;

    while (!stack.empty()) {
        int node = stack.pop();
        // do some logic
        for (int neighbor: graph[node]) {
            if (!seen.contains(neighbor)) {
                seen.add(neighbor);
                stack.push(neighbor);
            }
        }
    }

    return ans;
}
```

## Graph: BFS

```java
public int fn(int[][] graph) {
    Queue<Integer> queue = new LinkedList<>();
    Set<Integer> seen = new HashSet<>();
    queue.add(START_NODE);
    seen.add(START_NODE);
    int ans = 0;

    while (!queue.isEmpty()) {
        int node = queue.remove();
        // do some logic
        for (int neighbor: graph[node]) {
            if (!seen.contains(neighbor)) {
                seen.add(neighbor);
                queue.add(neighbor);
            }
        }
    }

    return ans;
}
```

## Backtracking

```java
public int backtrack(STATE curr, OTHER_ARGUMENTS...) {
    if (BASE_CASE) {
        // modify the answer
        return 0;
    }

    int ans = 0;
    for (ITERATE_OVER_INPUT) {
        // modify the current state
        ans += backtrack(curr, OTHER_ARGUMENTS...)
        // undo the modification of the current state
    }
}
```

## Dynamic programming: top-down memoization

```java
Map<STATE, Integer> memo = new HashMap<>();

public int fn(int[] arr) {
    return dp(STATE_FOR_WHOLE_INPUT, arr);
}

public int dp(STATE, int[] arr) {
    if (BASE_CASE) {
        return 0;
    }

    if (memo.contains(STATE)) {
        return memo.get(STATE);
    }

    int ans = RECURRENCE_RELATION(STATE);
    memo.put(STATE, ans);
    return ans;
}
```

To convert a top-down solution to a bottom-up one:

Initialize an array
dp
dp that is sized according to the state variables. For example, let's say the input to the problem was an array
nums
nums and an integer
k
k that represents the maximum number of actions allowed. Your array
dp
dp would be 2D with one dimension of length
nums.length
nums.length and the other of length
k
k. In the top-down approach, we had a function dp. We want these two to be equivalent. For example, the value of dp(4, 6) can now be found in dp[4][6].

Set your base cases, same as the ones you are using in your top-down function. In the example we just looked at, we had dp(0) = dp(1) = 0. We can initialize our dp array values to 0 to implicitly set this base case. As you'll see soon, other problems will have more complicated base cases.

Write a for-loop(s) that iterate over your state variables. If you have multiple state variables, you will need nested for-loops. These loops should start iterating from the base cases and end at the answer state.

Now, each iteration of the inner-most loop represents a given state, and is equivalent to a function call to the same state in top-down. Copy-paste the logic from your function into the for-loop and change the function calls to accessing your array. All
dp(...)
dp(...) changes into
dp[...]
dp[...].

We're done!
dp
dp is now an array populated with the answer to the original problem for all possible states. Return the answer to the original problem, by changing
return dp(...)
return dp(...) to
return dp[...]
return dp[...].

## Build a trie


```java
// note: using a class is only necessary if you want to store data at each node.
// otherwise, you can implement a trie using only hash maps.
class TrieNode {
    // you can store data at nodes if you wish
    int data;
    Map<Character, TrieNode> children;
    TrieNode() {
        this.children = new HashMap<>();
    }
}

public TrieNode buildTrie(String[] words) {
    TrieNode root = new TrieNode();
    for (String word: words) {
        TrieNode curr = root;
        for (char c: word.toCharArray()) {
            if (!curr.children.containsKey(c)) {
                curr.children.put(c, new TrieNode());
            }

            curr = curr.children.get(c);
        }

        // at this point, you have a full word at curr
        // you can perform more logic here to give curr an attribute if you want
    }

    return root;
}
```

## Dijkstra's algorithm



```java
int[] distances = new int[n];
Arrays.fill(distances, Integer.MAX_VALUE);
distances[source] = 0;

Queue<Pair<Integer, Integer>> heap = new PriorityQueue<Pair<Integer,Integer>>(Comparator.comparing(Pair::getKey));
heap.add(new Pair(0, source));

while (!heap.isEmpty()) {
    Pair<Integer, Integer> curr = heap.remove();
    int currDist = curr.getKey();
    int node = curr.getValue();
    
    if (currDist > distances[node]) {
        continue;
    }
    
    for (Pair<Integer, Integer> edge: graph.get(node)) {
        int nei = edge.getKey();
        int weight = edge.getValue();
        int dist = currDist + weight;
        
        if (dist < distances[nei]) {
            distances[nei] = dist;
            heap.add(new Pair(dist, nei));
        }
    }
}
```