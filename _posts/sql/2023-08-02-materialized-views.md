---
title:  "Materialized views"
date:   2023-08-02 14:25:00
categories: ['SQL']
tags: ['SQL']
---
{% include toc title="Index" %}


Materialized views in Oracle (Scheduled Queries in GCP BigQuery) can be scheduled for regular refreshes. 
A scheduled refresh ensures that the data in the materialized view is kept up-to-date with the data in the underlying tables.

In Oracle, there are different ways to schedule the refresh of materialized views:

# Manual Refresh
   By default, materialized views are set to be refreshed manually. You can manually refresh a materialized view using
the `DBMS_MVIEW` package or the `DBMS_SNAPSHOT` package. For example:
```sql
-- Manual refresh using DBMS_MVIEW package
BEGIN
  DBMS_MVIEW.REFRESH('materialized_view_name');
END;
```

# Refresh on Commit
   You can configure a materialized view to be automatically refreshed.
whenever there is a commit on the master tables that the materialized view depends on. 

This is achieved by using the `REFRESH FAST ON COMMIT` option when creating the materialized view.
```sql
-- Refresh on commit
CREATE MATERIALIZED VIEW materialized_view_name
REFRESH FAST ON COMMIT
AS
SELECT ...
FROM ...
```

# Refresh on Demand
   You can also schedule a materialized view to be refreshed at specific time intervals (e.g., hourly, daily, weekly)
using the Oracle Scheduler. This involves creating a scheduled job to perform the refresh at the desired frequency.
```sql
-- Create a scheduled job to refresh the materialized view
BEGIN
  DBMS_SCHEDULER.CREATE_JOB (
    job_name => 'materialized_view_refresh_job',
    job_type => 'PLSQL_BLOCK',
    job_action => 'BEGIN DBMS_MVIEW.REFRESH(''materialized_view_name''); END;',
    start_date => SYSTIMESTAMP,
    repeat_interval => 'FREQ=HOURLY',
    enabled => TRUE
  );
END;
```

In this example, a scheduled job named 'mv_refresh_job' is created to refresh the materialized view 'mv_name' hourly.

* refresh of materialized views may take time and can affect database performance. 
* consider the size of the materialized views, the frequency of data changes in the underlying tables,
* `FAST` refreshes are more efficient when there are incremental changes to the data, while `COMPLETE` refreshes are more time-consuming but may be necessary for complex queries.