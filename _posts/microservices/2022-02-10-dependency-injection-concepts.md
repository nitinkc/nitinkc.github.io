---
# layout: static
title:  "Dependency Injection"
date:   2022-02-10 20:55:00
categories: Spring Microservices
tags: [Spring Microservices, Spring Boot]
---
{% include toc title="Index" %}

# Dependency Injection Concepts using Spring 5

**IOC(Inversion Of Control)**

Giving control to the container to get instance of object is called Inversion of Control. 
* instead of you are creating object using new operator, let the container do that for you.

**DI(Dependency Injection)**:  Way of injecting properties to an object is called Dependency injection.

We have three types of Dependency injection
* Constructor Injection
* Setter/Getter Injection
* Interface Injection

Spring support only Constructor Injection and Setter/Getter Injection.

### Dependency Injection is done in 3 ways

1. By class properties - least preferred 
  * Using private properties is <span style="color:red">**EVIL**</span>
2. By Setters - Area of much debate
	
```java
private GreetingService greetingService;
@Autowired
//@Qualifier("setterGreetingService")
public void setGreetingService(@Qualifier("setterGreetingService") GreetingService greetingService) {
    this.greetingService = greetingService;
}
```

3. By Constructor - Most Preferred
```java
private GreetingService greetingService;
//Constructor, With Spring 5 no need to explicitly mention @Autowired, but its a good practice
public A3ConstructorInjectedController(GreetingService greetingService) {
    this.greetingService = greetingService;
}
```


#### DI via Interfaces is highly preferred
* Allows runtime to decide implementation to inject
* Follows Interface Segregation Principle of SOLID
* Also, makes your code more testable

**Types of Injection:**

##### Field Injection
AVOID THIS
{: .notice--danger}
it's generally not recommended because it makes testing and mocking dependencies more challenging.

**Constructor injection is preferred for better testability.**

You can annotate a class field directly with `@Autowired`. Spring will find the appropriate
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

`@Primary` - Multiple beans of the same type and one is intended to go in by default 
           
`@Profile` - making a profile active from the application.properties

default profile is added 

`@Profile({"en","default"})`
