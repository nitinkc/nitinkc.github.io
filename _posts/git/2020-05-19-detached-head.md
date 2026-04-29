---
title: Submodules & Detached Head Problem
date: 2020-05-19 19:14:00
categories:
- Git
tags:
- Troubleshooting
- Version Control
---

{% include toc title="Index" %}

# Cloning a Project with Submodules

## With `--recurse-submodules` (Recommended)

Fetch submodules in parallel with `-j` flag:

```shell
git clone --recurse-submodules -j6 https://github.com/nitinkc/spring-microservices.git

git clone --recurse-submodules -j8 https://github.com/nitinkc/SpringBootProjects.git
```

## Without `--recurse-submodules`

If you already cloned without submodules:

```shell
git clone https://github.com/nitinkc/spring-microservices.git
cd spring-microservices

# Initialize and clone all submodules
git submodule update --init --recursive

# Or use parallel fetching
git submodule update --init --recursive --jobs 6
```

## Pulling Latest Changes

```shell
git pull --recurse-submodules
```

# Adding and Initializing Submodules

## Add a new submodule to existing project

```shell
git submodule add <GitHub Repo URL>
```

## Initialize existing submodules

```shell
git submodule init
git submodule update 
```

# Detached Head Problem

After cloning, submodules are checked out at a specific commit (detached HEAD state), not on a branch.

## Quick Fix: Checkout all submodules on main branch

```shell
git submodule foreach 'git checkout main'
```

Or if some repos use `master` instead of `main`:

```shell
git submodule foreach 'git checkout main || git checkout master'
```

## Permanent Fix: Track a branch in `.gitmodules`

Add the branch name in the `.gitmodules` file:

```ini
[submodule "foo"]
    path = foo
    url = ...
    branch = main
```

Then update submodules to the tip of the tracked branch:

```shell
git submodule update --remote
```

## Manual Resolution (for complex cases)

See [git-submodule-demo](https://github.com/nitinkc/git-submodule-demo/blob/master/README.md) for detailed steps:

```sh
git log --graph --decorate --pretty=oneline --abbrev-commit master origin/master
git log -n 2
git checkout 957833d728b3249d22a3b3160f3a48b72c576d91
git checkout -b temp
git checkout master
git merge temp
git branch -d temp  # delete temp branch
```

# Removing a Submodule

```shell
git submodule deinit -f -- my-project
git rm --cached my-project                                        
```

Then:
* Delete the entry from `.gitmodules` file
* Commit and push the changes

**Cleaning the local `.git` repo:**

* Delete the entry from `.git/config` file
* Delete the project folder from `.git/modules/<git-project-name>`

> **Tip:** Instead of manual cleanup, just commit the `.gitmodules` changes and re-clone the project
