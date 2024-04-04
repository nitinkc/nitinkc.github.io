---
title:  "SpringBoot Reference"
date:   2023-09-15 11:50:00
categories: Spring Microservices
tags: [Spring Microservices, CRUD]
---
{% include toc title="Index" %}

# Stereotype Annotations

[All Annotations](https://springframework.guru/spring-framework-annotations/)
{: .notice--success}

Basic philosophy of Spring Boot : **Conventions over configurations**

**@Component**
* **Purpose**: Marks a class as a Spring component or bean.
* **Commonly Used in**: Utility classes, business logic classes, and other non-specialized components.

**@Controller** 
* **Purpose**: Marks a class as a Spring MVC controller.
* **Use Case**: Used for classes that handle HTTP requests in a Spring MVC web application.
* **Commonly Used in**: Classes that define request mappings, handle user input, and return views or data to the client.
  
**@Service**
* **Purpose**: Marks a class as a service or business logic component.
* **Use Case**: Typically used for classes that contain the business logic of the application.
* **Commonly Used in**: Service layer classes that encapsulate business rules, data processing, and interactions with 
  repositories or other services.

**@Repository**
* **Purpose**: Marks a class as a Spring Data repository.
* **Use Case**: Used for classes that interact with a database or external data source.
* **Commonly Used in**: Data access objects (DAOs) that perform CRUD (Create, Read, Update, Delete) operations on 
  entities.

## Config
[app.yml/app.props - Application Yaml settings](https://nitinkc.github.io/spring/microservices/spring-revisions/#application-yaml-settings)

Set a desired Port
```shell
server.port=8089
```

## Banner

[Spring Boot banner generator](https://springhow.com/spring-boot-banner-generator/)

For Ascii banner, put the ASCII Art in banner.txt in and it will be taken
[Sample file](https://github.com/nitinkc/spring-5-restful-web/blob/master/src/main/resources/banner.txt)

to turn off the banner
```yaml
spring:
  main:
    banner-mode: "off"
```
For image banner, put the logo.png file and

```yaml
spring:
  banner:
    image:
      location: logo.png
```

## Initial Data Setup

keep the sql script in the resources folder by the name `data.sql`

[Sample Data file](https://github.com/nitinkc/spring-data-jpa/blob/master/src/main/resources/data.sql)

# Scans

**Component Scan** :

By default, the package containing the main method is scanned. In addition to it, to scan other
packages, following annotation is used.

```java
@ComponentScan(basePackages = {"com.spring5.concepts","com.spring5.services"})
``` 


`@ComponentScan` is used to specify the packages that Spring should scan to discover Spring-managed components like 
beans, controllers, services, etc.

```java
@ComponentScan(basePackages = {
        "com.test.animals", 
        "com.flowers"
})
```

**Entity Scan** :

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

**SpringBootApplication ScanBasePackages:**

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

[https://nitinkc.github.io/spring/microservices/dependency-injection-concepts/](https://nitinkc.github.io/spring/microservices/dependency-injection-concepts/)
{: .notice--success}

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


# Sequence of execution

Postman/browser/client -> Controller -> Service -> Repository -> Service -> Controller
{: .notice--info}

# REST APIs

[https://nitinkc.github.io/microservices/Idempotence-HTTP-methods/#designing-restful-uris](https://nitinkc.github.io/microservices/Idempotence-HTTP-methods/#designing-restful-uris)
{: .notice--success}

```shell
Retrieve all Users - GET /users
Create a User - POST /users
Retrieve one User - GET /users/{id} -> /users/1
Delete a User - DELETE /users/{id} -> /users/1
Retrieve all posts for a User - GET /users/{id}/posts
Create a posts for a User - POST /users/{id}/posts
Retrieve details of a post - GET /users/{id}/posts/{post_id}
```

# Controller Vs RestController

`@Controller` on a Controller class needs `@ResponseBody` with method name
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

[https://nitinkc.github.io/spring/microservices/GET-rest-calls/](https://nitinkc.github.io/spring/microservices/GET-rest-calls/)
{: .notice--success}

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

Between `value` and `path` attribute, **value** is commonly used to describe the path  

**Shortened GetMapping**
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

[Path Variable vs Request Param](https://nitinkc.github.io/spring/microservices/spring-request-parameter/)
{: .notice--success}

### Validation 

[Validations in Detail](https://nitinkc.github.io/spring/microservices/spring-validations/)
{: .notice--success}

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
    @JsonProperty("studentIds")//If the name in the request body differs from variable name
    private List<String> studentIdList;
    @Email(message = "Incorrect EmailID received from DB")
    private String emailId;
}
```

# POST Request

[POST Request in Detail](https://nitinkc.github.io/spring/microservices/POST-Requests/)
{: .notice--success}

```java
@RequestMapping(method = RequestMethod.POST) 
//OR
@PostMapping("/students")
```

### With Map as Request Body

if request body is like below, a map can be used
```json
{
  "values":["10","12.5","50","100"]
}
```
**Curl Request**
```shell
curl --location 'localhost:8090/student/db/studentIdsByMap' \
--header 'Content-Type: application/json' \
--data '{
    "values": ["1","2","3","4","5",""]
}'
```
Read the Request Body using `@RequestBody` in the method parameter into either a Map, for simple structures or a class for complex

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
**Curl Request**
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
Controller with **@RequestBody**
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
{: .notice--success}

##### Map Struct
[Map Struct in Detail](https://nitinkc.github.io/spring/microservices/mapstruct-mapper-details/)
{: .notice--success}

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

Spring Data JPA is an implementation of Java Persistence API

# Custom Exceptions

[Java Exceptions](https://nitinkc.github.io/java/exceptions/)
{: .notice--success}

[Spring Exceptions](https://nitinkc.github.io/spring/microservices/spring-exception-404/)
{: .notice--success}

Use `@ControllerAdvice` or `@RestControllerAdvice` for Global exception handling.

### Difference between `@ControllerAdvice` & `@RestControllerAdvice`
The primary difference is in the **type of responses** they handle. 
* @RestControllerAdvice is geared toward RESTful services, where responses are typically data-centric (e.g., JSON or 
XML),
* while @ControllerAdvice is used in 
traditional web applications, where responses often include both views and data.

### HikariCP
HikariCP, often referred to simply as Hikari, is a popular and high-performance connection pool library for Java applications.

Connection pooling is a technique used to efficiently manage and reuse database connections in applications that interact with a relational
```yml
spring.jpa.properties.hibernate.default_schema="chinookMusic"
spring.datasource.url = jdbc:postgresql://localhost:5432/mydb

# or combined 
spring.datasource.url=jdbc:postgresql://postgres:5432/mydb?currentSchema=test
```

# Read Environment properties

Use the Environment dependency
```java
@Autowired 
private Environment environment;

int portNumber = Integer.parseInt(environment.getProperty("server.port"));

```

Another method by @Value Annotation

```java
@Value("${custom.value}")
private String customVal;
```

# Rest Template
Refer the following page for details
[Rest Template](https://nitinkc.github.io/microservices/rest-template/)

### Application Yaml settings
{% gist nitinkc/5dd5f552cc1033347f2868ea6e6b7ad7 %}
