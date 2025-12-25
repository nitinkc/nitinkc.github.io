---
title: JIRA Filters
date: 2024-09-13 13:45:00
categories:
- Developer Tools
tags:
- Project Management
- Agile
---

### With createdtime in last 60 days

```jql
issuetype = "Backmerge Task" AND created >= -60d and fixVersion in (R23.0.0.0)
```

### Dependencies Created By a team

```jql
issuetype in (Defect, "Warranty Observations") 
AND component = Reporting 
AND "Team Responsible" = Falcon 
AND status not in (Done, Release, Rejected) 
ORDER BY cf[15323] DESC, labels DESC, created DESC
```

### Open Epics

```jql
issuetype in (Epic) AND 
component = Reporting AND 
"Team Responsible" = Icon-Plus 
AND status not in (Done, Release, Rejected) 
ORDER BY labels DESC, cf[15323], created DESC
```

### Self with status - Not Done

```jql
assignee = currentUser() AND "Team Responsible" =  Falcon  and  status not in (Done, Skipped, "In Production")
```

```jql
assignee = currentUser() AND resolution = Unresolved AND status not in (Done, Release, Rejected, Closed, "Create an Enhancement") order by updated DESC
```