---
categories:
- Microservices
date: 2024-09-12 16:00:00
tags:
- Spring Boot
title: Aspect Oriented Programming (AOP)
---

{% include toc title="Index" %}

Aspect-Oriented Programming (AOP) in Spring Boot is used to separate **cross-cutting concerns (like logging exceptions)**
from the business logic of an application.

Cross-cutting concerns are aspects of a program that affect multiple modules,
such as logging, security, and transaction management.

**Key Concepts**

# Aspect:

A module that encapsulates a cross-cutting concern.
It defines the code that should be executed at specific points in the
application.

# Join Point:

A point during the execution of the application where an aspect can be applied.
Examples include method execution, object instantiation, etc.

# Advice:

The **action** taken (method) by an aspect at a join point. There are several
types of advice:

- `Before`: Executes before the join point.
- `After`: (finally) advice - Always executed. Executes after the join point,
  regardless of the outcome.
- `After Returning`: Executes after the join point if it completes normally.
- `After Throwing`: Executes if the join point throws an exception.
- `Around`: Most powerful - Surrounds the join point, allowing you to modify its
  execution.

# Pointcut:

An **expression** that specifies where advice should be applied. It defines
which join points are matched by the advice.

# Weaving:

The process of integrating aspects into the codebase.
This can happen at various times, such as at compile-time, load-time, or
runtime.

# Interceptors
interceptors are components that allow you to **insert behavior** `before, after, or around` method 
executions or other `join points` (like field access or object construction) without modifying the actual code of those methods.

- Interceptors are a type of advice in AOP. 
- They are used to intercept the execution of a method or process and apply cross-cutting concerns such as:
  - Logging
  - Security checks
  - Transaction management
  - Performance monitoring
  - Caching

### How Interceptors Work
Interceptors are typically used in "around" advice, which means they can:
- Execute before the target method
- Optionally proceed to the target method
- Execute after the target method

This gives them full control over the method execution.

```java
@Around("execution(* com.example.service.*.*(..))")
public Object logExecutionTime(ProceedingJoinPoint joinPoint) throws Throwable {
    long start = System.currentTimeMillis();
    Object result = joinPoint.proceed(); // Proceed to the actual method
    long duration = System.currentTimeMillis() - start;
    System.out.println("Execution time: " + duration + "ms");
    return result;
}

```


#### Method Interceptors: Wrap method calls
Execute logic before and after a method runs.
```java
@Aspect
public class LoggingAspect {

    @Around("execution(* com.example.service.MyService.doWork(..))")
    public Object logMethodCall(ProceedingJoinPoint joinPoint) throws Throwable {
        System.out.println("Before method: " + joinPoint.getSignature());
        Object result = joinPoint.proceed(); // Proceed to the actual method
        System.out.println("After method: " + joinPoint.getSignature());
        return result;
    }
}
```
##### Constructor Interceptors: Wrap object creation
Intercept and wrap logic around object instantiation.

```java
@Aspect
public class ConstructorAspect {

    @Before("execution(com.example.model.User.new(..))")
    public void beforeConstructor(JoinPoint joinPoint) {
        System.out.println("Creating instance of: " + joinPoint.getSignature().getDeclaringTypeName());
    }
}
```
#### Field Interceptors: Wrap field access (read/write)
Intercept reading or writing to a field.
```java
@Aspect
public class FieldAccessAspect {

    @Before("get(String com.example.model.User.name)")
    public void beforeFieldRead(JoinPoint joinPoint) {
        System.out.println("Reading field: " + joinPoint.getSignature());
    }

    @Before("set(String com.example.model.User.name)")
    public void beforeFieldWrite(JoinPoint joinPoint) {
        System.out.println("Writing to field: " + joinPoint.getSignature());
    }
}
```
# How AOP Works in Spring Boot

- **Define Aspects**: Create **classes** annotated with `**@Aspect**` that
  define the cross-cutting concerns.
- **Configure Pointcuts**: Specify where and when the advice should be applied **using pointcut expressions**.
- **Apply Advice**: Use annotations to define the **type of advice** and **associate** it with the pointcuts.

