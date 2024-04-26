---
title:  "Git Revert"
date:   2024-04-20 13:30:00
categories: ['Git']
tags: ['Git']
---

`git revert` is useful when you want to undo the changes made by a specific commit without rewriting history

```shell
git revert <commit-hash>
```

if the git log looks like

```log
* f6a4e5b Fixed a bug in the new feature
* d4c1b2a Added new functionality
* a2b3c4d Initial commit
```
and the following git command is used
```shell
git revert d4c1b2a
```
Git will open a text editor to enter a commit message for the revert commit. 
It usually pre-populates the message with something like "Revert 'Added new functionality". 
Modify this message if needed, save, and exit the editor.

If there are no conflicts, Git will automatically create a new commit that reverts the changes introduced by commit d4c1b2a.
Commit history will now include the revert commit:

```log
* 2468abc (HEAD -> main) Revert "Added new functionality for user registration"
* f6a4e5b Fixed a bug in the new feature
* d4c1b2a Added new functionality
* a2b3c4d Initial commit
```