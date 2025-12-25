---
categories: Microservices
date: 2023-09-15 11:50:00
tags:
- Spring Boot
- Reference
- Documentation
- Guide
title: SpringBoot Reference
---

{% include toc title="Index" %}

# Concepts

## Loose Coupling

Loose coupling refers to designing a system where components are minimally
dependent on each other.

- This allows for easier modification, testing, and maintenance because changes
  in one component have little to no impact on others.
- By Autowiring, we achieve loose coupling.

> By using `new` keyword (instantiating an obejct), we **tightly couple** the
> dependency which is not good

- **Tightly Coupled:**
  ```java
  public class UserService {
      private final UserRepository userRepository = new UserRepository(); // Directly creating a dependency
      // Methods using userRepository
  }
  ```

- **Loosely Coupled (using Dependency Injection):**
  ```java
  public class UserService {
      private final UserRepository userRepository;
      // Constructor Injection
      public UserService(UserRepository userRepository) {
          this.userRepository = userRepository;
      }
      // Methods using userRepository
  }
  ```

Here, `UserService` is loosely coupled with `UserRepository` because it doesn’t
create the dependency itself.
Instead, `UserRepository` is injected into `UserService`, making it easier to
swap out `UserRepository` implementations.

## Inversion of Control

Instead of the Class taking responsibility of creating the object, the framework
manages it for you

- the control of **object creation** and **dependency management** is 
**_inverted_** from the application code to a framework.
- The framework manages the lifecycle and interactions of objects.

## Dependency Injection

Dependency Injection (DI) is a design pattern used to **implement IoC** (
Inversion of Control).

- In DI, the framework (like Spring) handles the **creation and injection of
  dependencies** or **bean instantiation beans and wiring dependencies**,
  rather than the classes managing their own dependencies.

# Stereotype Annotations

