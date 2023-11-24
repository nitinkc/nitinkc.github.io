---
title:  "Mockito Junit Tests"
date:   2023-11-16 18:55:00
categories: [Microservices]
tags: [Microservices]
---
{% include toc title="Index" %}

**SUMMARY**

Mockito with Junit

- Class `MyService` is SUT (System Under Test)
- Class `SomeService` is Dependency (which is mocked).

| Feature                       | Mockito Unit Tests                                                            | Spring Boot Integration Tests                                               |
|-------------------------------|-------------------------------------------------------------------------------|-----------------------------------------------------------------------------|
| **Purpose**                   | Test individual units in isolation.                                           | Test the interaction of multiple units in a Spring context.                 |
| **Testing Framework**         | Mockito (or JUnit + other testing frameworks).                                | Spring Boot Test (JUnit is commonly used).                                  |
| **Annotation for Test Class** | `@RunWith(MockitoJUnitRunner.class)` or `@ExtendWith(MockitoExtension.class)` | `@SpringBootTest`                                                           |
| **Mock Creation Annotation**  | `@Mock`                                                                       | `@MockBean`                                                                 |
| **Application Context**       | Not required (Mocks are manually injected).                                   | Automatically loads Spring application context.                             |
| **Dependency Injection**      | Manual (Mocks injected using `@InjectMocks`)                                  | Automatic (Spring Boot injects mocks using or `@Autowired` or `@MockBean`). |

### Unit Testing 
with `@ExtendWith(MockitoExtension.class)`

{% gist nitinkc/331712fb268a8922178daee046c2d24f %}

**Purpose**:

- Enables Mockito for mocking objects during tests. 
- Focuses on isolating and testing specific components or classes.

**Usage**:

- Used in conjunction with Mockito annotations like `@Mock`, `@InjectMocks`, etc.
- Does not start the Spring context; it's focused on unit testing.

```java
@ExtendWith(MockitoExtension.class)
@TestInstance(TestInstance.Lifecycle.PER_CLASS)
class MyClassTest {
}
```

### Integration Testing
with `@SpringBootTest` & `@ExtendWith(SpringExtension.class)` with JUnit5
    - When @SpringBootTest is used, it implicitly includes @ExtendWith(SpringExtension.class)

If you are using both Spring and Mockito in the same test class
ensure that you initialize Mockito annotations using `MockitoAnnotations.openMocks(this)` in the `@BeforeEach` method to
correctly set up the mocks.
{: .notice--info}
{% gist nitinkc/90f1d2e8313a18608fe6fa4c9cac279a %}

**Purpose**:

- Loads the full Spring application context.
- Enables Spring integration with JUnit 5.
- Replaces `@RunWith(SpringRunner.class)` when using JUnit 5.
- Tests the application as if it were running in a real environment.

 **Usage**:

- Suitable for end-to-end testing and ensuring components work together.
- Higher code coverage as it exercises the entire application stack.
- Sets up the Spring context before test methods are executed and closes it afterward.
- Used to create a testing environment with a fully configured Spring application context.

```java
@SpringBootTest // Load the Spring Boot application context
//@SpringBootTest(classes = BigQueryTestConfiguration.class)
@ExtendWith(SpringExtension.class) // Enable Spring integration with JUnit 5
// When @SpringBootTest is used, it implicitly includes @ExtendWith(SpringExtension.class)
class MyIntegrationTest {
}
```

# JUnit 5 Annotations:

**Test Annotation:**

- `@Test` : Identifies a method as a test method.
```java
   @Test
   void myTestMethod() {
       // Test logic
   }
```

**Lifecycle Annotations:**

- `@BeforeAll` : Denotes a method that should be run before all tests in a class.
- `@BeforeEach`: Denotes a method that should be run before each test method.
- `@AfterEach` : Denotes a method that should be run after each test method.
- `@AfterAll` : Denotes a method that should be run after all tests in a class.


**Test Assertion Annotations:**

