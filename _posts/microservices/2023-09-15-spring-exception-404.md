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

If a custom response code is to be sent, use @ResponseStatus(HttpStatus.NOT_FOUND)

##### Custom Exception
```java
@ResponseStatus(HttpStatus.NOT_FOUND)
public class UserNotFoundException extends RuntimeException {
    public UserNotFoundException(String message) {
        super(message);
    }
}
```

# Generic Exception

Similar format of exception for all the Classes.
```java
@RestController
@ControllerAdvice
public class CustomizedResponseEntiryExceptionHandler extends ResponseEntityExceptionHandler {

    @ExceptionHandler(Exception.class)
    public final ResponseEntity<Object> handleAllException(Exception ex, WebRequest request){
        ExceptionResponse exceptionResponse = new ExceptionResponse(new Date(), ex.getMessage(), request.getDescription(false));
        return  new ResponseEntity(exceptionResponse, HttpStatus.INTERNAL_SERVER_ERROR);
    }
}
```