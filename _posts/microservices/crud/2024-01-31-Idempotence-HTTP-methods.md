---
title:  "Idempotence & HTTP Methods - Designing RESTful URI's"
date:   2023-01-31 03:53:00
categories: [Microservices]
tags: [Microservices]
---
{% include toc title="Index" %}

# HTTP Methods

| HTTP Method                 | Description                                                                  | Format                 |
|:----------------------------|:-----------------------------------------------------------------------------|:-----------------------| 
| `GET` - fetch               | getting the information                                                      | Idempotent, Repeatable |
| `PUT` - update the old data | Updating  information                                                        | Idempotent, Repeatable |
| `POST` -  submit new data   | Creating new information using Collection based URI (UNIQUE id not present)  | **Non-Idempotent**     |
| `DELETE`                    | Deleting an information                                                      | Idempotent, Repeatable |


# **Idempotence**

Call multiple times without changing the result beyond the initial call.  

A refresh/resend button on an idempotent method will **reload without any effect**, but on non idempotence, 
code/client side code should warn about data duplication

Idempotency is **NOT** directly enforced by the HTTP protocol, it's a critical principle in API design and 
implementation, and **programmers are responsible** for ensuring that their APIs behave idempotently where appropriate.

## Note
It is possible to INSERT a new row using both PUT and POST calls. The code would perform the same, but the idempotency 
is not maintained in case the PUT method is used to insert a new row in DB. Multiple executions of put will add a new row each time.

```java
//Add a new User
//@PostMapping("/add")
@PutMapping("/add")
public ResponseEntity<Map<String,Object>> addNewUser(@Valid @RequestBody User user){
    User savedUser = userService.save(user);//USer service creates a new Id for new request and save a new record
    return ResponseEntity
            .status(HttpStatus.CREATED)
            .body(getStringObjectMap(savedUser));
}
```

In RESTful APIs, `POST` is typically used to **create a new resource**, while PUT is used to **update an existing resource**

* POST requests are not idempotent, meaning that multiple identical requests might result in different outcomes (e.g., multiple resources created).
* PUT requests are idempotent, meaning that multiple identical requests should have the same outcome (e.g., updating the same resource).

**creating a new resource each time, the method would be NON IDEMPOTENT.**

Decide whether you want the operation to be idempotent or not. 

If you intend to create a new resource each time, **then POST is appropriate**.

If you want to ensure that the same resource is updated regardless of how many times the request is made, then PUT should be used.
Use PUT method **only when updating an existing resource**. 

For PUT, If the resource doesn't exist, consider returning a 404 Not Found status code.

**Implement Idempotent Operations:**
For PUT requests, ensure that the operation is idempotent by making the same update regardless of how many times the request is made.


CASE 1: Creating a new user into a system : POST - one time activity. should not repeat

CASE 2: Creating a new order or a repeated order for the same User : POST

CASE 3: Updating the created order or user data : PUT


# Designing RESTful URI's

2 types of Resource URI's

* Instance Resource URI
* Collection URI (Resource names in plural)

**Instance Resource URI**
• Unique id of the resource in the URI


```shell
/profiles/{profileId}
/messages/{messageId}
/messages/{messageId}/comments/{commentId} #comment belongs to a message
/messages/{messageId}/likes/{likeId}
```


**Collection URI (Resource names in plural)**
`/messages` for all messages

```shell
#Represents all the comments for a particular messageId 
/messages/{messageId}/comments
```

**Query Parameter for Pagination and Filtering**

`offset` is the starting point 

`limit` is the page size

For get request, pass as a path parameter
```shell
#Represents all the comments for a particular messageId 
/messages?offset=30&limit=10
```

or for the post request, can be sent in the request body as well
```json
{
    "startDate":"2023-12-01",
    "endDate":"2024-01-11",
    "limit": 1,
    "offset": 0
}
```

for POST, to maintain non-idempotence, perform the following steps:

- Check if the resource already exists before creating a new one.
- If the resource exists, return an appropriate error response (e.g., `409 Conflict` or `422 Unprocessable Entity`).
- If the resource doesn't exist, proceed with creating a new one and a `201 Created`response is returned with the location of the newly created resource.

```java
// Check if the user with the same identifier already exists
if (userService.existsById(user.getId())) {
    // Resource already exists, return 409 Conflict
    return ResponseEntity
        .status(HttpStatus.CONFLICT)
        .body(Collections.singletonMap("message", "User with the same ID already exists"));
}
```

To fulfill the requirement of using the PUT method only for updating an existing resource and 
returning a 404 Not Found status code if the resource doesn't exist,

```java
// Check if the user already exists
if (userService.findByphoneOrEmail(user).size() > 0) {//find by Id or email or phone or any other pseudo primary key
        // Resource does not exist, return 404 Not Found
	return ResponseEntity.notFound().build();
}
```
