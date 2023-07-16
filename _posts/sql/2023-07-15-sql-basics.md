---
title:  "SQL Basics"
date:   2023-07-15 17:45:00
categories: ['SQL']
tags: ['SQL']
---


## Default schemas
* Postgres - public
* SQL Server - dbo
* MySQL -
* Oracle - sys

```sql
-- Postgres
select * from information_schema.tables
where table_schema='public';
```

## Constraints 
-- CONSTRAINTS
* PRIMARY KEY -- Make sure that the column does not have null values and is always having unique records
* FOREIGN KEY
* NOT NULL -- Define a column as not null if you never want to have null values in it.
* **CHECK** -- Validates with the given list of values
```sql
create table test
(
	gender	varchar(10) check (gender in ('M', 'F', 'Male', 'Female'))
);
```
* UNIQUE -- Avoid duplicate values. But it allows NULL values.
```sql
create table test
(
	id	varchar(15) unique,
);
```
* IDENTITY column 
