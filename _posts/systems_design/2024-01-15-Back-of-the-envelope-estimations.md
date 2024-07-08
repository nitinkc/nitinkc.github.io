---
title:  "Back of the envelop estimations"
date:   2024-01-15 17:30:00
categories: [System Design]
tags: [System Design]
---
{% include toc title="Index" %}

### Hard Drives
* HDD - 100 MBps
* SSD - 500 MBps
* Memory Card - 1GBps 

### Networks
* 4G/LTE - 30MBps to 100MBPS
* LAN - 1 GBPS
* 5G - to be introduced
* 40Gbps (5GBps - GigaBytes per second) - network throughput for a good data center
    - if i have a file of 5GB, it will take a second to transfer the file from one one node to the other


Assume a good quality image of 1 MB
 * Thumbnail is 1/10th of the actual image -> 100 KB


| **HORIZONTAL**                     | **VERTICAL** | Notes                                                         |
|:-----------------------------------|:------------|---------------------------------------------------------------|
| L1 cache reference (per core)      | 0.5 ns      | 6 Lakh times faster than RAM                                  |
| L2 cache reference                 | 7 ns        | 14~15 times slower than L1                                    |
| Read 1MB sequentially from disk    | 30ms        |                                                               |
| Write 1MB into the disk            |             | 2 times than Read approximately (for HDD), for SSD, 1.2 times |
| Read 1MB sequentially from Memory  | 300μs (250μs) | 1 lakh times faster than disk                                 |
| Send 1MB over 1Gbps network        | 10ms        | $$ \frac{1\times 8 * 10^6}{10^9} \approx 10\times 10^{-3} $$  |
| Read 1MB over 1Gbps network        | 10ms        |                                                               |
| Compress 1MB using Zippy           | 10ms        | for 1KB, $$ \frac{10 * 10^{-3}}{10^{-3}} = 10μs $$            |
| Compression ratio                  |             |                                                               |
| Round trip within same Data center | 150μs       ||
| Round trip CA -> Netherland -> CA  | 500ms       ||


* Compress data before sending over internet

# QPS - Queries per second

Peak QPS = 2 to 5 times QPS

### Time Estimations

1 Day has $ \textrm{86400 seconds} = 24\times 60\times 60 \approx 90K secs $

100 Million load per day 


$ \text{Load per second} = \frac{100 \times 10^6}{90 \times 10^3} = \frac{100{,}000{,}000}{90{,}000} = 1111.11\overline{1} \approx 1200 $ 


Denominator is slightly increased to 90K so for lesser denominator the output will increase

# Estimates

1. DAU : Daily Average Users eg. 300 million MAU
2. Usage per DAU = 10 -25% make a post  (QPS : Queries per second)
3. Scale Factor : estimate how much higher the traffic would peak, compared to the average

![](https://www.youtube.com/watch?v=UC5xf8FbdJc)

### Latency Numbers : 

Billion is $ 10^9 $
nanosecond is 1 billionth of a second

Million is $ 10^6 $
microsecond is 1 millionth of a second

![](https://www.youtube.com/watch?v=FqR5vESuKe0)


# Levels of Availability
| Availability (%)   | Downtime per Year | Examples of Suitable Applications                            |
|:-------------------|:------------------|:-------------------------------------------------------------|
| 99.00% (Two 9's)   | ~3.65 days        | Non-critical applications, occasional downtime acceptable    |
| 99.90% (Three 9's) | ~8.76 hours       | Internal business applications, moderate uptime requirement  |
| 99.99% (Four 9's)  | ~52.6 minutes     | Customer-facing applications, e-commerce sites               |
| 99.999% (Five 9's) | ~5.26 minutes     | Mission-critical applications, financial services            |
| 99.9999% (Six 9's) | ~31.5 seconds     | Highly critical systems, emergency services                  |