![aopConcepts.png]({{ site.url }}/assets/images/aopConcepts.png)

## Add Dependency

```yaml
implementation 'org.springframework.boot:spring-boot-starter-aop'
```

## Define an aspect

On Class

- `@Aspect`: Marks the class as an aspect.
- `@Component`: Makes the aspect a Spring bean so that it can be detected by the
  Spring container.

On methods

- `@Before`: Defines advice to execute before methods in the specified package.
- `@After`: Defines advice to execute after methods in the specified package.
- `@Around` : The most flexible type of advice because it allows you to do
  things like
  change the method's return value, throw an exception, or completely prevent
  the method from running.

## Pointcut Expression:

`execution(* com.spring.reference.service.*.*(..))`

- execution(...): This is a pointcut **designator** that specifies which method
  executions the advice should apply to.
- `*`: Represents the **return type** of the method. Here, * is a wildcard that
  matches any return type.
- `com.spring.reference.service.*.*(..)`:
    - `com.spring.reference.service`: Specifies the **package** where the
      methods are located.
    - `*`: The first * represents **any class** within the specified package.
    - `*`: The second * represents **any method** name within the classes of the
      specified package.
    - `(..)`: Represents **any number of parameters** (including zero). The `..`
      wildcard matches any arguments.

![pointcutExpression.png]({{ site.url }}/assets/images/pointcutExpression.png)

# Advanced Pointcut Expressions

## Common Pointcut Patterns

```java
// 1. Method execution patterns
execution(public * *(..))                    // All public methods
execution(* set*(..))                       // All setter methods
execution(* com.example.service.*Service.*(..)) // All methods in service classes ending with 'Service'
execution(public String com.example.*.get*()) // Public methods returning String starting with 'get'

// 2. Annotation-based pointcuts
@annotation(org.springframework.transaction.annotation.Transactional)
@annotation(com.example.annotation.LogExecution)

// 3. Within specific classes or packages
within(com.example.service.*)               // Within service package
within(com.example.service.UserService)     // Within specific class

// 4. Target object patterns
target(com.example.service.BaseService)     // Target implements/extends BaseService
this(com.example.service.UserService)       // Proxy implements UserService

// 5. Method arguments
args(String, ..)                            // First parameter is String
args(String, int)                           // Exactly String and int parameters
```

## Combining Pointcut Expressions

```java
@Aspect
@Component
public class CombinedPointcutsAspect {
    
    // Define reusable pointcuts
    @Pointcut("execution(* com.example.service.*.*(..))")
    public void serviceLayer() {}
    
    @Pointcut("execution(* com.example.repository.*.*(..))")
    public void repositoryLayer() {}
    
    @Pointcut("@annotation(org.springframework.transaction.annotation.Transactional)")
    public void transactionalMethods() {}
    
    // Combine pointcuts with logical operators
    @Before("serviceLayer() && transactionalMethods()")
    public void beforeTransactionalService(JoinPoint joinPoint) {
        log.info("Executing transactional service method: {}", joinPoint.getSignature().getName());
    }
    
    // OR operator
    @Around("serviceLayer() || repositoryLayer()")
    public Object measurePerformance(ProceedingJoinPoint joinPoint) throws Throwable {
        // Performance measurement logic
    }
    
    // NOT operator
    @After("serviceLayer() && !transactionalMethods()")
    public void afterNonTransactionalService(JoinPoint joinPoint) {
        log.info("Completed non-transactional service method: {}", joinPoint.getSignature().getName());
    }
}
```

# Custom Annotations for AOP

## Creating Custom Annotations

```java
// Custom annotation for logging
@Target(ElementType.METHOD)
@Retention(RetentionPolicy.RUNTIME)
public @interface LogExecution {
    String value() default "";
    boolean includeArgs() default false;
    boolean includeResult() default false;
}

// Custom annotation for performance monitoring
@Target(ElementType.METHOD)
@Retention(RetentionPolicy.RUNTIME)
public @interface MonitorPerformance {
    long threshold() default 1000L; // milliseconds
    boolean logSlowOperations() default true;
}

// Custom annotation for security
@Target(ElementType.METHOD)
@Retention(RetentionPolicy.RUNTIME)
public @interface RequiresRole {
    String[] value();
}
```