`Assertions` : Class for multiple assertion annotations like `@assertTrue`, `@assertFalse`, etc.

```java
@Test
void testAssertions() {
    assertTrue(true, "Assertion message for true condition");
    assertFalse(false, "Assertion message for false condition");
    assertEquals(expected, actual, "The values are not equal!");//The message will be printed when the assertion fails
    IllegalArgumentException exception = Assertions.assertThrows(IllegalArgumentException.class, () -> {
        calculator.add(value, 4);
}
```

### Test the exception

```java
// Call the method under test
FutureException exception = org.junit.jupiter.api.Assertions.assertThrows(FutureException.class, () -> {
   myQueryService.getOptionsData(anyString());
   });
```

**Parameterized Tests:**

- `@ParameterizedTest` : Denotes that the annotated method is a parameterized test.
- `@ValueSource` : Provides a single value for a parameterized test.
- `@CsvSource` : Provides CSV-formatted values for a parameterized test.
- `@NullSource`	:  pass a null value

{% gist nitinkc/c717619a463c0e5dad5d111c5b938a3c%}

**@RepeatedTest** : Indicates that the annotated method is a repeated test.

```java
@RepeatedTest(3)
void repeatedTest() {
    // Test logic to be repeated 3 times
}
```

**Conditional Test Execution:**

- `@Disabled` : Disables a test class or method.

```java
@Test
@Disabled("Not implemented yet")
void disabledTest() {
    // Test logic (disabled)
}
```

**Tagging and Filtering:**

- `@Tag` : Allows tagging tests for later filtering.
- `@DisplayName` : Defines a custom display name for a test class or method.
{% gist nitinkc/0bb4ecd84922071d63b19212ec3e979b%}

# Mockito Annotations:
 
**Mocking Annotations:**

- `@Mock` : Creates a mock object.
- `@Spy` : Creates a spy (partial mock) object. 
  - The real methods of the object are invoked unless they are explicitly stubbed.

{% gist nitinkc/5ee058d8b256f9a2148853d90357230c%}

**Mock the response to 2 DB Calls**

{% gist nitinkc/ebcd341d1c7523c93e561ea962d46a10 %}

**Verification Annotations:**

- `@MockitoSettings` : Provides additional settings for Mockito.

**@MockitoSettings(strictness = Strictness.LENIENT)**

- Mockito allows leniency regarding stubbed methods that are not explicitly invoked during the test.
- The key point is that Mockito won't enforce strict verification of interactions with the mock.

```java
@MockitoSettings(strictness = Strictness.LENIENT)//Can be applies at class level as well
@Test
void lenientMockingTest() {
    when(someDependency.someMethod()).thenReturn("Mocked result");
    String result = someDependency.someMethod();
    assertEquals("Mocked result", result, "Lenient mocking test failed");
}
```

- **VerificationMode** : Configures the verification mode (times, atLeastOnce, etc.).

{% gist nitinkc/eb5d1c7c09a7cb437324c8d7f7602352%}

- `@Captor` : Captures argument values for further assertions.

```java
@Captor
private ArgumentCaptor<String> stringCaptor;
```

# Spring Testing Annotations:

**Integration Testing:**

- `@SpringBootTest` : Loads the Spring application context for integration tests.
- `@DataJpaTest` : Configures a test for JPA-based tests.

**Dependency Injection:**

- `@Autowired` : Injects a bean into a test class or method.
- `@MockBean` : Mocks a bean when used with `@SpringBootTest`.

{% gist nitinkc/a19869d601670d92f2c8c6527c5e0db2 %}

**Transaction Management:**

- `@Transactional` : Specifies that a test method should be run within a transaction.

```java
@Transactional
@Test
void transactionalTest() {
    // Test logic within a transaction
}
```
**Web Testing:** Testing a Controller

- `@WebMvcTest` : Configures a test for Spring MVC-based tests.

```java
@WebMvcTest(MyController.class)
class MyControllerTest {
    // Web testing logic
}
```
{% gist nitinkc/fc3a9ce93277e2bdb29322230b823378 %}

