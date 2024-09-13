---
title:  "Architecture"
date:   2024-09-12 14:02:00
categories: [System Design]
tags: [System Design]
---
{% include toc title="Index" %}

# Model 1 Architecture
In the Model 1 Architecture, the JSPs handle both the presentation and some business logic directly.
- All JSP's

```mermaid!
graph TD
    A[User Request] --> B[Servlet]
    B --> C[JSP]
    C --> D[User Response]
```

# Model 2 Architecture (MVC)
In Model 2, also known as MVC (Model-View-Controller), the architecture is divided
into three main components: Model, View, and Controller.

```mermaid!
graph TD
    A[User Request] --> B[Front Controller]
    B --> C[Controller]
    C --> D[Model]
    D --> E[View]
    E --> F[User Response]
```

# Model 2 Front Controller Architecture
In this variation, a single Front Controller routes requests to appropriate controllers,
which then interact with the Model and View.

```mermaid!
graph TD
    A[User Request] --> B[Front Controller]
    B --> C[Controller 1]
    B --> D[Controller 2]
    C --> E[Model]
    D --> F[Model]
    E --> G[View 1]
    F --> H[View 2]
    G --> I[User Response]
    H --> I[User Response]
```

