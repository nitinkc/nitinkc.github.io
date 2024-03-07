---
title:  "Exception Handling in Spring"
date:   2023-09-15 21:30:00
categories: Spring Microservices
tags: [Spring Microservices]
---
{% include toc title="Index" %}

[Simple Global Exception Handler Project with Notes](https://github.com/nitinkc/SpringBoot-GlobalExceptionHandling)

[SpringBoot Reference Project with more complexities](https://github.com/nitinkc/SpringBoot-reference)

If the data doesn't exist, a custom exception can be thrown if needed
```java
//Retrieve specific users
@GetMapping(path = "/user/{id}")
public User retrieveUserById(@PathVariable int id) throws UserNotFoundException {
    Optional<User> user = userRepository.findById(id);

    return user.orElseThrow(
            () -> new UserNotFoundException("User with id " + id + " is not found"));
}
```

##### Custom Business Exception

The `UserNotFoundException` can be defined as

```java
//@ResponseStatus(HttpStatus.NOT_FOUND)//Seems Optional, the one in the Global exceptional handler takes precedence
public class UserNotFoundException extends RuntimeException {
    public UserNotFoundException(String message) {
        super(message);
    }
}

//Or Make a generic exception and use it by extending
public class UserNotFoundException extends BusinessException {
    public UserNotFoundException(String message) {
        super(message);
    }
}
```

# Global Exception Handler

Similar format of exception for all the Exception Classes.

The `ResponseEntityExceptionHandler` class in Spring MVC is designed to handle exceptions and provide appropriate 
responses. By extending ResponseEntityExceptionHandler, you inherit its functionality and can override methods 
to customize the exception handling behavior.

However, **it's not strictly necessary** to extend ResponseEntityExceptionHandler to create a global exception 
handler. You can create a global exception handler without extending ResponseEntityExceptionHandler, 
but you would need to handle the response creation manually.

```java
//@RestControllerAdvice
@ControllerAdvice
public class CustomizedResponseEntityExceptionHandler extends ResponseEntityExceptionHandler {
    @ExceptionHandler(Exception.class)
    public final ResponseEntity<Object> handleAllException(Exception ex, WebRequest request){
        ExceptionResponse exceptionResponse = new ExceptionResponse(new Date(), ex.getMessage(), request.getDescription(false));
        return  new ResponseEntity(exceptionResponse, HttpStatus.INTERNAL_SERVER_ERROR);
    }
}

@ControllerAdvice
@Slf4j
@Order(Ordered.HIGHEST_PRECEDENCE) // Set the highest precedence
public class ValidationExceptionHandler {
    ...
}
```
# Difference between RestControllerAdvice and ControllerAdvice

`@ControllerAdvice`

- Targets all Spring MVC controllers, including those that return views (ModelAndView).
It is typically used in applications where controllers return both views and data (JSON/XML responses).
The handler methods in a class annotated with @ControllerAdvice can return a variety of objects including ModelAndView, ResponseEntity, HttpHeaders, HttpEntity, etc., providing flexibility in response handling.

`@RestControllerAdvice`

- Targets only classes annotated with `@RestController` or those that return `@ResponseBody`.
- It is specifically designed for RESTful web services where controllers exclusively produce data in the form of JSON or XML responses.
- The handler methods in a class annotated with @RestControllerAdvice typically return response entities like ResponseEntity or plain objects (which are automatically serialized to JSON/XML), 
as they are designed to handle data-centric exceptions in a RESTful context.

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
@Slf4j
@RestControllerAdvice
public class GlobalExceptionHandler extends ResponseEntityExceptionHandler {
    //Handling 2 exception classes. Notice the parameter of handleNotFoundExceptions method (BusinessException exception)
    @ExceptionHandler(value = {UserNotFoundException.class, StudentNotFoundException.class})
    @ResponseStatus(HttpStatus.NOT_FOUND)
    public ResponseEntity<ExceptionResponse> handleNotFoundExceptions(BusinessException exception, final HttpServletRequest request) {
        ExceptionResponse error = ExceptionResponse.builder()
                .from("From Exception Response")
                .errorMessage(exception.getMessage())
                .requestedURI(request.getRequestURI())
                .exceptionType(exception.getClass().getSimpleName())
                .methodName(request.getMethod())
                .errorCode(ErrorCodes.ERR_122.getErrorCode()+" :: "+ ErrorCodes.ERR_122.getErrorMessage())
                .thrownByMethod(exception.getStackTrace()[0].getMethodName())
                .thrownByClass(exception.getStackTrace()[0].getClassName())
                .timestamp(ZonedDateTime.now().format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss.SSS a z(O)")))
                .build();

        return new ResponseEntity<>(error, HttpStatus.NOT_FOUND);
    }
}
```

Sample response from a properly handled exception
```json5
{
    "from": "From Exception Response",
    "errorCode": "122 :: ERROR: Entity is not present in the DB",
    "errorMessage": "User with id a0eebc99-9c0b-4ef8-bb6d-06bb9bdddddd is not found",
    "methodName": "GET",
    "requestedURI": "/users/a0eebc99-9c0b-4ef8-bb6d-6bb9bdddddd",
    "thrownByMethod": "lambda$findById$0",
    "thrownByClass": "com.spring.reference.service.UserService",
    "exceptionType": "UserNotFoundException",
    "timestamp": "2024-03-03 22:24:38.477 PM MST(GMT-7)"
}
```

# Handling Validation Errors

[https://nitinkc.github.io/spring/microservices/spring-validations/](https://nitinkc.github.io/spring/microservices/spring-validations/)

if incorrect email is sent `/test/email?email=ab.cdef.gmail.com` for the API

```java
 @GetMapping("/email")
public String testEmail(@Valid @Email(message = "Please provide a valid email address")
                        @RequestParam(value = "email") String email,
                        @RequestParam(value = "greet", required = false, defaultValue = "No Val from Request") String greet,
                        @RequestParam(value = "count", required = false, defaultValue = "-1") Integer count) {

    StringBuilder sb= new StringBuilder();
    sb.append(email).append(" email OK").append("\nCount is ").append(count).append("\n").append(greet);
    return sb.toString();
}
```

Handle the `ConstraintViolationException`

```java
@ExceptionHandler(ConstraintViolationException.class)
protected ResponseEntity<MyExceptionResponse> handleRequestParamNotValid(Exception exception, final HttpServletRequest request) {

    MyExceptionResponse error = MyExceptionResponse.builder()
            .from("Validation Exception Response from handleRequestParamNotValid")
            .errorMessage(exception.getMessage())
            .requestedURI(request.getRequestURI())
            .exceptionType(exception.getClass().getSimpleName())
            .methodName(request.getMethod())
            .errorCode(ErrorCodes.ERR_122.getErrorCode()+" :: "+ ErrorCodes.ERR_122.getErrorMessage())
            .thrownByMethod(exception.getStackTrace()[0].getMethodName())
            .thrownByClass(exception.getStackTrace()[0].getClassName())
            .timestamp(ZonedDateTime.now().format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss.SSS a z(O)")))
            .build();

    return new ResponseEntity<>(error, HttpStatus.BAD_REQUEST);
}
```

```json5
{
    "from": "Validation Exception Response from handleRequestParamNotValid",
    "errorCode": "122 :: ERROR: Entity is not present in the DB",
    "errorMessage": "testEmail.email: Please provide a valid email address",
    "methodName": "GET",
    "requestedURI": "/test/email",
    "thrownByMethod": "invoke",
    "thrownByClass": "org.springframework.validation.beanvalidation.MethodValidationInterceptor",
    "exceptionType": "ConstraintViolationException",
    "timestamp": "2024-03-03 23:05:04.961 PM MST(GMT-7)"
}
```

# Ordered.HIGHEST_PRECEDENCE

If there are two handlers for an exception in two separate classes, the one with higher precedence will execute first.

Example for `BadInputException`, the one from `ValidationExceptionHandler` takes priority
```java
@ControllerAdvice
@Slf4j
@Order(Ordered.HIGHEST_PRECEDENCE) // Set the highest precedence
public class ValidationExceptionHandler {
    @ExceptionHandler(BadInputException.class)
    public ResponseEntity<Object> handleAllExceptions(BadInputException ex, WebRequest request) {
        String errorMessage = " An error occurred:"  + ex.getMessage() + "\n" +
                "With description :: " + request.getDescription(true);
        
        return new ResponseEntity<>(errorMessage, HttpStatus.INTERNAL_SERVER_ERROR);
    }
}
```

Same exception is handled in another class
```java
@Slf4j
@RestControllerAdvice
public class GlobalExceptionHandler extends ResponseEntityExceptionHandler {
    
    //Handling 2 exception classes. Notice the parameter of handleNotFoundExceptions method (BusinessException exception)
    @ExceptionHandler(value = {WordsNotFoundException.class, BadInputException.class})
    @ResponseStatus(HttpStatus.NOT_FOUND)
    public ResponseEntity<MyExceptionResponse> handleNotFoundExceptions(Exception exception, final HttpServletRequest request) {
        MyExceptionResponse error = MyExceptionResponse.builder()
                .from("From Exception Response")
                .errorMessage(exception.getMessage())
                .requestedURI(request.getRequestURI())
                .exceptionType(exception.getClass().getSimpleName())
                .methodName(request.getMethod())
                .errorCode(ErrorCodes.ERR_122.getErrorCode() + " :: " + ErrorCodes.ERR_122.getErrorMessage())
                .thrownByMethod(exception.getStackTrace()[0].getMethodName())
                .thrownByClass(exception.getStackTrace()[0].getClassName())
                .timestamp(ZonedDateTime.now().format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss.SSS a z(O)")))
                .build();

        return new ResponseEntity<>(error, HttpStatus.NOT_FOUND);
    }
}
```