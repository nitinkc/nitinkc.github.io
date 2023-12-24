---
title:  "Useful git commands"
date:   2021-02-01 11:30:00
categories: ['Git']
tags: ['Git']
---

{% include toc title="Index" %}

Most used git commands after cloning a project. Target is to create a new feature branch to be used for development and be used for a  pull request.

## Create new Feature Branch for development
```sh
# First checkout the branch from which a new branch is to be created
git checkout <existing develop branch> # Example : future-develop
git pull  # Optional

## Pull the latest changes from parent branch into child
# must be in the child branch. Resolve any conflicts
git merge parent

#Create your branch (2 in 1 command)
git checkout -b feature/<branch-name>
# Make your changes  and commit the files
git commit -m <file names>
# Add the branch remotely
git push -u origin <branch> # (-u short for --set-upstream option)
```
# Swith commits

### uncommited changes 

Take uncommitted changes from one branch to another
```sh
# With Git 2.23
git switch -c <new-branch>

# The same could be achieved prior to Git 2.23 by
git checkout -b <new-branch>
```

### committed changes

If, by accident, a commit is made in one feature branch, but it was supposed t be in some other branch

```sh
# Find the commit hash
git cherry-pick 0359ca8b 
```
## Remove Accidental Pushes from Remote
```bash
git rm <filename or folder> # removes the file from the repo but also deletes it from the local file system.

# To remove the file from the remote repo and not delete it from the local file system use:
git rm --cached <filename or folder>

# remove from local as well as remote
git rm -r --cached <filename or folder>

# Then commit the changes
```

## Creating fresh Repository

Creating a fresh Project Local
	1. Create a repo on Github and copy the repo name.

	2. Create an IntelliJ/ Eclipse Project as a new project and goto that path using command prompt

Execute the following in Command prompt

```sh
# Initialize a repository
git init

# Create .gitignore and put data
vim .gitignore

# ************** Add some data and files *********************
#Add the files you have worked upon
git add . #(it will take care of ignore files)

#Commit the changes
git commit -m "my_message"

#Add the remote Repo git (ONLY FIRST TIME)
git remote add <branch name (any)> <http git repo address>
git remote add origin <http git repo address> OR
git remote add github <http git repo address> # instead of origin, github is the remote branch

#Add the remote Repo git
git push -u origin master (master is our local repo, branch name)
```

## Delete a remote branch using
```sh
git push origin --delete <branchName>
git push origin :old_branch
```

## Delete branch from remote repository
```sh
git push origin --delete [branchname]
```

## Delete branch from local repository
```sh
git branch -d [branchname]
```

## Rename a branch
```sh
# rename a branch while pointed to any branch:
git branch -m <oldname> <newname>

# If you want to rename the current branch, you can simply do:
git branch -m <newname>
```

## Push local branch to repo.
```
 git push --set-upstream origin <Branch name>
 ```

# Stash

## View and Clear Stash

Acts as local clipboard to git

```sh
# Clear all the stash in one go
git stash clear

# Find all the stash with index Id
git stash list

# Take the index from the stash list
git stash drop stash@{index}
```

Stash from one branch and bring it on another

If changes are made accidentally on a branch where its not needed, then stash the changes and then 
bring back into the other branch


`--keep-index` allows to stash all changes that were not added to staging area.

It safer to run `git stash apply` as it does not remove stashed changes instead of `git stash pop`. Conflicts might also occur.

 ## Links

 [https://ndpsoftware.com/git-cheatsheet.html#loc=workspace](https://ndpsoftware.com/git-cheatsheet.html#loc=workspace)

 [https://git-school.github.io/visualizing-git/#cherry-pick](https://git-school.github.io/visualizing-git/#cherry-pick)