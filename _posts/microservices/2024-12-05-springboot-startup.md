---
categories:
- Microservices
date: 2024-12-05 15:00:00
tags:
- Spring Boot
- Initialization
title: Spring Boot Startup Process
---

{% include toc title="Index" %}

### [Demo Project](https://github.com/nitinkc/springboot-lifecycle)
---
# 1. **Application Entry Point**
- The entry point for a Spring Boot application is typically a class annotated with `@SpringBootApplication`.
- The `@SpringBootApplication` annotation is a combination of:
    - `@EnableAutoConfiguration`: Enables Spring Boot's auto-configuration mechanism.
    - `@ComponentScan`: Scans for components in the current package and sub-packages.
    - `@Configuration`: Marks the class as a source of bean definitions.

The `SpringApplication.run()` method is invoked to start the application and triggers the entire startup process.

```java
@SpringBootApplication
public class Application {
    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
}
```

---

# 2. **Startup Process**

## 2.1 **SpringApplication Initialization & Detection**
- A `SpringApplication` object is created when the application is run.
- Key tasks during initialization include:
  - Detecting the application type (`SERVLET`, `REACTIVE`, or `NONE`).
  - Loading `ApplicationContextInitializers` and `ApplicationListeners`.
  - Setting default properties for the application.

> The application type is set using the `SpringApplication` class.
> The detection logic is encapsulated in the `deduceApplicationType()` method.

