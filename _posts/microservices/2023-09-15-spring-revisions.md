---
title:  "Spring Boot Revisions"
date:   2023-09-15 11:50:00
categories: Spring Microservices
tags: [Spring Microservices, CRUD]
toc: true
---

# Stereotype Annotations

@Component, @Controller, @Service, and @Repository 

Port used = 8089
```shell script
server.port=8089
```
1. HelloWorld using Request Mapping
```java
   @RequestMapping(method= RequestMethod.GET,path="/requestMapping")
```
http://localhost:8089/api/v0/hello-world/requestMapping

2. GetMapping
```java
@GetMapping(path="/getMapping")
```
http://localhost:8089/api/v0/hello-world/getMapping

3. GettMapping returning a bean (JSON Response)
```java
@GetMapping(path="/getBean")
public HelloWorldReturnBean helloWorldReturnBean() {
    return new HelloWorldReturnBean("Hello World - From HelloWorldReturnBean");
}
```
http://localhost:8089/api/v0/hello-world/getBean

4. Passing in a path variable in the GET request
```java
@GetMapping(path = "/pathVariable/{var_name}")
public String helloWorldPathVariable(@PathVariable("var_name") String name) {
    return String.format("The Value returned is %s", name);
}
```
http://localhost:8089/api/v0/hello-world/pathVariable/{var_name}

# URIs
Retrieve all Users - GET /users

Create a User - POST /users

Retrieve one User - GET /users/{id} -> /users/1

Delete a User - DELETE /users/{id} -> /users/1

Retrieve all posts for a User - GET /users/{id}/posts

Create a posts for a User - POST /users/{id}/posts

Retrieve details of a post - GET /users/{id}/posts/{post_id}


# GET Request

`@RequestMapping(method = RequestMethod.GET)` OR
`@GetMapping("/student/{studentId}")`

Read the Path Variable 
`@PathVariable` in the method parameter

```java
@GetMapping("/student/{studentId}")
public ResponseEntity<Student> getStudentById(@PathVariable Long studentId) {
    return ResponseEntity.ok(studentService.getStudentById(userId));
}
```

### Map model to Response and add return validation

### Add Validation to the Request

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


# POST Request

`@RequestMapping(method = RequestMethod.POST)` OR
`@PostMapping("/students")`

Read the Request Body 
`@RequestBody` in the method parameter


