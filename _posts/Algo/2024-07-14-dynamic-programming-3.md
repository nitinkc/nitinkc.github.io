---
title: "Dynamic Programming - Grids"
date:  2024-07-14 18:27:00
categories: Algorithms
tags: [Algorithms]
---

{% include toc title="Index" %}---

# Grids

**Bottom-up Approach**

1. An array that answers the problem for a given state
2. Base cases
2. A recurrence relation to transition between states

[Unique Paths](https://leetcode.com/problems/unique-paths/description/)

$ dp[\text{row}][\text{col}] = dp[\text{row} - 1][\text{col}] + dp[\text{row}][\text{col} - 1] $

- dp arry is used top keep the intermediate calculations
- return the rightmost bottom array `return dp[r-1][c-1];`
- the `row > 0` and `col > 0` takes care of filling the 1's on the edges.

##### Bottom-up  approach

```java
int[][] dp = new int[m][n];
dp[0][0] = 1; // Base case
        
for(int row = 0; row < m; row++){
    for(int col = 0;col < n; col++){
        if(row > 0)
            dp[row][col] += dp[row-1][col];//coming from top row to bottom
        if(col > 0)
            dp[row][col] += dp[row][col-1];//coming from left to right
    }
}
return dp[r-1][c-1];
```

##### The final dp grid

The dp grid has the total number of paths at each i,j

|---|---|---|
| 1 | 1 | 1 |
| 1 | 2 |**3**|
| 1 |**3** | **6**|

### Grids with Obstacles

1's are the obstacles in the grid

|---|---|---|
| 0 | 0 | 0 |
| 0 | 1 | 0 |
| 0 | 0 | 0 |

{% gist nitinkc/02c9e363b02313ba7e8acc5733c653d2 %}

[Minimum Path Sum](https://leetcode.com/problems/minimum-path-sum/description/)

Using the same grid with ebverything under the same loop

```java
public int minPathSum(int[][] grid) {
    int r = grid.length;
    int c = grid[0].length;

    for(int row = 0; row < r; row++){
        for(int col = 0; col < c; col++){
            if(row == 0 && col == 0) continue;//already initialyzed
            if(row == 0 && col > 0){
                grid[row][col] = grid[row][col] + grid[row][col-1];
            }else if(col == 0 && row > 0){
                grid[row][col] = grid[row][col] + grid[row-1][col];
            }else{
                grid[row][col] = grid[row][col] + Math.min(grid[row-1][col], grid[row][col-1]);
            }
        }
    }

    return grid[r-1][c-1];
}
```

Using Auxiliary Array

```java
public int minPathSum(int[][] grid) {
    int r = grid.length;
    int c = grid[0].length;
    
    int[][] dp = new int[r][c];
    dp[0][0] = grid[0][0];

    for(int row = 0; row < r; row++){
        for(int col = 0; col < c; col++){
            if(row == 0 && col == 0) continue;//already initialyzed
            if(row == 0 && col > 0){
                dp[row][col] = grid[row][col] + dp[row][col-1];
            }else if(col == 0 && row > 0){
                dp[row][col] = grid[row][col] + dp[row-1][col];
            }else{
                dp[row][col] = grid[row][col] + Math.min(dp[row-1][col], dp[row][col-1]);
            }
        }
    }

    return dp[r-1][c-1];
}
```

less complex solution

```java
public int minPathSum(int[][] grid) {
   int r = grid.length;
   int c = grid[0].length;

   int[][] dp = grid;
    //dp[0][0] = grid[0][0];

   for(int row = 1; row < r; row++){
    dp[row][0] += grid[row-1][0]; 
   }
   for(int col = 1; col < c; col++){
    dp[0][col] += grid[0][col-1]; 
   }
   
   for(int row = 1; row < r; row++){
    for(int col = 1; col < c; col++){
       dp[row][col] = grid[row][col] + Math.min(dp[row-1][col], dp[row][col-1]);
    }
   }
   return dp[r-1][c-1];
}
```