---
title:  "Savepoint"
date:   2023-08-02 14:03:00
categories: ['SQL']
tags: ['SQL']
---
{% include toc title="Index" %}

[Oracle Live SQL](https://livesql.oracle.com/apex/livesql/s/ehw922orljedhs8ikbguduh0)

In Oracle, you can view the savepoints defined within a transaction using the `DBMS_TRANSACTION` package.
Specifically, you can use the `DBMS_TRANSACTION.SAVEPOINT_EXISTS` function to check if a particular savepoint exists,
and the `DBMS_TRANSACTION.SET_SAVEPOINT` function to set a savepoint within the transaction.

Please note that savepoints are useful primarily for debugging and error handling purposes. 
In most scenarios, you don't need to explicitly check for the existence of savepoints. 
Instead, you can use them in exception blocks to handle errors more gracefully and roll back to 
specific points within a transaction if needed.
```sql
drop table if exists employees;

CREATE TABLE employees (
  emp_id NUMBER PRIMARY KEY,
  emp_name VARCHAR2(100)
);

INSERT INTO employees (emp_id, emp_name) VALUES (1, 'John Doe');
INSERT INTO employees (emp_id, emp_name) VALUES (2, 'Jane Smith');
INSERT INTO employees (emp_id, emp_name) VALUES (3, 'Robert Johnson');

COMMIT;

-- Assume we have a table called "employees" with columns "emp_id" and "emp_name"

-- Start the transaction
BEGIN
  -- Insert the first record
  INSERT INTO employees (emp_id, emp_name) VALUES (4, 'John');

  -- Create a Savepoint after the first record insertion
  SAVEPOINT sp_insert_record1;

  -- Check if the Savepoint sp_insert_record1 exists
 -- IF DBMS_TRANSACTION.SAVEPOINT_EXISTS('sp_insert_record1') = 1 THEN
    DBMS_OUTPUT.PUT_LINE('Savepoint sp_insert_record1 exists.');
--  ELSE
--    DBMS_OUTPUT.PUT_LINE('Savepoint sp_insert_record1 does not exist.');
--  END IF;

  -- Insert the second record
  INSERT INTO employees (emp_id, emp_name) VALUES (5, 'Jane');

  -- Create a Savepoint after the second record insertion
  SAVEPOINT sp_insert_record2;
  DBMS_OUTPUT.PUT_LINE('Savepoint sp_insert_record2 exists.');

  -- Insert the third record
  INSERT INTO employees (emp_id, emp_name) VALUES (6, 'Robert');

   DBMS_OUTPUT.PUT_LINE(10/0);

  -- Commit the transaction to save all changes
  COMMIT;
EXCEPTION
  WHEN OTHERS THEN
    -- Roll back to the first Savepoint (sp_insert_record1) if an error occurs
    ROLLBACK TO SAVEPOINT sp_insert_record1;
    DBMS_OUTPUT.PUT_LINE('Error occurred. Rolled back to the first Savepoint.');
    RAISE; -- Reraise the exception to the caller
END;

```