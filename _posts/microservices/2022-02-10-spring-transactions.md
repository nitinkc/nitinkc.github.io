---
# layout: static
title:  "Spring Transactions"
date:   2022-02-09 20:55:00
categories: Spring Microservices
tags: [Spring Microservices, Spring Boot]
---
{% include toc title="Index" %}


# Spring Transactions


## Admission Service

1. Register a Student
2. Register Student in Department
3. Register Student in Hostel (Optional and based on Gender)
4. Register Student in a Society (Optional)

In the above Example, the transaction is propagated in the same order as mentioned above.

# Transaction Propagation

[Tx Pitfalls](https://medium.com/@safa_ertekin/common-transaction-propagation-pitfalls-in-spring-framework-2378ee7d6521)

[Tx Propagation](https://www.javainuse.com/spring/boot-transaction-propagation)

Let's consider a transaction : Student Service -> Department Service

**REQUIRED** (Default Transaction Propagation) - Always executes in a transaction. If there is any existing transaction it uses it. 
If none exists then only a new one is created

If Student Service does not have a Transactional Annotation, and Department Service has REQUIRED, then a new Tx will be created.


**MANDATORY** - Always executes in a transaction. If there is any existing transaction it is used. If there is no existing transaction it will throw an exception.

If Student Service does not have a Transactional Annotation, and Department Service has 
```java
@Transactional(propagation = Propagation.MANDATORY)
```
then the exception 
```java
nested exception is org.springframework.transaction.IllegalTransactionStateException: No existing transaction found for transaction marked with propagation 'mandatory'] with root cause
org.springframework.transaction.IllegalTransactionStateException: No existing transaction found for transaction marked with propagation 'mandatory' 
```

**NEVER** - Always executes with out any transaction. It throws an exception if there is an existing transaction
If Student Service has a Transactional Annotation, and Department Service has 
```java
@Transactional(propagation = Propagation.NEVER)
```
Then there should be an exception. In the Replicated Example, appears that the default save method of JPA creates an internal Tx which is why it works.

**REQUIRES_NEW** : Always executes in a new transaction. If there is any existing transaction it gets suspended.
Irrespective of the Calling method, the new Transaction is created. If the calling method has a Tx, then its suspended and gets resumed after the called Tx is completed.


```java
20-02-02 Sun 01:17:18.333 DEBUG JpaTransactionManager Creating new transaction with name [org.springframework.data.jpa.repository.support.SimpleJpaRepository.save]: PROPAGATION_REQUIRED,ISOLATION_DEFAULT
20-02-02 Sun 01:17:18.371 DEBUG JpaTransactionManager Committing JPA transaction on EntityManager [SessionImpl(1422485332<open>)]

20-02-02 Sun 01:17:18.381 DEBUG JpaTransactionManager Creating new transaction with name [com.learn.transaction.myAdmissionService.daoService.DepartmentService.saveDepartment]: PROPAGATION_REQUIRES_NEW,ISOLATION_DEFAULT
20-02-02 Sun 01:17:18.396 DEBUG JpaTransactionManager Committing JPA transaction on EntityManager [SessionImpl(1422485332<open>)]

20-02-02 Sun 01:17:18.398 DEBUG JpaTransactionManager Creating new transaction with name [com.learn.transaction.myAdmissionService.daoService.HostelService.saveHostel]: PROPAGATION_REQUIRES_NEW,ISOLATION_DEFAULT
20-02-02 Sun 01:17:18.414 DEBUG JpaTransactionManager Committing JPA transaction on EntityManager [SessionImpl(1422485332<open>)]

20-02-02 Sun 01:17:18.417 DEBUG JpaTransactionManager Creating new transaction with name [com.learn.transaction.myAdmissionService.daoService.SocietyService.saveSociety]: PROPAGATION_REQUIRES_NEW,ISOLATION_DEFAULT
20-02-02 Sun 01:17:18.432 DEBUG JpaTransactionManager Committing JPA transaction on EntityManager [SessionImpl(1422485332<open>)]
```
## Isolation - For Concurrent Transactions

The default transaction isolation taken is that of the underlying database.

* The default isolation level is **REPEATABLE READ**  for MySQL database.
* H2 - The default is **read committed**. H2 supports only three isolation levels; read uncommitted, read committed and serializable 
which can only be set at the connection level (not per transaction).
* Oracle only supports **read committed** (default) and serializable.

## Isolation Problems
[Isolation Eg](https://www.javainuse.com/spring/boot-transaction-isolation)
[Isolation Article](https://medium.com/@elliotchance/sql-transaction-isolation-levels-explained-50d1a2f90d8f)

* **Dirty Reads** : When current transaction reads a row written by another uncommitted transaction that is in progress.
* **Non-repeatable Reads** : It occurs when current transaction reads the same data within one Transaction, but gets two 
different values, because another transaction has been committed during the life of the current transaction.
* **Phantom Reads** : (special case of non repeatable read) A phantom read happens when current transaction re-executes 
a query with search condition, receiving different results, because there has been a recently-committed transaction 
between two reads of the current Transaction.

## SQL Solution
The SQL Standard defines four isolation levels 

* **Read uncommitted** permits dirty reads, non repeatable reads and phantom reads.
* **Read committed** permits non repeatable reads and phantom reads.
* **Repeatable read** permits only phantom reads.
* **Serializable** does not permit any read errors but is slower as it is absolute Isolation.


# Rollback

Programatically handle roll back in the event of a checked exception.

In case of a checked exceptions the previously executed transactions do not get rolled back automatically even if transaction annotation is used. 
This is achieved via the RollbackFor annotation.

A checked exception is a type of exception that must be either caught or declared in the method in which it is thrown

Example: With Admission Service, if an invalid Hostel Exception is thrown, then the Tx prior to Hostel Tx (Student and Department) would be committed successfully, which is not desirable.
The requirement here is to have Student, Department, Hostel and Society Txs to be completed in its entirety or not committed at all.


```java
@Transactional(rollbackFor = InvalidHostelException.class)
   public void addStudent(Student student, Department department, Hostel hostel, Society society)
                        throws InvalidHostelException {
}
```

Logs:
```log
20-02-02 Sun 02:34:37.324 DEBUG JpaTransactionManager Found thread-bound EntityManager [SessionImpl(1417143744<open>)] for JPA transaction
20-02-02 Sun 02:34:37.324 DEBUG JpaTransactionManager Participating in existing transaction
Hibernate: select department0_.student_enrolled as student_1_1_0_, department0_.dept_name as dept_nam2_1_0_ from department department0_ where department0_.student_enrolled=?
20-02-02 Sun 02:34:37.327 DEBUG JpaTransactionManager Initiating transaction rollback
20-02-02 Sun 02:34:37.327 DEBUG JpaTransactionManager Rolling back JPA transaction on EntityManager [SessionImpl(1417143744<open>)]
20-02-02 Sun 02:34:37.332 DEBUG JpaTransactionManager Not closing pre-bound JPA EntityManager after transaction
20-02-02 Sun 02:34:37.340 DEBUG OpenEntityManagerInViewInterceptor Closing JPA EntityManager in OpenEntityManagerInViewInterceptor
20-02-02 Sun 02:34:37.341 DEBUG DispatcherServlet Failed to complete request: com.learn.transaction.myAdmissionService.exception.InvalidHostelException: Boys Hostel cannot be assigned to Female Student
20-02-02 Sun 02:34:37.355 ERROR [dispatcherServlet] Servlet.service() for servlet [dispatcherServlet] in context with path [] threw exception [Request processing failed; nested exception is com.learn.transaction.myAdmissionService.exception.InvalidHostelException: Boys Hostel cannot be assigned to Female Student] with root cause
com.learn.transaction.myAdmissionService.exception.InvalidHostelException: Boys Hostel cannot be assigned to Female Student
	at com.learn.transaction.myAdmissionService.AdmissionService.addStudent(AdmissionService.java:42)
```

## References

[Good Summary](https://stackoverflow.com/questions/8490852/spring-transactional-isolation-propagation)

[Details of Spring Tx](https://www.marcobehler.com/guides/spring-transaction-management-transactional-in-depth)

[employee organization example](https://www.javainuse.com/spring/boot-transaction)
