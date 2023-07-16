---
title:  "SQL Revisions"
date:   2016-04-15 11:45:00
categories: ['SQL']
tags: ['SQL']
---


{% include toc title="Index" %}


[Exercise 1](https://en.wikibooks.org/wiki/SQL_Exercises/Employee_management){:target="\_blank"}

[Exercise 2](https://en.wikibooks.org/wiki/SQL_Exercises){:target="\_blank"}

##### SQL

<i class="fa fa-question"></i> Retrieve a particular empid.

> <i class="fa fa-check"></i>
>  Use **where** clause

<i class="fa fa-question"></i> How many types to delete the data

> - truncate (deletes data but not table): TRUNCATE removes all rows from a table
> - The DELETE command is used to remove rows from a table
>     + DELETE FROM emp WHERE job = 'CLERK';
>     +  you need to COMMIT or ROLLBACK the transaction to make the change permanent
> - drop table/database : deletes a table/database
>     +  All the tables' rows, indexes and privileges will also be removed
>     +  The operation cannot be rolled back.

**Find count departments id where more than 5 employees.**

``` sql
select count(*) AS "# employees", d.dname
      from dept d, employees e, mapping m
      where e.eid = m.eid AND d.did = m.did
      group by d.dname
      having count(*) > 5;
```

**SET Theory**: Inline-view, TOP-N Analysis
```sql
-- Select 11th heighest salary.
select EMP_ID, SALARY
from (select * from EMPLOYEE order by salary desc)
where rownum < 12
MINUS
select EMP_ID, SALARY
from (select * from EMPLOYEE order by salary desc)
where rownum < 11
```

**Name all the depts with more than 5 employees.**

```sql
select d.dname
      from dept d, employees e, mapping m
      where e.eid = m.eid AND d.did = m.did
      group by d.dname
      having count(*) > 5;
```

## JOINS

JOINS : To combine rows from two or more tables, based on common fields between them.

**INNER JOIN**: (Common Type) – EQUI JOIN, NON-EQUI JOIN, NATURAL JOIN, SELF JOIN

  Return rows as long as there one match in both tables

**OUTER JOIN** (Smarter than inner)– LEFT, RIGHT & FULL

_OUTER is result of INNER & some additional data from one of the tables or from both the tables_

  - **LEFT OUTER JOIN**: Return all rows from the left table, even if there are
 no matches in the right table and all matching rows from right

  - **RIGHT OUTER JOIN**: Return all rows from the right table and matching rows from left

  - **FULL OUTER JOIN**: Return rows when there is a match in one of the tables

![alt text]({{ site.url }}/media/Joins.png)

> The USING clause

The USING clause is used if several columns share the same name but you don’t want to join using all of these common columns. The columns listed in the USING clause can’t have any qualifiers in the statement, including the WHERE clause.

> The ON clause

The ON clause is used to join tables where the column names don’t match in both tables. The join conditions are removed from the filter conditions in the WHERE clause.

```SQL
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

-----------

<i class="fa fa-question"></i> explain plan, performance tuning.

 - The EXPLAIN PLAN statement displays execution plans chosen by the Oracle optimizer for SELECT, UPDATE, INSERT, and DELETE statements. A statement's execution plan is the sequence of operations Oracle performs to run the statement.

<i class="fa fa-question"></i> syntax for finding indexes in tuning.

> Indexes are special lookup tables that the database search engine can use to
> speed up data retrieval. An index is a pointer to data in a
> table.
> <pre>
> CREATE UNIQUE INDEX index_name
ON table_name (column_name)
> </pre>
<i class="fa fa-question"></i> full table scan

<i class="fa fa-question"></i> index advantegs of indexes in sql tuning? What is the syntax of doing that.
> Indexes are a performance drag when the time comes to modify records.

<i class="fa fa-question"></i>

> Multiple Conditions : AND <br>
> ``` sql
> SELECT * from EMP WHERE salary > 10000 AND dateofjoining > ‘1-Jan-1990’ ;
> ```
> <br>Range Selection - BETWEEN
> ``` sql
> SELECT * from EMP WHERE salary between 9000 AND 20000;
> ```
> <br>Exact List Matching
> ```sql
> SELECT * from EMP WHERE employeeID IN (3001,  3002);
> ```

<i class="fa fa-question"></i> Full table scan

 - A full table scan occurs when an index is either not used or there is no index on the table(s)
 - Full table scans should be avoided when reading large tables.For example, a full table scan is performed when a table that does not have an index is read
 -  FTS will be performed even though an index is present on that table.
     +  If a query does have a WHERE clause, but none of the columns in that WHERE clause match.
     +  when WHERE clause prevents the use of an index like below.
     +  If the NOT EQUAL (the “<>“) operator is used.
     +  If the NOT operator is used.
     +  If the wildcard operator is used in the first position of a comparison string. An example is “WHERE NAME LIKE ‘%INTERVIEW%'”.
