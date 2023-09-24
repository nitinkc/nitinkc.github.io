---
title:  "Spring Boot Revisions"
date:   2023-09-15 11:50:00
categories: Spring Microservices
tags: [Spring Microservices, CRUD]
toc: true
---

# Stereotype Annotations

Basic philosophy of Spring Boot : Conventions over configurations
{: .notice--info}

##### @Component
* **Purpose**: Marks a class as a Spring component or bean.
* **Use Case**: Generally used as a generic stereotype for any Spring-managed component.
* **Commonly Used in**: Utility classes, business logic classes, and other non-specialized components.

##### @Controller 
* **Purpose**: Marks a class as a Spring MVC controller.
* **Use Case**: Used for classes that handle HTTP requests in a Spring MVC web application.
* **Commonly Used in**: Classes that define request mappings, handle user input, and return views or data to the client.
  
##### @Service
* **Purpose**: Marks a class as a service or business logic component.
* **Use Case**: Typically used for classes that contain the business logic of the application.
* **Commonly Used in**: Service layer classes that encapsulate business rules, data processing, and interactions with 
  repositories or other services.

##### @Repository
* **Purpose**: Marks a class as a Spring Data repository.
* **Use Case**: Used for classes that interact with a database or external data source.
* **Commonly Used in**: Data access objects (DAOs) that perform CRUD (Create, Read, Update, Delete) operations on 
  entities.

# REST APIs

```shell
Retrieve all Users - GET /users
Create a User - POST /users
Retrieve one User - GET /users/{id} -> /users/1
Delete a User - DELETE /users/{id} -> /users/1
Retrieve all posts for a User - GET /users/{id}/posts
Create a posts for a User - POST /users/{id}/posts
Retrieve details of a post - GET /users/{id}/posts/{post_id}
```

# Appliation Yaml settings
Set a desired Port
```shell script
server.port=8089
```

# Scans

## ComponentScan

`@ComponentScan` is used to specify the packages that Spring should scan to discover Spring-managed components like 
beans, controllers, services, etc.

```java
@ComponentScan(basePackages = {
        "com.test.animals", 
        "com.flowers"
})
```
## Entity Scan

`@EntityScan` is specific to Spring Data JPA. 
* It's used to specify the packages where JPA entities are located.
* This is important because Spring Data JPA needs to know where the entity classes are in order to create 
 repositories  and perform CRUD operations.


```java
@EntityScan(basePackages = {"com.learningJPA.dSpringDataRepository"
        ,"com.learningJPA.eTest.model"
        //,"com.learningJPA.hibernate.*"
}) 
```

## SpringBootApplication ScanBasePackages:

`@SpringBootApplication` is a meta-annotation that combines several annotations, including @ComponentScan.
* scanBasePackages within @SpringBootApplication allows you to specify the base packages to scan for Spring 
components. 
* used in the main application class.
* It also scans the default package where the main application class is located.
* exclude argument is used to exclude specific auto-configurations, which means that Spring Boot won't automatically 
  configure the classes mentioned.

```java
@SpringBootApplication(
    scanBasePackages = {
        "com.test.package1",
        "com.test.service.security"
    },
    exclude = { JmxAutoConfiguration.class })
```

# @Autowired & Dependency Injection

Eliminates the need of creating a new object and hence the need of constructors from the components
`StudentService studentService = new StudentService();`
```java
@Autowired
StudentService studentService;//Free to use studentService object within the class anywhere
```

`@Autowired`  used for automatic dependency injection.

**Dependency injection** is a design pattern in which objects are **provided** with their dependencies (i.e., the 
objects they need to collaborate with) rather than creating those dependencies themselves.

**Automatic Injection**: When you annotate a field, setter method, or constructor with @Autowired, Spring will 
automatically inject the required dependency (another Spring bean) at runtime.  

* You don't need to create or instantiate the dependent object manually; Spring takes care of it.

#### Types of Injection:

##### Field Injection
AVOID THIS
{: .notice--danger}
it's generally not recommended because it makes testing and mocking dependencies more challenging. 

Constructor injection is preferred for better testability.

You can annotate a class field directly with @Autowired. Spring will find the appropriate 
bean to inject based on the field's type.

```java
@Service
public class StudentServiceWithDb {
  @Autowired
  private StudentRepository studentRepository;

  @Autowired
  private StudentMapper studentMapper;

  // Other methods of StudentServiceWithDb
}
```

