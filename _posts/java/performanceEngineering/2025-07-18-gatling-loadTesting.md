---
title: Gatling - Microservices Load Testing
date: 2025-07-18 08:30:00
categories:
- Performance Engineering
tags:
- Performance
- Microservices
- Testing
- Load Testing
- Gatling
- Kafka
- HTTP
---

{% include toc title="Index" %}

## Detailed tutorials
[https://nitinkc.github.io/GatlingLearning/](https://nitinkc.github.io/GatlingLearning/)

## Introduction to Load Testing

Load testing is a critical aspect of performance engineering that simulates real-world user behavior
and system load to evaluate how your system behaves under stress. 

Gatling is a powerful open-source framework designed specifically for load testing microservices, 
with particular strength in testing HTTP and async systems like Kafka, NATS, EventHub.

### Why Load Testing Matters

Before deploying to production, you need to understand:
- **Capacity**: How many concurrent users can your system handle?
- **Performance**: How fast does your system respond under load?
- **Stability**: Does your system remain stable or degrade gracefully?
- **Bottlenecks**: Where are the performance constraints in your architecture?

## Part 1: Fundamental Concepts

### Performance Testing Types

| Type               | Purpose                                 | Load Pattern             | Use Case                  |
|:-------------------|:----------------------------------------|:-------------------------|:--------------------------|
| **Load Testing**   | Measure performance under expected load | Realistic, constant      | Normal operations         |
| **Stress Testing** | Find breaking point                     | Continuous increase      | System limits             |
| **Soak Testing**   | Long-running stability                  | Constant over hours/days | Memory leaks, degradation |
| **Spike Testing**  | Sudden traffic surge                    | Quick ramp to peak       | Black Friday scenarios    |

### Key Metrics to Monitor

#### Latency Metrics
**Latency** is the time taken to process a request from client to server and back. Understanding latency distribution is critical:

- **Mean Latency**: Average response time
  - Simple to understand but can hide outliers
  - Example: Mean = 100ms (but some requests took 5000ms!)

- **Median (p50)**: 50th percentile
  - Half of requests complete faster than this
  - Better than mean for non-normal distributions

- **p95 Latency**: 95th percentile
  - 95% of requests complete within this time
  - 5% of users experience worse performance
  - **Industry guideline**: For web apps, target <500ms; for APIs, <200ms

- **p99 Latency**: 99th percentile
  - 99% of requests complete within this time
  - Captures most extreme cases
  - **Industry guideline**: For web apps, target <1000ms; for APIs, <500ms

- **p99.9 Latency**: 99.9th percentile
  - Extreme outliers; indicates tail performance
  - Important for SLA compliance

**Example:**
```
If you have 10,000 requests:
- p95 = 300ms means 9,500 requests ≤ 300ms
- p99 = 800ms means 9,900 requests ≤ 800ms
- The remaining 100 requests (1%) took >800ms
```

#### Throughput Metrics

- **RPS (Requests Per Second)**: How many requests your system can handle per second
- **TPS (Transactions Per Second)**: Complete business transactions per second
- **Success Rate**: Percentage of successful requests (HTTP 2xx/3xx)
- **Error Rate**: Percentage of failed requests

#### Resource Metrics (monitored via Datadog)

- **CPU Utilization**: % of CPU used
- **Memory Usage**: RAM consumed
- **Network I/O**: Bytes sent/received
- **Disk I/O**: Read/write operations
- **Connection Pools**: Active database/service connections

## Part 2: Open Model Load Patterns

Open model patterns simulate **unlimited concurrent users** (open-ended), meaning the system keeps 
accepting new users without waiting for others to disconnect. 
This contrasts with closed models where a fixed number of users cycle through scenarios.

### OPEN_CONSTANT_LOAD

**Definition**: Maintain a constant rate of new requests per second throughout the test.

**Characteristics**:
- Fixed number of users entering the system per second
- Simulates consistent, predictable traffic
- Users don't leave; only new ones arrive
- Useful for: Baseline performance, API rate limits, steady-state behavior

**Real-World Scenario**:
- E-commerce website: 50 new customer sessions arriving every second
- Expected behavior: Consistent latency, predictable resource usage
- What to watch for: Degradation if queue builds up, eventual saturation

**Metrics to Observe**:
- Response time should remain stable
- Throughput should plateau at system capacity
- If latency increases linearly, system is saturating


### OPEN_RAMP_LOAD

**Definition**: Linearly increase the rate of new requests over time, from a starting rate to an ending rate.

**Characteristics**:
- Gradual increase in user arrival rate
- Simulates gradually increasing traffic (e.g., morning peak, event launch)
- Smooth transition helps identify at what point system starts degrading
- Useful for: Finding breaking points, capacity planning, stress testing

**Real-World Scenario**:
- Streaming service: 10 new viewers/sec ramping to 100 viewers/sec during prime time
- Event launch: Gradual increase as users discover and join
- What to watch for: The "elbow" point where latency starts increasing sharply

**Metrics to Observe**:
```
Time (sec) | Users/sec | p95 Latency | p99 Latency | CPU %
0-100      | 10        | 50ms        | 75ms        | 20%
100-300    | 35        | 80ms        | 120ms       | 35%
300-500    | 60        | 200ms       | 500ms       | 65%
500-600    | 100       | 1000ms      | 5000ms      | 95%  <- Saturation point
```

**Capacity Planning Example**:
- System handles up to 60 users/sec with acceptable latency
- At 100 users/sec, latency degrades unacceptably
- **Conclusion**: Provision infrastructure to handle 60 users/sec minimum, 80+ for headroom

### OPEN_STEP_LOAD

**Definition**: Increase load in discrete steps (stairs) rather than smoothly, holding each step for a duration before increasing.

**Characteristics**:
- Step-wise increase: e.g., 10 users → 20 users → 40 users
- Each step held for a fixed duration
- Allows system to stabilize at each level before increasing
- Useful for: Understanding behavior at specific load levels, system recovery, queue behavior

**Real-World Scenario**:
- Database deployment: Gradually increase load to watch query performance
- Cache warming: Step testing allows cache to populate at each level
- Microservice chain: Each step allows all services to adapt

**Metrics to Observe**:
- Latency at each step level
- Recovery time after each increase
- Resource utilization trends
- Queue depths and connection pool saturation

**Step Load Benefits**:
```
Step 1 (10 users): Baseline, system cold
  ↓ Wait 2 min: System warms up, caches fill
Step 2 (20 users): Can compare with baseline
  ↓ Wait 2 min: Observe stability
Step 3 (40 users): Performance degradation pattern emerges
  ↓ Eventually find breaking point
```
### Comparison: Constant vs Ramp vs Step

| Aspect                         | Constant       | Ramp                     | Step                     |
|:-------------------------------|:---------------|:-------------------------|:-------------------------|
| **User Arrival**               | Flat           | Linear                   | Stair-step               |
| **Test Duration**              | Flexible       | Longer (linear increase) | Moderate + plateaus      |
| **Best For**                   | Baseline tests | Finding capacity limits  | Understanding thresholds |
| **Load Predictability**        | High           | Increasing               | Staged                   |
| **System Recovery Observable** | No             | Ongoing                  | Yes, between steps       |
| **Real-world Match**           | Steady traffic | Gradual peak             | Multiple shift changes   |

## Part 3: Understanding Gatling Scenarios

A **scenario** in Gatling is the core building block that simulates a user journey.
It defines what actions a virtual user performs, in what order, with what data, and under what conditions.

### Scenario Execution Flow

When you run a Gatling simulation with a scenario, here's what happens:

```
1. Simulation Starts
   ↓
2. Protocol Configuration Loaded (baseUrl, headers, etc.)
   ↓
3. Feeders Initialized (CSV data, random generators, etc.)
   ↓
4. Virtual Users Spawned (according to injection profile)
   ├─ User 1 starts scenario
   ├─ User 2 starts scenario
   ├─ User 3 starts scenario
   └─ ... (up to configured load)
   ↓
5. Each User Executes Scenario Steps Sequentially
   ├─ Send request 1
   ├─ Wait/pause
   ├─ Send request 2
   ├─ Extract data from response
   └─ Continue until scenario ends
   ↓
6. User Completes One Iteration
   ↓
7. User Restarts Scenario (loops infinitely by default)
   ↓
8. All Users Stop When Test Duration Expires
```

### Scenario Structure

A scenario has three main components:

```java
ScenarioBuilder scenario = scenario("Scenario Name")
    // 1. SETUP: Initialize data/variables
    .exec(session -> {
        return session.set("userId", "user-123");
    })
    
    // 2. ACTION: Execute requests
    .exec(http("Request 1")
        .get("/api/users/#{userId}"))
    
    .pause(1, 3)  // Think time between requests
    
    // 3. EXTRACT: Parse response and store for next request
    .exec(http("Request 2")
        .get("/api/products")
        .check(jmesPath("$.items[0].id").saveAs("productId")))
    
    // 4. LOOP: Return to action or extract
    .repeat(5) {  // Repeat 5 times
        exec(http("Request 3")
            .post("/api/cart")
            .body(StringBody("{\"productId\":\"#{productId}\"}")))
    }
```

### Gatling Feeders: Data Injection
**Feeders** are how you provide external data to your scenarios (user IDs, email addresses, CSV records, etc.).
Without feeders, you'd be testing the same data repeatedly, which isn't realistic.

#### Feeder Types

##### 1. **Auto Feeder** (Built-in data generators)
Auto feeders generate random or sequential data on-the-fly:

**Example: kafkaCreateScenario**

In your configuration:
```json
{
    "scnName": "kafkaCreateScenario",
    "loadTPS": 100,
    "feederType": "auto"
}
```
This means: Generate 100 messages/sec with automatically generated data (sequential IDs, random values, timestamps, etc.).



##### 2. **CSV Feeder** (File-based data)

CSV feeders read data from files, allowing you to test with real-world data:

**Example: kafkaCreateDynamicScenario**

In configuration:
```json
{
    "scnName": "kafkaCreateDynamicScenario",
    "feederType": "csv",
    "feederFile": "test_feed"
}
```

This means: Load data from `test_feed.csv` and use those values in requests.

#### Feeder Variable Interpolation

When you use `#{variableName}` in requests, Gatling:
1. Looks up `variableName` in the current session
2. Replaces `#{variableName}` with the actual value
3. Sends the request with real data

```java
// From feeder: userId = "user-123"
scenario("Example")
    .feed(feeder)
    .exec(http("Get User")
        .get("/api/users/#{userId}"))  // Becomes: /api/users/user-123
    .exec(session -> {
        String userId = session.getString("userId");  // Access in code
        return session.set("userName", "John");
    })
    .exec(http("Update User")
        .post("/api/users/#{userId}")  // Still: /api/users/user-123
        .body(StringBody("{\"name\": \"#{userName}\"}")))  // "John"
```

### Scenario Lifecycle: Complete Example

Let's trace through a real scenario execution with your Kafka configuration:

```java
public class KafkaLoadTestSimulation extends Simulation {

    // 1. PROTOCOL CONFIGURATION
    KafkaProtocolBuilder kafkaProtocol = kafka
        .bootstrap.servers("kafka-broker:9092")
        .producerConfig(ProducerConfig.ACKS_CONFIG, "all");

    // 2. SCENARIO 1: Auto-generated data
    ScenarioBuilder kafkaCreateScenario = scenario("kafkaCreateScenario")
        // Feeder initialized here (creates data on-the-fly)
        .feed(autoDataFeeder())
        
        // Iteration starts: User gets data from feeder
        .exec(
            kafka("Send Message")
                .send("${EXEC_ENV}-domain-message-syndication")
                .messageKey("#{userId}")
                .payload(
                    """
                    {
                        "transactionId": "#{transactionId}",
                        "userId": "#{userId}",
                        "amount": #{amount}
                    }
                    """
                )
                // Verify message was sent
                .check(kafka.producerSentMessageStatus().is("OK"))
        )
        
        // Wait before next iteration
        .pause(Duration.ofMillis(1000 / 100))  // 100 TPS = 10ms between messages
        
        // Iteration ends, user loops back to feeder for next data
        ;

    // 3. SCENARIO 2: CSV-based data
    ScenarioBuilder kafkaCreateDynamicScenario = scenario("kafkaCreateDynamicScenario")
        // Feeder initialized: CSV file loaded
        .feed(csv("cope_feed.csv").circular())
        
        // Iteration starts: User gets row from CSV
        .exec(
            kafka("Send Dynamic Message")
                .send("${EXEC_ENV}-domain-message-syndication")
                .messageKey("#{accountId}")  // From CSV column
                .payload(
                    """
                    {
                        "copeName": "#{copeName}",
                        "accountId": "#{accountId}",
                        "amount": #{amount},
                        "region": "#{region}"
                    }
                    """
                )
                .check(kafka.producerSentMessageStatus().is("OK"))
        )
        
        .pause(Duration.ofMillis(1000 / 100))  // Same TPS
        ;

    // 4. SETUP: Define which scenarios to run and how
    {
        setUp(
            // kafkaCreateScenario: 100 messages/sec for 5 minutes
            kafkaCreateScenario.injectOpen(constantUsersPerSec(100).during(300))
                .andThen(
                    // After first scenario, run second scenario
                    kafkaCreateDynamicScenario.injectOpen(constantUsersPerSec(100).during(300))
                )
        )
        .protocols(kafkaProtocol)
        .assertions(
            global().successfulRequests().percent().gt(99.5)
        );
    }
```

### Scenario Execution Timeline

Here's what happens during execution with 100 TPS (messages per second):

```
Time     | User 1           | User 2           | User 3           | Notes
---------|------------------|------------------|------------------|------------------
0s       | Feed data 001    | Feed data 002    | Feed data 003    | 100 users created
         | Send msg 001     | Send msg 002     | Send msg 003     |
         | Wait 10ms        | Wait 10ms        | Wait 10ms        | 100 TPS = 10ms/msg
10ms     | Feed data 004    | Feed data 005    | Feed data 006    | Feeder cycles
         | Send msg 004     | Send msg 005     | Send msg 006     |
         | Wait 10ms        | Wait 10ms        | Wait 10ms        |
20ms     | ...continues...  | ...continues...  | ...continues...  | 100 msgs sent so far
...      |                  |                  |                  |
100ms    | Feed data 050    | Feed data 051    | Feed data 052    | 1000 msgs sent
...      |                  |                  |                  |
300s     | Test Duration    | Test Duration    | Test Duration    | Stops - all users exit
(5min)   | Exceeded         | Exceeded         | Exceeded         | Total: 30,000 msgs
```

### Key Points About Scenario Execution

1. **Each Virtual User is Independent**
   - User 1 and User 2 don't know about each other
   - Each has their own session and feeder data
   - They can pull from same CSV (which is fine) or have separate random data

2. **Feeders Provide Data Per Iteration**
   ```java
   // Iteration 1: Get row 1 from feeder
   .feed(csvFeeder)
   .exec(http("Request").post("/api/..."))
   
   // Loop back to feed() → Iteration 2: Get row 2 from feeder
   // (scenarios loop infinitely by default)
   ```

3. **Variable Scope is Per-Session**
   ```java
   .feed(csvFeeder)  // userId = "user-123" in this session
   .exec(session -> session.set("extraData", "value"))  // Add more data
   .exec(http("Request").get("/api/users/#{userId}"))  // Use both
   ```

4. **Pause/Think Time is Critical**
   - Simulates real users who don't hammer the server instantly
   - Without `pause()`, you test unrealistic conditions
   - With 100 TPS and `pause(10ms)`: 1000ms / 100 = 10ms between messages

5. **CSV Feeder Strategies**
   - `.circular()`: Loop back to start when exhausted
   - `.queue()`: Stop when exhausted (best for limited test data)
   - `.shuffle()`: Randomize order each cycle

### Scenario Configuration Mapping

Your configuration maps to Gatling like this:

```json
{
    "scnName": "kafkaCreateScenario",
    "templateRequestFile": "kfk_create.json",
    "path": "${EXEC_ENV}-rtdx-salestxn-syndication",
    "loadTPS": 100,
    "feederType": "auto"
}
```

Maps to:

```java
ScenarioBuilder kafkaCreateScenario = scenario("kafkaCreateScenario")
    .feed(autoDataFeeder())  // ← feederType: "auto"
    .exec(
        kafka("Send Message")
            .send("${EXEC_ENV}-rtdx-salestxn-syndication")  // ← path
            .payload(loadJsonTemplate("kfk_create.json"))  // ← templateRequestFile
    )
    .pause(Duration.ofMillis(1000 / 100));  // ← loadTPS: 100

setUp(
    kafkaCreateScenario.injectOpen(constantUsersPerSec(100).during(300))
)
```

### Advanced: Custom Feeders

For complex scenarios, create custom feeders:

```java
private Feeder<Object> customBusinessLogicFeeder() {
    return new Iterator<Map<String, Object>>() {
        @Override
        public boolean hasNext() { return true; }
        
        @Override
        public Map<String, Object> next() {
            Map<String, Object> data = new HashMap<>();
            
            // Custom logic: Generate realistic transaction
            String copeId = "COPE-" + (Math.random() * 100);
            double amount = 1000 + (Math.random() * 9000);  // $1000-$10000
            String timestamp = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss'Z'")
                .format(new Date());
            
            data.put("copeId", copeId);
            data.put("amount", amount);
            data.put("timestamp", timestamp);
            data.put("region", selectRandomRegion());
            
            return data;
        }
    };
}
```

## Part 3: HTTP Simulations (Request-Response)

HTTP load testing simulates synchronous request-response cycles, the most common pattern in microservices.

### Basic HTTP Simulation

```java
package simulations;

import io.gatling.javaapi.core.*;
import io.gatling.javaapi.http.*;
import static io.gatling.javaapi.core.CoreDsl.*;
import static io.gatling.javaapi.http.HttpDsl.*;

public class HttpApiSimulation extends Simulation {

    HttpProtocolBuilder httpProtocol = http
        .baseUrl("https://api.example.com")
        .contentTypeHeader("application/json")
        .acceptLanguageHeader("en-US,en;q=0.9");

    ScenarioBuilder scenario = scenario("API Users Scenario")
        .exec(
            http("GET /users")
                .get("/users")
                .check(status().is(200))
        )
        .pause(2) // Wait 2 seconds between requests
        .exec(
            http("POST /users")
                .post("/users")
                .body(StringBody("{\"name\":\"John\"}"))
                .check(status().is(201))
        );

    {
        setUp(scenario.injectOpen(constantUsersPerSec(10).during(300)))
            .protocols(httpProtocol);
    }
}
```

### HTTP Simulation with Assertions and Metrics

```java
public class HttpLoadSimulation extends Simulation {

    HttpProtocolBuilder httpProtocol = http
        .baseUrl("https://api.example.com")
        .acceptHeader("application/json");

    ScenarioBuilder userJourney = scenario("E-commerce Journey")
        .exec(http("Browse Products")
            .get("/products")
            .queryParam("page", "1")
            .check(status().is(200))
            .check(jmesPath("$.total").exists()))
        .pause(1, 3)
        .exec(http("View Product Details")
            .get("/products/#{productId}")
            .check(status().is(200)))
        .pause(2, 5)
        .exec(http("Add to Cart")
            .post("/cart")
            .body(StringBody("{\"productId\":\"#{productId}\",\"quantity\":1}"))
            .check(status().is(200)))
        .pause(1, 2);

    {
        setUp(
            userJourney.injectOpen(rampUsersPerSec(5).to(50).during(600))
        )
        .protocols(httpProtocol)
        .assertions(
            global().responseTime().p95().lt(500),      // p95 latency < 500ms
            global().responseTime().p99().lt(1000),     // p99 latency < 1s
            global().successfulRequests().percent().gt(99.0)  // >99% success rate
        );
    }
}
```

### Observing HTTP Metrics with Datadog

When running HTTP simulations:
1. **Instrument your API** with Datadog APM
2. **Metrics to capture**:
   - Request latency (p50, p95, p99)
   - Response status codes (200, 500, etc.)
   - Error rates
   - Throughput (requests/sec)
   - Database query times
   - External service call times

3. **Example Datadog Dashboard Query**:
```
trace_analytics { service:my-api | stats avg(duration), p99(duration), count() by http.status_code }
```

## Part 4: Kafka Simulations (Event-Driven)

Kafka load testing differs fundamentally from HTTP testing—it's about testing **asynchronous event streams**, producer throughput, consumer lag, and message ordering.

### Key Differences: HTTP vs Kafka

| Aspect          | HTTP                           | Kafka                                  |
|:----------------|:-------------------------------|:---------------------------------------|
| **Pattern**     | Request-Response (synchronous) | Pub-Sub (asynchronous)                 |
| **Latency**     | End-to-end (request+response)  | Produce latency + consumer lag         |
| **Measurement** | Response time                  | Time-to-message + processing lag       |
| **Success**     | HTTP 200 response              | Message consumed and processed         |
| **Failure**     | HTTP error code                | Message lost, lag, partition rebalance |
| **Load Model**  | Concurrent users               | Messages/sec per partition             |

### Kafka Simulation Concepts

#### What to Load Test in Kafka

1. **Producer Load**:
   - How many messages/sec can producers push?
   - Message size impact
   - Acks configuration (0, 1, all)
   - Compression impact

2. **Consumer Load**:
   - Consumer lag under different throughputs
   - Rebalance impact
   - Fetch group behavior
   - Consumer processing time

3. **Broker Load**:
   - Partition leadership changes
   - Replication lag
   - Disk I/O
   - Network saturation

#### Example: Kafka Producer Simulation

```java
package simulations;

import io.gatling.core.Predef.*;
import io.gatling.kafka.Predef.*;
import org.apache.kafka.clients.producer.ProducerConfig;

import static io.gatling.core.Predef.*;
import static io.gatling.kafka.Predef.*;

public class KafkaProducerSimulation extends Simulation {

    KafkaProtocolBuilder kafkaProtocol = kafka
        .bootstrap.servers("localhost:9092")
        .producerConfig(ProducerConfig.ACKS_CONFIG, "all")  // Wait for all replicas
        .producerConfig(ProducerConfig.COMPRESSION_TYPE_CONFIG, "snappy");

    ScenarioBuilder producerScenario = scenario("Kafka Producer Load")
        .exec(
            kafka("Send Event")
                .send("user-events")  // Topic
                .messageKey("user-123")  // Partition key
                .payload(
                    """
                    {
                        "userId": "user-123",
                        "action": "click",
                        "timestamp": "${timestamp}"
                    }
                    """
                )
                .check(kafka.producerSentMessageStatus().is("OK"))
        )
        .pause(100, 500);  // 100-500ms between events

    {
        setUp(
            producerScenario.injectOpen(constantUsersPerSec(100).during(600))
        )
        .protocols(kafkaProtocol)
        .assertions(
            global().successfulRequests().percent().gt(99.5)  // >99.5% messages sent
        );
    }
}
```

#### Example: Kafka Consumer Simulation (Consumer Lag Testing)

```java
public class KafkaConsumerSimulation extends Simulation {

    KafkaProtocolBuilder kafkaProtocol = kafka
        .bootstrap.servers("localhost:9092")
        .consumerConfig("group.id", "gatling-consumer-group")
        .consumerConfig("auto.offset.reset", "earliest");

    ScenarioBuilder consumerScenario = scenario("Kafka Consumer Processing")
        .exec(
            kafka("Consume Events")
                .consume("user-events")  // Topic
                .maxDurationInSeconds(300)
                .printReceivedMessages(false)
        );

    {
        setUp(
            consumerScenario.injectOpen(constantUsersPerSec(50).during(600))
        )
        .protocols(kafkaProtocol)
        .assertions(
            global().responseTime().p95().lt(5000),  // Processing lag p95 < 5s
            global().responseTime().p99().lt(10000)  // Processing lag p99 < 10s
        );
    }
}
```

### Kafka Load Testing Metrics

When testing Kafka with Datadog:

1. **Producer Metrics**:
   - `kafka.producer.records_per_sec`: Messages produced per second
   - `kafka.producer.byte_rate`: Bytes sent per second
   - `kafka.producer.request_latency`: Latency of producer requests (p95, p99)
   - `kafka.producer.failed_sends`: Failed message counts

2. **Consumer Metrics**:
   - `kafka.consumer.lag`: How far behind consumers are
   - `kafka.consumer.records_consumed_rate`: Messages consumed per second
   - `kafka.consumer.fetch_latency`: Time to fetch batch of messages
   - `kafka.consumer_group.rebalance_latency`: Rebalance duration

3. **Broker Metrics**:
   - `kafka.replication.under_replicated_partitions`: Partition replication issues
   - `kafka.broker.disk_used`: Disk space consumed
   - `kafka.network.bytes_in_per_sec` / `bytes_out_per_sec`: Network I/O

### Typical Kafka Load Test Scenarios

#### Scenario 1: Constant Producer Load
```java
// Simulate 1000 events/sec continuously for real-time analytics
injectOpen(constantUsersPerSec(1000).during(600))
```
**Metrics**: Measure producer latency, broker CPU, and replication lag

#### Scenario 2: Consumer Lag Catchup
```java
// Produce 5000 msg/sec for 60 sec, then 100 msg/sec for consumers to catch up
.injectOpen(
  constantUsersPerSec(5000).during(60),
  constantUsersPerSec(100).during(600)
)
```
**Metrics**: Observe how long consumers take to reach equilibrium

#### Scenario 3: Spike Test (Event)
```java
// Normal: 100 msg/sec, then sudden spike to 10,000 msg/sec
.injectOpen(
  constantUsersPerSec(100).during(60),
  rampUsersPerSec(100).to(10000).during(30),
  constantUsersPerSec(10000).during(60)
)
```
**Metrics**: Check for message loss, rebalances, and broker recovery time

## Part 5: Performance Targets and SLAs

### Recommended Latency SLAs

| Service Type | p95 Target | p99 Target | p99.9 Target |
|--------------|-----------|-----------|--------------|
| **User-Facing Web** | <300ms | <1000ms | <3000ms |
| **Mobile App API** | <200ms | <500ms | <2000ms |
| **Internal Service** | <100ms | <300ms | <1000ms |
| **Batch Processing** | <5000ms | <30000ms | N/A |
| **Real-time Analytics** | <1000ms | <5000ms | <30000ms |
| **Kafka Event Stream** | <100ms (produce) | <500ms (produce) | <500ms (consumer lag per msg) |

### Error Rate Targets

- **Acceptable**: <0.1% error rate (99.9% success)
- **Good**: <0.01% error rate (99.99% success)
- **Excellent**: <0.001% error rate (99.999% success, "five nines")

### Sample Datadog Monitors

```json
{
  "name": "High p99 Latency Alert",
  "type": "metric alert",
  "query": "avg:trace.web.request.duration{service:my-api,resource_name:/api/users}.percentile(99) > 1000",
  "threshold": 1000,
  "alert_message": "p99 latency exceeded 1 second"
}
```

```json
{
  "name": "Kafka Consumer Lag Alert",
  "type": "metric alert",
  "query": "avg:kafka.consumer_group.lag{group:my-consumer-group} > 10000",
  "threshold": 10000,
  "alert_message": "Consumer lag exceeded 10k messages"
}
```

## Part 6: Running Gatling Tests with Results Analysis

### Running the Simulation

```bash
# Navigate to your Gatling project
cd ~/gatling-project

# Run HTTP simulation
mvn gatling:test -Dgatling.simulationClass=simulations.HttpLoadSimulation

# Run Kafka simulation
mvn gatling:test -Dgatling.simulationClass=simulations.KafkaProducerSimulation
```

### Reading Gatling Results

After test completion, open the HTML report:
```
target/gatling/[simulation-name]-[timestamp]/index.html
```

Key sections:
1. **Global Stats**: Overall p50, p75, p95, p99, max latencies
2. **Request Name**: Breakdown by endpoint/topic
3. **Response Time Distribution**: Histogram of response times
4. **Requests/Responses**: Success rate, errors over time
5. **Scenario**: User ramp-up over time

### Integration with Datadog

1. **Install Datadog Agent** on load test machine
2. **Tag metrics**:
   ```java
   // In your Gatling simulation
   httpProtocol.header("x-test-id", "gatling-load-test-001")
   ```
3. **Query results**:
   ```
   avg:trace.web.request.duration{x-test-id:gatling-load-test-001} by http.status_code
   ```

## Part 7: Best Practices and Common Pitfalls

### Best Practices

1. **Baseline First**: Run constant load test to establish baseline metrics
2. **Ramp Gradually**: Never jump directly to max load; use ramp tests
3. **Realistic Scenarios**: Simulate actual user behavior (think times, realistic payloads)
4. **Monitor System Under Test**: Use Datadog to watch CPU, memory, disk I/O during tests
5. **Run Multiple Iterations**: One test doesn't tell the full story; repeat 3-5 times
6. **Test in Staging First**: Never surprise production with load tests
7. **Define Acceptance Criteria**: What are your p95/p99 targets before testing?
8. **Profile Under Load**: Use Datadog APM to find slow queries and services

### Common Pitfalls

1. **Not Using Realistic Think Times**: Batching all requests too quickly
   ```java
   // Bad: No think time
   scenario.exec(http("Call 1").get("/api/1"))
           .exec(http("Call 2").get("/api/2"));
   
   // Good: Realistic delays
   scenario.exec(http("Call 1").get("/api/1"))
           .pause(2, 5)  // 2-5 second think time
           .exec(http("Call 2").get("/api/2"));
   ```

2. **Load Testing from Single Machine**: Single machine becomes bottleneck
   - Solution: Use Gatling Enterprise or distributed testing

3. **Ignoring Warm-up**: JVM, caches need time to initialize
   - Solution: Run 5-10 min constant load before actual test

4. **Wrong Metrics**: Focusing only on mean latency
   - Solution: Always track p95, p99, p99.9 percentiles

5. **Not Testing Failure Scenarios**: Only testing happy path
   - Solution: Include error injection, chaos testing (10% errors)

## Summary: The Load Testing Workflow

```
1. Define Objectives
   ├─ Target latency (p95, p99)
   ├─ Expected load (users/sec or msg/sec)
   └─ Acceptable error rate

2. Design Simulation
   ├─ Baseline constant load test (5 min)
   ├─ Ramp test to find breaking point (10 min)
   └─ Soak test to check stability (30-60 min)

3. Execute Test
   ├─ Monitor system metrics (Datadog)
   ├─ Watch application logs
   └─ Record results

4. Analyze Results
   ├─ Compare against objectives
   ├─ Identify bottlenecks
   └─ Check Datadog traces for slow services

5. Optimize & Re-test
   ├─ Tune database queries
   ├─ Scale services
   ├─ Increase connection pools
   └─ Repeat testing
```

Understanding TPS of 200, 500 and 1000 :
TPS (Transactions Per Second) = messages sent to Kafka per second from your load test.
In an open workload model (which dps-load code uses), Gatling injects requests at a fixed rate regardless of service backpressure (i.e., it keeps sending at the target rate and measures failures/latency).
For Kafka, one “transaction” is typically one message (one send() call), so 200 TPS = 200 messages/sec across the specified topics.

Intended Target : COPe should be able to process double the amount of production traffic (~1000tps)

Steps to hit ~1000 TPS (double production Load)

setLOAD MULTIPLIER WITH RESPECT TO PROD VOLUME=2 or set the scenario LOAD_TPS to 1000 explicitly (in the pipleline)
Run for a meaningful duration (e.g., 10–30 minutes) to observe stability, not just spikes.
Confirm achieved TPS in Datadog 

## Part 8: Datadog Traces, Operations, and Annotations

### What is a Trace in Datadog?

A **trace** is a complete record of a request's journey through your entire distributed system, from the initial entry point to the final response. Instead of looking at metrics in isolation, traces show you exactly what happened at every step.

#### Trace Anatomy

```
Incoming Request (HTTP)
    ↓
Entry Service (Trace Starts)
    ├─ Operation 1: Authenticate User
    │   └─ Span: Check cache
    │   └─ Span: Query database
    │
    ├─ Operation 2: Validate Request
    │   └─ Span: Schema validation
    │
    ├─ Operation 3: Call Downstream Service A
    │   └─ Span: Network call to Service A
    │       └─ Nested Operation in Service A: Process Data
    │           └─ Span: Database query
    │           └─ Span: Cache write
    │
    ├─ Operation 4: Call Downstream Service B
    │   └─ Span: Network call to Service B
    │       └─ Nested Spans in Service B
    │
    └─ Operation 5: Build Response
        └─ Span: Serialize response
    ↓
Response Sent (Trace Ends)
```

**Key Point**: A trace is the entire flow; **operations** are logical groupings; **spans** are individual units of work.

### Spans vs Operations vs Traces

| Term | Definition | Example |
|:-----|:-----------|:--------|
| **Trace** | Complete request journey across all services | `GET /api/orders` start-to-finish |
| **Span** | Individual unit of work (database query, network call, function execution) | `db.query: SELECT * FROM orders` |
| **Operation** | Named logical grouping of spans (request handler, method call) | `POST /api/orders`, `userService.authenticateUser()` |
| **Service** | The application/microservice doing the work | `order-api`, `user-service`, `payment-service` |

**Visual Example**:

```
Trace ID: abc123def456
├─ Span 1: request_handler (operation: POST /api/orders)
│   ├─ Span 1.1: auth_check (operation: authenticate_user)
│   │   ├─ Span 1.1.1: redis_get (operation: cache_lookup)
│   │   │   Duration: 2ms
│   │   │   Tags: cache_hit=true
│   │   └─ [Redis returns user cached]
│   │   Duration: 3ms total
│   │
│   ├─ Span 1.2: validate_order (operation: validate_request)
│   │   ├─ Span 1.2.1: schema_validate
│   │   │   Duration: 1ms
│   │   └─ [JSON schema validation]
│   │   Duration: 1ms total
│   │
│   ├─ Span 1.3: rpc_call_payment_service (operation: process_payment)
│   │   Service: payment-service
│   │   Duration: 150ms
│   │   └─ [Includes nested spans from payment-service]
│   │
│   └─ [All child spans completed]
│   Duration: 156ms total (entire request)
└─ [Response sent]
```

### What are Operations?

An **operation** is a name you assign to a span that describes the work being done. It's how Datadog groups similar work together.

#### Examples of Operations

```java
// HTTP Request Operation
span.setOperationName("GET /api/users/{id}")  // Operation shows the HTTP method + path

// Database Operation
span.setOperationName("db.query.select")  // What kind of DB operation

// Cache Operation
span.setOperationName("redis.get")  // What cache system and operation

// RPC/Service Call Operation
span.setOperationName("payment-service.process_payment")  // Service.method

// Message Queue Operation
span.setOperationName("kafka.send")  // Queue type and operation

// Custom Operation
span.setOperationName("calculate_discount")  // Business logic
```

#### How to Set Operations in Code

```java
import io.opentelemetry.api.trace.Tracer;
import io.opentelemetry.api.trace.Span;

public class OrderService {
    
    private final Tracer tracer;
    
    public OrderService(Tracer tracer) {
        this.tracer = tracer;
    }
    
    public Order processOrder(String orderId) {
        // Create a span with operation name
        Span span = tracer.spanBuilder("process_order")
            .setAttribute("order.id", orderId)
            .setAttribute("service", "order-api")
            .startSpan();
        
        try {
            // Your business logic
            Order order = fetchOrder(orderId);
            
            // Nested span (child operation)
            Span paymentSpan = tracer.spanBuilder("process_payment")
                .setParent(span)
                .setAttribute("payment.amount", order.getTotal())
                .startSpan();
            
            try {
                processPayment(order);
            } finally {
                paymentSpan.end();
            }
            
            return order;
        } finally {
            span.end();
        }
    }
}
```

### What are Annotations in Datadog?

**Annotations** are markers or tags you add to spans to provide context and searchability. They help you filter, search, and group traces in Datadog.

#### Types of Annotations (Tags)

1. **Standard Tags** (Datadog-defined):
   ```java
   span.setTag("http.method", "POST");        // HTTP method
   span.setTag("http.status_code", 200);      // Response status
   span.setTag("http.url", "/api/orders");    // Request URL
   span.setTag("span.kind", "client");        // Type of span
   span.setTag("error", true);                // Marks span as error
   span.setTag("error.message", "Timeout");   // Error details
   ```

2. **Custom Tags** (application-specific):
   ```java
   span.setTag("user.id", "user-123");
   span.setTag("order.id", "order-456");
   span.setTag("environment", "production");
   span.setTag("feature.flag", "new-checkout");
   span.setTag("cache.hit", true);
   span.setTag("database.rows_affected", 5);
   ```

3. **Performance Tags**:
   ```java
   span.setTag("db.rows_returned", 100);
   span.setTag("api.response_size_bytes", 4096);
   span.setTag("queue.message_size", 1024);
   span.setTag("cache.operation", "set");
   span.setTag("retry.attempt", 2);
   ```

#### Example: Adding Annotations to HTTP Requests

```java
import io.opentelemetry.instrumentation.annotations.WithSpan;
import io.opentelemetry.api.trace.Span;
import io.opentelemetry.api.common.Attributes;

@RestController
@RequestMapping("/api/orders")
public class OrderController {
    
    @PostMapping
    public ResponseEntity<Order> createOrder(@RequestBody OrderRequest request) {
        Span span = Span.current();
        
        // Add context about the request
        span.setAllAttributes(Attributes.builder()
            .put("http.request.body_size", request.toString().length())
            .put("customer.id", request.getCustomerId())
            .put("order.total_amount", request.getTotal())
            .put("order.item_count", request.getItems().size())
            .put("shipping.region", request.getRegion())
            .build());
        
        try {
            Order savedOrder = orderService.saveOrder(request);
            
            // Annotate success
            span.setAllAttributes(Attributes.builder()
                .put("order.creation_success", true)
                .put("order.id", savedOrder.getId())
                .build());
            
            return ResponseEntity.status(201).body(savedOrder);
        } catch (Exception e) {
            // Annotate error
            span.setAllAttributes(Attributes.builder()
                .put("error", true)
                .put("error.type", e.getClass().getName())
                .put("error.message", e.getMessage())
                .build());
            throw e;
        }
    }
}
```

### Client All Operations: What HTTP Requests Show

When Datadog instruments your application, it automatically captures information about **all HTTP operations** your application makes (outbound to other services). This is called **client-side tracing**.

#### HTTP Request Information Captured

```
Outbound HTTP Call from Service A → Service B:

Operation Name: POST https://payment-service:8080/api/process-payment

Span Details:
├─ Duration: 145ms
├─ Status: 200 OK
├─ Method: POST
├─ URL: https://payment-service:8080/api/process-payment
├─ Request Headers:
│   ├─ Content-Type: application/json
│   ├─ Authorization: Bearer token...
│   └─ X-Trace-ID: abc123def456
├─ Request Body Size: 512 bytes
├─ Response Status: 200
├─ Response Headers:
│   ├─ Content-Type: application/json
│   └─ X-Response-Time: 140ms
├─ Response Body Size: 1024 bytes
├─ Downstream Service: payment-service
└─ Tags:
    ├─ http.status_code: 200
    ├─ http.method: POST
    ├─ http.url: /api/process-payment
    ├─ peer.service: payment-service
    ├─ span.kind: client
    └─ error: false
```

#### What Data You Can Extract

**1. Service Dependencies**:
```
From traces you can see:
- order-api calls → payment-service (all HTTP calls)
- payment-service calls → bank-gateway (all external APIs)
- user-service calls → cache (Redis)
- All network paths and communication patterns
```

**2. Latency Breakdown**:
```
Request to order-api: GET /api/orders
├─ Request parsing: 1ms
├─ Authentication: 3ms
├─ Validate: 1ms
├─ Call payment-service: 145ms  ← Slowest part!
│   └─ payment-service processes: 140ms
├─ Database write: 5ms
└─ Response serialization: 2ms
Total: 157ms
```

**3. Error Propagation**:
```
Request failed at:
- order-api calls payment-service
  - payment-service calls bank-gateway
    - bank-gateway returns 500 (timeout)
  - payment-service returns 503 (propagated error)
- order-api returns 503 to client

Error trace: bank-gateway timeout → payment-service error → order-api error
```

**4. Database Queries Called**:
```
When order-service calls database:
├─ db.query: SELECT * FROM users WHERE id = ?
│   ├─ Duration: 5ms
│   ├─ Rows returned: 1
│   └─ Database: PostgreSQL
├─ db.query: INSERT INTO orders (...)
│   ├─ Duration: 8ms
│   └─ Rows affected: 1
└─ db.query: UPDATE inventory SET stock = stock - 1
    ├─ Duration: 3ms
    └─ Rows affected: 1

Total database time: 16ms (out of 157ms total)
```

**5. Cache Operations**:
```
Cache calls made during request:
├─ redis.get: user:123
│   ├─ Duration: 2ms
│   └─ cache.hit: true  ← Came from cache!
├─ redis.set: order:456
│   ├─ Duration: 1ms
│   └─ ttl: 3600
└─ redis.del: user:123:temp
    ├─ Duration: 1ms
    └─ [Deleted temporary cache]

Cache hit rate from traces: 85% ✓ (good)
```

### Tracing Architecture in Datadog

```
Your Application (with APM Agent)
│
├─ Generates Spans (automatic instrumentation)
│  ├─ HTTP requests/responses
│  ├─ Database queries
│  ├─ Cache operations
│  ├─ Message queue sends/receives
│  └─ Custom code (manual instrumentation)
│
├─ Adds Tags/Annotations
│  ├─ service name
│  ├─ environment (prod/staging)
│  ├─ span.kind (server/client)
│  ├─ http.status_code
│  ├─ error (true/false)
│  └─ custom business tags
│
└─ Sends to Datadog Agent → Datadog Backend
   │
   └─ Datadog Processes Traces
      ├─ Correlates spans by trace ID
      ├─ Builds trace waterfall view
      ├─ Calculates latencies
      ├─ Detects errors and anomalies
      └─ Stores for querying
```

### Example: Complete Trace Analysis During Load Test

During your Gatling load test targeting 1000 TPS, you'd see traces like this:

```
Trace ID: load-test-xyz-001
Request: POST /api/transaction (from Gatling at t=0s)

Timeline:
0ms   → Request enters order-api
        Operation: handle_create_transaction
        Tags: load_test=true, scenario=kafkaCreateScenario

2ms   → order-api checks cache
        Operation: redis.get
        Tags: cache_key=user:123, cache.hit=true
        Duration: 2ms

4ms   → Validate transaction
        Operation: validate_transaction
        Duration: 2ms

6ms   → Call payment-service (RPC)
        Operation: POST /payment/authorize
        Tags: peer.service=payment-service
        Duration: 140ms  ← This is slow!
        
        Inside payment-service (nested):
        ├─ Validate payment: 10ms
        ├─ Check fraud service: 60ms  ← Even slower!
        │   └─ fraud-service calls external API: 55ms
        ├─ Database insert: 5ms
        └─ Return: 65ms

146ms → order-api writes to Kafka
        Operation: kafka.produce
        Topic: rtdx-salestxn-syndication
        Duration: 5ms
        Tags: partition=0, message_size=512bytes

151ms → order-api sends response
        Total trace duration: 151ms
        Tags: http.status_code=200, success=true
```

**Insights from this trace**:
- Total latency: 151ms (acceptable)
- Slowest operation: fraud-service (60ms)
  - **Action**: Scale fraud-service or add caching
- Network calls: payment-service is a bottleneck
  - **Action**: Consider batch processing
- Kafka write: Very fast (5ms)
  - **Status**: ✓ Good

### How to Query Traces in Datadog

Once traces are collected, you can query them to answer questions:

```
1. Find all slow requests (p95 > 500ms):
   trace:
     duration:[500ms TO *]
     service:order-api

2. Find all failed Kafka operations:
   trace:
     error:true
     resource_name:"kafka.produce"

3. Find requests where downstream service was slow:
   trace:
     service:payment-service
     duration:[100ms TO *]

4. Find traces for specific load test:
   trace:
     tags.load_test:true
     tags.scenario:kafkaCreateScenario

5. Correlate high latency with high CPU:
   trace:
     duration:[500ms TO *]
   correlate with
   metric:system.cpu.user > 80%
```

### Setting Up Datadog APM for Your Application

#### Java/Spring Boot Setup

```xml
<!-- In pom.xml -->
<dependency>
    <groupId>com.datadoghq</groupId>
    <artifactId>dd-java-agent</artifactId>
    <version>latest</version>
</dependency>
```

```bash
# Run your application with Datadog agent
java -javaagent:dd-java-agent.jar \
     -Ddd.service=order-api \
     -Ddd.env=staging \
     -Ddd.version=1.0.0 \
     -Ddd.trace.sample.rate=0.5 \
     -jar application.jar
```

```java
// Manual instrumentation for custom operations
import com.datadoghq.trace.api.TracingContextFactory;
import com.datadoghq.trace.api.DDTracer;

public class CustomService {
    
    private static final DDTracer tracer = TracingContextFactory.getDDTracer();
    
    public void customOperation() {
        try (DDSpan span = tracer.traceWithSpan("my_custom_operation", () -> {
            span.setTag("user.id", "123");
            span.setTag("operation.type", "custom");
            
            // Your code here
            doWork();
        })) {
            // Span automatically closed
        }
    }
}
```

### Dashboard Query Examples for Load Testing

```
# Monitor HTTP Request Latencies During Test
trace.web.request.duration
  service:order-api
  by http.resource_name
```

```
# Track Kafka Production Rate
trace.kafka.produce.duration
  service:order-api
  by topic
  .as_count()
```

```
# Find Error Spikes During Load
trace.errors
  service:*
  where load_test:true
  over 1m
  .rollup(60)
```

```
# Correlate Slow Traces with High CPU
trace:
  duration > 500ms AND service:order-api
CORRELATED WITH
metric:system.cpu.user > 80%
```

## Conclusion

Gatling provides a powerful framework for load testing microservices:
- **HTTP simulations** validate synchronous API performance
- **Kafka simulations** test asynchronous event stream capacity
- **Open model patterns** (constant, ramp, step) progressively reveal system behavior
- **Latency percentiles** (p95, p99) tell the real performance story
- **Datadog traces** show exactly where time is spent in your system during tests
- **Operations and annotations** provide searchability and context for trace data

Start with baseline constant load tests, progress to ramp tests, then use step tests for detailed analysis. Always monitor your systems with Datadog traces to catch bottlenecks and understand service dependencies. Use trace data to drive optimization decisions.
