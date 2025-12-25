---
categories: Git
date: 2023-11-07 11:30:00
tags:
- Git
title: Git Merge, Rebase, Squash and Fast forward
---

{% include toc title="Index" %}
To combine multiple commits (squash) from the feature branch into one while
merging into the develop branch,
an `squash merge` or `interactive rebase`  approach can be used.

# Using IntelliJ Squash

Remove unnecessary commits by squashing intermediate commits into one.

![squash_intelliJ.png](/assets/images/git/squash_intelliJ.png)

# Rebase

An alternate to merge is Rebase. Rebase is used to integrate changes from one
branch to another

### Interactive Rebase

```shell
git rebase -i develop

# pick or squash
pick abc123 First commit message
squash def456 Second commit message
squash hij789 Third commit message
```

If the changes are pushed into the feature branch on the server, then do an
interactive rebase with remote/develop

```shell
git rebase -i origin/develop
# squash the commits and then force push
git push --force
```

### Using IntelliJ

![IntelliJRebase.png](/assets/images/intelliJ/IntelliJRebase.png)

Squash the unwanted commits
![intelliJInteractiverebase.png](/assets/images/intelliJ/intelliJInteractiverebase.png)

## When to use Rebase?

When your feature branch is local and changing history will not affect others.

- Use `git rebase` when you want to update your feature branch with the latest
  changes from the main branch (usually `main` or `develop`).
- It's suitable when you desire a linear commit history for your branch, making
  it easier to understand the sequence of changes.

> Note: `git rebase` should be used with caution in collaborative environments
> where rewriting history may affect others.
> In such cases, consider using `git merge` to incorporate changes from the main
> branch.

# Fast-Forward

When the merge from branch A happens with Branch B, and Branch B does not have
new commits, the fast forward merge happens.
You get message "You have performed a fast-forward merge."

If both the branches to be merged has changes, Recursive merge happens.

```shell
git checkout develop
git merge --no-ff feature/new-feature
```

<img src="/assets/images/git/rebase.png" width="300" height="300">

![](https://www.youtube.com/watch?v=0chZFIZLR_0)