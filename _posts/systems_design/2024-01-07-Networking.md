---
title: "Computer Networks"
date:  2024-01-07 08:44:00
categories: [System Design]
tags: [System Design]
---

# 7 Layers of OSI

> Aap president se trans network datalink phasao

1. Application
2. Presentation
3. Session --> Behavioural
4. Transport --> Routing
5. Network --> Routing
6. DataLink --> Routing
7. Physical

Physical Layer Adds the Start and End delimiter for a message

### The NIC and the MAC Address

An NIC (Network Interface Card) is a **hardware component** that allows computers to connect to a network. 
- both wired (Ethernet) and wireless (Wi-Fi) networks

An NIC has a MAC (Media Access Control) address. 
- It is a 48-bit address represented. Six groups of two hexadecimal digits separated by colons (e.g., 00:1A:2B:3C:4D:5E). 
- The MAC address is used at the **data link layer** of the OSI model to ensure that data packets are delivered to the correct destination on a local network.

To **route** the message to the correct device we need both `IP Address` and `MAC Address`

                    ] 4. Transport
         Routing    ] 5. Network
                    ] 6. DataLink

DNS : IP Address to Website/business domain name address mapping

Internet Backbone - DNS


NAT : Network Address Translation Protocol


HTTP - Build over TCP
- Guaranteed Delivery
- Client server model - One sends, one receives

Websockets - Peer-To-Peer
- Build over TCS
- bi-directional communication
- It allows for Peer-to-Peer communication. 
  - It establishes a duplex connection allowing both devices to send and receive requests
- possible to open a two-way interactive communication session
- XMPP (Extensible Messaging and Presence Protocol) which is an open XMLTechnology for real-time communication.

UDP : User Datagram Protocol
- Time sensitive transmissions
- Realtime delivery
- No ACK
- [Details](https://www.cloudflare.com/learning/ddos/glossary/user-datagram-protocol-udp/)


TCP 
- Guaranteed Delivery
- Ordering of messages
- Retries upon failures

# Communication Standards: 

### REST
very common protocol and is used over HTTP.

It is stateless because rather than relying on the server to remember the previous requests,
REST applications require each request to contain all of the information necessary for the server to understand it.

Requests are cacheable

Thrift

Thrift has a code generator which generates data structures that can be serialized using Thrift, 
and client and server stubs for RPC, in different languages.

### GraphQL 
we can request the specific attributes. So it saves bandwidth and also providessecurity

### gPRC
is generally used by microservices to communicate internally.It is written over HTTP 2.0


# Head-of-Line Blocking in HTTP

Head-Of-Line blocking occurs when the message/data packet at the head of the queue cannot move forward due to congestion 
even if other messages/packets behind this one could

HTTP 2.0 solves this problem using Multiplexing. 
It implements multiplexing by breaking the messages/data packets into frames and are sent in streams. 

Each stream has a stream ID. So,when you get a message of a stream ID, that stream is going to be blocked until all the 
messages having the stream IDs are processed.

HTTP 2.0 solved Head of Line Blocking, but it is still written over TCP. Even though data packets are broken into 
logical streams, they are not independent because they are running on the same TCP


# Protocols for video transmission

HTTP is not good for video transmission because:Videos are broken into chunks. Since HTTP is stateless, the client has 
to specify which chunk it wants because the server does not know about the previous requests.

HTTP is written over TCP which is not optimal for live streaming. Because in live streaming, if the video packet does 
not reach the client then there is no point in retrying because the data is old.So UDP is better for live-streaming. 

However, in some cases where we need, guaranteeddelivery TCP is preferred.

##### HTTP-DASH
DASH stands for Dynamic Adaptive Streaming over HTTPThis protocol runs over TCP. So there is guaranteed delivery and ordering.

The basic idea is, that the client sends a signal to the main server based on the data you can handle

In Mac devices, HLS [HTTP live streaming](https://www.cloudflare.com/learning/video/what-is-http-live-streaming/) is used. 
It is very similar to HTTP-DASH

##### Web-RTC
WebRTC uses peer-to-peer communication . HTTP 2.0, HTTP-DASH and QUIC (HTTP 3.0) used client-server communication

How does peer-to-peer communication work?

First, the clients get the addresses of the other clients from the server.
Then the server sends the information to both the clients.
Clients use this information to connect.

Since it does not require a serverIt is fast.It saves bandwidth.

It is more robust because even if the server crashes, clients can keep talking to each other.
