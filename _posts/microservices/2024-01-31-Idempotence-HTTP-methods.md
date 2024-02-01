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


**Idempotence** : Call multiple times without changing the result beyond the initial call.  

A refresh/resend button on an idempotent method will **reload without any effect**, but on non idempotence, 
browser warns about data duplication 

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
