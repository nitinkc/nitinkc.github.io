---
title:  "Git - Cleanup Maintenance"
date:   2023-11-14 20:30:00
categories: ['Git']
tags: ['Git']
---
{% include toc title="Index" %}

```shell
git remote prune origin && git repack && git prune-packed && git reflog expire --expire=1.month.ago && git gc --aggressive
```

# prune
`git remote prune origin`
- checks the remote repository (origin or any custom name) for branches that **no longer exist on the remote**
- and removes the corresponding remote-tracking branches from your local repository.

For branches created on local and pushed to remote,
```shell
git checkout -b feature/new-feature-branch
git push --set-upstream origin feature/new-feature-branch
```

Delete the branch from repo and run `git remote prune origin` and check the pruned branch on the local

```shell
git remote prune origin
Pruning origin
URL: https://github.com/nitinkc/x.git
 * [pruned] origin/feature/new-feature-branch
```

It does not, however, remove the entry from the config set by `--set-upstream`
```editorconfig
[branch "feature/new-feature-branch"]
	remote = origin
	merge = refs/heads/feature/new-feature-branch
```
It can be removed with `--unset-upstream`
```shell
git branch --unset-upstream feature/new-feature-branch
```

# repack

- Combine objects
- Compress objects
- Remove redundant objects

If repack is used without any options/switch, it performs a repack operation with the default settings

```shell
git repack -adf --depth=100
```
- `a`  all objects.
- `d` Removes unreferenced objects.
- `f` Forces the repack even (if it doesn't save space)
- `depth=100` Controls the depth of the delta chain used to represent objects.

# prune pack

# reflog expire