##### Setter Injection
AVOID THIS
{: .notice--danger}
Like field injection, it's less recommended than constructor injection for the same reasons—it can make testing and mocking dependencies more complex.

Annotate a setter method with @Autowired. Spring will call this method and pass the required dependency when 
initializing the bean.

```java
@Service
public class StudentServiceWithDb {
  private StudentRepository studentRepository;
  private StudentMapper studentMapper;

  //Setter Injection
  @Autowired
  public void setStudentRepository(StudentRepository studentRepository) {
    this.studentRepository = studentRepository;
  }

  @Autowired
  public void setStudentMapper(StudentMapper studentMapper) {
    this.studentMapper = studentMapper;
  }

  // Other methods of StudentServiceWithDb
}
```
##### Constructor Injection

Annotate a constructor with @Autowired. Spring will use this constructor to create 
the bean and pass the required dependencies as constructor arguments.

> Constructor injection is considered a best practice 

because it ensures that a bean is fully initialized when created.

```java
@Service
public class StudentServiceWithDb {

    private final StudentRepository studentRepository;
    private final StudentMapper studentMapper;

    @Autowired // Constructor Injection
    public StudentServiceWithDb(StudentRepository studentRepository, StudentMapper studentMapper) {
        this.studentRepository = studentRepository;
        this.studentMapper = studentMapper;
    }

    // Other methods of StudentServiceWithDb
}
```
Dependency Resolution: If there are multiple beans of the same type that can be injected, Spring will perform
dependency resolution based on the bean's name (if provided) or type.

You can also use `@Qualifier` in conjunction  
with `@Autowired` to specify which bean to inject if there are multiple candidates.

```java
public interface PaymentService {
    String processPayment();
}
```

The two implementations are

```java
@Service("creditCardService")
public class CreditCardPaymentService implements PaymentService{
    @Override
    public String processPayment() {
        return "Paid via credit card";
    }
}
```
```java
@Service("onlineBankingService")
public class OnlineBankingService implements PaymentService{
    @Override
    public String processPayment() {
        return "Paid via Online Banking";
    }
}
```
The use of `@Qualifier` 

```java
@RestController
@RequestMapping("/payment")
public class PaymentController {
    private PaymentService creditCardpaymentService;
    private PaymentService onlineBankingpaymentService;

    @Autowired
    public PaymentController(@Qualifier("creditCardService") PaymentService creditCardPaymentService,
                             @Qualifier("onlineBankingService") PaymentService onlineBankingpaymentService) {
        this.creditCardpaymentService = creditCardPaymentService;
        this.onlineBankingpaymentService = onlineBankingpaymentService;
    }
    // Other methods of PaymentController
}
```

# Sequence of execution

Postman/client -> Controller -> Service -> Repository -> Service -> Controller
{: .notice--info}

# Controller Vs RestController

Controller needs `@ResponseBody` with method name
```java
@Controller
@RequestMapping(method= RequestMethod.GET, path = "/health",
        produces = { "application/json", MediaType.APPLICATION_XML_VALUE})
public class HealthCheckController {
    @RequestMapping(path = "/check", method = RequestMethod.GET)
    public @ResponseBody String hello(){// ResponseBody Annotation is compulsory
        return "Health is Ok";
    }
}
```

# GET Request

```java
@RequestMapping(method = RequestMethod.GET, 
        path = "/student/{studentId}")
```
OR

```java
@GetMapping(value = "/student/{studentId}", 
        path = "/student/{studentId}",
        produces = { "application/json", MediaType.APPLICATION_XML_VALUE})
```

Between value and path attribute, value is commonly used to describe the path  

Shortened GetMapping
```java
@GetMapping(path="/getMapping")
```

### GetMapping returning a bean (JSON Response)
```java
@GetMapping(path="/getBean")
public HelloWorldReturnBean helloWorldReturnBean() {
    return new HelloWorldReturnBean("Hello World - From HelloWorldReturnBean");
}
```

### Path variable

http://localhost:8089/api/v0/hello-world/pathVariable/{var_name}
{: .notice--info}

Read the Path Variable with `@PathVariable` in the method parameter
```java
@GetMapping("/student/{studentId}")
public ResponseEntity<Student> getStudentById(@PathVariable Long studentId) {
    return ResponseEntity.ok(studentService.getStudentById(userId));
}
```
```java
@GetMapping(path = "/pathVariable/{var_name}")
public String helloWorldPathVariable(@PathVariable("var_name") String name) {
    return String.format("The Value returned is %s", name);
}
```

