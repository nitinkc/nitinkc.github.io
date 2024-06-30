---
title:  "Serverless Architecture"
date:   2024-06-29 21:02:00
categories: [System Design]
tags: [System Design]
---
{% include toc title="Index" %}

One of the most popular serverless architectures is Function as a Service (FaaS)

Each function will perform a specific task when triggered by an event, such as an incoming email or an HTTP reques

When a function is invoked, the cloud provider either executes the function on a running server, or, if there is no server currently running, it spins up a new server to execute the function.

Serverless architecture is a cloud computing execution model where the cloud provider dynamically manages the allocation and provisioning of servers. Despite the name, servers are still used, but developers don't have to manage them. Instead, they focus on writing code.

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

**Function Deploymen**t: Developers write functions and deploy them to a serverless platform.

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
Microservices: Serverless is ideal for breaking down applications into small, manageable services.
Real-Time File/Stream Processing: Functions can be triggered by data changes in storage or streams.
Web Applications: Backend services for web applications can be implemented as serverless functions.
Scheduled Tasks: Cron jobs or scheduled maintenance tasks can be handled efficiently.
Chatbots and Voice Assistants: Serverless can power chatbots and voice interfaces with event-driven functions.

# Advantages
Reduced Operational Complexity: No need to manage infrastructure.
Cost Efficiency: Pay-as-you-go pricing model.
Scalability: Automatic scaling based on demand.
Faster Time to Market: Focus on writing code rather than managing servers.

# Disadvantages
Cold Start Latency: Functions may experience latency when invoked for the first time.
Limited Execution Duration: Functions typically have a maximum execution timeout.
Vendor Lock-In: Applications may become dependent on a specific cloud provider's implementation.
Complexity in Testing and Debugging: Distributed and event-driven nature can complicate testing and debugging.


# Example with Google Cloud Functions (Java)

Go to Google Cloud Console and navigate to Cloud Functions.

Create a new function and choose a runtime (e.g., Java 11).

Configure the trigger type to HTTP.
Write Function Code:

Below is a basic example of a Java Cloud Function that handles an HTTP POST request and returns a response.
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
  public String service(HttpRequest request, HttpResponse response) throws IOException {
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
  }

  // Define request and response classes
  @Getter
  @Setter
  @AllArgsConstructor    
  static class MyRequest {
    private String name;
  }

  @Getter
  @Setter
  @AllArgsConstructor
  static class MyResponse {
    private String message;
  }
}

```

```curl
curl -X POST \
  https://region-project-id.cloudfunctions.net/function-name \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "Alice"
}'
```

```json
{
  "message": "Hello, Alice! Your HTTP request was successful!"
}
```