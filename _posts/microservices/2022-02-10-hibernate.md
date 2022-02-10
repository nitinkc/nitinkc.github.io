---
# layout: static
title:  "Hibernate"
date:   2022-02-10 20:55:00
categories: Spring Microservices
tags: [Spring Microservices, Spring Boot]
---
{% include toc title="Index" %}

# One To Many
A one-to-many association links two tables based on a Foreign Key column so that the child table record references
the Primary Key of the parent table row.

This association can either be Unidirectional One to Many association or Bidirectional One to Many

* The bidirectional association requires the **child entity** mapping to provide a **@ManyToOne** annotation,
* The unidirectional @OneToMany association is simple as parent-side requires One to many annotation.

###