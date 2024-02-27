---
# layout: static
title:  "Spring Data JPA & CRUD - GET PUT POST DELETE"
date:   2022-02-09 20:55:00
categories: Spring Microservices
tags: [CRUD]
---

{% include toc title="Index" %}

## Using JpaRepository

```java
@Repository
public interface StudentRepository extends JpaRepository<Student, Long> {
}
```

> Avoiding Service layer for simplicity

##### Get a list of all the users
```java
@RestController
@RequestMapping("/jpa")
public class StudentController {
	@Autowired
	private StudentRepository studentRepository;
	// Retrieve all users, bypassing service
	@GetMapping(path = "/students")
	public List<Student> retrieveAllUsers() {
		return studentRepository.findAll();
	}
}
```

##### Get a student based on id 

With support of the use of Java 8 OPTIONAL, Null values can be easily avoided.

```java
// Retrieve specific users
@GetMapping(path = "/student/{id}")//from get request parameter
public Student retrieveUserById(@PathVariable("id") @NotBlank Long id) {
    Optional<Student> optional = studentRepository.findById(id);//To Accommodate Null return

    if (!optional.isPresent()){
        throw new StudentNotFoundException("id:" + id);
    }

    Student foundStudent = optional.get();
    return foundStudent;
}
```

Another Approach

```java
// Retrieve specific users
@GetMapping(path = "/student/{id}")
public Student retrieveUserById(@PathVariable("id") @NotBlank Long id) {
    return studentRepository.findById(id)
            .orElseThrow(() -> new StudentNotFoundException("id:" + id));
}
```

## POST Rest Calls (Creating a new Entity)

Doing this in Controller Class is not recommended. Service Layer is avoided for simplicity.
```java
@PostMapping("/student")
public ResponseEntity<Object> createStudent(@Valid @RequestBody Student student){
    System.err.println("###################################### POST Begins ######################################");
    Student savedStud = studentRepository.save(student);
    System.err.println("###################################### POST Ends ######################################");
    URI location = ServletUriComponentsBuilder
            .fromCurrentRequest()
            .path("/{id}")
            .buildAndExpand(savedStud.getId())
            .toUri();
    
    return (ResponseEntity<Object>) ResponseEntity.created(location).build();
}
```

In Postman, create a POST call **{{address}}{{port}}/api/jpa/student** with Request Body RAW and JSON as 
```json
{
"name": "Nitin",
"dob": "2019-12-08T01:19:11.760+0000"
}
```


## PUT Request (modifying an existing Value) 

Use of Java 8 Map.

In this approach, A PUT Request can also be used to Create a new entry in case the passed id DOES NOT Exist in the DB.
**Not recommended** to save, if ID doesn't exist as **id would not be known** for a new entry
```java
@PutMapping("/student/{id}")
public Student modifyValue(@RequestBody Student newStudent, @PathVariable Long id){
    return studentRepository.findById(id)
            .map(student -> {
                student.setName(newStudent.getName());
                student.setDob(newStudent.getDob());
                return studentRepository.save(student);
            })
            .orElseGet(() -> {//Not recommended to save, if doesn't exist as ID WILL not be known for a new entry
                newStudent.setId(id);
                return studentRepository.save(newStudent);
            });
}
```

## Generic Exception (With Controller Advice)

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

## DELETE Rest Call

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
Delete a user by passing its ID to a delete postman request- **{{address}}{{port}}/api/hardCodedData/user/1**


## Validations

Use of @Valid in the Controller class forces a validation check. The validation is defined in the Entity class

in Controller
```java
//Add a new User
@PostMapping("/users")
public ResponseEntity<Object> addNewUser(@Valid  @RequestBody User user){
```

User Entity Class (Using Lombok)
```java
@Data
public class User {
	private Integer id;
	@Size(min=2,message = "Names should be at least characters long")
	private String name;
	@Past(message = "DOB Cannot be in the Future")
	private Date dob;
}
```

Exception for Failed Validations in the customized response entity exception handler
```java
 //Exception for Failed Validations
@Override
protected ResponseEntity<Object> handleMethodArgumentNotValid(MethodArgumentNotValidException ex, HttpHeaders headers, HttpStatus status, WebRequest request){

    ExceptionResponse exceptionResponse = new ExceptionResponse(new Date(), "Validation Failed", ex.getBindingResult().toString());
    return  new ResponseEntity(exceptionResponse, HttpStatus.BAD_REQUEST);
}
```