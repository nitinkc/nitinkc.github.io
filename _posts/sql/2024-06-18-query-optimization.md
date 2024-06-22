---
title:  "Query Optimization"
date:   2024-06-18 14:25:00
categories: ['SQL']
tags: ['SQL']
---
{% include toc title="Index" %}

![](https://www.youtube.com/watch?v=BHwzDmr6d7s)

[How SQL queries are executed in DB](https://github.com/ByteByteGoHq/system-design-101?tab=readme-ov-file#how-is-an-sql-statement-executed-in-the-database)

[Query Execution Plan](https://github.com/ByteByteGoHq/system-design-101?tab=readme-ov-file#visualizing-a-sql-query)


Indices can be saved in B-Trees or Bitmap Index

For where clause, comparisons should be  SARGABLE - **S**earch **ARG**ument **ABLE**
- refers to queries that can use indices for faster execution

B-Tree Index

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