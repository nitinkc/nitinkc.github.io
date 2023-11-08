---
title:  "Git Reset - Revert"
date:   2023-11-07 11:30:00
categories: ['Git']
tags: ['Git']
---

{% include toc title="Index" %}

Scenario: if a few commits are found to be stale and want to go back to the previous commits

![1.png](..%2F..%2Fassets%2Fimages%2Fgit%2F1.png)

# Special Symbol usage

**HEAD** is a reference variable that always points to the **recent commit** of the current branch (tip of the current branch)

tilde `~` and caret `^` symbols are used to point to a position relative to a HEAD or a commit hash.
* Tilde symbol `~`: Used to point to the previous commits from base HEAD
* Caret symbol `^`: Used to point to the immediate parent commit from the current referenced commit

#### Reverts but keeps the history

Either mention the number of commits to go back to using `HEAD~n` or explicitly mention the Hash commit id. 

```shell
git revert --no-commit HEAD~3
git revert 5b2e4af
```
With revert, a new commit is created with the reverted code and it keeps the "old bad commit" history that can be viewed.

<iframe
src="https://www.youtube.com/embed/1yaUn_PhlM8" 
    title="git revert - local and remote" frameborder="0" 
    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
    allowfullscreen>
</iframe>

### Git Reset

Deletes history, but dangerous to use for older commits. Just use to remove accidental commits 

```shell

git reset HEAD~3
git reset --hard 5b2e4af
git reset 5b2e4af #takes --hard by default
 
# Force push in case the accidental commits
git push -f
```

<iframe 
    src="https://www.youtube.com/embed/RLeD529jYfo" 
    title="Git Revert" 
    frameborder="0" 
    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
    allowfullscreen>
</iframe>

### Git Reset Options

* git reset --soft,  keep the files, and stage all changes back automatically.
* git reset --hard,  completely destroy any changes and remove them from the local directory. USE WITH CAUTION, try only on your feature branches.
* git reset --mixed, keeps all files the same but unstages the changes. This is the most flexible option, it doesn’t modify files.

![2.png](..%2F..%2Fassets%2Fimages%2Fgit%2F2.png)
[//]: # (<img src="../assets/images/git/2.png" alt="2.png" style="width: 50%; height:60%; border: 1px solid #ccc;">)