## Using Custom Annotations with AOP

```java
@Aspect
@Component
@Slf4j
public class CustomAnnotationAspect {
    
    @Around("@annotation(logExecution)")
    public Object logMethodExecution(ProceedingJoinPoint joinPoint, LogExecution logExecution) throws Throwable {
        String methodName = joinPoint.getSignature().getName();
        String customMessage = logExecution.value().isEmpty() ? methodName : logExecution.value();
        
        // Log method entry
        if (logExecution.includeArgs()) {
            log.info("Entering {}: args={}", customMessage, Arrays.toString(joinPoint.getArgs()));
        } else {
            log.info("Entering {}", customMessage);
        }
        
        try {
            Object result = joinPoint.proceed();
            
            // Log method exit
            if (logExecution.includeResult()) {
                log.info("Exiting {}: result={}", customMessage, result);
            } else {
                log.info("Exiting {}", customMessage);
            }
            
            return result;
        } catch (Exception e) {
            log.error("Exception in {}: {}", customMessage, e.getMessage());
            throw e;
        }
    }
    
    @Around("@annotation(monitorPerformance)")
    public Object monitorMethodPerformance(ProceedingJoinPoint joinPoint, MonitorPerformance monitorPerformance) throws Throwable {
        long startTime = System.currentTimeMillis();
        
        try {
            Object result = joinPoint.proceed();
            long executionTime = System.currentTimeMillis() - startTime;
            
            if (executionTime > monitorPerformance.threshold() && monitorPerformance.logSlowOperations()) {
                log.warn("SLOW OPERATION: {} took {} ms (threshold: {} ms)", 
                    joinPoint.getSignature().getName(), executionTime, monitorPerformance.threshold());
            } else {
                log.debug("Method {} executed in {} ms", joinPoint.getSignature().getName(), executionTime);
            }
            
            return result;
        } catch (Exception e) {
            long executionTime = System.currentTimeMillis() - startTime;
            log.error("Method {} failed after {} ms: {}", 
                joinPoint.getSignature().getName(), executionTime, e.getMessage());
            throw e;
        }
    }
    
    @Before("@annotation(requiresRole)")
    public void checkSecurity(JoinPoint joinPoint, RequiresRole requiresRole) {
        // Get current user (this would typically come from SecurityContext)
        String currentUserRole = getCurrentUserRole(); // Your implementation
        
        boolean hasRequiredRole = Arrays.stream(requiresRole.value())
            .anyMatch(role -> role.equals(currentUserRole));
            
        if (!hasRequiredRole) {
            throw new SecurityException("Access denied. Required roles: " + 
                Arrays.toString(requiresRole.value()) + ", Current role: " + currentUserRole);
        }
    }
    
    private String getCurrentUserRole() {
        // Implementation to get current user role
        return "USER"; // Placeholder
    }
}
```

## Service Class Using Custom Annotations

```java
@Service
public class UserService {
    
    @LogExecution(value = "Creating new user", includeArgs = true, includeResult = true)
    @MonitorPerformance(threshold = 500L)
    public User createUser(String name, String email) {
        // User creation logic
        return new User(name, email);
    }
    
    @RequiresRole({"ADMIN", "MANAGER"})
    @LogExecution("Deleting user")
    public void deleteUser(Long userId) {
        // User deletion logic
    }
    
    @MonitorPerformance(threshold = 2000L, logSlowOperations = true)
    public List<User> getAllUsers() {
        // Potentially slow operation
        return userRepository.findAll();
    }
}
```

# Real-World AOP Use Cases

## 1. Caching Aspect

