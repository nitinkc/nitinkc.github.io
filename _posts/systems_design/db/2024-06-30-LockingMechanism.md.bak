---
categories: System Design
date: 2024-06-30 11:02:00
tags:
- System Design
title: DB Locking mechanism
---

{% include toc title="Index" %}

# Pessimistic locking

pessimistic concurrency control - places a lock on a record (row) as soon as one
user starts to update it

- other users have to wait until the lock is released.

"Select for update" works by locking the rows returned

Cons :
Deadlock free code is challenge

- not scalabkle if locked for far too long

# Optimistic locking

also called optimistic concurrency control

2 ways to implement : version number and timestamp

version number is more accurate as server clock can be inaccurate

# 3 DB Constraints

what os change data capture?

2 phase commit - db protocol, used to guarantee atomic transaction commit across
multiple nodes.

Saga