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

#### Step 1

Class level annotations

```java
@ExtendWith(MockitoExtension.class)
@MockitoSettings(strictness = Strictness.LENIENT)
```

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

@MockBean from package `org.springframework.boot.test.mock.mockito`
@Mock package `org.mockito`;

used for mocking beans in integration tests or unit tests that involve Spring's application context

Bean Mocking: It allows you to replace a real Spring bean in the application context with a mock object for testing purposes. 

This is particularly useful when you want to isolate and test specific components without interacting with the real 
implementations of certain beans.

Testing: @MockBean is commonly used in integration tests and unit tests where you are testing components that rely on
other beans or dependencies. 

By using @MockBean, you can control the behavior of these dependencies to simulate different scenarios for testing.

Behavior Control: It allows you to define the behavior of mocked beans using mocking frameworks like Mockito or EasyMock. 
You can specify what methods should return when invoked and how they should behave during the test.

@MockBean is used to mock the `SomeDependency` bean.


The `@ExtendWith(SpringExtension.class)` annotation is used in JUnit 5 to enable the Spring Framework's integration with JUnit for testing. 
It replaces the JUnit 4 `@RunWith(SpringRunner.class)` when you are using JUnit 5.

Here's what it does:

1. **Spring Integration**: It tells JUnit 5 to integrate with the Spring Framework, allowing you to perform integration 
testing by loading Spring's application context.

2. **Spring Boot**: When you're using Spring Boot, this annotation is often used to create a testing environment with a 
fully configured Spring application context, including the application's beans, configurations, and properties.

3. **Setup**: It sets up the Spring context before test methods are executed and closes it afterward. 
This ensures that you can use the Spring features and components in your tests.

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


argument might not match exactly with the one used when the `getRecordFromView` method is called in your code. 
Mockito uses argument matching to determine which method behavior to mock based on the arguments provided.

when you are providing specific arguments
Mockito will only match the `when` statement when these exact arguments are used in the actual method call. 

If the actual method call uses different instances of the parameters object, for example, the when statement won't match, 
and the mock won't be triggered.

You are using anyString() and any() as argument matchers. These matchers are more lenient and will match any argument of the specified type.
In this case, Mockito will match the when statement for any combination of strings and any object, 
so it will return mockData for any method call to getRecordFromView.

@MockitoSettings(strictness = Strictness.LENIENT)


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
   List<Map<String, Object>> mockDataFromApi = getMockResponseFromFile("response/idt-patient-profile/dataForTreatmentOrders.json");

        //mocking the DB Call of getDataForTreatmentOrder
        when(reportsBigQueryServiceMock
        .getRecordFromView(anyString(), anyString(), anyMap()))
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

Get the JSON Response from IntelliJ Debuigger after the DB Call
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
        List<Map<String, Object>> mockDataFromApi = getMockResponseFromFile("response/idt-patient-profile/dataForTreatmentOrders.json");

        List<Map<String, Object>> mockProviderResponse = new ArrayList<Map<String, Object>>() {{
            add(new HashMap<String, Object>() {{
                put("PROVIDER_IDENTIFIER", "15034");
                put("provider","John Doe");
            }});
        }};

        // Mock the behavior of the two DB calls
        when(reportsBigQueryServiceMock.getRecordFromView(anyString(), anyString(), anyMap()))
                .thenReturn(mockDataFromApi)//mocking the DB Call of getDataForTreatmentOrder
                .thenReturn(mockProviderResponse);//mocking the DB Call of private getOrderProvidersFormattedNamesByIds

```



Here's the information formatted in Markdown:

1. **`@SpringBootTest`**:
    - `@SpringBootTest` is part of the Spring Boot Testing framework and is used for integration testing. It starts the Spring application context, loads the full Spring application context configuration, and tests your application as if it were running in a real environment. It's primarily used for end-to-end testing and ensuring that all components of your application work together as expected.
    - When you use `@SpringBootTest`, it may lead to higher code coverage because it exercises the entire application stack, including controllers, services, and repositories. However, it might also introduce more complex and slower tests compared to unit tests.

2. **`@ExtendWith(MockitoExtension.class)`**:
    - `@ExtendWith(MockitoExtension.class)` is used with JUnit 5 to enable Mockito for mocking dependencies in unit tests. Mockito is a library for creating mock objects to isolate the unit under test and focus on testing specific components or classes in isolation.
    - It's primarily used for unit testing, where you want to isolate a class or component from its dependencies and focus on its behavior in isolation. This type of testing often leads to more focused and faster tests.
    - When you use `@ExtendWith(MockitoExtension.class)`, you are not starting the Spring context, so it's not an integration test.

The code coverage you observe may differ between these two approaches because they serve different testing purposes:

- `@SpringBootTest` is likely to have higher code coverage because it tests the application as a whole and exercises many components.

- `@ExtendWith(MockitoExtension.class)` focuses on unit testing and is not intended to provide the same level of code coverage as integration tests. It allows you to isolate a specific class or component and stub/mock its dependencies. It's less concerned with the interactions and coverage of the entire application.

The choice between these testing approaches depends on your testing goals and the specific scenarios you want to cover. Integration tests with `@SpringBootTest` are suitable for testing the overall behavior of the application, while unit tests with `@ExtendWith(MockitoExtension.class)` are suitable for isolating and testing specific components in isolation.