```java
@Aspect
@Component
@Slf4j
public class CachingAspect {
    
    private final ConcurrentHashMap<String, Object> cache = new ConcurrentHashMap<>();
    
    @Around("@annotation(cacheable)")
    public Object cacheMethod(ProceedingJoinPoint joinPoint, Cacheable cacheable) throws Throwable {
        String key = generateKey(joinPoint);
        
        // Check cache first
        if (cache.containsKey(key)) {
            log.info("Cache HIT for key: {}", key);
            return cache.get(key);
        }
        
        // Execute method if not in cache
        log.info("Cache MISS for key: {}, executing method", key);
        Object result = joinPoint.proceed();
        
        // Store in cache
        cache.put(key, result);
        return result;
    }
    
    private String generateKey(ProceedingJoinPoint joinPoint) {
        return joinPoint.getSignature().toString() + ":" + Arrays.toString(joinPoint.getArgs());
    }
}

// Usage
@Service
public class ProductService {
    
    @Cacheable
    public Product getProductById(Long id) {
        // Expensive database operation
        return productRepository.findById(id);
    }
}
```

## 2. Audit Trail Aspect

```java
@Aspect
@Component
@Slf4j
public class AuditAspect {
    
    @Autowired
    private AuditLogRepository auditLogRepository;
    
    @After("execution(* com.example.service.*.create*(..) || * com.example.service.*.update*(..) || * com.example.service.*.delete*(..))")
    public void auditDataModification(JoinPoint joinPoint) {
        String methodName = joinPoint.getSignature().getName();
        String className = joinPoint.getTarget().getClass().getSimpleName();
        Object[] args = joinPoint.getArgs();
        
        AuditLog auditLog = AuditLog.builder()
            .action(methodName)
            .entityType(className)
            .parameters(Arrays.toString(args))
            .timestamp(LocalDateTime.now())
            .userId(getCurrentUserId())
            .build();
            
        auditLogRepository.save(auditLog);
        log.info("Audit log created for {}.{}", className, methodName);
    }
    
    private String getCurrentUserId() {
        // Get current user from security context
        return "current-user-id";
    }
}
```

## 3. Retry Mechanism Aspect

```java
@Target(ElementType.METHOD)
@Retention(RetentionPolicy.RUNTIME)
public @interface Retry {
    int maxAttempts() default 3;
    long delay() default 1000L; // milliseconds
    Class<? extends Exception>[] retryFor() default {Exception.class};
}

@Aspect
@Component
@Slf4j
public class RetryAspect {
    
    @Around("@annotation(retry)")
    public Object retryMethod(ProceedingJoinPoint joinPoint, Retry retry) throws Throwable {
        int attempts = 0;
        Exception lastException = null;
        
        while (attempts < retry.maxAttempts()) {
            try {
                attempts++;
                log.info("Attempt {} for method {}", attempts, joinPoint.getSignature().getName());
                return joinPoint.proceed();
            } catch (Exception e) {
                lastException = e;
                
                // Check if this exception type should trigger a retry
                boolean shouldRetry = Arrays.stream(retry.retryFor())
                    .anyMatch(retryException -> retryException.isAssignableFrom(e.getClass()));
                    
                if (!shouldRetry || attempts >= retry.maxAttempts()) {
                    break;
                }
                
                log.warn("Method {} failed on attempt {}, retrying in {} ms: {}", 
                    joinPoint.getSignature().getName(), attempts, retry.delay(), e.getMessage());
                    
                Thread.sleep(retry.delay());
            }
        }
        
        log.error("Method {} failed after {} attempts", 
            joinPoint.getSignature().getName(), retry.maxAttempts());
        throw lastException;
    }
}

// Usage
@Service
public class ExternalApiService {
    
    @Retry(maxAttempts = 5, delay = 2000L, retryFor = {IOException.class, TimeoutException.class})
    public String callExternalApi(String endpoint) {
        // API call that might fail
        return restTemplate.getForObject(endpoint, String.class);
    }
}
```

# Example Code