[All Annotations](https://springframework.guru/spring-framework-annotations/)
{: .notice--success}

> Basic philosophy of Spring Boot : **Conventions over configurations**

**@Component**

* **Purpose**: Marks a class as a Spring component or bean.
* **Commonly Used in**: Utility classes, business logic classes, and other
  non-specialized components.

**@Controller**

* **Purpose**: Marks a class as a Spring MVC controller.
* **Use Case**: Used for classes that handle HTTP requests in a Spring MVC web
  application.
* **Commonly Used in**: Classes that define request mappings, handle user input,
  and return views or data to the client.

**@Service**

* **Purpose**: Marks a class as a service or business logic component.
* **Use Case**: Typically used for classes that contain the business logic of
  the application.
* **Commonly Used in**: Service layer classes that encapsulate business rules,
  data processing, and interactions with
  repositories or other services.

**@Repository**

* **Purpose**: Marks a class as a Spring Data repository.
* **Use Case**: Used for classes that interact with a database or external data
  source.
* **Commonly Used in**: Data access objects (DAOs) that perform CRUD (Create,
  Read, Update, Delete) operations on
  entities.

# Config

Set a desired Port

```shell
server.port=8089
```

### Application Yaml settings

{% gist nitinkc/5dd5f552cc1033347f2868ea6e6b7ad7 %}

> Good Practice : Design application configuration using
`@ConfigurationProperties` to ensure Type Safety

```yaml
myConfig:
  flag: true
  message: "From YAML"
  number: 100
```

Type Safety can be ensured with this

```java
@Component
@ConfigurationProperties("myConfig")
public class MyConfiguration {
    private boolean flag;
    private String message;
    private int number;
```

# Banner

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

# Springboot Startup process
[https://nitinkc.github.io/spring/microservices/springboot-startup/](https://nitinkc.github.io/spring/microservices/springboot-startup/)

# Initial Data Setup

keep the sql script in the resources folder by the name `data.sql`

[Sample Data file](https://github.com/nitinkc/spring-data-jpa/blob/master/src/main/resources/data.sql)

# Scans

## Component Scan

By default, the package containing the main method is scanned.

- `@ComponentScan` is used to specify the packages that Spring should scan to
  discover Spring-managed components like
  beans, controllers, services, etc.

```java
@ComponentScan(basePackages = {"com.spring5.concepts",
        "com.spring5.services"
        "com.test.animals",
        "com.flowers"
})
```

## Entity Scan

`@EntityScan` is specific to Spring Data JPA.

* It's used to specify the packages where JPA entities are located.
* This is important because Spring Data JPA needs to know where the entity
  classes are in order to create
  repositories and perform CRUD operations.

```java
@EntityScan(basePackages = {"com.learningJPA.dSpringDataRepository"
        ,"com.learningJPA.eTest.model"
        //,"com.learningJPA.hibernate.*"
}) 
```

## SpringBootApplication ScanBasePackages

`@SpringBootApplication` is a meta-annotation that combines several annotations,
including `@ComponentScan`.

* `scanBasePackages` within `@SpringBootApplication` allows you to specify the
  base packages to scan for Spring
  components.
* used in the main application class.
* It also scans the default package where the main application class is located.
* exclude argument is used to exclude specific auto-configurations, which means
  that Spring Boot won't automatically
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

### Autowiring

- byType
- byName
- constructor - similar to byType, but through constuctor

[https://nitinkc.github.io/spring/microservices/dependency-injection-concepts/#Autowiring](https://nitinkc.github.io/spring/microservices/dependency-injection-concepts/#Autowiring)

Eliminates the need to create a new object and hence the need of constructors
from the components
`StudentService studentService = new StudentService();`

```java
@Autowired
StudentService studentService;//Free to use studentService object within the class anywhere
```

`@Autowired`  used for automatic dependency injection.

- Spring should find the matching bean and wire the dependency

**Dependency injection** is a design pattern in which objects are **provided**
with their dependencies (i.e., the
objects they need to collaborate with) rather than creating those dependencies
themselves.

**Automatic Injection**: When you annotate a field, setter method, or
constructor with `@Autowired`, Spring will
automatically inject the required dependency (another Spring bean) at runtime.

### Constructor vs Setter Injection

- Constructor Injection for Mandatory Dependencies
- Setter Injection for Optional Dependencies

### Lombok
To use the `@RequiredArgsConstructor` annotation. Mark the fields you want to
include in the constructor as `final` or annotate them with `@NonNull`.

```java
@RequiredArgsConstructor
public class UserService {
    private final UserRepository userRepository;
```


# Sequence of execution

```
Postman/browser/client -> Controller -> Service -> Repository -> Service -> Controller
```

# REST APIs

- Retrieve all Users - GET `/users`
- Create a User - POST `/users`
- Retrieve one User - GET `/user/{id}` -> `/user/1`
- Delete a User - DELETE `/user/{id}` -> `/user/1`
- Retrieve all posts for a User - GET `/user/{id}/posts`
- Create a posts for a User - POST `/user/{id}/posts`
- Retrieve details of a post - GET `/user/{id}/posts/{post_id}`

## Best Practices

- Use Plurals

[https://nitinkc.github.io/microservices/Idempotence-HTTP-methods/#designing-restful-uris](https://nitinkc.github.io/microservices/Idempotence-HTTP-methods/#designing-restful-uris)
{: .notice--success}

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

Between `value` and `path` attribute, **value** is commonly used to describe the
path

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

- At Class level, add `@Validated` annotation and at the `@Valid` at the
  parameter level
- Check the `required` and `defaultValue` arguments of RequestParam Annotation

```java
@RestController
@RequestMapping("/test") 
@Validated
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

**Curl Request**

```shell
curl --location 'localhost:8090/student/db/studentIdsByMap' \
--header 'Content-Type: application/json' \
--data '{
    "values": ["10","12.5","50","100"]
}'
```

Read the Request Body using `@RequestBody` in the method parameter into either a
Map, for simple structures or a class for complex

```java
@PostMapping(path = "/studentIdsByMap",
            consumes = {MediaType.APPLICATION_JSON_VALUE},
            produces = {"application/json"})
public List<StudentDto> getStudentByIdsByMap(@RequestBody Map<String,List<Integer>> mapStudentIds){
        ...
}
```

### With Class as Request Body

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

Controller with **`@RequestBody`**

```java
@PostMapping(path = "/studentIdsByClassName",
            consumes = {MediaType.APPLICATION_JSON_VALUE},
            produces = {"application/json"})
public StudentDtoClass getStudentByIdsRequestBody(@RequestBody StudentRequestBody studentRequestBody){
        ...
}
```

# Service

For a single student Id, JPA's findById method can be utilized. It returns an
Optional, so if in case the return is
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

If the class structure of DAO Class is different from the DTO Class, then
separate mappers or convertors can be written.

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

The method that returns a List of objects, based on the multiple student id's
passed can be written using the
`findAllByIds` method of JpaRepository Interface.

```java
List<Student> studentDetailsList = studentRepository.findAllById(studentIdList);
```

In order to convert the list of DAO objects to a list of DTO objects, the
intuition could be of for loop

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

Use `@ControllerAdvice` or `@RestControllerAdvice` for Global exception
handling.

### Difference between `@ControllerAdvice` & `@RestControllerAdvice`

The primary difference is in the **type of responses** they handle.

* @RestControllerAdvice is geared toward RESTful services, where responses are
  typically data-centric (e.g., JSON or
  XML),
* while @ControllerAdvice is used in
  traditional web applications, where responses often include both views and
  data.

### HikariCP

HikariCP, often referred to simply as Hikari, is a popular and high-performance
connection pool library for Java applications.

Connection pooling is a technique used to efficiently manage and reuse database
connections in applications that interact with a relational

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

# CommandLineRunner

[https://nitinkc.github.io/spring/microservices/CommandLineRunner/](https://nitinkc.github.io/spring/microservices/CommandLineRunner/)

```java
@Component
@Slf4j
@RequiredArgsConstructor
@Order(value = 1)
@ConditionalOnExpression("${dateExpiration:false}")
public class RutWhileBooting implements CommandLineRunner {

    private final LicenseService licenseService;
    @Override
    public void run(String... args) throws Exception {
        log.info("Starting Runner : ExpiryDate");
        //Do processing
        licenseService.runJob();
    }
}
```

# Scheduling a Job

[https://nitinkc.github.io/spring/microservices/spring-scheduler/](https://nitinkc.github.io/spring/microservices/spring-scheduler/)
use `@EnableScheduling` on the application main class

```java
@Component
@AllArgsConstructor
public class DailyTaskScheduler {
    private final MyService myService;

    @Scheduled(cron = "0 0 0 * * *") // Executes at midnight every day
    //@Scheduled(fixedRate = 5000) // Executes every 5 seconds (5000 milliseconds) for testing
    public void runDailyTask() {
        myService.runJob();
    }
```

# Spring Boot Actuator

## Monitoring

- /env, /metrics, /trace, /dump
- /beans, / autoconfig, /configprops, /mappings

## Metric logging - Prometheus and micrometer

[Prometheus and micrometer](https://nitinkc.github.io/spring/microservices/Prometheus-micrometer/)

# Design Patterns in Spring

- Front Controller - Dispatcher Servlet
- Prototype - Beans
- Dependency Injection
- Factory Pattern - Bean Factory & Application Context
- Template Method - org.springframework.web.servlet.mvc.AbstractController

# Aspect Oriented Programming - AOP

[https://nitinkc.github.io/spring/microservices/spring-aop/](https://nitinkc.github.io/spring/microservices/spring-aop/)


# Bean Scope
[https://nitinkc.github.io/microservices/spring-beans/#bean-scope](https://nitinkc.github.io/microservices/spring-beans/#bean-scope)

# Spring Security

[Spring Security](https://nitinkc.github.io/spring/microservices/spring-security-concepts/)
{: .notice--success}

Spring Security is a powerful and highly customizable authentication and access-control framework. It is the de-facto standard for securing Spring-based applications.

## Key Concepts

- **Authentication**: The process of verifying the identity of a user, device, or system. It answers the question, "Who are you?".
- **Authorization**: The process of determining whether an authenticated user has permission to access a specific resource or perform a particular action. It answers the question, "What are you allowed to do?".
- **Principal**: The currently authenticated user. It can be represented as an object within Spring Security's `SecurityContext`.
- **GrantedAuthority**: Represents a permission granted to the principal. It is typically expressed as a role (e.g., `ROLE_ADMIN`, `ROLE_USER`).
- **SecurityContextHolder**: Provides access to the `SecurityContext`, which holds the `Authentication` object and other security-related information.

## Configuration

Spring Security can be configured using a `SecurityFilterChain` bean. This is the most common way to configure security in a Spring Boot application.

```java
@Configuration
@EnableWebSecurity
public class SecurityConfig {

    @Bean
    public SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
        http
            .authorizeHttpRequests(authorize -> authorize
                .requestMatchers("/public/**").permitAll()
                .requestMatchers("/admin/**").hasRole("ADMIN")
                .anyRequest().authenticated()
            )
            .formLogin(withDefaults());
        return http.build();
    }

    @Bean
    public UserDetailsService userDetailsService() {
        UserDetails user = User.withDefaultPasswordEncoder()
            .username("user")
            .password("password")
            .roles("USER")
            .build();
        UserDetails admin = User.withDefaultPasswordEncoder()
            .username("admin")
            .password("password")
            .roles("ADMIN")
            .build();
        return new InMemoryUserDetailsManager(user, admin);
    }
}
```

In this example:
- Requests to `/public/**` are permitted for everyone.
- Requests to `/admin/**` are only allowed for users with the `ADMIN` role.
- All other requests require authentication.
- A form-based login is enabled with default settings.
- An in-memory user store is configured with two users: `user` and `admin`.

## Annotations

- **`@EnableWebSecurity`**: Enables Spring Security's web security support and provides the Spring MVC integration.
- **`@EnableMethodSecurity`**: Enables method-level security.
- **`@PreAuthorize`**: Used to secure methods with a SpEL (Spring Expression Language) expression. The method will only be invoked if the expression evaluates to `true`.
- **`@PostAuthorize`**: Allows for authorization logic to be executed after the method has been invoked.
- **`@Secured`**: A simpler annotation for role-based security. For example, `@Secured("ROLE_ADMIN")`.

# Reactive Programming (Spring WebFlux)

[Reactive Programming with Spring WebFlux](https://nitinkc.github.io/spring/microservices/spring-webflux-reactive/)
{: .notice--success}

Spring WebFlux is a fully non-blocking, reactive web framework for building modern, scalable applications. It is an alternative to Spring MVC and is built on top of Project Reactor.

## Key Concepts

- **Reactive Streams**: A standard for asynchronous stream processing with non-blocking backpressure. Key interfaces are `Publisher`, `Subscriber`, `Subscription`, and `Processor`.
- **Mono**: A `Publisher` that emits 0 or 1 element. Represents a single, asynchronous value or an empty result.
  - `Mono<User> findUserById(String id);`
- **Flux**: A `Publisher` that emits 0 to N elements. Represents a sequence of asynchronous values.
  - `Flux<User> findAllUsers();`
- **Backpressure**: A mechanism that allows a `Subscriber` to control the rate at which a `Publisher` produces data, preventing the `Subscriber` from being overwhelmed.

## WebFlux vs. Spring MVC

| Feature           | Spring MVC (Blocking)                               | Spring WebFlux (Non-Blocking)                             |
|-------------------|-----------------------------------------------------|-----------------------------------------------------------|
| **Thread Model**  | Thread-per-request                                  | Event-loop model (few threads handle many requests)       |
| **Dependencies**  | `spring-boot-starter-web`                           | `spring-boot-starter-webflux`                             |
| **API Style**     | Imperative, synchronous (`User`, `List<User>`)      | Functional, reactive (`Mono<User>`, `Flux<User>`)          |

# Advanced Testing

[Advanced Testing in Spring Boot](https://nitinkc.github.io/spring/microservices/spring-advanced-testing/)
{: .notice--success}

Spring Boot provides a rich set of testing utilities to write comprehensive unit, integration, and end-to-end tests.

## Test Slices

Test slices allow you to test a specific layer or "slice" of your application in isolation. This is faster than loading the entire application context.

- **`@WebMvcTest`**: For testing the web layer (controllers) without the full application context. It auto-configures `MockMvc`.
  ```java
  @WebMvcTest(UserController.class)
  public class UserControllerTest {
      @Autowired
      private MockMvc mockMvc;

      @MockBean
      private UserService userService;

      @Test
      void shouldReturnUser() throws Exception {
          given(userService.getUserById("1")).willReturn(new User("Nitin", "nitin@test.com"));
          mockMvc.perform(get("/users/1"))
              .andExpect(status().isOk())
              .andExpect(jsonPath("$.name").value("Nitin"));
      }
  }
  ```
- **`@DataJpaTest`**: For testing the persistence layer (JPA repositories). It uses an in-memory database by default and rolls back transactions after each test.
  ```java
  @DataJpaTest
  public class UserRepositoryTest {
      @Autowired
      private TestEntityManager entityManager;

      @Autowired
      private UserRepository userRepository;

      @Test
      void shouldFindUserByUsername() {
          User user = new User("Nitin", "nitin@test.com");
          entityManager.persist(user);
          entityManager.flush();

          Optional<User> found = userRepository.findByUsername("Nitin");
          assertThat(found).isPresent();
          assertThat(found.get().getEmail()).isEqualTo("nitin@test.com");
      }
  }
  ```
- **`@JsonTest`**: For testing JSON serialization and deserialization.

## Testcontainers

Testcontainers is a Java library that provides lightweight, throwaway instances of common databases, Selenium web browsers, or anything else that can run in a Docker container. This is ideal for true integration testing.

- **Dependency**: Add `org.testcontainers:junit-jupiter` and the specific container module (e.g., `postgresql`).
- **Usage**:
  ```java
  @SpringBootTest
  @Testcontainers
  class UserServiceIntegrationTest {
      @Container
      static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:13-alpine");

      @DynamicPropertySource
      static void configureProperties(DynamicPropertyRegistry registry) {
          registry.add("spring.datasource.url", postgres::getJdbcUrl);
          registry.add("spring.datasource.username", postgres::getUsername);
          registry.add("spring.datasource.password", postgres::getPassword);
      }

      @Autowired
      private UserService userService;

      @Test
      void testWithRealDatabase() {
          // Your integration test logic here
      }
  }
  ```

# Resilience and Fault Tolerance

[Resilience with Resilience4J](https://nitinkc.github.io/spring/microservices/resilience4j-spring-boot/)
{: .notice--success}

In distributed systems, services can fail. Resilience patterns help your application gracefully handle such failures. Resilience4J is a lightweight, easy-to-use fault tolerance library inspired by Netflix Hystrix.

## Key Patterns

- **Circuit Breaker**: Prevents repeated calls to a failing service. After a certain number of failures, the circuit "opens," and all subsequent calls fail immediately (or are redirected to a fallback) for a configured duration. This gives the failing service time to recover.
  - **States**: `CLOSED` (calls allowed), `OPEN` (calls fail-fast), `HALF_OPEN` (limited calls to check recovery).
- **Retry**: Automatically re-invokes a failed operation. Useful for transient errors like temporary network glitches.
- **Bulkhead**: Limits the number of concurrent calls to a specific service, preventing one slow service from exhausting all resources and causing cascading failures.
- **Rate Limiter**: Controls the rate of requests to a service (e.g., 100 requests per second).
- **Time Limiter**: Sets a timeout for asynchronous operations.

## Example with Circuit Breaker

1.  **Dependencies**: Add `spring-cloud-starter-circuitbreaker-resilience4j`.
2.  **Configuration** (`application.yml`):
    ```yaml
    resilience4j.circuitbreaker:
      instances:
        myApiService:
          registerHealthIndicator: true
          slidingWindowSize: 10
          minimumNumberOfCalls: 5
          permittedNumberOfCallsInHalfOpenState: 3
          automaticTransitionFromOpenToHalfOpenEnabled: true
          waitDurationInOpenState: 5s
          failureRateThreshold: 50
          eventConsumerBufferSize: 10
    ```
3.  **Usage in Code**:
    ```java
    @Service
    public class MyApiService {

        @CircuitBreaker(name = "myApiService", fallbackMethod = "fallback")
        public String fetchData() {
            // Call to an external, potentially failing service
            return restTemplate.getForObject("http://external-api/data", String.class);
        }

        public String fallback(Throwable t) {
            // Return a default value or a cached response
            return "Fallback data";
        }
    }
    ```

# Database Migration

[Database Migration with Flyway](https://nitinkc.github.io/spring/microservices/flyway-database-migration/)
{: .notice--success}

Database migration tools like Flyway and Liquibase help you version-control your database schema, making it easy to evolve your database structure in a consistent and automated way.

## Why Use It?

- **Version Control for DB**: Treat your schema changes like code.
- **Automation**: Apply schema changes automatically on application startup.
- **Consistency**: Ensures all environments (dev, test, prod) are using the same schema version.
- **Rollbacks**: Simplifies the process of reverting to a previous schema state (more supported in Liquibase).

## Flyway

Flyway is a popular open-source database migration tool that favors simplicity and convention over configuration.

1.  **Dependency**: Add `org.flywaydb:flyway-core`.
2.  **SQL Scripts**: Create SQL migration scripts in `src/main/resources/db/migration`. The naming convention is crucial: `V<VERSION>__<DESCRIPTION>.sql`.
    - `V1__create_user_table.sql`
    - `V2__add_email_to_user.sql`
    ```sql
    -- V1__create_user_table.sql
    CREATE TABLE users (
        id BIGINT PRIMARY KEY,
        username VARCHAR(255) NOT NULL
    );
    ```
    ```sql
    -- V2__add_email_to_user.sql
    ALTER TABLE users ADD COLUMN email VARCHAR(255);
    ```
3.  **Execution**: On startup, Spring Boot will automatically detect Flyway and run any new migration scripts. Flyway uses a `flyway_schema_history` table in your database to track which migrations have already been applied.

## Liquibase

Liquibase is another powerful migration tool that uses XML, YAML, or JSON changelogs instead of pure SQL, which can make it more database-agnostic.

- **Changelog File**: You define changesets in a master changelog file.
- **Changesets**: Each changeset is an atomic unit of change, identified by an `id` and `author`.

# Containerization & Cloud-Native

[Containerizing Spring Boot with Docker](https://nitinkc.github.io/spring/microservices/docker-spring-boot/)
{: .notice--success}

Containerization, particularly with Docker, is the standard for packaging and deploying modern applications. Cloud-native practices enable applications to be scalable, resilient, and manageable in dynamic environments like Kubernetes.

## Docker

Docker allows you to package your application and its dependencies into a standardized unit called a container.

### Dockerfile

A `Dockerfile` is a script containing instructions to build a Docker image.

```dockerfile
# Use an official OpenJDK runtime as a parent image
FROM openjdk:17-jdk-slim

# Set the working directory in the container
WORKDIR /app

# Copy the fat jar into the container at /app
COPY target/my-app-0.0.1-SNAPSHOT.jar app.jar

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Run the jar file
ENTRYPOINT ["java", "-jar", "app.jar"]
```

### Multi-Stage Builds

A multi-stage build is a best practice that helps keep your final image small and secure by separating the build environment from the runtime environment.

```dockerfile
# --- Build Stage ---
FROM maven:3.8.5-openjdk-17 AS build
WORKDIR /source
COPY . .
RUN mvn clean package -DskipTests

# --- Runtime Stage ---
FROM openjdk:17-jdk-slim
WORKDIR /app
COPY --from=build /source/target/*.jar app.jar
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]
```

## Cloud-Native Best Practices

- **Configuration Management**: Externalize configuration using ConfigMaps in Kubernetes or a dedicated config server (like Spring Cloud Config) instead of baking it into the image.
- **Health Checks**: Implement liveness and readiness probes (`/actuator/health/liveness`, `/actuator/health/readiness`). Kubernetes uses these to know if your application is running correctly and ready to receive traffic.
- **Graceful Shutdown**: Ensure your application handles `SIGTERM` signals to shut down gracefully, finishing in-flight requests and releasing resources. Spring Boot does this by default.
- **Stateless Services**: Design your services to be stateless. State should be stored in an external database or cache (like Redis or a distributed database). This allows you to scale your application horizontally with ease.
- **Distributed Tracing**: Use tools like Zipkin or Jaeger to trace requests as they travel across multiple microservices, which is essential for debugging in a distributed system.
- **Changesets**: Each changeset is an atomic unit of change, identified by an `id` and `author`.
            return "Fallback data";
        }
    }
    ```
          // Your integration test logic here
      }
  }
  ```
| **API Style**     | Imperative, synchronous (`User`, `List<User>`)      | Functional, reactive (`Mono<User>`, `Flux<User>`)          |
- **`@Secured`**: A simpler annotation for role-based security. For example, `@Secured("ROLE_ADMIN")`.