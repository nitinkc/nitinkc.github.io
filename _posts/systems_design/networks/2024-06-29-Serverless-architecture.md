---
title:  "Serverless Architecture"
date:   2024-06-29 21:02:00
categories: [System Design]
tags: [System Design]
---
{% include toc title="Index" %}

Serverless architecture is a cloud computing execution model where the cloud provider dynamically manages the 
allocation and provisioning of servers.

Despite the name, servers are still used, but developers don't have to manage them. Instead, they focus on writing code.

One of the most popular serverless architectures is **Function as a Service** (FaaS)

Each function will perform a specific task when triggered by an event, such as an incoming email or an HTTP reques

When a function is invoked, the cloud provider 
- either executes the function on a running server, 
- - or, if there is no server currently running, it spins up a new server to execute the function.

@startuml
actor User
actor EventSource as ES

User -> "API Gateway" : HTTP Request
"API Gateway" -> Function : Trigger Event
ES -> Function : Trigger Event
Function -> "Cloud Service" : Request Data
"Cloud Service" -> Function : Respond with Data
Function -> User : Response

note right of Function
Stateless, ephemeral function
executed on demand.
end note
@enduml


# Key Characteristics
**No Server Management**: Developers don't have to worry about server provisioning, scaling, or maintenance.

**Event-Driven**: Functions are triggered by events such as HTTP requests, database changes, file uploads, etc.

**Automatic Scaling**: The infrastructure automatically scales up or down based on the load.

**Cost-Efficient**: You pay only for the compute time you consume, not for pre-allocated resources.

# How Serverless Works

**Function Deployment**: Developers write functions and deploy them to a serverless platform.

**Event Triggering**: Functions are triggered by specific events like HTTP requests, database changes, or scheduled tasks.

**Execution**: The serverless platform executes the function in a stateless compute container.

**Scaling**: The platform scales the number of running instances of the function as needed.

**Billing**: Users are billed based on the number of executions and the resources consumed during execution.

# Serverless Platforms
- AWS Lambda: A service that lets you run code without provisioning or managing servers.
- Google Cloud Functions: A lightweight, event-based asynchronous compute solution.
- Azure Functions: A solution for easily running small pieces of code in the cloud.
- IBM Cloud Functions: Based on Apache OpenWhisk, it allows event-driven programming on the IBM Cloud.

# Use Cases
- Microservices: Serverless is ideal for breaking down applications into small, manageable services.
- Real-Time File/Stream Processing: Functions can be triggered by data changes in storage or streams.
- Web Applications: Backend services for web applications can be implemented as serverless functions.
- Scheduled Tasks: Cron jobs or scheduled maintenance tasks can be handled efficiently.
- Chatbots and Voice Assistants: Serverless can power chatbots and voice interfaces with event-driven functions.

# Advantages
- Reduced Operational Complexity: No need to manage infrastructure.
- Cost Efficiency: Pay-as-you-go pricing model.
- Scalability: Automatic scaling based on demand.
- Faster Time to Market: Focus on writing code rather than managing servers.

# Disadvantages
- Cold Start Latency: Functions may experience latency when invoked for the first time.
- Limited Execution Duration: Functions typically have a maximum execution timeout.
- Vendor Lock-In: Applications may become dependent on a specific cloud provider's implementation.
- Complexity in Testing and Debugging: Distributed and event-driven nature can complicate testing and debugging.

# Example with Google Cloud Functions (Java)

- Go to Google Cloud Console and navigate to Cloud Functions.
- Create a new function and choose a runtime (e.g., Java 11).
- Configure the trigger type to HTTP.
- Write Function Code:

Java Cloud Function code that handles an HTTP POST request and returns a response.
```java
import com.google.cloud.functions.HttpFunction;
import com.google.cloud.functions.HttpRequest;
import com.google.cloud.functions.HttpResponse;
import com.google.gson.Gson;
import java.io.IOException;
import java.io.PrintWriter;

public class HelloWorld implements HttpFunction {

  private static final Gson gson = new Gson();

  @Override
  public MyResponse service(HttpRequest request, HttpResponse response) throws IOException {
    // Parse the incoming JSON body
    String requestBody = request.getReader().lines().reduce("", (s1, s2) -> s1 + s2);
    String name = gson.fromJson(requestBody, MyRequest.class).getName();

    // Prepare the response
    MyResponse responseBody = new MyResponse("Hello, " + name + "! Your HTTP request was successful!");

    // Set response properties
    response.setContentType("application/json");
    response.setStatusCode(200);
    PrintWriter writer = new PrintWriter(response.getWriter());
    writer.print(gson.toJson(responseBody));
    return responseBody;
  }

  // Define request and response classes
  @Getter
  @Setter
  @AllArgsConstructor    
  class MyRequest {
    private String name;
  }

  @Getter
  @Setter
  @AllArgsConstructor
  class MyResponse {
    private String message;
  }
}

```
Request
```curl
curl -X POST \
  https://region-project-id.cloudfunctions.net/function-name \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "Alice"
}'
```

Response
```json
{
  "message": "Hello, Alice! Your HTTP request was successful!"
}
```



# Serverless Architecture vs. Container Architecture

## Container Architecture

**Overview:**
- Containers are lightweight, standalone, and executable software packages that include everything needed to run a piece of software, including the code, runtime, libraries, and system tools.
- Containers use the host system's kernel but isolate the application's processes, ensuring that each container is independent of others.

**Advantages:**
1. **Portability:** Containers can run on any system that supports the container runtime, ensuring consistent environments across development, testing, and production.
2. **Isolation:** Containers provide a high level of process isolation, helping to prevent conflicts and enhance security.
3. **Efficiency:** Containers are lightweight and use fewer resources than virtual machines, allowing for higher density on the same hardware.
4. **Flexibility:** Full control over the runtime environment, enabling custom configurations and optimizations.

**Disadvantages:**
1. **Management Overhead:** Containers require orchestration tools (like Kubernetes) for managing deployment, scaling, and operations.
2. **Complexity:** Container orchestration can be complex and may require a steep learning curve.
3. **Security:** Containers share the host OS kernel, which can pose security risks if not properly managed.

**Use Cases:**
- Microservices architecture
- Continuous integration/continuous deployment (CI/CD) pipelines
- Applications requiring consistent environments across different stages
- Legacy application modernization

## Comparison

| Aspect                  | Serverless Architecture                               | Container Architecture                                   |
|-------------------------|-------------------------------------------------------|---------------------------------------------------------|
| **Cost Model**          | Pay-per-execution                                     | Pay for allocated resources                              |
| **Scaling**             | Automatic, event-driven scaling                       | Manual or automated scaling with orchestration tools     |
| **Deployment Speed**    | Fast deployment, less setup required                  | Slower, more setup needed                                |
| **Management**          | Minimal operational management                        | Requires management of orchestration and underlying infrastructure |
| **Execution Time**      | Typically limited by provider constraints             | No inherent limits, depends on resource allocation       |
| **Control**             | Limited control over the runtime environment          | Full control over the runtime environment                |
| **Isolation**           | Function-level isolation                              | Process-level isolation                                  |
| **Use Cases**           | Event-driven tasks, microservices, data processing    | Microservices, CI/CD, consistent environments            |

## Conclusion

- **Serverless architecture** is ideal for event-driven applications, microservices, and workloads that require automatic scaling without the need for managing infrastructure.
- **Container architecture** is suitable for applications that need consistent environments, full control over the runtime, and efficient resource utilization with container orchestration.
