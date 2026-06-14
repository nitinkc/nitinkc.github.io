---
title: "Agile Principles & Scrum vs Kanban Comparison"
date: 2026-04-06
categories: [management]
tags: [agile, scrum, kanban, principles, comparison]
---

{% include toc title="Index" %}

# The 12 Agile Principles

If you need a quick refresher on Agile basics and values first, see {% link _posts/management/2024-09-19-agile.md %}.

The Agile Manifesto is supported by twelve principles that guide agile software development practices.

---

## 1. Customer Satisfaction Through Early Delivery

> Our highest priority is to satisfy the customer through early and continuous delivery of valuable software.

**In Practice:** Deliver working software frequently, get feedback early and often, prioritize features that provide immediate value.

## 2. Welcome Changing Requirements

> Welcome changing requirements, even late in development. Agile processes harness change for the customer's competitive advantage.

**In Practice:** Embrace change as an opportunity, don't fight against new requirements, use change to help customers stay competitive.

## 3. Deliver Working Software Frequently

> Deliver working software frequently, from a couple of weeks to a couple of months, with a preference to the shorter timescale.

**In Practice:** Aim for 2-4 week delivery cycles. Shorter iterations reduce risk and provide more feedback opportunities.

## 4. Business and Developers Must Work Together

> Business people and developers must work together daily throughout the project.

**In Practice:** Product Owner available to the team, regular collaboration, shared understanding of goals and priorities.

## 5. Build Projects Around Motivated Individuals

> Build projects around motivated individuals. Give them the environment and support they need, and trust them to get the job done.

**In Practice:** Create a supportive environment, remove obstacles, trust the team's expertise, empower self-organization.

## 6. Face-to-Face Communication

> The most efficient and effective method of conveying information to and within a development team is face-to-face conversation.

**In Practice:** Prioritize direct communication, co-locate teams when possible, use video calls for remote teams.

## 7. Working Software is the Primary Measure

> Working software is the primary measure of progress.

**In Practice:** Focus on delivering working increments, don't measure progress by documents or plans, demo working software regularly.

## 8. Sustainable Development Pace

> Agile processes promote sustainable development. The sponsors, developers, and users should be able to maintain a constant pace indefinitely.

**In Practice:** Avoid burnout, no death marches, maintain a steady sustainable velocity.

## 9. Technical Excellence

> Continuous attention to technical excellence and good design enhances agility.

**In Practice:** Invest in code quality, refactor regularly, practice Test-Driven Development (TDD), don't accumulate technical debt.

## 10. Simplicity

> Simplicity—the art of maximizing the amount of work not done—is essential.

**In Practice:** Build only what's needed, avoid over-engineering, YAGNI (You Aren't Gonna Need It), focus on the MVP.

## 11. Self-Organizing Teams

> The best architectures, requirements, and designs emerge from self-organizing teams.

**In Practice:** Let teams decide how to work, avoid micromanagement, trust collective wisdom, enable autonomous decision-making.

## 12. Regular Reflection and Adjustment

> At regular intervals, the team reflects on how to become more effective, then tunes and adjusts its behavior accordingly.

**In Practice:** Hold Sprint Retrospectives, implement improvements immediately, continuous process improvement.

---

## The Agile Manifesto

These principles support the four core values:

| We Value | Over |
|----------|------|
| **Individuals and interactions** | Processes and tools |
| **Working software** | Comprehensive documentation |
| **Customer collaboration** | Contract negotiation |
| **Responding to change** | Following a plan |

> *While there is value in the items on the right, we value the items on the left more.*

---

## Principles in Scrum Context

| Principle | How Scrum Implements It |
|-----------|------------------------|
| Customer satisfaction | Sprint Reviews with stakeholders |
| Welcome change | Product Backlog can be updated anytime |
| Frequent delivery | Regular Sprint increments |
| Daily collaboration | Daily Scrum, PO availability |
| Motivated individuals | Self-organizing teams |
| Face-to-face | Scrum events, co-location |
| Working software | "Done" increments each Sprint |
| Sustainable pace | Consistent Sprint length, velocity |
| Technical excellence | Definition of Done, quality focus |
| Simplicity | Sprint Goal focus, backlog prioritization |
| Self-organizing | Team decides how to work |
| Reflect and adjust | Sprint Retrospective |

---

# Scrum vs Kanban

Both Scrum and Kanban are Agile frameworks, but they have different approaches to managing work.

## Key Differences