[POST Request](https://nitinkc.github.io/spring/microservices/POST-Requests/)


# Stereotype Annotations

> Basic philosophy : Conventions over configurations

```java
@Component 
@Controller 
@Service
@Repository
```

## Controller Vs RestController

Controller needs `@ResponseBody` with method name
```java
@Controller
@RequestMapping("/health")
public class HealthCheckController {
    @RequestMapping(path = "/check", method = RequestMethod.GET)
    public @ResponseBody String hello(){
        return "Health is Ok";
    }
}
```

```java
 @RequestMapping(path = "/requestMapping/{studentId}",
            produces = { "application/json", MediaType.APPLICATION_XML_VALUE,  MediaType.APPLICATION_PDF_VALUE})
public @ResponseBody StudentDto getStudentByIdRequestMapping(@PathVariable String studentId){
        ...
}
```

## Scans

Entity Scan vs

```java
@EntityScan(basePackages = {"com.learningJPA.dSpringDataRepository"
        ,"com.learningJPA.eTest.model"
        //,"com.learningJPA.hibernate.*"
}) 
```

What is this??
```java
@SpringBootApplication(
    scanBasePackages = {
        "com.test.package1",
        "com.test.service.security"
    },
    exclude = { JmxAutoConfiguration.class })
```

ComponentScan

```java
@ComponentScan(basePackages = {
        "com.test.animals", 
        "com.flowers"
})
```

## Autowired Dependency Injection

Eliminates the need of creating a new object and hence the need of constructors from the components

`StudentService studentService = new StudentService();`
```java
@Autowired
StudentService studentService;//Free to use studentService object within the class anywhere
```

# Mappings

### GetMapping

```java
@RequestMapping(method= RequestMethod.GET,path="/requestMapping")
```

```java
@GetMapping(
        value = "/{studentId}", 
        path = "/{studentId}",
        consumes = {MediaType.TEXT_PLAIN_VALUE, MediaType.APPLICATION_JSON_VALUE},
        produces = { "application/json", MediaType.APPLICATION_XML_VALUE, MediaType.APPLICATION_PDF_VALUE}
)
```

### Difference between PathVariable and RequestParam


##### Read the Path Variable

`@PathVariable` in the method parameter

```java
@GetMapping("/student/{studentId}")
public ResponseEntity<Student> getStudentById(@PathVariable Long studentId) {
    return ResponseEntity.ok(studentService.getStudentById(userId));
}
```

##### Reading via RequestParam

> ```javascript
> /jpa/students/pagination?pageSize=5&pageNo=1&sortBy=email
> ```

```java
// Retrieve all users page by page
@GetMapping(path = "/students/pagination")
public List<Student> 
    retrieveAllUsersPagination(@RequestParam(defaultValue = "0") Integer pageNo,
                                                @RequestParam(defaultValue = "10") Integer pageSize,
                                                @RequestParam(defaultValue = "id") String sortBy) {
        ...
}
```

### POST Mappings

Read the request body using `@RequestBody ` into either a Map, for simple structures or a class for complex

### With Map as Request Body

if request body is like below, a map can be used
```json
{
  "values":["10","12.5","50","100"]
}
```

```java
@PostMapping(path = "/studentIdsByMap",
            consumes = {MediaType.APPLICATION_JSON_VALUE},
            produces = {"application/json"})
public List<StudentDto> getStudentByIdsByMap(@RequestBody Map<String,List<Integer>> mapStudentIds){
        ...
}
```

Curl Request

```shell
curl --location 'localhost:8090/student/db/studentIdsByMap' \
--header 'Content-Type: application/json' \
--data '{
    "studentIds": ["1","2","3","4","5",""]
}'
```


### With Class as Request Body

```json
{
  "greeting":"Hi from postman.",
  "count":5,
  "studentIds": ["1","2","3","4","5"]
}
```

```java
@PostMapping(path = "/studentIdsByClassName",
            consumes = {MediaType.APPLICATION_JSON_VALUE},
            produces = {"application/json"})
public StudentDtoClass getStudentByIdsRequestBody(@RequestBody StudentRequestBody studentRequestBody){
        ...
}
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

```shell
curl --location 'localhost:8090/student/db/studentIdsByClassName' \
--header 'Content-Type: application/json' \
--data '{
    "greeting":"Hi from postman.",
    "count":5,
    "studentIds": ["1","2","3","4","5"]
}'
```

# Service

For a single student Id, JPA's findById method can be utilized. It returns an Optional, so if in case the return is
a null Optional Class findById can be utilized

```java
Optional<Student> studentById = studentRepository.findById(studentId);//Method from JPA Repo, returns Optional
Student student = studentById.orElseGet(Student::new);//Return empty constructor if no data/Null
```

The supplier in orElseGet can be rewritten in whichever way feels intuitive.
```java
Student student = studentById.orElseGet(Student::new);//Return empty constructor if no data/Null
//student = studentById.orElseGet(() -> new Student());
//student = studentById.orElseGet(() -> Student.builder().build());
```

If the class structure of DAO Class is different than the DTO Class, then separate mappers or convertors can be written.

The convert method takes in DAO Object and returns DTO object
```java
StudentDto studentDto = studentMapper.convert(student);//Convertor/Mapper/Transformer
```

Mapper of convertor can be written as

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

Over all the service class with method to return a single student object would look like
```java
@Service
public class StudentServiceWithDb {
    @Autowired
    StudentRepository studentRepository;
    @Autowired
    StudentMapper studentMapper;

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

The method that returns a List of objects, based on the multiple student id's passed can be written using the
findAllByIds method of JpaRepository Interface.

```java
List<Student> studentDetailsList = studentRepository.findAllById(studentIdList);
```
In order to convert the list of DAP objects to a list of DTO objects, the intuition could be of for loop like this

```java
 //Intuitive way
List<StudentDto> studentDtoList = new ArrayList<>();
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

# Simple Jackson Mapping

```java
@JsonProperty("studentIds")//If the name in the request body differs from variable name
 private List<String> studentIdList;
```


### Add Validation to the Request

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

# Custom Exceptions

Use `@ControllerAdvice` or `@RestControllerAdvice` for Global exception handling.

Use `@ResponseStatus(HttpStatus.NOT_FOUND)` to denote the exception code

The custom exception class can extend Exception or RunTimeException
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
public class ExceptionResponse {
    private String errorCode;
    private String errorMessage;
    private String requestedURI;
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
        ExceptionResponse error = new ExceptionResponse();
        error.setErrorMessage(exception.getMessage());
        error.setRequestedURI(request.getRequestURI());
        error.setErrorCode(ERR_122.getErrorCode()+" :: "+ERR_122.getErrorMessage());

        return error;
    }

    @ExceptionHandler(value = {DbDownException.class})
    @ResponseStatus(HttpStatus.NOT_FOUND)
    public @ResponseBody
    ExceptionResponse handleDbExceptions(
            StudentNotFoundException exception, final HttpServletRequest request) {
        ExceptionResponse error = new ExceptionResponse();
        error.setErrorMessage(exception.getMessage());
        error.setRequestedURI(request.getRequestURI());
        error.setErrorCode(ERR_123.getErrorCode()+" :: "+ERR_123.getErrorMessage());

        return error;
    }
}

```


