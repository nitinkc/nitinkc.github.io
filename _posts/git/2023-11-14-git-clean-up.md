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