```java
@Aspect @Component @Slf4j
public class LoggingAspect {
  @Before("execution(* com.spring.reference.service.*.*(..))")
  public void logBefore(JoinPoint joinPoint) {
    log.info("AOP : Before method: " + joinPoint.getSignature().getName());
  }

  @After("execution(* com.spring.reference.service.UserServiceForAOP.*(..))") //Adding a specific Class
  public void logAfter(JoinPoint joinPoint) {
    log.info("AOP : After method: " + joinPoint.getSignature().getName());
  }

  @AfterThrowing(pointcut = "execution(* com.spring.reference.service.UserServiceForAOP.updateUserExceptionally(..))", throwing = "exception") //Adding a specific class and its specific method
  public void logAfterThrowing(JoinPoint joinPoint, Throwable exception) {
    log.error("AOP : Exception in method: {} with message: {}", joinPoint.getSignature().getName(), exception.getMessage());
  }

  @Around("execution(* com.spring.reference.service.UserServiceForAOP.*(..))")
  public Object logExecutionTime(ProceedingJoinPoint joinPoint) throws Throwable {
    long startTime = System.currentTimeMillis();

    Object proceed = null;
    try {
      // Proceed with the original method execution
      proceed = joinPoint.proceed();
    } finally {
      long executionTime = System.currentTimeMillis() - startTime;
      log.info("AOP : Method {} executed in {} ms", joinPoint.getSignature(), executionTime);
    }

    return proceed;
  }
}

# AOP Configuration and Best Practices

## EnableAspectJAutoProxy Configuration

```java
@Configuration
@EnableAspectJAutoProxy(proxyTargetClass = true) // Force CGLIB proxies
public class AopConfiguration {
    
    // Custom aspect beans can be defined here
    @Bean
    public CustomAspect customAspect() {
        return new CustomAspect();
    }
}
```

## Understanding Proxy Types

### JDK Dynamic Proxies vs CGLIB Proxies

```java
// Interface-based service (JDK Dynamic Proxy)
public interface UserService {
    User findById(Long id);
}

@Service
public class UserServiceImpl implements UserService {
    @Override
    public User findById(Long id) {
        // Implementation
    }
}

// Class-based service (CGLIB Proxy required)
@Service
public class ProductService {
    public Product findById(Long id) {
        // Implementation - no interface
    }
}
```

## Order of Aspect Execution

```java
@Aspect
@Component
@Order(1) // Higher precedence
public class SecurityAspect {
    // Security checks first
}

@Aspect
@Component
@Order(2) // Lower precedence
public class LoggingAspect {
    // Logging after security
}

@Aspect
@Component
@Order(3) // Lowest precedence
public class PerformanceAspect {
    // Performance monitoring last
}
```

## Testing AOP Aspects

### Unit Testing Aspects

```java
@ExtendWith(MockitoExtension.class)
class LoggingAspectTest {
    
    @Mock
    private ProceedingJoinPoint joinPoint;
    
    @Mock
    private MethodSignature signature;
    
    @InjectMocks
    private LoggingAspect loggingAspect;
    
    @Test
    void shouldLogMethodExecution() throws Throwable {
        // Arrange
        when(joinPoint.getSignature()).thenReturn(signature);
        when(signature.getName()).thenReturn("testMethod");
        when(joinPoint.proceed()).thenReturn("result");
        
        // Act
        Object result = loggingAspect.logExecutionTime(joinPoint);
        
        // Assert
        assertThat(result).isEqualTo("result");
        verify(joinPoint).proceed();
    }
    
    @Test
    void shouldHandleExceptionInMethod() throws Throwable {
        // Arrange
        when(joinPoint.getSignature()).thenReturn(signature);
        when(signature.getName()).thenReturn("testMethod");
        when(joinPoint.proceed()).thenThrow(new RuntimeException("Test exception"));
        
        // Act & Assert
        assertThrows(RuntimeException.class, () -> 
            loggingAspect.logExecutionTime(joinPoint));
    }
}
```

### Integration Testing with AOP

```java
@SpringBootTest
@ActiveProfiles("test")
class AopIntegrationTest {
    
    @Autowired
    private UserService userService;
    
    @MockBean
    private UserRepository userRepository;
    
