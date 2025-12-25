---
categories: System Design
date: 2024-06-21 20:00:00
tags:
- Networking
- WebSockets
- Real-time
title: 'Web Sockets '
---

{% include toc title="Index" %}

# Problems with http

**HTTP Polling**

- Short Polling - client sends request to the server in fixed time intervals

Chances of lots of empty responses

**Long polling**

- wait for responses for a longer duration

**Server Sent Events  (SSE)**

unidirectional connection - server can push as much data as possible but its
just unidirectional connection from server to the client

good for instagram lives, notification systems broadcasrting

# Websockets

- persistent, low latency bi-directional full duplex data exchange
- facilitate realtime data exchange
- ideal for applications where instant updates are critical, like chat
  applications, online gaming, trading platforms

HTTP 101 Switching Protocols

The first connection will be the HTTP handshake request with an upgrade header

```shell
Connection: Upgrade

response
Upgrade: websocket
Status Code: 101 Switching Protocols
```

then the persistent connection is established
![webSockets.png](/assets/images/webSockets.png)

## How WebSockets Work:

**Handshake**: The connection starts with a WebSocket handshake, which is an
HTTP request/response upgrade process. The client sends an HTTP request to the
server with an Upgrade header.

**Upgrade**: If the server supports WebSockets, it agrees to the upgrade and
establishes a WebSocket connection, switching from the HTTP protocol to the
WebSocket protocol.

**Communication**: Once the connection is established, both the client and
server can send and receive messages at any time. These messages are sent over
the same TCP connection, allowing for real-time communication.

| HTTP           | WebSockets                                |
|:---------------|:------------------------------------------|
| Stateless      | Stateful                                  |  
| unodirectional | bi-directional over single TCP connection |
| half duplex    | full duplex                               |

# Close a WebSocket Connection

**Initiation**: Either the client or the server can initiate the close handshake
by sending a close frame. This frame is identified by an opcode of `0x8`.

**Close Frame**: The close frame may include an optional payload with a close
code and a reason for closure. The close code is a 2-byte unsigned integer that
indicates the reason for closure. Some common close codes are:

| Close Code | Meaning                                                                                                                                 |
|:-----------|:----------------------------------------------------------------------------------------------------------------------------------------|
| 1000       | Indicates a normal closure, meaning the purpose for which the connection was established has been fulfilled.                            |
| 1001       | Indicates that an endpoint is "going away", such as a server going down or a browser navigating away from the page.                     |
| 1002       | Indicates a protocol error was encountered.                                                                                             |
| 1003       | Indicates that the received data type cannot be accepted (e.g., an endpoint that only understands text data received a binary message). |
| 1006       | Indicates that the connection was closed abnormally (used internally and not sent on the wire).                                         |

**Response**: Upon receiving a close frame, the other party (client or server)
should respond with its own close frame if it hasn't already sent one. This
acknowledges the close request and allows both parties to gracefully close the
connection.

**Closing the Connection**: After sending and receiving the close frames, the
underlying TCP connection is closed. This ensures that all resources related to
the WebSocket connection are properly released.

 ```plantuml!
actor Client
actor Server

Client -> Server : WebSocket Handshake
Server --> Client : WebSocket Handshake Response

Client <-> Server : WebSocket Connection (Full-duplex)

Client -> Server : Data Frame
Server -> Client : Data Frame

Client -> Server : Close Frame (Opcode: 0x8, Optional Payload)
Server --> Client : Close Frame (Acknowledge)

Client <-> Server : TCP Connection Closure
```