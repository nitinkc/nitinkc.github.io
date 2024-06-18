---
title: "Live Streaming"
date: 2024-06-14 11:02:00
categories: [System Design]
tags: [System Design]
---
{% include toc title="Index" %}

![](https://www.youtube.com/watch?v=7AMRfNKwuYo)
video content delivery from streamer's computer to the viewer's device (glass-to-glass latency) 

Video processing is compute-intensive

Video Capture -> Encoders (OBS, Webcam Capture, phone camera)

Real-time Messaging Protocol (RTMP) 
    - TCP-based protocol

Secured Reliable transport - could replace RTMP
- UDP based 
- promises lower latency
- better resilience to poor network conditions.






HTTP Live Streaming (HLS)



