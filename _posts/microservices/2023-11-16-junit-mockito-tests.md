---
title:  "Mockito Junit Tests"
date:   2023-11-16 18:55:00
categories: [Microservices]
tags: [Microservices]
---

# Mockito with Junit

- Class `MyService` is SUT (System Under Test)
- Class `SomeService` is Dependency (which is mocked). 

### Argumnent Matchers
`any()` - be generic always, by passing all the arguments as arg matchers or be specific

# Annotations

### Integration Testing with `@SpringBootTest`:

- **Purpose**:
    - Integration testing using the Spring Boot Testing framework.
    - Loads the full Spring application context.
    - Tests the application as if it were running in a real environment.

- **Usage**:
    - Suitable for end-to-end testing and ensuring components work together.
    - Higher code coverage as it exercises the entire application stack.

## Unit Testing with `@ExtendWith(MockitoExtension.class)`:

- **Purpose**:
    - Unit testing using Mockito for mocking dependencies.
    - Enables Mockito for mocking objects during tests.
    - Focuses on isolating and testing specific components or classes.

- **Usage**:
    - Used in conjunction with Mockito annotations like `@Mock`, `@InjectMocks`, etc.
    - Does not start the Spring context; it's focused on unit testing.

## Mocking Beans with `@MockBean`:

- **Purpose**:
    - Mocks beans in integration tests or unit tests involving Spring's application context.
    - Replaces real Spring beans with mock objects for testing purposes.

- **Usage**:
    - Particularly useful when you want to isolate and test specific components without interacting with real implementations.
    - Allows control over the behavior of dependencies to simulate different scenarios.

## `@ExtendWith(SpringExtension.class)`:

- **Purpose**:
    - Enables Spring integration with JUnit 5.
    - Replaces `@RunWith(SpringRunner.class)` when using JUnit 5.

- **Usage**:
    - Sets up the Spring context before test methods are executed and closes it afterward.
    - Used to create a testing environment with a fully configured Spring application context.

## JUnit 5 Annotations:

1. **Test Annotation:**
    - `@Test`
        - Identifies a method as a test method.
```java
   @Test
   void myTestMethod() {
       // Test logic
   }
```
2. **Lifecycle Annotations:**
    - `@BeforeAll`
        - Denotes a method that should be run before all tests in a class.
    - `@BeforeEach`
        - Denotes a method that should be run before each test method.
    - `@AfterEach`
        - Denotes a method that should be run after each test method.
    - `@AfterAll`
        - Denotes a method that should be run after all tests in a class.

```java
@BeforeAll
static void setUpBeforeAll() {
    // Setup logic before all tests
}

@BeforeEach
void setUpBeforeEach() {
    // Setup logic before each test
}

@AfterEach
void tearDownAfterEach() {
    // Teardown logic after each test
}

@AfterAll
static void tearDownAfterAll() {
    // Teardown logic after all tests
}
```
3. **Test Assertion Annotations:**
    - `@Assertions`
        - Container for multiple assertion annotations like `@assertTrue`, `@assertFalse`, etc.

```java
@Test
void testAssertions() {
    assertTrue(true, "Assertion message for true condition");
    assertFalse(false, "Assertion message for false condition");
}
```
4. **Parameterized Tests:**
    - `@ParameterizedTest`
        - Denotes that the annotated method is a parameterized test.
    - `@ValueSource`
        - Provides a single value for a parameterized test.
    - `@CsvSource`
        - Provides CSV-formatted values for a parameterized test.

```java
@ParameterizedTest
@ValueSource(ints = {1, 2, 3})
void testWithParameter(int value) {
    // Test logic with parameter
}
```
5. **Repeated Tests:**
    - `@RepeatedTest`
        - Indicates that the annotated method is a repeated test.

```java
@RepeatedTest(3)
void repeatedTest() {
    // Test logic to be repeated 3 times
}
```
6. **Conditional Test Execution:**
    - `@Disabled`
        - Disables a test class or method.

```java
@Test
@Disabled("Not implemented yet")
void disabledTest() {
    // Test logic (disabled)
}
```
7. **Tagging and Filtering:**
    - `@Tag`
        - Allows tagging tests for later filtering.
    - `@DisplayName`
        - Defines a custom display name for a test class or method.

