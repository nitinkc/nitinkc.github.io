---
title:  "Spring Validations"
date:   2023-09-15 20:30:00
categories: Spring Microservices
tags: [Spring Microservices, Spring Boot]
---
{% include toc title="Index" %}


# Validations

Both the dependencies are required for the vaidations to work well
```shell
// https://mvnrepository.com/artifact/jakarta.validation/jakarta.validation-api
implementation group: 'jakarta.validation', name: 'jakarta.validation-api', version: '3.1.0-M1'
// https://mvnrepository.com/artifact/org.hibernate.validator/hibernate-validator
implementation group: 'org.hibernate.validator', name: 'hibernate-validator', version: '8.0.1.Final'
```

Use of @Valid in the Controller class forces a validation check. The validation is defined in the Entity class

The @NotBlank annotation is part of the `javax.validation.constraints` package, 
which is a standard part of the Java Bean Validation (JSR 380) specification. 

However, the implementation of this specification, including the actual validation logic for annotations 
like @NotBlank, is provided by validation frameworks like Hibernate Validator.

Hibernate Validator is one such implementation of the rules specified by the Bean Validation specification 


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

```java
@NotNull
@NotEmpty
@NotBlank : to have at least one character
@Min and @Max: only for numerical field
@Pattern : string field following a particular regular expression.
@Email : specialization with @Pattern for a valid email address.
```
