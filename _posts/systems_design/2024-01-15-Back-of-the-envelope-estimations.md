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

Peak QPS = 2 times QPS

### Time Estimations

1 Day has $$ \textrm{86400 seconds} = 24\times 60\times 60 \approx 90K secs $$

100 Million load per day 

Load per second = $$ 100\times10^6 \divide 90\times 10^3 = 1111.11 \approx 1200 $$. Denominator is slightly increased to 90K so for lesser denominator the output will increase