---
title: Idempotence & HTTP Methods - Designing RESTful URI's
date: 2023-01-31 03:53:00
categories:
- Microservices
tags:
- Spring Boot
- REST
---

{% include toc title="Index" %}

# Introduction
This article explores HTTP methods, the concept of idempotence, and best practices for designing RESTful URIs in microservices.

# HTTP Methods Overview

| HTTP Method                 | Description                                                                 | Idempotent?            |
|:----------------------------|:----------------------------------------------------------------------------|:-----------------------| 
| `GET` - fetch               | Retrieving information                                                       | Yes                    |
| `PUT` - update              | Updating existing information                                               | Yes                    |
| `POST` - create             | Creating new information using collection-based URIs (no unique ID present) | No                     |
| `DELETE`                    | Deleting information                                                        | Yes                    |

## PUT vs PATCH
Both PUT and PATCH are used for editing resources, but they differ in payload requirements:
- **PUT** requires the complete request payload for the resource.
- **PATCH** requires only the fields being changed.

# Idempotence
**Concept**: Same output for the same input. Handling duplicate requests ensures that repeated calls
do not alter the result beyond the initial call.

In microservices, idempotence is crucial for handling accidental duplicates from message brokers, 
API retries, or user actions. It prevents unintended side effects like data duplication.

> Idempotency is not enforced by the HTTP protocol; developers must implement it in their APIs.

## Implementing Idempotence
To achieve idempotence:
1. Generate a unique identifier for each request.
2. Store the ID in the database to detect and discard duplicates.

For example, a refresh or resend on an idempotent method reloads without effect,
while non-idempotent methods should warn about potential duplication.

## Idempotence in Practice
- **POST**: Typically non-idempotent, as multiple calls create multiple resources.
- **PUT**: Should be idempotent; multiple identical calls update the same resource without creating duplicates.
- **GET/DELETE**: Naturally idempotent.

### Example: Handling PUT for Creation (Non-Idempotent)
Using PUT to insert a new row can violate idempotence if not handled properly, as multiple calls might add new rows.

```java
// Example: Using PUT to add a new user (not recommended for creation)
// This would create a new user each time if not checked
@PutMapping("/add")
public ResponseEntity<Map<String,Object>> addNewUser(@Valid @RequestBody User user){
    User savedUser = userService.save(user); // Creates new ID each time
    return ResponseEntity.status(HttpStatus.CREATED).body(getStringObjectMap(savedUser));
}
```

### Best Practices for POST and PUT
- **POST**: Use for creating new resources. To maintain non-idempotence, check for existing resources:
  ```java
  // Check if user exists before creating
  if (userService.existsById(user.getId())){
      return ResponseEntity.status(HttpStatus.CONFLICT)
          .body(Collections.singletonMap("message", "User already exists"));
  }
  // Proceed to create
  ```
- **PUT**: Use only for updating existing resources. Return 404 if the resource doesn't exist:
  ```java
  // Check if user exists for update
  if (userService.findByPhoneOrEmail(user).isEmpty()) {
      return ResponseEntity.notFound().build();
  }
  // Proceed to update
  ```

### Use Cases
- **Case 1**: Creating a new user (one-time): Use POST.
- **Case 2**: Creating orders (may repeat for same user): Use POST.
- **Case 3**: Updating user/order data: Use PUT.

# Designing RESTful URIs
RESTful URIs should be intuitive and resource-oriented. There are two main types: instance URIs and collection URIs.

## Instance Resource URIs
Include a unique ID for the specific resource.

Examples:
```
/profiles/{profileId}
/messages/{messageId}
/messages/{messageId}/comments/{commentId}
/messages/{messageId}/likes/{likeId}
```

## Collection URIs
Use plural resource names for collections.

Examples:
```
/messages  # All messages
/messages/{messageId}/comments  # Comments for a specific message
```

## Pagination and Filtering
Use query parameters for pagination and filtering to manage large datasets.

- **Parameters**:
  - `offset`: Starting point (e.g., 0 for first page).
  - `limit`: Number of items per page (e.g., 10).

- **GET Example**:
  ```
  /messages?offset=30&limit=10
  ```

- **POST Example** (parameters in body):
  ```json
  {
      "startDate": "2023-12-01",
      "endDate": "2024-01-11",
      "limit": 1,
      "offset": 0
  }
  ```
