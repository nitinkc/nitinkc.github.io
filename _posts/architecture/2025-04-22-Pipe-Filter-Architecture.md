---
categories:
- Architecture
date: 2025-04-22 14:02:00
tags:
- Pipeline
- Design Patterns
title: The Pipeline (or Pipe-Filter) architectural style
---

{% include toc title="Index" %}
> Category : Concurrency Architecture

The **Pipeline (or Pipe-Filter) architectural style** is a design pattern used in concurrent programming to process data streams. 

# **Key Components**
**Filters**: These are the processing units that transform data. 
- Each filter performs a specific operation on the data, such as sorting, parsing, or transforming.

**Pipes**: These are connectors that pass data from one filter to another. 
- Pipes ensure that data flows smoothly between filters.

# **Characteristics**
**Sequential Processing**: Data flows through a sequence of filters connected by pipes. 
- Each filter processes the data and passes it to the next filter.

**Independent Filters**: Filters operate independently and do not share state. 
- This allows for parallel processing and scalability.

**Modularity**: Filters can be added, removed, or replaced without affecting the overall system.
- This makes the architecture flexible and easy to maintain.

Google Cloud Platform (**GCP**) offers several services and tools that can be used to implement the Pipeline (Pipe-Filter) architectural style. 

### **Dataflow**
Google Cloud Dataflow is a fully managed service for stream and batch processing. 
- It allows you to create pipelines that transform and analyze data. 
- Each step in the pipeline can be considered a filter, and the data flows through these steps via connectors (pipes).

### **Composer**
Google Cloud Composer is a managed **workflow orchestration service** built on Apache **Airflow**.
- It allows you to define workflows as Directed Acyclic Graphs (DAGs), where each task in the DAG can be seen as a filter, and the edges between tasks act as pipes.

### **Pub/Sub**
Google Cloud Pub/Sub is a messaging service that enables asynchronous communication between different components. 
- You can use Pub/Sub to connect various filters, where each filter processes the data and publishes the results to a topic, which is then consumed by the next filter.

### **Cloud Functions**
Google Cloud Functions can be used to create small, single-purpose functions that act as filters.
- These functions can be triggered by events (such as changes in a database or messages in Pub/Sub), process the data, and pass it to the next function or service.

# Notes
## Apache Beam
is an open-source, unified programming model designed to _define and execute_ **data processing pipelines**
- **Pipeline**: The top-level container for the data processing workflow.
- **PCollection**: Represents a distributed data set that can be processed in parallel.
- **PTransform**: Represents a data processing operation, such as a transformation or aggregation.

## Apache Airflow - Workflows as Code:
is an open-source platform designed to programmatically author, schedule, and monitor **workflows**. 
- It's particularly useful for orchestrating complex data pipelines and automating tasks.
- **DAG** (Directed Acyclic Graph): Represents a workflow, consisting of tasks with dependencies.
- **Operators**: Define the tasks within a DAG, such as executing a Bash command, running a Python function, or transferring data.
- **Scheduler**: Manages the execution of tasks based on defined schedules and dependencies.
- **Executor**: Executes tasks, either locally or distributed across multiple workers.

# Directed Acyclic Graphs (DAGs) with Google Cloud Dataflow:

**Real-Time ETL Pipeline**

Build a real-time ETL (Extract, Transform, Load) pipeline that **ingests data** from various sources, processes it, 
and loads it into **BigQuery** for analytics.

## Steps
### Ingestion

- **Source**: Data is ingested from multiple sources such as Pub/Sub topics, databases, or log files.
- **Dataflow**: A Dataflow job is triggered to start processing the incoming data.

### Transformation
- **Filter 1**: Data is cleaned and normalized. For example, removing duplicates, handling missing values, and standardizing formats.
- **Filter 2**: Data is enriched with additional information. For instance, adding geolocation data based on IP addresses.
- **Filter 3**: Data is aggregated to compute metrics like average, sum, or count.

### Loading
- **Sink**: The processed data is loaded into BigQuery for further analysis and reporting.

## DAG Representation

> Monitor :  Dataflow Monitoring Interface on Google Cloud Platform.

```
Pub/Sub -> Dataflow -> Filter 1 -> Filter 2 -> Filter 3 -> BigQuery
```

```java
import org.apache.beam.sdk.Pipeline;
import org.apache.beam.sdk.io.gcp.pubsub.PubsubIO;
import org.apache.beam.sdk.io.gcp.bigquery.BigQueryIO;
import org.apache.beam.sdk.transforms.MapElements;
import org.apache.beam.sdk.transforms.SimpleFunction;
import org.apache.beam.sdk.transforms.Combine;
import org.apache.beam.sdk.values.TypeDescriptor;
import org.apache.beam.sdk.options.PipelineOptionsFactory;
import org.apache.beam.sdk.options.PipelineOptions;

public class RealTimeETLPipeline {

    public static void main(String[] args) {
        PipelineOptions options = PipelineOptionsFactory.fromArgs(args).create();
        Pipeline pipeline = Pipeline.create(options);

        pipeline
            .apply("Read from Pub/Sub", PubsubIO.readStrings().fromTopic("projects/my-project/topics/my-topic"))
            .apply("Clean Data", MapElements.via(new SimpleFunction<String, String>() {
                @Override
                public String apply(String input) {
                    // Implement your data cleaning logic here
                    return cleanData(input);
                }
            }))
            .apply("Enrich Data", MapElements.via(new SimpleFunction<String, String>() {
                @Override
                public String apply(String input) {
                    // Implement your data enrichment logic here
                    return enrichData(input);
                }
            }))
            .apply("Aggregate Data", Combine.globally(new SumFn()).withoutDefaults())
            .apply("Write to BigQuery", BigQueryIO.writeTableRows()
                .to("my-project:my_dataset.my_table")
                .withSchema("SCHEMA_AUTODETECT")
                .withWriteDisposition(BigQueryIO.Write.WriteDisposition.WRITE_APPEND));

        pipeline.run().waitUntilFinish();
    }

    private static String cleanData(String input) {
        // Your data cleaning logic
        return input.trim();
    }

    private static String enrichData(String input) {
        // Your data enrichment logic
        return input + ", enriched";
    }

    static class SumFn extends Combine.CombineFn<String, String, String> {
        @Override
        public String createAccumulator() {
            return "";
        }

        @Override
        public String addInput(String accumulator, String input) {
            // Your aggregation logic
            return accumulator + input;
        }

        @Override
        public String mergeAccumulators(Iterable<String> accumulators) {
            StringBuilder merged = new StringBuilder();
            for (String acc : accumulators) {
                merged.append(acc);
            }
            return merged.toString();
        }

        @Override
        public String extractOutput(String accumulator) {
            return accumulator;
        }
    }
}
```