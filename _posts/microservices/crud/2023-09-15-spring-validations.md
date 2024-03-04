---
title:  "Spring Validations"
date:   2023-09-15 20:30:00
categories: Spring Microservices
tags: [Spring Microservices, Spring Boot]
---
{% include toc title="Index" %}


# Validations

Both the dependencies are required for the validations to work well
```shell
// https://mvnrepository.com/artifact/jakarta.validation/jakarta.validation-api
implementation group: 'jakarta.validation', name: 'jakarta.validation-api', version: '3.1.0-M1'
// https://mvnrepository.com/artifact/org.hibernate.validator/hibernate-validator
implementation group: 'org.hibernate.validator', name: 'hibernate-validator', version: '8.0.1.Final'
```

Validation annotations like `@Pattern`,`@NotNull`, etc., are typically used to validate input parameters or fields 
of Java objects before they are processed by the application logic. 

They are not automatically applied to the response body.


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
    @Id
    private UUID id;

    @NotBlank(message = "Name is required")
    @Size(min=3,message = "Names should be at-least 3 characters long")
    private String name;

    @Past(message = "DOB Cannot be in the Future")
    @Column(name = "date_of_birth")
    private Date dob;

    @ValidPhoneNumber(message = "Can be in the format {1111111111, (111) 111 1111, 111-111-1111}")
    private String phone;

    @Email(message = "Please provide a valid email address")
    private String email;
}
```

Exception for Failed Validations in the customized response entity exception handler
```java
@ExceptionHandler(MethodArgumentNotValidException.class)
public ResponseEntity<MyExceptionResponse> handleValidationExceptions(MethodArgumentNotValidException ex, final HttpServletRequest request) {
    Map<String, String> errors = new HashMap<>();
    ex.getBindingResult().getAllErrors().forEach((error) -> {
        String fieldName = ((FieldError) error).getField();
        String errorMessage = error.getDefaultMessage();
        errors.put(fieldName, errorMessage);
    });

    MyExceptionResponse myExceptionResponse = MyExceptionResponse.builder()
            .from("ExceptionResponse")
            .timestamp(ZonedDateTime.now().format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss.SSS a z(O)")))
            //.exceptionType(ex.getBindingResult().toString())
            .errorMessage(errors.toString())
            .requestedURI(request.getRequestURI())
            .methodName(request.getMethod())
            .errorCode(ErrorCodes.ERR_140.getErrorCode()+" :: "+ ErrorCodes.ERR_140.getErrorMessage())
            .thrownByMethod(ex.getStackTrace()[0].getMethodName())
            .thrownByClass(ex.getStackTrace()[0].getClassName())
            .build();

    return ResponseEntity.badRequest().body(myExceptionResponse);
}
```

Explore the following validations

```java
@NotNull
@NotEmpty
@NotBlank : to have at least one character
@Min and @Max: only for numerical field
@Pattern : string field following a particular regular expression.
@Email : specialization with @Pattern for a valid email address.
```

# User defined Validator

```java
@Documented
@Constraint(validatedBy = {})
@Pattern(regexp = "^\\(?(\\d{3})\\)?[- ]?(\\d{3})[- ]?(\\d{4})$") //Covers {"1111111111", "(111) 111 1111", "111-111-1111"};
@ReportAsSingleViolation
@Retention(RetentionPolicy.RUNTIME)
@Target({ElementType.FIELD, ElementType.PARAMETER})
public @interface ValidPhoneNumber {

    String message() default "Invalid phone number";

    Class<?>[] groups() default {};

    Class<? extends Payload>[] payload() default {};
}
```

Invoke the custom validator using the required Annotation
```java
@Data
public class ExampleRequest {
    @NotBlank
    @ValidPhoneNumber
    private String phoneNumber;//valid = {"1111111111", "(111) 111 1111", "111-111-1111"};

}
```

For a request body with 

```json5
{
    "name" : "hh",
    "dob" : "2070-01-31",
    "email": "test.test.com",
    "phone":"333 333 33333"
}
```

All validation will be invoked for the user model

```json5
{
    "from": "ExceptionResponse",
    "errorCode": "140 :: Error: :: Validation Error",
    "errorMessage": "{phone=Can be in the format {1111111111, (111) 111 1111, 111-111-1111}, dob=DOB Cannot be in the Future, name=Names should be at-least 2 characters long, email=Please provide a valid email address}",
    "methodName": "POST",
    "requestedURI": "/users/add",
    "thrownByMethod": "resolveArgument",
    "thrownByClass": "org.springframework.web.servlet.mvc.method.annotation.RequestResponseBodyMethodProcessor",
    "exceptionType": null,
    "timestamp": "2024-03-04 00:52:39.455 AM MST(GMT-7)"
}
```