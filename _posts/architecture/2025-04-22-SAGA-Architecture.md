---
categories:
- Architecture
date: 2025-04-22 14:02:00
tags:
- Microservices
title: SAGA Architecture Style & 2-Phase Commit
---

{% include toc title="Index" %}

> Category : Concurrency Architecture

A two-phase commit (2PC) is a protocol used to ensure all participants in a distributed transaction either commit or rollback changes in a coordinated manner, maintaining data consistency across multiple systems.

# How 2PC Works:
### Preparation Phase:
- The coordinator sends a request to all participants to prepare for the transaction.
- Each participant performs necessary operations and responds with a vote (commit or abort).

### Commit Phase:
- If all participants vote to commit, the coordinator sends a commit request.
- If any participant votes to abort, the coordinator sends a rollback request.

Two different approaches to implementing the Saga pattern in distributed systems:
- Saga with orchestration
- Saga with choreography

---

# Achieving 2PC in Spring Boot:

## Use JTA (Java Transaction API):
- Spring Boot supports JTA for managing distributed transactions. Configure JTA in your application to handle 2PC.

## Configure Transaction Manager:
- Set up a transaction manager that supports 2PC, such as Atomikos or Bitronix.

## Define Transactional Boundaries:
- Annotate methods with `@Transactional` to define transactional boundaries.

## Handle Distributed Transactions:
- Ensure all participating services and databases are configured to support JTA transactions

# **Saga with Choreography:**
In the choreography approach, each service involved in the transaction listens for events and performs its local transaction.

- If a service completes its transaction **successfully**, it publishes an event that **triggers the next service in the sequence**.
- If a service detects a **failure**, it publishes compensating events to undo the previous actions (using the catch block).

This approach is **decentralized** and relies on event-driven communication.

#### **Advantages:**
- **Decoupled Services:** Each service operates independently and only needs to know about the events it listens to and publishes.
- **Simplicity:** Easy to implement for simple workflows without strict ordering requirements.

#### **Disadvantages:**
- **Complexity in Ordering:** Managing the sequence of events can become complex if there are strict ordering requirements.
- **Debugging Challenges:** It can be difficult to trace and debug the flow of events across multiple services.

### **Example - Saga Pattern with Choreography:**

#### **Order Service:**
The `OrderService` creates an order and publishes an `OrderCreatedEvent`. 
- If an error occurs, it publishes an `OrderCancelledEvent` to trigger rollback actions.

```java
@Service
public class OrderService {

    @Autowired
    private EventPublisher eventPublisher;

    @Transactional
    public void createOrder(Order order) {
        try {
            // Perform order creation logic
            eventPublisher.publish(new OrderCreatedEvent(order.getOrderId(), order.getProduct(), order.getQuantity()));
        } catch (Exception e) {
            //Rollback event / Compensating Event
            eventPublisher.publish(new OrderCancelledEvent(order.getOrderId()));
        }
    }
}
```
#### **Inventory Service:**
The `InventoryService` listens(`@EventListener` handleOrderCreated()) for `OrderCreatedEvent` to update inventory. 
- If an error occurs, it publishes an `InventoryRestoredEvent` to revert inventory changes. 
- It also listens for `OrderCancelledEvent`(handleOrderCancelled()) to restore inventory.

```java
@Service
public class InventoryService {

    @EventListener
    @Transactional
    public void handleOrderCreated(OrderCreatedEvent event) {
        try {
            // Update inventory logic
        } catch (Exception e) {
            // Publish compensating event
            eventPublisher.publish(new InventoryRestoredEvent(event.getOrderId(), event.getProduct(), event.getQuantity()));
        }
    }

    @EventListener
    @Transactional
    public void handleOrderCancelled(OrderCancelledEvent event) {
        // Restore inventory logic
    }
}
```

### In the event of Service failure itself:
1. **Retry Mechanism:** Implement a retry mechanism for the failed service. If a service is temporarily down, the system can retry the operation after a certain interval.
2. **Dead Letter Queue:** Use a dead letter queue to store failed messages. When a service is down, the messages can be moved to the dead letter queue and retried once the service is back up.
3. **Compensating Transactions:** Define compensating transactions in each service to undo the changes made by previous steps. If a service is down, other services can listen for failure events and execute compensating actions.

---

# **Saga with Orchestration:**
In the orchestration approach, a **central orchestrator (or coordinator)** manages the sequence of transactions.

The orchestrator **sends commands** to each service to perform its local transaction and **waits for a response** before proceeding to the next step. This approach **centralizes the control flow**.

#### **Advantages:**
- **Centralized Control:** The orchestrator manages the sequence and can enforce strict ordering of transactions.
- **Easier Debugging:** The flow of transactions is easier to trace and debug since the orchestrator handles the coordination.

#### **Disadvantages:**
- **Single Point of Failure:** The orchestrator becomes a critical component, and its failure can impact the entire transaction.
- **Potential Bottleneck:** The orchestrator can become a bottleneck if not properly scaled.

### **Example - Saga Pattern with Orchestration:**

#### **Order Service:**
The `OrderService` delegates the order creation process to the `SagaOrchestrator`.

#### **Order Service:**
```java
@Service
public class OrderService {

    @Autowired
    private SagaOrchestrator sagaOrchestrator;

    @Transactional
    public void createOrder(Order order) {
        sagaOrchestrator.startSaga(order);
    }
}
```

#### **Saga Orchestrator:**
The `SagaOrchestrator` coordinates the transaction sequence. 
- It processes payment and updates inventory. 
- If an error occurs, it triggers compensating actions(within catch block) to refund payment and restore inventory.

```java
@Service
public class SagaOrchestrator {

    @Autowired
    private PaymentService paymentService;

    @Autowired
    private InventoryService inventoryService;

    @Transactional
    public void startSaga(Order order) {
        try {
            paymentService.processPayment(order);
            inventoryService.updateInventory(order);
        } catch (Exception e) {
            // Trigger compensating actions
            paymentService.refundPayment(order);
            inventoryService.restoreInventory(order);
        }
    }
}
```

## Handling Rollbacks:
If any service fails, the orchestrator triggers compensating actions to revert the changes made by previous services. This ensures that the system remains consistent.

---

# **Choosing Between Choreography and Orchestration:**
- **Use Choreography** if your services are relatively independent and the transaction flow is simple.
- **Use Orchestration** if you need strict control over the transaction sequence and easier debugging.