**SERVLET**: A traditional web application based on the [Servlet API](https://www.linkedin.com/advice/0/what-java-servlet-skills-web-development-zaqff#:~:text=The%20web%20server%20passes%20the,displays%20it%20on%20the%20screen).
- Detected if `javax.servlet.Servlet` or `javax.servlet.http.HttpServletRequest` is on the classpath.
- `spring-boot-starter-web` dependency.

**REACTIVE**: A reactive web application built using Spring WebFlux.
- Detected if `org.springframework.web.reactive.DispatcherHandler` or related WebFlux classes are present on the classpath.
- `spring-boot-starter-webflux` dependency.

**NONE**: A non-web application, such as a batch or CLI tool.
- Selected if neither the SERVLET nor REACTIVE indicators are found.
- This is typical for applications that do not need a web server, such as CLI tools or batch processing jobs.

```java
//CONSTRUCTOR
public SpringApplication(ResourceLoader resourceLoader, Class<?>... primarySources) {
  this.resourceLoader = resourceLoader;
  Assert.notNull(primarySources, "PrimarySources must not be null");
  this.primarySources = new LinkedHashSet<>(Arrays.asList(primarySources));
  //NOTE THIS
  this.properties.setWebApplicationType(WebApplicationType.deduceFromClasspath());
  this.bootstrapRegistryInitializers = new ArrayList<>(
          getSpringFactoriesInstances(BootstrapRegistryInitializer.class));
  setInitializers((Collection) getSpringFactoriesInstances(ApplicationContextInitializer.class));
  setListeners((Collection) getSpringFactoriesInstances(ApplicationListener.class));
  this.mainApplicationClass = deduceMainApplicationClass();
}

//DEDUCE LOGIC
static WebApplicationType deduceFromClasspath() {
		if (ClassUtils.isPresent(WEBFLUX_INDICATOR_CLASS, null) && !ClassUtils.isPresent(WEBMVC_INDICATOR_CLASS, null)
				&& !ClassUtils.isPresent(JERSEY_INDICATOR_CLASS, null)) {
			return WebApplicationType.REACTIVE;
		}
		for (String className : SERVLET_INDICATOR_CLASSES) {
			if (!ClassUtils.isPresent(className, null)) {
				return WebApplicationType.NONE;
			}
		}
		return WebApplicationType.SERVLET;
	}
```

### What Happens After Detection
**1. Setting the Application Context**

Based on the detected type, Spring Boot selects the appropriate ApplicationContext implementation:
- `AnnotationConfigServletWebServerApplicationContext` for SERVLET.
- `AnnotationConfigReactiveWebServerApplicationContext` for REACTIVE.
- `AnnotationConfigApplicationContext` for NONE.

**2. Configuring the Embedded Server**

- For SERVLET applications, an **embedded servlet container** (e.g., Tomcat, Jetty) is initialized.
- For REACTIVE applications, **a reactive server** (e.g., Netty) is initialized.
- For NONE, no server is started.

**3. Initializing Dispatcher**

- SERVLET: The `DispatcherServlet` is configured for handling HTTP requests.
- REACTIVE: The `DispatcherHandler` is initialized for reactive request handling.

## 2.2 **Application Listeners Execution**
- `ApplicationListeners` handle various lifecycle events during startup, such as environment preparation and context initialization.
- Examples of lifecycle events include:
  - Preparing the environment.
  - Initializing the application context.

### **How to Listen to Events**

### 1. **Implementing `ApplicationListener` Interface**

`@Component` gets initiated with with `SpringApplication.run(DemoApplication.class, args);`
```java
@Slf4j
@Component
public class ApplicationReadyListener implements ApplicationListener<ApplicationReadyEvent> {
    @Override
    public void onApplicationEvent(ApplicationReadyEvent event) {
        log.info("[LOG] ApplicationReadyEvent Listner via Component: Application is ready.");
    }
}
```

whereas, if Stereotype annotation is not used, then add explicitly
```java
@Slf4j
public class ApplicationStartingListener implements ApplicationListener<ApplicationStartingEvent> {
    @Override
    public void onApplicationEvent(ApplicationStartingEvent event) {
        log.info("[LOG] ApplicationStartingEvent: Application is starting...");
    }
}
```

Explicit adding
```java
public static void main(String[] args) {
    SpringApplication app = new SpringApplication(DemoApplication.class);
    // Add event listeners for logging application lifecycle
    app.addListeners(new ApplicationStartingListener());

    app.run(args);
}
```

### 2. Using `@EventListener` Annotation
```java
@Component
public class MyEventListener {
    @EventListener
    public void handleReadyEvent(ApplicationReadyEvent event) {
        log.info("Application is ready!");
    }
}
```

### 3. Programmatically Adding Listeners
```java
public static void main(String[] args) {
    SpringApplication app = new SpringApplication(Application.class);
    app.addListeners(event -> {
        if (event instanceof ApplicationReadyEvent) {
            System.out.println("Application is ready!");
        }
    });
    app.run(args);
}
```

### **Sequence of Events**
1. **ApplicationStartingEvent**
- Triggered when the application starts.
- No context or environment is available.

2. **ApplicationEnvironmentPreparedEvent**
  - Triggered when the environment is prepared (properties, profiles, etc.).
  - Context is not created yet.

3. **ApplicationContextInitializedEvent**
  - Triggered after the context is initialized but before bean definitions are loaded.

4. **ApplicationPreparedEvent**
  - Triggered after the context is prepared but before it is refreshed.

5. **ApplicationStartedEvent**
  - Triggered after the context is refreshed and before runners are invoked.

6. **ApplicationReadyEvent**
  - Triggered after runners have been executed and the application is ready to serve requests.

7. **ContextClosedEvent**
  - Triggered during shutdown when the context is closing.

8. **ApplicationFailedEvent**
  - Triggered if the application fails to start due to an exception.

## 2.3 **Banner**
Either use app config
```yaml
spring:
  main:
    banner-mode: "off"
```
Or use java code
```java
public static void main(String[] args) {
  SpringApplication app = new SpringApplication(Application.class);
  app.setBannerMode(Banner.Mode.OFF); // Example of customizing the startup
  app.run(args);
}
```
---

# 3. **Environment Preparation**
Spring Boot creates and configures an `Environment` object to manage application 
properties and profiles. 

Key steps include:
- Loading properties from various sources:
  - Configuration files (e.g., `application.properties` or `application.yml`).
  - Environment variables.
  - Command-line arguments.
- Determining and activating profiles for different environments, such as `dev` or `prod`.

```java
@SpringBootApplication
public class Application {
    public static void main(String[] args) {
        SpringApplication app = new SpringApplication(Application.class);
        app.addListeners(event -> {
            if (event instanceof ApplicationEnvironmentPreparedEvent) {
                System.out.println("Environment Prepared: " + event);
            }
        });
        app.run(args);
    }
}
```

---

# 4. **Creating the Application Context**
In Spring Boot, the creation of the `ApplicationContext` is a critical step that
determines the environment and structure of the application.

## **What is the Application Context?**
The `ApplicationContext` is an **interface** in Spring that provides the
following functionalities:
1. Loading and managing beans.
2. Resolving dependencies.
3. Publishing and listening to application events.
4. Integrating with the environment.

Spring Boot **dynamically** selects the appropriate `ApplicationContext`
implementation based on the application type.

## **Types of Application Contexts in Spring Boot**
Spring Boot uses different types of `ApplicationContext` implementations 
depending on the detected application type:

1. **Servlet-Based Applications**:
  - **Context Used**: `ServletWebServerApplicationContext`
  - **Purpose**: Configures a servlet-based web application with an embedded web server like Tomcat or Jetty.
  - **Usage**: Typical for traditional web applications built with Spring MVC.

2. **Reactive Applications**:
  - **Context Used**: `ReactiveWebServerApplicationContext`
  - **Purpose**: Configures a reactive web application using WebFlux and an embedded reactive server like Netty.
  - **Usage**: For modern, non-blocking, and event-driven applications.

3. **CLI or Non-Web Applications**:
  - **Context Used**: `GenericApplicationContext`
  - **Purpose**: Configures an application without a web server, such as batch jobs or command-line tools.
  - **Usage**: For non-web Spring Boot applications

```java
public static void main(String[] args) {
    SpringApplication app = new SpringApplication(Application.class);
    app.setApplicationContextClass(AnnotationConfigApplicationContext.class); // Setting custom ApplicationContext
    ConfigurableApplicationContext context = app.run(args);
    log.info("[LOG] ApplicationContext in use: {}", context.getClass().getName());
}
```

## What Happens During Application Context Creation
**Bean Definitions:**
- The `ApplicationContext` scans for and registers bean definitions
(via `@ComponentScan`, `@Configuration`, etc.).

**Configuration Processing:**
- Processes configuration classes (`@Configuration`) and applies Spring Boot’s auto-configuration.

**Environment Integration:**
- Integrates application **properties and profiles** into the context.

**Lifecycle Event Publishing:**
- Publishes lifecycle events such as `ApplicationStartedEvent` and `ContextRefreshedEvent`.

---

# 5. **Auto-Configuration and Component Scanning**
Spring Boot evaluates conditions defined in each auto-configuration class
(e.g., `@ConditionalOnClass`, `@ConditionalOnProperty`) to decide if the class should be applied.

### 5.1 **Component Scanning**
- The `@ComponentScan` annotation scans the base package and sub-packages for 
Spring-managed components, such as:
  - Services
  - Repositories
  - Controllers
  - Configuration classes
  
```java
@Component
public class MyService {
    public void serve() {
        System.out.println("Service is running");
    }
}
```

### 5.2 **Auto-Configuration**
- Auto-configuration uses the `@EnableAutoConfiguration` annotation.
- It leverages `META-INF/spring.factories` to load relevant configuration classes automatically.
- Conditional annotations (`@Conditional`) determine which configurations should be applied.
```java
@Configuration
@ConditionalOnMissingBean(MyService.class)
public class MyServiceAutoConfiguration {
    @Bean
    public MyService myService() {
        return new MyService();
    }
}
```
---
# 6. **Bean Definitions and Dependency Injection**

### 6.1 **Bean Creation**
- Beans are registered in the application context through:
  - Component scanning.
  - Explicit definitions in configuration classes.
  - Auto-configuration.

### 6.2 **Dependency Injection**
- Dependencies are resolved and injected into beans through mechanisms like:
  - Constructor injection.
  - Field injection.
  - Setter injection.

```java
@Configuration
public class MyConfiguration {
    @Bean
    public MyBean myBean() {
        return new MyBean();
    }
}

@Component
public class MyBeanConsumer {
    private final MyBean myBean;

    @Autowired
    public MyBeanConsumer(MyBean myBean) {
        this.myBean = myBean;
    }

    public void printMessage() {
        log.info("Bean is injected: " + myBean);
    }
}
```
---
# 7. **Application Context Refresh**

The application context is refreshed to perform tasks such as:
- Instantiating and configuring all beans.
- Resolving placeholders and configuration properties.
- Registering and initializing any lifecycle components or runners.
```java
@Component
public class ContextRefreshListener implements ApplicationListener<ContextRefreshedEvent> {
    @Override
    public void onApplicationEvent(ContextRefreshedEvent event) {
        System.out.println("Context Refreshed: " + event);
    }
}
```
---
# 8. **Embedded Server Initialization (For Web Applications)**

### 8.1 **Server Startup**
- The embedded web server (e.g., Tomcat, Jetty, or Undertow) is started during this phase.

### 8.2 **DispatcherServlet Initialization**
- The `DispatcherServlet` is registered in the servlet context and initialized to handle HTTP requests.

```java
@RestController
public class MyController {
    @GetMapping("/")
    public String home() {
        return "Welcome to Spring Boot!";
    }
}
```
---
# 9. **Application Execution**

### 9.1 **Lifecycle Events**
- Spring Boot triggers application lifecycle events, including:
  - `ApplicationStartedEvent` – Signaling the application startup phase.
  - `ApplicationReadyEvent` – Signaling that the application is ready.

### 9.2 **Custom Logic Execution**
- Any custom initialization logic defined in `CommandLineRunner` or `ApplicationRunner` beans is executed.
```java
@Component
public class MyCommandLineRunner implements CommandLineRunner {
    @Override
    public void run(String... args) throws Exception {
        System.out.println("Executing custom logic at startup");
    }
}
```
---
# 10. **Application Ready**

The application is fully initialized and ready to handle its tasks:
- For web applications, the server is ready to process requests.
- For CLI or batch applications, the main process begins execution.
---
# Summary

The Spring Boot startup process consists of several well-defined steps:
1. Initializing the `SpringApplication`.
2. Preparing the environment and loading properties.
3. Creating and refreshing the application context.
4. Registering beans and performing dependency injection.
5. Starting the embedded server (if applicable).
6. Running custom application logic.