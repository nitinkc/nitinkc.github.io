---
# layout: static
title:  "POST API"
date:   2023-09-15 02:15:00
categories: Spring Microservices
tags: [CRUD]
---
{% include toc title="Index" %}

## Post Mapping with request Body

Code sample for a POST request using Spring Boot. Sample code converts Temperature from Farenheit to Celcius.

In all the examples below, `ResponseEntity.ok()` method is used, that takes in the response body as its argument.

```java
public static <T> ResponseEntity<T> ok(T body)
``` 

##### Scenario 1
**Convert the temperature given in Request Body of POST call.**
```shell
POST : http://localhost:8100/temperature-converter/value
```

**Request Body :**
```json
{
    "value":"10"
}
```
**Controller:**

**_@RequestBody Map<String, Double> value_** captures the request body in a map and is extracted using the map key.

**_ResponseEntity\<Double\>_** to return a Double Value
```java
@PostMapping(path = "/temperature-converter/value")
public ResponseEntity<Double> convertTemperature(@RequestBody Map<String, Double> value) {
    return ResponseEntity
            .status(HttpStatus.OK)
            .body(temperatureConvertorService.convertTemperatureValue(value.get("value")));    
}
```

##### Scenario 2: 

Convert **List of temperatures** given in Request Body of POST call and return converted List

POST : http://localhost:8100/temperature-converter/values

**Request Body :**
```json
{
    "values":["10","12.5","50","100"]
}
```
**Controller:**
```java
@PostMapping(path = "temperature-converter/values")
    public ResponseEntity<List<Double>> convertTemperatures(@RequestBody Map<String, List<Double>> body) {
        //Extract the List out of the Request body
        List<Double> temperatures = body.get("values");
        return ResponseEntity.ok(temperatureConvertorService.convertTemperatureValues(temperatures));
    }
```

Notice the response entity returning a List of converted temperatures.

##### Scenario 3: 
Convert **List of temperatures** given in Request Body with the Temperature units of POST call and return converted List
```shell
POST : http://localhost:8100/temperature-converter/
```
**Request Body :**
```json
{
    "from":"F",
    "to":"C",
    "values":["10","12.5","50","111"]
}
```
**Controller:** This time, the request body is directly mapped with the Object

```java
@PostMapping(path = "temperature-converter/")
    public ResponseEntity<List<Double>> convertTemperaturesUsingObject(@RequestBody Temperature value) {
        return ResponseEntity.ok(temperatureConvertorService.convertTemperatureValues(value.getValues()));
    }
```


# POST - Create Data

**Controller Class**
```java
//Add a new User
@PostMapping("/users")
public void addNewUser(@RequestBody User user){
    userDAOService.save(user);

}
```

**DAOService Class**
```java
//Save a new User
public void save(User user) {
    if(user.getId() == null){
        user.setId(++usersCount);
    }
    users.add(user);
    return;
}
```

In Postman, create a POST call
```shell
{{address}}{{port}}/api/hardCodedData/users
```

with Request Body - resembling User class
```json
{
"name": "Kid",
"dob": "2019-12-08T01:19:11.760+0000"
}
```
Returns 200 OK
{: .notice--info}

### POST Method enhancement 

to return HTTP Status Code and URI

```java
//Add a new User
@PostMapping("/users")
public ResponseEntity<Object> addNewUser(@RequestBody User user){
    User savedUser = userDAOService.save(user);

    //Send the URI of the saved Object
    URI location = ServletUriComponentsBuilder
            .fromCurrentRequest()
            .path("/{id}")
            .buildAndExpand(savedUser.getId()).toUri();

    return ResponseEntity.created(location).build();
}
```
Returns 201 Created
{: .notice--info} 