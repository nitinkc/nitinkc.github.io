---
title:  "Java Systems Stats"
date:   2023-10-17 08:30:00
categories: ['Java']
tags: ['Java']
---
{% include toc title="Index" %}
## Stats

```java
 System.out.println("Available Processors : " + Runtime.getRuntime().availableProcessors());
 System.out.println("Total Memory : " + Runtime.getRuntime().totalMemory());
 System.out.println("Fork Join Pool : " + ForkJoinPool.commonPool());
```

Notice the difference between the total number of processors and parallelism in the thread pool complying
`# of threads <= # of cores`

```log
Available Processors : 16
Total Memory : 545259520
Fork Join Pool : java.util.concurrent.ForkJoinPool@659e0bfd[Running, parallelism = 15, size = 0, active = 0, running = 0, steals = 0, tasks = 0, submissions = 0]
```