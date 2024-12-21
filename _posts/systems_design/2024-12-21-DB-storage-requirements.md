---
title:  "Database Requirements Estimation"
date:   2024-12-21 02:30:00
categories: [System Design]
tags: [System Design]
---

# 1. **Data Size per User**
- **User Profile Data**:
  - **1KB - 10KB per user** (depends on complexity).
- **Activity Logs**:
  - **100KB - 500KB per user/day** (depending on app type and usage).
- **Media (e.g., images, videos)**:
  - **100KB - several MB per user** (depending on the app).
- **Example**: A social media platform with **10M DAUs**, each generating 
**100KB of data/day** results in **1TB/day** of data.

# 2. **Traffic Volume (API Calls)**
- **API Calls per User per Day**:
  - **30 - 100 API calls per user per day** (typical range, depends on the app).
- **Total API Calls per Day**:
  - DAU of **1M users** with **50 API calls/user/day** results in **50M API calls/day**.
  - For a **10M DAU** app, that's **500M API calls/day**.
- **Reads vs Writes**:
  - **Reads**: 70%-90% of operations in typical apps.
  - **Writes**: 10%-30% of operations (may vary by app).
- **Example**: If 50M API calls/day are made and 20% are writes, that's **10M writes/day**.

# 3. **Storage Requirements**
- **Data Growth**:
  - Estimate **10%-20% monthly growth** in data (adjust as per the type of app and stage of company).
- **Storage per User**:
  - User-related data: **1KB - 10KB per user**.
  - Media-heavy apps: **100KB - several MB per user**.
- **Example**:
  - For **10M DAUs** with **1KB per user profile data** and **100KB for activity logs**, total storage could be:
    - **User data**: 10M users * 1KB = **10GB**.
    - **Activity logs**: 10M users * 100KB = **1TB** of logs per day.
- **Total Storage Estimate**: **1TB - 10TB/day** for a platform with heavy activity.

# 4. **Database Operations**
- **Reads**: 70% - 90% of operations.
- **Writes**: 10% - 30% of operations.
- **Write-heavy applications** (e.g., logging services) will have higher write percentages.
- **Example**: For **50M API calls/day** with 80% reads and 20% writes, that results in:
  - **Reads**: 40M reads/day.
  - **Writes**: 10M writes/day.

# 5. **Sharding and Partitioning**
- **Sharding Strategy**: Split data across multiple databases based on user ID, region, or other logical partitioning methods.
- **Example**:
  - A database shard might handle **1M - 10M users**, or it could be based on geographic regions.
  - For **50M DAUs**, you might have **5-10 shards**, each handling **5M-10M users**.

# 6. **Replication and Availability**
- **Primary and Replica DBs**: Use primary-replica databases to scale reads.
  - **Replicas**: Typically **2-5 replicas** for high availability.
- **Example**: For a system with **50M API calls/day** and heavy read traffic, replicas help distribute the load across multiple databases.

# 7. **Indexes**
- **Indexing for Speed**: Commonly used for fast querying (e.g., user IDs, timestamps).
- **Trade-offs**: Indexes improve read performance but can degrade write performance.
- **Example**: Indexing **user IDs** for a **user profile look-up** or **timestamps** for **activity logs**.

# 8. **Backup and Disaster Recovery**
- **Backup Strategy**: Regular backups (e.g., hourly, daily) to ensure data recovery in case of failure.
- **Example**: For an e-commerce platform with **50M DAUs** and heavy transactions, backups might be taken **every 30 minutes to 1 hour**.

# General Tips for Database Requirements Estimation
- **Assume 10%-20% Growth in Data**: Always account for data growth, especially in rapidly growing apps.
- **Use 70%-90% Reads and 10%-30% Writes**: As a general rule, reads typically outnumber writes unless your app is very write-heavy (e.g., logging systems).
- **Consider the App Type**: For media-heavy apps, storage and data volume will be significantly higher.
- **Factor in Sharding and Partitioning**: Plan for horizontal scaling via sharding when DAU grows.
