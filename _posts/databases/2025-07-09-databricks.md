---
# layout: static
title:  "Azure Databricks & Apache Spark"
date:   2025-07-09 15:25:00
categories: Database
tags: [Database]
---


![DataEngineer_RefArchtecture.png]({{ site.url }}/assets/images/DataEngineer_RefArchtecture.png){:width="70%" height="50%"}
![dataEngineeringPlatform-refArchi.png]({{ site.url }}/assets/images/dataEngineeringPlatform-refArchi.png){:width="70%" height="50%"}


# Lakehouse Medallion Architecture
After Data ingestion/integration Build the system in layers with 3 minimum layers

![lakehouse-medallion-architecture.png]({{ site.url }}/assets/images/lakehouse-medallion-architecture.png){:width="70%" height="50%"}

## Data Collection/Ingestion
Batch Mode: Collection of Data in periodic intervals
Stream Mode: Collect as and when the data is generated

## Data Processing
- Bronze layer - Raw data after collecting from Source systems
- Silver Layer - Read data from Bronze layer, do required processing
- Gold Layer - preparing data for consumption, filling results into the desired data models

# Azure Databricks Platform Architecture
![azure-databrics-platform-architecture.png]({{ site.url }}/assets/images/Fazure-databrics-platform-architecture.png){:width="70%" height="50%"}