---
title:  "SQL/Query Optimization"
date:   2024-06-18 14:25:00
categories: ['SQL']
tags: ['SQL']
---
{% include toc title="Index" %}

![](https://www.youtube.com/watch?v=BHwzDmr6d7s)

[How SQL queries are executed in DB](https://github.com/ByteByteGoHq/system-design-101?tab=readme-ov-file#how-is-an-sql-statement-executed-in-the-database)

[Query Execution Plan](https://github.com/ByteByteGoHq/system-design-101?tab=readme-ov-file#visualizing-a-sql-query)

# DB Index
A database index is like an efficient **lookup table** that allows a database to find data much faster. It uses Data structues like B-Tree, HashMap, Bitmaps etc.

- index helps to avoid full scan for a single row in a massive table
- with index, the pointer helps to get the exact address of the indexed column

An index on a non-primary column allows the database to quickly locate rows based on the indexed column's values, without scanning the entire table

- columns that are frequently used in WHERE clauses, JOIN conditions, or ORDER BY clauses are good candidates for indexing.

@startuml

entity "Employees" as Employees {
+ employee_id : INT
  --
  first_name : VARCHAR(50)
  last_name : VARCHAR(50)
  email : VARCHAR(100)
  department : VARCHAR(50)
  hire_date : DATE
  --
  PRIMARY KEY(employee_id)
  }

@enduml


Creating index for Employees Table
```sql
CREATE INDEX idx_department ON employees(department);
       
-- Analyze Query Performance
EXPLAIN SELECT * FROM employees WHERE department = 'Sales';
```

Composite Index
```sql
CREATE INDEX idx_first_last_name ON employees(first_name, last_name);
-- Analyze Query Performance
EXPLAIN SELECT * FROM employees WHERE first_name = 'John' AND last_name = 'Doe';
```

# Types of Database Indexes
###  based on Key Attributes:
**Primary Index**: Automatically created when a primary key constraint is defined on a table. 

**Clustered Index**
A clustered index determines the physical order of data in a table. 
A table can have only **one clustered index** because the data rows can be stored in only one order. 

The primary index is usually a clustered index, but a clustered index can be created on other columns as well. 

When a table has a clustered index, the data rows are stored in the same order as the index.

A clustered index is most useful for **searching in a range**. Only one clustered index can exist per table.

```sql
CREATE CLUSTERED INDEX idx_department ON employees(department);
-- The data rows in the employees table will be stored in the order of the department values.
```

**Non-clustered or Secondary Index**: This index does not store data in the order of the index. Instead, it provides a list of virtual pointers or references to the location where the data is actually stored.

@startuml
entity "Employees" as Employees {
+ employee_id : INT
--
first_name : VARCHAR(50)
last_name : VARCHAR(50)
email : VARCHAR(100)
department : VARCHAR(50)
hire_date : DATE
--
PRIMARY KEY(employee_id)
}

note "Primary Index on employee_id (Clustered)" as Primary
Primary .. Employees

entity "Secondary Index on last_name" as Secondary {
--
last_name : VARCHAR(50)
--
}
Secondary .. Employees

entity "Clustered Index on department" as Clustered {
--
department : VARCHAR(50)
--
}
Clustered .. Employees
@enduml


### based on Data Coverage:
Dense index: Has an entry for every search key value in the table. Suitable for situations where the data has a small number of distinct search key values or when fast access to individual records is required.

Sparse index: Has entries only for some of the search key values. Suitable for situations where the data has a large number of distinct search key values.

Specialized Index Types:
Bitmap Index: Excellent for columns with low cardinality (few distinct values). Common in data warehousing.

Hash Index: A index that uses a hash function to map values to specific locations. Great for exact match queries.

Filtered Index: Indexes a subset of rows based on a specific filter condition. Useful to improve query speed on commonly filtered columns.

Covering Index: Includes all the columns required by a query in the index itself, eliminating the need to access the underlying table data.

Function-based index: Indexes that are created based on the result of a function or expression applied to one or more columns of a table.

Full-Text Index: A index designed for full-text search, allowing for efficient searching of text data.

Spatial Index: Used for indexing geographical data types.


# Datastructures used in Indexing
Indices can be saved in 
- B-Tree (Balanced Tree) or variation of it
- HashMaps
- Bitmap Index

For where clause, comparisons should be  SARGABLE - **S**earch **ARG**ument **ABLE**
- refers to queries that can use indices for faster execution

# B-Tree Index

B-Tree indices are commonly used for columns with a wide range of values and support equality and range queries efficiently.

Range Query
```sql
-- Assuming an index on the `salary` column
SELECT * FROM employees
WHERE salary BETWEEN 50000 AND 100000;
```

Composite Index Query
```sql
-- Assuming a composite index on the `last_name` and `first_name` columns
SELECT * FROM employees
WHERE last_name = 'Smith' AND first_name = 'John';
```

Bitmap Index

Bitmap indices are more efficient for columns with a low cardinality, such as gender or status columns.

Equality Query on Low Cardinality Column
```sql
-- Assuming a bitmap index on the `gender` column
SELECT * FROM employees
WHERE gender = 'F';
```

Ensuring SARGABLE Queries

# Do's and Dont's
Avoid Functions on Indexed Columns: Functions on indexed columns prevent the use of the index.
```sql
-- Not SARGABLE
SELECT * FROM employees
WHERE YEAR(hire_date) = 2020;

-- SARGABLE
SELECT * FROM employees
WHERE hire_date BETWEEN '2020-01-01' AND '2020-12-31';
```

Avoid Operations on Indexed Columns: Operations on indexed columns also prevent the use of the index.
```sql
-- Not SARGABLE
SELECT * FROM employees
WHERE salary + 1000 = 50000;

-- SARGABLE
SELECT * FROM employees
WHERE salary = 49000;
```

Use AND for Composite Indexes: Ensure all parts of the composite index are used in the query.
```sql
-- Assuming a composite index on (last_name, first_name)
-- Not fully SARGABLE (only uses part of the index)
SELECT * FROM employees
WHERE last_name = 'Smith';

-- Fully SARGABLE
SELECT * FROM employees
WHERE last_name = 'Smith' AND first_name = 'John';
```

