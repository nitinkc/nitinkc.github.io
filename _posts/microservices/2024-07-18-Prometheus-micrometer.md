---
title:  "Prometheus/Micrometer"
date:   2024-07-18 17:00:00
categories: Spring Microservices
tags: [Spring Microservices, Spring Boot]
---
{% include toc title="Index" %}

In Prometheus, metrics can be categorized into several types based on the **nature of the data** they represent.

# Counter
A counter is a cumulative metric that represents a single numerical value that only ever goes up (and resets when the process restarts). Counters are typically used to represent counts of events or increments over time.

```java
private final MeterRegistry meterRegistry;
private Counter requestCounter;
private final LicenseService licenseService;

  @PostConstruct
  public void initializeMetrics() {
    // Counter
    requestCounter = Counter.builder("a_counter_http_requests_total")
            .description("Number of times the job request run")
            .tags("licenseJobCounter", "example")
            .register(meterRegistry);

      // Schedule task to simulate user arrivals
      Executors.newSingleThreadScheduledExecutor()
              .scheduleAtFixedRate(this::processRequest, 0, 100, TimeUnit.SECONDS);
  }

// Example method using Counter
public void processRequest() {
    licenseService.runJob();
    requestCounter.increment();
}
```
# Gauge
A gauge is a metric that represents a single numerical value that can arbitrarily go up and down. Gauges are used for measured values like temperatures or current memory usage, where the value can both increase and decrease.
```java
private final MeterRegistry meterRegistry;
AtomicInteger activeUsers = new AtomicInteger(0);
private Gauge activeUsersGauge;

@PostConstruct
public void initializeMetrics() {
activeUsersGauge =
    Gauge.builder("a_guage_active_users", activeUsers, AtomicInteger::get)
        .description("Number of active users")
        .register(meterRegistry);

// Schedule task to simulate user arrivals
ScheduledExecutorService executorService = Executors.newSingleThreadScheduledExecutor();
executorService.scheduleAtFixedRate(this::userLoggedIn, 0, 1, TimeUnit.SECONDS);
}

// Example method using Gauge
public int userLoggedIn() {
    return activeUsers.incrementAndGet();
}
```
# Summary
Similar to a histogram, a summary samples observations (usually durations or sizes) over a sliding time window and calculates configurable quantiles over these samples.

```java
private final MeterRegistry meterRegistry;
private DistributionSummary responseSizesSummary;

@PostConstruct
public void initializeMetrics() {
    // Distribution Summary (Summary)
    responseSizesSummary = DistributionSummary.builder("a_summary_http_response_sizes")
            .description("Distribution of HTTP response sizes")
            .baseUnit("bytes")
            .register(meterRegistry);

    processHttpResponse();
}

// Example method using Distribution Summary (Summary)
public void processHttpResponse() {
    int simulateHttpResponseSize = (int) (Math.random() * 1000);
    // Simulate processing and get response size
    responseSizesSummary.record(simulateHttpResponseSize);
}
```
# Histogram
A histogram samples observations (usually durations or sizes) and counts them in configurable buckets. It also provides a sum of all observed values.


# Untyped
Untyped metrics are similar to gauges, but they don't have a specified type. They can be used when the value semantics don't fit the typical gauge or counter models.
```java
private final MeterRegistry meterRegistry;
private final AtomicLong customValue = new AtomicLong(0);
private final LicenseService licenseService;
@PostConstruct
public void initializeMetrics() {
    customValue.set(licenseService.runJob());
    // Untyped metric example
    meterRegistry.gauge("a_custom_untyped_metric", customValue); // Example of an untyped gauge
}
```

# Timer

```java
@PostConstruct
public void initializeMetrics() {

    // Timer
    requestTimer = Timer.builder("a_timer_http_request_duration_seconds")
            .description("HTTP request duration")
            .register(meterRegistry);

    // Long Task Timer
    longTaskTimer = LongTaskTimer.builder("a_long_task_http_request_duration_seconds")
            .description("Duration of long-running tasks")
            .register(meterRegistry);

    // Schedule task to simulate user arrivals
    ScheduledExecutorService executorService = Executors.newSingleThreadScheduledExecutor();
    executorService.scheduleAtFixedRate(this::processHttpRequest, 0, 100, TimeUnit.SECONDS);

}
```

# Final output

[http://localhost:8090/actuator/prometheus](http://localhost:8090/actuator/prometheus)

```prometheus
# HELP a_counter_http_requests_total Number of times the job request run
# TYPE a_counter_http_requests_total counter
a_counter_http_requests_totallicenseJobCounterexample 1.0
# HELP a_custom_untyped_metric
# TYPE a_custom_untyped_metric gauge
a_custom_untyped_metric 1173.0
# HELP a_guage_active_users Number of active users
# TYPE a_guage_active_users gauge
a_guage_active_users 15.0
# HELP a_license_days_remaining Days remaining until License expiration
# TYPE a_license_days_remaining gauge
a_license_days_remaininglicense_days_remainingRemaining days 1173.0
# HELP a_license_expiration_counter_total
# TYPE a_license_expiration_counter_total counter
a_license_expiration_counter_totaltypecounter 18.0
# HELP a_license_expiration_days_summary_days Summary of days until License expiration
# TYPE a_license_expiration_days_summary_days summary
a_license_expiration_days_summary_days_count 0
a_license_expiration_days_summary_days_sum 0.0
# HELP a_license_expiration_days_summary_days_max Summary of days until License expiration
# TYPE a_license_expiration_days_summary_days_max gauge
a_license_expiration_days_summary_days_max 0.0
# HELP a_long_task_http_request_duration_seconds Duration of long-running tasks
# TYPE a_long_task_http_request_duration_seconds summary
a_long_task_http_request_duration_seconds_count 0
a_long_task_http_request_duration_seconds_sum 0.0
# HELP a_long_task_http_request_duration_seconds_max Duration of long-running tasks
# TYPE a_long_task_http_request_duration_seconds_max gauge
a_long_task_http_request_duration_seconds_max 0.0
# HELP a_summary_http_response_sizes_bytes Distribution of HTTP response sizes
# TYPE a_summary_http_response_sizes_bytes summary
a_summary_http_response_sizes_bytes_count 1
a_summary_http_response_sizes_bytes_sum 364.0
# HELP a_summary_http_response_sizes_bytes_max Distribution of HTTP response sizes
# TYPE a_summary_http_response_sizes_bytes_max gauge
a_summary_http_response_sizes_bytes_max 364.0
# HELP a_timer_http_request_duration_seconds HTTP request duration
# TYPE a_timer_http_request_duration_seconds summary
a_timer_http_request_duration_seconds_count 1
a_timer_http_request_duration_seconds_sum 0.296439955
# HELP a_timer_http_request_duration_seconds_max HTTP request duration
# TYPE a_timer_http_request_duration_seconds_max gauge
a_timer_http_request_duration_seconds_max 0.296439955
```


global:
scrape_interval: 60s

Grafana queries the data stored in Prometheus (or other data sources) to create visualizations on its dashboards.