**Testing Components:**

- `@ComponentScan` : Configures component scanning for the test context.

```java
@ComponentScan(basePackages = "com.example")
class MyComponentScanTest {
    // Test logic with custom component scanning
}
```

**Profile Configuration:**

- `@ActiveProfiles` : Specifies which bean definition profiles should be active.

```java
@ActiveProfiles("test")
class MyProfileTest {
    // Test logic with the "test" profile active
}
```

**Property Source Configuration:**

-`@TestPropertySource` : Configures properties for the test context.

```java
@TestPropertySource(locations = "classpath:test.properties")
class MyPropertySourceTest {
    // Test logic with properties from test.properties
}
```

###  Argument Matchers:

- `anyString()` and `any()` are argument matchers in Mockito.
- `any()` - be generic always, by passing all the arguments as arg matchers or be specific
- They are more lenient, allowing matching for any argument of the specified type.
- **`@MockitoSettings(strictness = Strictness.LENIENT)`**:
    - Configures the strictness level of Mockito.
    - In lenient mode, Mockito is more permissive with interactions, allowing non-stubbed method calls.

**Common Errors**

**Use Argument matchers only on the Mocks**

```java
 // Mocking the behavior of reportsBigQueryService
List<Map<String, Object>> mockDBCall = dataAccessObjectMock.getRecordFromView(anyString(), anyString(), any());
when(mockDBCall).thenReturn(data);//mockDBCall == data initialized in @BeforeEach void setUp()
```

**DO NOT** use the argument Matchers on SUT, or injectableMocks

```java
// Call the method under test
List<Map<String, Object>> result = yourServiceUnderTest.getDataById(anyString(), "sample", "facility");
```

```java
org.mockito.exceptions.misusing.InvalidUseOfMatchersException: 
Invalid use of argument matchers!
```

# Mock Dummy Data

**Create with Dummy data**
{% gist nitinkc/769c03ae85f79b0af7d1bf95f82133c5 %}


**Create from a json file**
{% gist nitinkc/0420dcc14a5d0a4094fd85c32ae80a16 %}

# Debugging

Get the JSON Response from IntelliJ Debugger (after the DB Call) or from service request. Use breakpoint to evaluate expression
```java
new com.fasterxml.jackson.databind.ObjectMapper()
        .registerModule(new com.fasterxml.jackson.datatype.jsr310.JavaTimeModule())
        .disable(com.fasterxml.jackson.databind.SerializationFeature.WRITE_DATES_AS_TIMESTAMPS) 
        .writerWithDefaultPrettyPrinter() 
        .writeValueAsString(data);
```



### Autowired vs InjectMock

`@Autowired`:
- Use `@Autowired` when you want Spring to inject real beans (actual instances managed by the Spring container)into Spring-managed components.
- **Sring Framework annotation** used for automatic dependency injection, used in Spring-managed components, such as services, controllers, and repositories.
- When you use @Autowired, Spring injects the dependency into the field or constructor of the class.
- This is commonly used in **integration tests** or when you are testing Spring components that rely on other Spring-managed beans.

`@InjectMocks` 
- Use `@InjectMocks` when you want Mockito to inject mocks into the fields of your test class for the purpose of unit testing,
  particularly when you're testing a class in isolation and want to control the behavior of its dependencies.
- **Mockito annotation** used to automatically inject mocked dependencies into the fields of a test class.
- It is typically used in **unit tests** when you want to mock the dependencies of the class under test.

### Mock and MockBean

`@Mock` : @Mock is part of the Mockito framework, which is used for creating mock objects in **unit tests**.
- Mockito will create a mock for each field annotated with @Mock and inject the mocks into the fields annotated with `@InjectMocks`.

`@MockBean` : @MockBean is used in the context of Spring Boot tests, especially for **integration testing**.
- When you use @MockBean, you are creating a mock of a Spring bean. 
- This is useful when you want to replace a real bean with a mock in the Spring application context during the test.