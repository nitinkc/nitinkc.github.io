---
categories: Git
date: 2023-11-14 20:30:00
tags:
- Optimization
- Commands
title: Git Maintenance & Clean-up
---

{% include toc title="Index" %}

The Final command

```shell
git remote prune origin && git repack && git prune-packed && git reflog expire --expire=1.month.ago && git gc --aggressive
```

- `git remote prune origin`: Removes references to branches that have been
  deleted on the remote.
- `git repack -a -d`: Repack all objects and remove redundant packs.
- `git prune-packed`: Remove objects that are no longer referenced by any pack.
- `git reflog expire --expire=1.month.ago --all-ref`: Expire reflog entries
  older than 1 month (for all references).
- `git gc --aggressive:` Perform aggressive garbage collection to optimize the
  repository.

add as alias

```shell
# System alias from Terminal
alias gitclean="git remote prune origin && git repack && git prune-packed && git reflog expire --expire=1.month.ago && git gc --aggressive"
# Git aliasa
git config --global alias.cleanup '!git remote prune origin && git repack && git prune-packed && git reflog expire --expire=1.month.ago && git gc --aggressive'
```

# Git Maintenance

```shell
git maintenance start
```

modifies `.git/config` file to add a `maintenance.strategy` value set to
`incremental` with following values:

- `gc`: disabled.
- `commit-graph`: hourly.
- `prefetch`: hourly.
- `loose-objects`: daily.
- `incremental-repack`: daily.

```shell
[maintenance]
	auto = false
	strategy = incremental
```

[Refer Scaling monorepo maintenance](https://github.blog/open-source/git/scaling-monorepo-maintenance/?ref=blog.gitbutler.com#multi-pack-indexes)

# Key Git Maintenance Commands

Run Manually

```shell
git maintenance run
```

### `git gc` (Garbage Collection)

**Basic Usage:**

```sh
git gc
```

--aggressive: Perform a more thorough garbage collection.

```shell
git gc --aggressive
```

--prune=<date>: Remove objects older than the specified date.

```shell
git gc --prune=2.weeks.ago
```

Configure local repo for a daily run

```shell
git config --add maintenance.gc true
git config --add maintenance.gc daily
```

## prune

Removes objects that are not reachable from any commit.

```shell
git prune
git remote prune origin
git prune --expire=2.weeks.ago #Prune objects older than the specified date
```

- checks the remote repository (origin or any custom name) for branches that *
  *no longer exist on the remote**
- and removes the corresponding remote-tracking branches from your local
  repository.

For branches created on local and pushed to remote,

```shell
git checkout -b feature/new-feature-branch
git push --set-upstream origin feature/new-feature-branch
```

Delete the branch from repo and run `git remote prune origin` and check the
pruned branch on the local

```shell
git remote prune origin
Pruning origin
URL: https://github.com/nitinkc/x.git
 * [pruned] origin/feature/new-feature-branch
```

It doesn’t, however, remove the entry from the config set by `--set-upstream`

```text
[branch "feature/new-feature-branch"]
	remote = origin
	merge = refs/heads/feature/new-feature-branch
```

It can be removed with `--unset-upstream`

```shell
git branch --unset-upstream feature/new-feature-branch
```

# repack

Repacks objects to reduce the number of packs and optimize storage.

- Combine objects
- Compress objects
- Remove redundant objects

If repack is used without any options/switch, it performs a **repack operation
with the default settings**

```shell
git repack -adf --depth=100
git repack -a -d
```

- `a`  all objects.
- `d` Removes unreferenced objects.
- `f` Forces the repack even (if it doesn't save space)
- `depth=100` Controls the depth of the delta chain used to represent objects.

# reflog expire

Expires entries from the reflog to clean up old references.

```shell
git reflog expire --expire=2.weeks.ago --all-ref
```