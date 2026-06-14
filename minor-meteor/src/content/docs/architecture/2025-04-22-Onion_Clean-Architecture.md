---
title: Onion/Clean Architecture Style
date: 2025-04-22 14:02:00
categories:
- Architecture
tags:
- Architecture
---

{% include toc title="Index" %}

> Category : Layered Architecture

# Clean Architecture
Clean Architecture, popularized by **Robert C. Martin (Uncle Bob)**, emphasizes the separation of concerns and dependency inversion. It organizes code into concentric layers, each with a specific role:
- **Entities**: Core business rules and objects.
- **Use Cases**: Application-specific business rules.
- **Interface Adapters**: Converting data from the use cases to a format suitable for the outer layers.
- **Frameworks and Drivers**: External systems like databases, UI, and other frameworks [1](https://code-maze.com/dotnet-differences-between-onion-architecture-and-clean-architecture/).

# Onion Architecture
Onion Architecture, introduced by **Jeffrey Palermo**, also focuses on separation of concerns but visualizes the system as **concentric circles** (like an onion):
- **Domain Layer**: Core business logic and entities.
- **Service Layer**: Business services and operations.
- **Infrastructure Layer**: Technical concerns like data access.
- **Presentation Layer**: User interface and interaction 
- [Reference](https://code-maze.com/dotnet-differences-between-onion-architecture-and-clean-architecture/).

### Key Differences
While both architectures aim to **decouple business logic from technical concerns**, 
- Clean Architecture places a strong emphasis on **dependency inversion**, ensuring that the inner layers do not depend on the outer layers. 
- Onion Architecture, on the other hand, structures layers around a central domain model