| Aspect | Scrum | Kanban |
|--------|-------|--------|
| **Cadence** | Fixed-length Sprints (1-4 weeks) | Continuous flow |
| **Roles** | Product Owner, Scrum Master, Developers | No required roles |
| **Planning** | Sprint Planning at start of Sprint | Pull from backlog as capacity allows |
| **Work Items** | Sprint Backlog (fixed during Sprint) | Pulled directly from Product Backlog |
| **Changes** | Generally no changes during Sprint | Changes can happen anytime |
| **Board Reset** | Board resets each Sprint | Board is never reset |
| **Metrics** | Velocity | Lead time, cycle time, WIP |

---

## Scrum Flow

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   Product   │ ──► │    Sprint    │ ──► │    Done     │
│   Backlog   │     │   Backlog    │     │  Increment  │
└─────────────┘     └──────────────┘     └─────────────┘
                          │
                    Sprint Duration
                      (2-4 weeks)
```

**Scrum Events:**
1. Sprint Planning - Start of Sprint
2. Daily Scrum - Every day
3. Sprint Review - End of Sprint
4. Sprint Retrospective - End of Sprint

---

## Kanban Flow

```
┌─────────────┐     ┌─────────┐     ┌─────────┐     ┌──────┐
│   Product   │ ──► │  To Do  │ ──► │ Doing   │ ──► │ Done │
│   Backlog   │     │  (3)    │     │  (4)    │     │      │
└─────────────┘     └─────────┘     └─────────┘     └──────┘
                        WIP             WIP
                       Limit           Limit
```

**Kanban Practices:**
1. Visualize Work - Use a Kanban board
2. Limit WIP - Strict limits per column
3. Manage Flow - Monitor and optimize
4. Pull System - Items pulled when capacity allows

---

## WIP Limits in Kanban

**Work in Progress (WIP) Limits** are strict constraints on how many items can be in each column.

**Why WIP Limits?**
- Ensures items move across the board quickly
- Reduces context switching
- Identifies bottlenecks
- Improves flow and throughput

> An empty or nearly empty column signals the previous column to send another item. This is the **"pull" system** in action.

---

## Roles Comparison

### Scrum Roles

| Role | Responsibility |
|------|----------------|
| **Product Owner** | Manages backlog, defines priorities |
| **Scrum Master** | Ensures Scrum is followed, removes impediments |
| **Developers** | Create the product increment |

### Kanban Roles

| Role | Responsibility |
|------|----------------|
| **Product Owner** | Manages backlog (optional) |
| **Agile Coach** | Helps team maintain good habits (optional) |
| **Team** | Does the work |

---

## Meetings Comparison

### Scrum Meetings

| Meeting | Frequency | Duration |
|---------|-----------|----------|
| Sprint Planning | Start of Sprint | Up to 8 hours |
| Daily Scrum | Daily | 15 minutes |
| Sprint Review | End of Sprint | Up to 4 hours |
| Sprint Retrospective | End of Sprint | Up to 3 hours |

### Kanban Meetings

| Meeting | Frequency | Duration |
|---------|-----------|----------|
| Daily Standup | Daily | 15 minutes |
| Demo | As appropriate | Varies |
| Retrospective | Periodically | Varies |

---

## When to Use Each

### Use Scrum When:

- ✅ Working on new product development
- ✅ Team is new to Agile
- ✅ Need predictable delivery cadence
- ✅ Stakeholders need regular demos
- ✅ Work can be planned in iterations

### Use Kanban When:

- ✅ Support/maintenance work with unpredictable demand
- ✅ Continuous delivery environment
- ✅ Work items vary greatly in size
- ✅ Need maximum flexibility
- ✅ Already have a mature Agile team

---

## Hybrid Approaches

Many teams use elements of both:

**Scrumban** - Combines Scrum's structure with Kanban's flow:
- Use Scrum events with Kanban board
- Apply WIP limits within Sprints
- Continuous improvement from both frameworks

---

## Summary

| Choose | If You Need |
|--------|-------------|
| **Scrum** | Structure, roles, predictable cadence |
| **Kanban** | Flexibility, continuous flow, minimal overhead |
| **Scrumban** | Best of both worlds |

---

## Key Takeaways

1. **People over process** - Tools and processes are important, but skilled people working together are more important
2. **Working product** - Deliver value, not documents
3. **Collaboration** - Work with customers, not against contracts
4. **Adaptability** - Plans are useful, but being able to change is more useful

---

*The Agile Manifesto was created in 2001 by 17 software developers and remains the foundation of agile practices today.*