```java
@Test
@Tag("slow")
void slowTest() {
    // Test logic for slow tests
}
```
## Mockito Annotations:
 
1.**Mocking Annotations:**
    - `@Mock`
        - Creates a mock object.
    - `@Spy`
        - Creates a spy (partial mock) object.

```java
@Mock
private MyService myService;

@Spy
private MyComponent myComponent;
```
2. **Injection Annotations:**
    - `@InjectMocks`
        - Injects mock/spy dependencies into the test subject.

```java
@InjectMocks
private MyController myController;
```
3. **Verification Annotations:**
    - `@MockitoSettings`
        - Provides additional settings for Mockito.
    - `@Captor`
        - Captures argument values for further assertions.
    - `@VerificationMode`
        - Configures the verification mode (times, atLeastOnce, etc.).

```java
@Captor
private ArgumentCaptor<String> stringCaptor;

@MockitoSettings(strictness = Strictness.LENIENT)
@Test
void lenientMocking() {
    // Test logic with lenient mock settings
}
```
## Spring Testing Annotations:

1. **Integration Testing:**
    - `@SpringBootTest`
        - Loads the Spring application context for integration tests.
    - `@DataJpaTest`
        - Configures a test for JPA-based tests.

```java
@SpringBootTest
class MyIntegrationTest {
    // Integration test logic
}
```
2. **Dependency Injection:**
    - `@Autowired`
        - Injects a bean into a test class or method.
    - `@MockBean`
        - Mocks a bean when used with `@SpringBootTest`.

```java
@Autowired
private MyService myService;

@MockBean
private ExternalService externalService;
```
3. **Transaction Management:**
    - `@Transactional`
        - Specifies that a test method should be run within a transaction.

```java
@Transactional
@Test
void transactionalTest() {
    // Test logic within a transaction
}
```
4. **Web Testing:**
    - `@WebMvcTest`
        - Configures a test for Spring MVC-based tests.

```java
@WebMvcTest(MyController.class)
class MyControllerTest {
    // Web testing logic
}
```
5. **Profile Configuration:**
    - `@ActiveProfiles`
        - Specifies which bean definition profiles should be active.

```java
@ActiveProfiles("test")
class MyProfileTest {
    // Test logic with the "test" profile active
}
```
6. **Testing Components:**
    - `@ComponentScan`
        - Configures component scanning for the test context.

```java
@ComponentScan(basePackages = "com.example")
class MyComponentScanTest {
    // Test logic with custom component scanning
}
```
7. **Property Source Configuration:**
    - `@TestPropertySource`
        - Configures properties for the test context.

```java
@TestPropertySource(locations = "classpath:test.properties")
class MyPropertySourceTest {
    // Test logic with properties from test.properties
}
```
8. **Testing Annotations from JUnit Jupiter:**
    - Annotations like `@Test`, `@BeforeEach`, etc., can also be used in Spring tests.

```java
@Test
@DisplayName("Custom Test Name")
void customTestName() {
    // Test logic with a custom display name
}
```

## Additional Concepts:

- **Argument Matchers with Mockito**:
    - `anyString()` and `any()` are argument matchers in Mockito.
    - They are more lenient, allowing matching for any argument of the specified type.

- **`@MockitoSettings(strictness = Strictness.LENIENT)`**:
    - Configures the strictness level of Mockito.
    - In lenient mode, Mockito is more permissive with interactions, allowing non-stubbed method calls.

These annotations and concepts collectively provide a comprehensive testing strategy for both unit and integration testing in a Spring Boot application.


#### Declaring the Mocks
```java
BusinessImplementationBasedOnSomeService myMock = Mockito.mock(BusinessImplementationBasedOnSomeService.class);
```
OR

Prefer this way

```java
@Mock//The @Mock annotation is used to create mock objects for the dependencies of the class being tested.
// Mock objects simulate the behavior of real objects but don't have actual implementations.
private YourDataAccessObject dataAccessObjectMock;

@InjectMocks//@InjectMocks is applied to the class that you want to test.
// It tells the testing framework to inject the mock objects created with @Mock into the appropriate places within the class under test.
private YourService yourServiceUnderTest;

@InjectMocks
private BusinessImplementationBasedOnSomeService sut;

//Initialize the Mocks
@BeforeEach
void setUp() {
    MockitoAnnotations.initMocks(this);
}
```

