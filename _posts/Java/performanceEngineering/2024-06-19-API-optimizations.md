---
title:  "API Optimizations"
date:   2024-06-19 00:10:00
categories: ['Java',"Performance Engineering"]
tags: ['Java',"Performance Engineering"]
---

Identify actual bottlenecks through load testing and profiling

Optimize only when performance of API shows issues 

# 1.Caching

store the result of an expensive computation (redis or memchahed) to avoid redoing

# 2.Connection pooling

Maintaining a pool of open connections, rathen than making new DB connection each API Call.

Difficult to achieve this in a serverless infrastructure. Amazon RDS Proxy and Azure SQL DB serverless 
manage the connection pooling for you

# 3.N+1 Problem
When multiple queries are used to return data for a single resposne, like N queries for each of n comments for a post

# 4.Pagination 

with the use of limit and offset
to respond with one page worth of data


# 5.Serializers 
lightweight json serializers

# 6.Compression

Enable compression on Large API Response payloads

client decompresses the data

# 7.Asynchronous Logging



