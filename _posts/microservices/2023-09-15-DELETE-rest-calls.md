---
title:  "DELETE REST Calls"
date:   2023-09-15 21:30:00
categories: Spring Microservices
tags: [CRUD]
---
{% include toc title="Index" %}

# DELETE Rest Call

in DAOService
```java
//Delete a user
public User deleteById(int id){
    Iterator<User> itr = users.iterator();
    User deletedUser=null;
    //boolean idExists = false;
    while(itr.hasNext()){
        User currentUser = itr.next();
        if(id == currentUser.getId()){
            //idExists=true;
            deletedUser = currentUser;
            itr.remove();
        }
    }
    return deletedUser;
}
```

In Controller
```java
//Delete a User
@DeleteMapping(path = "/user/{id}")
public User deleteUserById(@PathVariable int id) throws UserNotFoundException {
    User user = userDAOService.deleteById(id);

    //If user is not found
    if(user == null){
        throw new UserNotFoundException("User with id " + id +" is not found");
    }
    return user;
}
```
Delete a user by passing its ID to a delete postman request-

`{{address}}{{port}}/api/hardCodedData/user/1`