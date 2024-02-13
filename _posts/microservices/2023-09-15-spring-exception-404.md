---
title:  "Exception Handling in Spring"
date:   2023-09-15 21:30:00
categories: Spring Microservices
tags: [Spring Microservices]
---
{% include toc title="Index" %}

# Exception upon Resource not found

If the data doesn't exist, a custom exception can be thrown
```java
//Retrieve specific users
@GetMapping(path = "/user/{id}")
public User retrieveUserById(@PathVariable int id) throws UserNotFoundException {
    User user = userDAOService.findById(id);

    //If user is not found
    if(user == null){
        throw new UserNotFoundException("User with id" + id +" is not found");
    }
    return user;
}
```


##### Custom Exception
If a custom response code is to be sent, use `@ResponseStatus(HttpStatus.NOT_FOUND)`

```java
@ResponseStatus(HttpStatus.NOT_FOUND)
public class UserNotFoundException extends RuntimeException {
    public UserNotFoundException(String message) {
        super(message);
    }
}
```

# Generic Exception and Controller Advice

Similar format of exception for all the Classes.
```java
@RestControllerAdvice
@ControllerAdvice
public class CustomizedResponseEntityExceptionHandler extends ResponseEntityExceptionHandler {

    @ExceptionHandler(Exception.class)
    public final ResponseEntity<Object> handleAllException(Exception ex, WebRequest request){
        ExceptionResponse exceptionResponse = new ExceptionResponse(new Date(), ex.getMessage(), request.getDescription(false));
        return  new ResponseEntity(exceptionResponse, HttpStatus.INTERNAL_SERVER_ERROR);
    }
}
```

### @ResponseStatus

Use `@ResponseStatus(HttpStatus.NOT_FOUND)` to denote the exception code

The custom exception class can extend Exception or RunTimeException. 

The `@ResponseStatus` of Global Exception class (The one with `@ControllerAdvice`) **takes precedence** if it's used in both
```java
@ResponseStatus(HttpStatus.NO_CONTENT)//200 series, //Seems Optional, the one in the Global exceptional handler takes precedence
public class StudentNotFoundException extends Exception {
    public StudentNotFoundException(String message) {
        super(message);
    }
}
```

If the requirement is to send the exception in business defined format, like below

```json
{
    "errorCode": "122 :: ERROR: Student is not present in the DB",
    "errorMessage": "The Student with Id 1009 does not exist",
    "requestedURI": "/student/db/1009"
}
```

Then the Custom Response class can be defined and be called into the GlobalException handler class
```java
public class ExceptionResponse {//Use Getters and Setters to avoid HttpMediaTypeNotAcceptableException
    private String errorCode;
    private String errorMessage;
    private String requestedURI;
    ...
}
```

Finally, we can take leverage of Global Exception handling.

```java
//@RestControllerAdvice
@ControllerAdvice
public class GlobalExceptionHandler {
    @ExceptionHandler(value = {StudentNotFoundException.class}) //Write the handler when such exception occurs
    @ResponseStatus(HttpStatus.NOT_FOUND)
    public ExceptionResponse handleStudentExceptions(//Method that executes upon encountering StudentNotFoundException
           StudentNotFoundException exception, final HttpServletRequest request) {
        //Set the desired fields
        ExceptionResponse error = ExceptionResponse.builder()
                .errorMessage(exception.getMessage())
                .requestedURI(request.getRequestURI())
                .exceptionType(exception.getClass().getSimpleName())
                .methodName(request.getMethod())
                .errorCode(ERR_122.getErrorCode()+" :: "+ERR_122.getErrorMessage())
                .thrownByMethod(exception.getStackTrace()[0].getMethodName())//Method Name
                .thrownByClass(exception.getStackTrace()[0].getClassName())//Class name, even the filename can be used
                .build();

        return error;
    }
}
```