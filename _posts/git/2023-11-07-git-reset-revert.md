---
title: Git Reset - Revert
date: 2023-11-07 11:30:00
categories:
- Git
tags:
- Commands
- Version Control
---

{% include toc title="Index" %}

**Scenario: if a few commits are found to be stale and you want to go back to
the previous commits**

[https://git-school.github.io/visualizing-git/#revert](https://git-school.github.io/visualizing-git/#revert)
![1.png](/assets/images/git/1.png)

# Special Symbol usage

**HEAD** is a reference variable that always points to the **recent commit** of
the current branch (tip of the current branch)

tilde `~` and caret `^` symbols are used to point to a position relative to a
HEAD or a commit hash.

* Tilde symbol `~`: Used to point to the previous commits from base HEAD
* Caret symbol `^`: Used to point to the immediate parent commit from the
  current referenced commit

#### Reverts but keeps the history

Either mention the number of commits to go back to using `HEAD~n` or explicitly
mention the Hash commit id.

```shell
git revert --no-commit HEAD~3
git revert 5b2e4af
```

With revert, a new commit is created with the reverted code and it keeps the "
old bad commit" history that can be viewed.

<iframe
src="https://www.youtube.com/embed/1yaUn_PhlM8"
title="git revert - local and remote" frameborder="0"
allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope;
picture-in-picture; web-share"
allowfullscreen>
</iframe>

### Git Reset

Deletes history, but dangerous to use for older commits. Just use to remove
accidental commits

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
allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope;
picture-in-picture; web-share"
allowfullscreen>
</iframe>

### Git Reset Options

* git reset --soft, keep the files, and stage all changes back automatically.
* git reset --hard, completely destroy any changes and remove them from the
  local directory. USE WITH CAUTION, try only on your feature branches.
* git reset --mixed, keeps all files the same but unstages the changes. This is
  the most flexible option, it doesn’t modify files.

![2.png](/assets/images/git/2.png)
[//]: # (<img src="/assets/images/git/2.png" alt="2.png" style="width: 50%; height:60%; border: 1px solid #ccc;">)

`git revert` is useful when you want to undo the changes made by a specific
commit without rewriting history

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
It usually pre-populates the message with something like "Revert 'Added new
functionality".
Modify this message if needed, save, and exit the editor.

If there are no conflicts, Git will automatically create a new commit that
reverts the changes introduced by commit d4c1b2a.
Commit history will now include the revert commit:

```log
* 2468abc (HEAD -> main) Revert "Added new functionality for user registration"
* f6a4e5b Fixed a bug in the new feature
* d4c1b2a Added new functionality
* a2b3c4d Initial commit
```