---
title:  "Git Rebase"
date:   2023-11-07 11:30:00
categories: ['Git']
tags: ['Git']
---

{% include toc title="Index" %}

# Fast-Forward

When the merge from branch A happens with Branch B, and Branch B does not have new commits, the fast forward merge happens. 
You get message "You have performed a fast-forward merge."

If both the branches to be merged has changes, Recursive merge happens.

![rebase.png](..%2F..%2Fassets%2Fimages%2Fgit%2Frebase.png)

# Rebase
An alternate to merge is Rebase. Rebase is used to integrate changes from one branch to another

## When to use Rebase?
When your feature branch is local and changing history will not affect others. Use git rebase to get new changes from master to your feature branch.

