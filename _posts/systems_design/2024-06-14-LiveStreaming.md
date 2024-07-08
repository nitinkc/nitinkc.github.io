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



# Videos on CDN's

How are they protected?

**Token-based authentication**: 
The CDN server sends each user request to the main server to authenticate whether the user can view the video. 
- If authorized, the CDN serves the video. 
- provides strong authentication but is slower (trade-off) and less secure since the CDN can access and misuse the user's token.

**Domain-based authentication**: The CDN server restricts video access based on the domain from which the request originates. 
- If the request comes from an allowed domain, the CDN serves the video; otherwise, access is denied. 
- This approach is simple and fast but vulnerable to domain spoofing and lacks user-specific authorization.

**Server-side authentication**: The user's request directly communicates with the server for authentication. 
- The server generates a token signed by the user's private key, indicating permission to access the video. 
- This token is then forwarded to the CDN, which verifies its authenticity using the public key and grants access accordingly. 
- The token can have a TTL to mitigate unauthorized sharing. 
- mix of security and efficiency.

Digital rights management (DRM) solutions can be used to prevent unauthorized copying or multiple IP addresses accessing the content. 


