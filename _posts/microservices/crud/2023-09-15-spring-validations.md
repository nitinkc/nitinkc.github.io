---
title:  "Spring Validations"
date:   2023-09-15 20:30:00
categories: Spring Microservices
tags: [Spring Microservices, Spring Boot]
---
{% include toc title="Index" %}

##### Validations applied?

**Validation at Request Body/Path Param/Request Param or Response Body**

Validation annotations like `@Pattern`,`@NotNull`, etc., are typically used to validate **input parameters or fields**
of Java objects **before** they are processed by the application logic.

Validations are **NOT** automatically applied to the response body (for ex, if the email field to be sent to UI, is a proper email),
it can be done manually

##### Dependencies
- The `@NotBlank` annotation is part of the `javax.validation.constraints` package, which is a standard part of the Java Bean Validation (JSR 380) specification.
- The implementation of  the rules specified by the Bean Validation specification (including the actual validation logic for annotations like `@NotBlank`), is provided by validation frameworks like Hibernate Validator.

Both the dependencies are required for the validations to work well
```groovy
// https://mvnrepository.com/artifact/jakarta.validation/jakarta.validation-api
implementation group: 'jakarta.validation', name: 'jakarta.validation-api', version: '3.1.0-M1'
// https://mvnrepository.com/artifact/org.hibernate.validator/hibernate-validator
implementation group: 'org.hibernate.validator', name: 'hibernate-validator', version: '8.0.1.Final'
```

### @Validated and @Valid
A brief summary of the differences between @Validated and @Valid:

**`@Validated`**: Spring-specific, enables method-level validation, and supports method parameter 
and return value validation.

`**@Valid**`: Standard Java EE annotation, primarily used for validating bean properties and method parameters at 
the field or method level.

In summary, @Validated is a useful annotation for enabling method-level validation in Spring MVC controllers, allowing you to validate method parameters and return values with ease.

##### @Valid

Use of `@Valid` in the Controller class forces a validation check. The validation is defined in the Entity class


**in Controller**
```java
//Add a new User
@PostMapping("/users")
public ResponseEntity<Object> addNewUser(@Valid  @RequestBody User user)
```

**User Entity Class (Using Lombok)**

`@ValidPhoneNumber`is a user defined Validator mentioned in the end of this blog.

```java
@Data
public class User {
    @Id
    private UUID id;

    @NotBlank(message = "Name is required")
    @Size(min=3,message = "Names should be at-least 3 characters long")
    @Pattern(regexp = "^[a-zA-Z\\s]+$", message = "Name must contain only alphabetical characters")
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

**`MethodArgumentNotValidException` for Failed Validations and exception handler**
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

**For a request body with**

```json5
{
    "name" : "hh",
    "dob" : "2070-01-31",
    "email": "test.test.com",
    "phone":"333 333 33333"
}
```

**All validation will be invoked for the user model**

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


##### Explore 

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

# @Validated

```java
@PostMapping("/admin/add")
public ResponseEntity<AdminDTO> createAdmin(@Validated(AdminDTO.AdminValidation.class) @RequestBody AdminDTO adminDTO) {
    // Business logic to create an admin
    return ResponseEntity.ok(adminDTO);
}
```

The AdminValidation interface is a marker interface used for defining a validation group in Bean Validation (JSR 380)


```java
@Data
public class AdminDTO {

    @NotBlank(message = "Username cannot be blank", groups = AdminValidation.class)
    private String username;

    @NotBlank(message = "Password cannot be blank", groups = AdminValidation.class)
    @Size(min = 8, message = "Password must be at least 8 characters long", groups = AdminValidation.class)
    private String password;

    // Other fields, constructors, getters, and setters

    // Define validation group for admin DTO
    public interface AdminValidation {}
}
```

```json5
{
    "username": "",
    "password":"12345"
}
```

```json5
{
    "from": "ExceptionResponse from MethodArgumentNotValidException",
    "errorCode": "140 :: Error: :: Validation Error",
    "errorMessage": "{password=Password must be at least 8 characters long, username=Username cannot be blank}",
    "methodName": "POST",
    "requestedURI": "/users/admin/add",
    "thrownByMethod": "resolveArgument",
    "thrownByClass": "org.springframework.web.servlet.mvc.method.annotation.RequestResponseBodyMethodProcessor",
    "exceptionType": null,
    "timestamp": "2024-03-07 01:15:47.356 AM MST(GMT-7)"
}
```

# Complex Validators

```java
@Documented
@Constraint(validatedBy = PasswordConstraintValidator.class)
@Target({ElementType.FIELD})
@Retention(RetentionPolicy.RUNTIME)
public @interface PasswordConstraint {
    String message() default "Password must contain at least two numbers and one special character (excluding '@')";
    Class<?>[] groups() default {};
    Class<? extends Payload>[] payload() default {};
}
```

The PasswordConstraintValidator class

```java
public class PasswordConstraintValidator implements ConstraintValidator<PasswordConstraint, String> {

    @Override
    public void initialize(PasswordConstraint constraintAnnotation) {}

    @Override
    public boolean isValid(String password, ConstraintValidatorContext constraintValidatorContext) {
        if (password == null) {
            return false;
        }

        // At least two numbers and one special character (excluding '@')
        String regex = "^(.*[0-9]){2,}.*[^A-Za-z0-9@]{1,}$";
        Pattern pattern = Pattern.compile(regex);
        Matcher matcher = pattern.matcher(password);

        return matcher.matches();
    }
}
```

The newly created annotation can be applied as
```java
public class AdminDTO {

    @NotBlank(message = "Username cannot be blank", groups = AdminValidation.class)
    private String username;

    @NotBlank(message = "Password cannot be blank", groups = AdminValidation.class)
    @Size(min = 8, message = "Password must be at least 8 characters long", groups = AdminValidation.class)
    @PasswordConstraint(message = "Password must contain at least two numbers and one special character (excluding '@')", groups = AdminValidation.class)
    private String password;

    // Other fields, constructors, getters, and setters
}
```