### RequestParam

/jpa/students/pagination?page_size=5&pageNo=1&sortBy=email
{: .notice--info}

Check the `required` and `defaultValue` arguments of RequestParam Annotation

```java
// Retrieve all users page by page
@GetMapping(path = "/students/pagination")
public List<Student> 
    retrieveAllUsersPagination(@RequestParam(defaultValue = "0") Integer pageNo,
                               @RequestParam(value = "page_size",required = false, defaultValue = "10") Integer pageSize,
                               @RequestParam(defaultValue = "id") String sortBy) {
        ...
}
```

### Validation 

[Validations in Detail](https://nitinkc.github.io/spring/microservices/spring-validations/)
{: .notice--danger}

##### Request Validation

At Class level, add `@Validated` annotation and at the `@Valid` at the parameter level

Check the `required` and `defaultValue` arguments of RequestParam Annotation

Simple validation at parameter level with simple class
```java
@RestController
@RequestMapping("/test") @Validated
public class ValidationController {

    @GetMapping("/email")
    public String testEmail(@Valid @Email(message = "Please provide a valid email address")
                            @RequestParam(value = "email") String email ,
                            @RequestParam(value = "greet", required = false, defaultValue = "No Val from Request") 
                            String greet,
                            @RequestParam(value = "count", required = false, defaultValue = "-1") Integer count) {

        StringBuilder sb= new StringBuilder();
        sb.append(email).append(" email OK").append("\nCount is ").append(count).append("\n").append(greet);
        return sb.toString();
    }
}
```

##### Response Validation

In the DTO Class (Using Lombok)

```java
@Data
public class StudentRequestBody {
    private int count;
    @JsonProperty("studentIds")//If the name in the request bofy differs from variable name
    private List<String> studentIdList;
    @Email(message = "Incorrect EmailID received from DB")
    private String emailId;
}
```

# POST Request

[POST Request in Detail](https://nitinkc.github.io/spring/microservices/POST-Requests/)
{: .notice--danger}

```java

@RequestMapping(method = RequestMethod.POST) OR
@PostMapping("/students")
```
Read the Request Body using `@RequestBody` in the method parameter into either a Map, for simple structures or a class for complex

### With Map as Request Body

if request body is like below, a map can be used
```json
{
  "values":["10","12.5","50","100"]
}
```

Curl Request

```shell
curl --location 'localhost:8090/student/db/studentIdsByMap' \
--header 'Content-Type: application/json' \
--data '{
    "values": ["1","2","3","4","5",""]
}'
```

```java
@PostMapping(path = "/studentIdsByMap",
            consumes = {MediaType.APPLICATION_JSON_VALUE},
            produces = {"application/json"})
public List<StudentDto> getStudentByIdsByMap(@RequestBody Map<String,List<Integer>> mapStudentIds){
        ...
}
```

### With Class as Request Body

```json
{
  "greeting":"Hi from postman.",
  "count":5,
  "studentIds": ["1","2","3","4","5"]
}
```
Curl Request

```shell
curl --location 'localhost:8090/student/db/studentIdsByClassName' \
--header 'Content-Type: application/json' \
--data '{
    "greeting":"Hi from postman.",
    "count":5,
    "studentIds": ["1","2","3","4","5"]
}'
```

Corresponding Java class to catch the request Body

```java
public class StudentRequestBody {
    private int count;
    @JsonProperty("studentIds")//If the name in the request body differs from variable name
    private List<String> studentIdList;
    private String greeting;
}
```
Controller
```java
@PostMapping(path = "/studentIdsByClassName",
            consumes = {MediaType.APPLICATION_JSON_VALUE},
            produces = {"application/json"})
public StudentDtoClass getStudentByIdsRequestBody(@RequestBody StudentRequestBody studentRequestBody){
        ...
}
```

# Service

For a single student Id, JPA's findById method can be utilized. It returns an Optional, so if in case the return is
a null Optional Class findById can be utilized.

### Return an Object

```java
Optional<Student> studentById = studentRepository.findById(studentId);//Method from JPA Repo, returns Optional
Student student = studentById.orElseGet(Student::new);//Return empty constructor if no data/Null
```

The supplier in orElseGet can be written in whichever way feels intuitive.
```java
Student student = studentById.orElseGet(Student::new);//Return empty constructor if no data/Null
//student = studentById.orElseGet(() -> new Student());
//student = studentById.orElseGet(() -> Student.builder().build());
```

##### Simple Mapper 

If the class structure of DAO Class is different from the DTO Class, then separate mappers or convertors can be written.

```java
StudentDto studentDto = studentMapper.convert(student);//Convertor/Mapper/Transformer
```
The convert method takes in a DAO Object and returns a DTO object

```java
@Component
public class StudentMapper {

    public StudentDto convert(Student studentById) {
        return StudentDto.builder()
                .fullName(studentById.getFirstName() + " " + studentById.getLastName())
                .city(studentById.getCityOfBirth())
                .sex(studentById.getGender())
                .university(studentById.getUniversity())
                .emailId(studentById.getEmail())//TODO: The email validation.
                .build();
    }
}
```

Over all the service class with method to return a single student object
```java
@Service
public class StudentServiceWithDb {
    @Autowired StudentRepository studentRepository;
    @Autowired StudentMapper studentMapper;

    public StudentDto getStudentById(int studentId) {
        Optional<Student> studentById = studentRepository.findById(studentId);//Method from JPA Repo, returns Optional
        Student student = studentById.orElseGet(Student::new);//Return empty constructor if no data/Null
        //student = studentById.orElseGet(() -> new Student());
        //student = studentById.orElseGet(() -> Student.builder().build());

        StudentDto studentDto = studentMapper.convert(student);//Convertor/Mapper/Transformer
        return studentDto;
    }
}
```

### Return a List of Object

The method that returns a List of objects, based on the multiple student id's passed can be written using the
`findAllByIds` method of JpaRepository Interface.

```java
List<Student> studentDetailsList = studentRepository.findAllById(studentIdList);
```
In order to convert the list of DAO objects to a list of DTO objects, the intuition could be of for loop

```java
 //Intuitive way
List<StudentDto> studentDtoList = new ArrayList<>();//Initialize the return array
for(Student s:studentDetailsList){
    StudentDto singleStudentDto = studentMapper.convert(s);
    studentDtoList.add(singleStudentDto);
}
```

But a better way of achieving this is the use of functional style of programming
```java
//Java 8
List<StudentDto> studentDtoList = studentDetailsList.stream()
        //.filter(Objects::nonNull)//Remove any null rows if needed
        .map(studentMapper::convert)
        .collect(Collectors.toList());
```

Finally, the overall method would be
```java
public List<StudentDto> getStudentByIds(List<Integer> studentIdList) {
    List<Student> studentDetailsList = studentRepository.findAllById(studentIdList);

    List<StudentDto> studentDtoList = studentDetailsList.stream()
            .map(studentMapper::convert)
            .collect(Collectors.toList());
    return studentDtoList;
}
```

# Mapping for DTO

##### Jackson Mapper
[Jackson Mapper in Detail](https://nitinkc.github.io/spring/microservices/jackson-mapper-details/)
{: .notice--danger}

##### Map Struct
[Map Struct in Detail](https://nitinkc.github.io/spring/microservices/mapstruct-mapper-details/)

The simple one is Jackson mapper, with lot of control 
```java
@JsonProperty("studentIds")//If the name in the request body differs from variable name
 private List<String> studentIdList;
```

Control other aspects of the DTO

* if empty values in the array is not needed
```java
@JsonInclude(JsonInclude.Include.NON_NULL)
@Data
public class Filters {
    @JsonProperty("treatmentDay")
    public String treatmentDay;
}
```

# Repository

Spring Data JAP is an implementation of Java Persistence API

# Custom Exceptions

Use `@ControllerAdvice` or `@RestControllerAdvice` for Global exception handling.

### Difference between `@ControllerAdvice` & `@RestControllerAdvice`
The primary difference is in the **type of responses** they handle. 
* @RestControllerAdvice is geared toward RESTful services, where responses are typically data-centric (e.g., JSON or 
XML),
* while @ControllerAdvice is used in 
traditional web applications, where responses often include both views and data.


### @ResponseStatus

Use `@ResponseStatus(HttpStatus.NOT_FOUND)` to denote the exception code

The custom exception class can extend Exception or RunTimeException. The `@ResponseStatus` of Global Exception class 
(The one with `@ControllerAdvice`) **takes precedence** if it's used in both
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

