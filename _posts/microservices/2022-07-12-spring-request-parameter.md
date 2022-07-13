---
# layout: static
title:  "Spring Request parameter"
date:   2022-07-12 20:04:00
categories: "Spring Microservices"
tags: ["Spring Microservices", Spring Boot]
---
{% include toc title="Index" %}


# GET : Request Parameter

If Requirement for the API is to get the summary of recent orders in the last 24 hours
```
localhost:8084/orders/dashboard/summary
```
OR pass an specific date to search
```
localhost:8084/orders/dashboard/summary?fromDate=2021-06-01&toDate=2022-06-17
```

Notice the defaultValue property of @RequestParam. This is useful when the dates are not passed. The fromDate takes the **current date** as default date to todate parameter takes **the end of the day today** as the default vale

Default value is set with default value with input e defaultValue = "#{T(java.time.LocalDateTime).now()}" 

The Corrosponding Spring Controller would look like

{% gist nitinkc/a3d6bc27b88b20abe0eb491f107930a0 %}

If, however, explicit dates are to be passed and particular type of Order is also to be passed in request parameter

```
localhost:8084/orders/dashboard/details?fromDate=2021-06-01&toDate=2022-06-17&orderType=Grocery Order
```

The corrosponding Controller would be as follows. 
{% gist nitinkc/d347e24dc5a08d8195cd86c5a32505be %}
