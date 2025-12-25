---
categories: SQL
date: 2023-07-15 17:45:00
tags:
- Basics
- Fundamentals
- Tutorial
- Database
title: SQL Basics
---

{% include toc title="Index" %}

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
* PRIMARY KEY -- Make sure that the column does not have null values and is
  always having unique records
* FOREIGN KEY
* NOT NULL -- Define a column as not null if you never want to have null values
  in it.
* **CHECK** -- Validates with the given list of values
  ```sql
  create table test(
      gender	varchar(10) check (gender in ('M', 'F', 'Male', 'Female'))
  );
  ```
* UNIQUE -- Avoid duplicate values. But it allows NULL values.
  ```sql
  create table test(
      id	varchar(15) unique,
  );
  ```
* IDENTITY column


- [Exercise 1](https://en.wikibooks.org/wiki/SQL_Exercises/Employee_management){:target="\_blank"}
- [Exercise 2](https://en.wikibooks.org/wiki/SQL_Exercises){:target="\_blank"}

#### How many ways to delete data?

- truncate (deletes data but not table): TRUNCATE removes all rows from a table
- The DELETE command is used to remove rows from a table
    - you need to COMMIT or ROLLBACK the transaction to make the change
      permanent
- drop table/database : deletes a table/database
    - All the tables' rows, indexes and privileges will also be removed
    - The operation cannot be rolled back.

**Find count of departments where there are more than 5 employees.**

``` sql
select count(*) AS "# employees", d.dname
      from dept d, employees e, mapping m
      where e.eid = m.eid AND d.did = m.did
      group by d.dname
      having count(*) > 5;
```

**SET Theory**: Inline-view, TOP-N Analysis

```sql
-- Select 11th highest salary.
select EMP_ID, SALARY
from (select * from EMPLOYEE order by salary desc)
where rownum < 12
MINUS
select EMP_ID, SALARY
from (select * from EMPLOYEE order by salary desc)
where rownum < 11
```

**Name all the departments with more than 5 employees.**

```sql
select d.dname
      from dept d, employees e, mapping m
      where e.eid = m.eid AND d.did = m.did
      group by d.dname
      having count(*) > 5;
```

## JOINS

[https://nitinkc.github.io/sql/sql-joins/](https://nitinkc.github.io/sql/sql-joins/)

### INNER JOIN
#### Explicit JOIN Syntax:

```sql
SELECT a.col, b.col
FROM A a
JOIN B b ON a.col = b.col;
```

#### Implicit JOIN Syntax (Comma Syntax)
```sql
SELECT a.col, b.col
FROM A a, B b
WHERE a.col = b.col;
```
- This syntax uses a comma to list the tables and specifies the join condition in the WHERE clause.
- It is an older style of writing joins and can be less clear, especially in complex queries with multiple joins.

### The USING clause

The USING clause is used if several columns share the same name but you don’t
want to join using all of these common columns. 
- The columns listed in the USING
clause can’t have any qualifiers in the statement, including the WHERE clause.

### The ON clause

The ON clause is used to join tables where the column names don’t match in both
tables. 
- The join conditions are removed from the filter conditions in the WHERE
clause.

```sql
-- OUTER JOIN is smarter than INNER
-- Customer – cust_id - 1,2,3
-- Sales – cust_id - 3, 6

Select * from customer c, sales s where c.cust_id = s.cust_id

Select * from customer c LEFT OUTER JOIN sales s ON c.cust_id = s.sales_id
Select * from customer c RIGHT OUTER JOIN sales s ON c.cust_id = s.sales_id
Select * from customer c FULL OUTER JOIN sales s ON c.cust_id = s.sales_id
```

```sql
-- INNER
select t1.* from t1, t2 where t1.c = t2.c
And t2.d > 2000

-- SELF JOIN only one table is involved in join
Select t1.* from KYC k1, KYC k2 where k1.kyc_ind = K2.kyc_ind

SELECT SSN, E.Name AS EName, LastName, D.Name AS DName, Department, Code, Budget
 FROM Employees E **INNER JOIN** Departments D
 **ON** E.Department = D.Code;

 **IS SAME AS**

 SELECT SSN, E.Name AS Name_E, LastName, D.Name AS Name_D, Department, Code, Budget
 FROM **Employees E, Departments D**
 **where** E.Department = D.Code;
```

**SELF JOIN** – only one table is involved in join <br>

```sql
SELECT e1.ename||' works for '||e2.ename  AS
"Employees and their Managers"
FROM emp e1 JOIN emp e2 ON (e1.mgr = e2.empno);
```

OR can be written as

```sql
SELECT e1.ename||' works for '||e2.ename  AS
"Employees and their Managers"
FROM emp e1, emp e2 where (e1.mgr = e2.empno);
```

# Group By

**Identify Aggregated Columns**: Look for columns that are being aggregated using functions like `SUM()`, `COUNT()`, `AVG()`, etc. 
- These columns **do not go** into the GROUP BY clause.

**Non-Aggregated Columns**: Any column that is not part of an aggregation function and is **included** in the **SELECT**
statement must be in the GROUP BY clause. 
- These are typically the columns you want to group your results by.

**Logical Grouping**: Think about the logical grouping of your data. 
- For example, if you want to group data by continent, then continent should be in the GROUP BY clause.


Given the CITY and COUNTRY tables, query the sum of the populations of all cities where the CONTINENT is 'Asia'.
```sql
SELECT co.CONTINENT AS continent, SUM(ci.POPULATION) AS s
FROM Country co, City c
WHERE ci.CountryCode = co.Code
AND co.CONTINENT = 'Asia'
GROUP BY co.CONTINENT;
```