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

[//]: # (![rebase.png]&#40;..%2F..%2Fassets%2Fimages%2Fgit%2Frebase.png&#41;)

<img src="..%2F..%2Fassets%2Fimages%2Fgit%2Frebase.png" width="300" height="300">

# Rebase
An alternate to merge is Rebase. Rebase is used to integrate changes from one branch to another

## When to use Rebase?
When your feature branch is local and changing history will not affect others.

- Use `git rebase` when you want to update your feature branch with the latest changes from the main branch (usually `master` or `main`).
- It's suitable when you desire a linear commit history for your branch, making it easier to understand the sequence of changes.
- This approach is best when working on a local feature branch, and changing history won't impact other team members.

> Note: `git rebase` should be used with caution in collaborative environments where rewriting history may affect others. 
> In such cases, consider using `git merge` to incorporate changes from the main branch.

# Using IntelliJ Squash

Remove unnecessary commits by squashing intermediate commits into one.

![squash_intelliJ.png](..%2F..%2Fassets%2Fimages%2Fgit%2Fsquash_intelliJ.png)