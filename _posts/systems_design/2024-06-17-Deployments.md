---
title: Deployments
date: 2024-06-17 11:02:00
categories:
- System Design
tags:
- CI/CD
---

{% include toc title="Index" %}

# Blue-Green Deployments

Never let the user see downtime

- if 10 servers serving, 5 deployment happening, 5 still serving

# Hot deployment

Redirect the traffic from load balancers or a proxy srvice to one env and deploy
on another

# Rollback strategy

Jenkins job opr script, if the service are up ort running

![](https://www.youtube.com/watch?v=AWVTKBUnoIg)

# 1. Big Bang Deployment

This strategy involves shutting down the old version of the application
completely and then starting up the new version.

It is the simplest and often the fastest method but comes with the risk of
significant downtime.

# 2. Rolling Deployment

In a rolling deployment, the new version of the application is gradually rolled
out to instances or servers one at a time.
This means that at any point in time, some instances are running the old version
and some are running the new version.

```markdown
Step 1: Deploy to instance 1
---------------------------------
| New  | Old  | Old  | Old  |
---------------------------------
Step 2: Deploy to instance 2
---------------------------------
| New  | New  | Old  | Old  |
---------------------------------
...
Final Step: All instances updated
---------------------------------
| New  | New  | New  | New  |
---------------------------------
``` 

# 3. Blue-Green Deployment

This strategy involves maintaining two identical environments:

- a "blue" environment running the current version and
- a "green" environment with the new version.

Traffic is switched from the blue to the green environment once the new version
is verified to be working correctly.

- Requires double the infrastructure (at least temporarily).

# 4. Canary Deployment

A canary deployment gradually rolls out the new version to a small subset of
servers (canaries) first,
then slowly increases the number if no issues are detected.

This allows for early detection of issues without impacting the majority of
users.

**Pros:**

- Limits the impact of potential issues.
- Allows for real-world testing with a small user base.

**Cons:**

- Requires robust monitoring and quick rollback mechanisms.
- More complex to implement and manage than rolling deployments.

```markdown
Step 1: Initial Deployment to Canary Users
-------------------------------------------
| Canary (5%) | Regular (95%) |
-------------------------------------------

Step 2: Gradual Increase
-------------------------------------------
| Canary (20%) | Regular (80%) |
-------------------------------------------

Step 3: Further Increase
-------------------------------------------
| Canary (50%) | Regular (50%) |
-------------------------------------------

Final Step: Full Deployment
-------------------------------------------
| New Feature (100%) |
-------------------------------------------
```

# 5. Feature Toggle - A/B Testing Deployment

Toggle button for features

A/B testing involves running two versions of the application simultaneously to
test different features or changes.

This strategy is often used for experimentation rather than for deploying new
versions, but it can be adapted for gradual rollouts.