    @Test
    void shouldApplyLoggingAspect() {
        // Arrange
        User user = new User("John", "john@example.com");
        when(userRepository.findById(1L)).thenReturn(Optional.of(user));
        
        // Act - AOP aspects should be applied
        User result = userService.findById(1L);
        
        // Assert
        assertThat(result).isEqualTo(user);
        // Verify logging occurred (using test appender or log capture)
    }
}
```

# Common AOP Pitfalls and Solutions

## 1. Self-Invocation Problem

```java
@Service
public class UserService {
    
    @LogExecution
    public void updateUser(User user) {
        // This internal call won't trigger AOP!
        validateUser(user);
        // Save user logic
    }
    
    @LogExecution
    public void validateUser(User user) {
        // Validation logic
    }
}

// Solution 1: Inject self-reference
@Service
public class UserService {
    
    @Autowired
    private UserService self;
    
    @LogExecution
    public void updateUser(User user) {
        // This will trigger AOP
        self.validateUser(user);
        // Save user logic
    }
    
    @LogExecution
    public void validateUser(User user) {
        // Validation logic
    }
}

// Solution 2: Extract to separate service
@Service
public class UserValidationService {
    @LogExecution
    public void validateUser(User user) {
        // Validation logic
    }
}

@Service
public class UserService {
    @Autowired
    private UserValidationService validationService;
    
    @LogExecution
    public void updateUser(User user) {
        validationService.validateUser(user); // AOP works!
        // Save user logic
    }
}
```

## 2. Final Methods Can't Be Proxied

```java
@Service
public class UserService {
    // This won't work with CGLIB proxies
    @LogExecution
    public final void processUser(User user) {
        // Logic here
    }
    
    // Solution: Remove final modifier or use interface
    @LogExecution
    public void processUserCorrect(User user) {
        // Logic here
    }
}
```

## 3. Private Methods Can't Be Intercepted

```java
@Service
public class UserService {
    
    public void processUser(User user) {
        // This internal call won't be intercepted
        validateUserPrivate(user);
    }
    
    @LogExecution // Won't work!
    private void validateUserPrivate(User user) {
        // Validation logic
    }
    
    // Solution: Make method public or protected
    @LogExecution // This works!
    protected void validateUserProtected(User user) {
        // Validation logic
    }
}
```

# Performance Considerations

## Optimizing AOP Performance

```java
@Aspect
@Component
public class OptimizedLoggingAspect {
    
    private static final Logger log = LoggerFactory.getLogger(OptimizedLoggingAspect.class);
    
    // Use specific pointcuts instead of broad ones
    @Pointcut("execution(* com.example.service.UserService.*(..))")
    public void userServiceMethods() {}
    
    // Check log level before expensive operations
    @Around("userServiceMethods()")
    public Object logExecutionTime(ProceedingJoinPoint joinPoint) throws Throwable {
        if (!log.isDebugEnabled()) {
            return joinPoint.proceed(); // Skip logging if not needed
        }
        
        long startTime = System.nanoTime();
        try {
            Object result = joinPoint.proceed();
            long duration = System.nanoTime() - startTime;
            log.debug("Method {} executed in {} ns", 
                joinPoint.getSignature().getName(), duration);
            return result;
        } catch (Exception e) {
            long duration = System.nanoTime() - startTime;
            log.error("Method {} failed after {} ns: {}", 
                joinPoint.getSignature().getName(), duration, e.getMessage());
            throw e;
        }
    }
}
```

# Conclusion

Spring AOP is a powerful tool for implementing cross-cutting concerns, but it should be used judiciously:

**Best Practices:**
- Use specific pointcut expressions to avoid unnecessary overhead
- Prefer custom annotations over complex pointcut expressions
- Be aware of proxy limitations (final methods, self-invocation)
- Test aspects thoroughly, both in isolation and integration
- Consider performance impact, especially for frequently called methods
- Use appropriate aspect ordering when multiple aspects apply

**When to Use AOP:**
- Logging and auditing
- Performance monitoring
- Security checks
- Transaction management
- Caching
- Error handling and retry logic

**When NOT to Use AOP:**
- Core business logic
- Simple operations that don't need cross-cutting behavior
- When it makes code harder to understand and debug
- Performance-critical paths where overhead matters
```