Here's a simple example of how to use `@ExtendWith(SpringExtension.class)`:

```java
@ExtendWith(SpringExtension.class) // Enable Spring integration with JUnit 5
@SpringBootTest // Load the Spring Boot application context
public class MyServiceTest {

    @Autowired
    private MyService myService;

    @Test
    public void myServiceMethodTest() {
        // Test myService that depends on Spring beans
        String result = myService.myServiceMethod();

        // Assertions
        assertEquals("Expected Result", result);
    }
}
```

# Common Errors

1. **DO NOT** use the argument Matchers on SUT, or injectableMocks
```java
// Call the method under test
List<Map<String, Object>> result = yourServiceUnderTest.getDataById(anyString(), "sample", "facility");
```

```log
org.mockito.exceptions.misusing.InvalidUseOfMatchersException: 
Invalid use of argument matchers!
```

Use Argument matchers only on the Mocks

```java
 // Mocking the behavior of reportsBigQueryService
List<Map<String, Object>> mockDBCall = dataAccessObjectMock.getRecordFromView(anyString(), anyString(), any());
when(mockDBCall).thenReturn(data);//mockDBCall == data initialized in @BeforeEach void setUp()
```

### Test the exception

```java
// Call the method under test
FutureException exception = org.junit.jupiter.api.Assertions.assertThrows(FutureException.class, () -> {
   myQueryService.getOptionsData(anyString());
   });
```

### Mock Data

Create with Dummy data
```java
// Prepare mock data
List<Map<String, Object>> mockData = new ArrayList<>();

Map<String, Object> customerData = Collections.singletonMap("key", "value");
mockData.add(patientData);

Empty Data
// Mocked empty data
List<Map<String, Object>> mockEmptyData = Collections.emptyList();
```

Create from a json file
```java
List<Map<String, Object>> mockDataFromApi = getMockResponseFromFile("response/my-data/json-data.json");

//mocking the DB Call of getDataForTreatmentOrder
when(myServiceMock.getData(anyString(), anyString(), anyMap()))
   .thenReturn(mockDataFromApi);

private List<Map<String, Object>> getMockResponseFromFile(String path) {
    List<Map<String,Object>> mockDataFromApi = new ArrayList<>();
    String response = null;
    try {
        response = getJsonStringFromFile(path);
    } catch (IOException e) {
        e.printStackTrace();
    }

    try {
        mockDataFromApi = mapper.readValue(response, new TypeReference<List<Map<String,Object>>>() {
        });
    } catch (IOException e) {
        e.printStackTrace();
    }
    return mockDataFromApi;
}

private String getJsonStringFromFile(String path) throws IOException {
    ClassLoader classLoader = getClass().getClassLoader();
    File file = new File(Objects.requireNonNull(classLoader.getResource(path)).getFile());
    return FileUtils.readFileToString(file, "UTF-8");
}
```

## Debugging

Get the JSON Response from IntelliJ Debugger (after the DB Call) or from service request. Use breakpoint to evaluate expression
```java
new com.fasterxml.jackson.databind.ObjectMapper()
        .registerModule(new com.fasterxml.jackson.datatype.jsr310.JavaTimeModule())
        .disable(com.fasterxml.jackson.databind.SerializationFeature.WRITE_DATES_AS_TIMESTAMPS) 
        .writerWithDefaultPrettyPrinter() 
        .writeValueAsString(data);
```

Mock the response to 2 DB Calls
```java
//Get the actual Query data as JSON from DB while debugging
List<Map<String, Object>> mockDataFromApi = getMockResponseFromFile("response/my-data/dataOrders.json");

List<Map<String, Object>> mockProviderResponse = new ArrayList<Map<String, Object>>() {{
            add(new HashMap<String, Object>() {{
                put("KEY_IDENTIFIER", "15034");
                put("customer","John Doe");
            }});
        }};

// Mock the behavior of the two DB calls
when(reportsBigQueryServiceMock.getRecordFromView(anyString(), anyString(), anyMap()))
     .thenReturn(mockDataFromApi)//mocking the DB Call of getDataForTreatmentOrder
     .thenReturn(mockProviderResponse);//mocking the DB Call of private getOrderProvidersFormattedNamesByIds
```