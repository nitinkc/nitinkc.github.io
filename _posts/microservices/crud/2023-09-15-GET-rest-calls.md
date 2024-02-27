---
title:  "GET REST Calls"
date:   2023-09-15 21:30:00
categories: Spring Microservices
tags: [CRUD]
---
{% include toc title="Index" %}

# Basic GET Calls

Creating a List of Objects for the Demo Purposes

In the DAO Service
```java
@Getter
@Setter
private static List<User> users = new ArrayList<>();
```

### Get a list of all the users

Utility methods (Later provided by @CrudRepository)
```java
// Retrieve all users
public List<User> findAll() {
    return getUsers();
}
````

In the Controller

No need to create an object of the DAOService. Use @Autowired annotation to get the object of the DAOService
```java
@Autowired
private UserDAOService userDAOService;
```
```java
//Retrieve all users
@GetMapping(path = "/users")
public List<User> retrieveAllUsers(){
    return userDAOService.findAll();
}
```
http://localhost:8089/api/hardCodedData/users

### Get a user based on id (from get request parameter)

In Controller
```java
//Retrieve specific users
@GetMapping(path = "/user/{id}")
public User retrieveUserById(@PathVariable int id){
    return userDAOService.findById(id);
}
```

In User DAOService
```java
// Retrieve users by Id
public User findById(int id) {
    if(getUsers().get(id) == null) {
        return null;
    }
    return getUsers().get(id);
	}
```
http://localhost:8089/api/hardCodedData/user/1

