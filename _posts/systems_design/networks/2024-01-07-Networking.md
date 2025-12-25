---
categories:
- System Design
date: 2024-01-07 08:44:00
tags:
- Networking
- Protocols
title: Computer Networks - The OSI Model
---

# 7 Layers of OSI

[https://github.com/ByteByteGoHq/system-design-101?tab=readme-ov-file#tcpip-encapsulation](https://github.com/ByteByteGoHq/system-design-101?tab=readme-ov-file#tcpip-encapsulation)

![](https://www.youtube.com/watch?v=0y6FtKsg6J4)

> Aap trans network datalink physical

1. Application
2. Presentation
3. Session --> Behavioural
   The above three can be clubbed into Application protocol layer due to too
   much of fine grained details
4. Transport --> Routing
5. Network --> Routing
6. DataLink --> Routing
7. Physical

Physical Layer Adds the Start and End delimiter for a message

![](https://www.escotal.com/Images/Network%20parts/osi.gif)

### The NIC and the MAC Address

An NIC (Network Interface Card) is a **hardware component** that allows
computers to connect to a network.

- both wired (Ethernet) and wireless (Wi-Fi) networks

An NIC has a MAC (Media Access Control) address.

- It is a 48-bit address represented. Six groups of two hexadecimal digits
  separated by colons (e.g., 00:1A:2B:3C:4D:5E).
- The MAC address is used at the **data link layer** of the OSI model to ensure
  that data packets are delivered to the correct destination on a local network.
- The MAC address is that of the router in the next hop, not the source adn
  destination computers
-

To **route** the message to the correct device we need both `IP Address` and
`MAC Address`

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
    - It establishes a duplex connection allowing both devices to send and
      receive requests
- possible to open a two-way interactive communication session
- XMPP (Extensible Messaging and Presence Protocol) which is an open
  XMLTechnology for real-time communication.

UDP : User Datagram Protocol

- Time sensitive transmissions
- Realtime delivery
- No ACK
- [Details](https://www.cloudflare.com/learning/ddos/glossary/user-datagram-protocol-udp/)

TCP

- Guaranteed Delivery
- Ordering of messages
- Retries upon failures

```markdown
+-------------------------------+
| 7. Application Layer          |
| - Data: Message               |
| - Header: Application Header  |
| - Provides network services   |
| - Protocols: HTTP, FTP, SMTP  |
|-------------------------------|
| HTTP Header + Data            |
+-------------------------------+
| 6. Presentation Layer          |
| - Data: Encrypted Message     |
| - Header: Presentation Header |
| - Data translation, encryption,|
|   compression                 |
+-------------------------------+
| 5. Session Layer               |
| - Data: Encrypted Message     |
| - Header: Session Header      |
| - Session establishment       |
| - Management and termination  |
+-------------------------------+
| 4. Transport Layer             |
| - Data: Segment (TCP)         |
|        Datagram (UDP)         |
| - Header: Transport Header    |
| - Reliable data transfer      |
| - Protocols: TCP, UDP         |
|-------------------------------|
| TCP Header + HTTP Header +    |
| Data                          |
+-------------------------------+
| 3. Network Layer               |
| - Data: Packet                |
| - Header: Network Header      |
| - Logical addressing, routing |
| - Protocol: IP                |
|-------------------------------|
| IP Header + TCP Header +      |
| HTTP Header + Data            |
+-------------------------------+
| 2. Data Link Layer             |
| - Data: Frame                 |
| - Header: Data Link Header    |
| - Trailer: Data Link Trailer  |
| - Node-to-node data transfer  |
| - Error detection/correction  |
| - MAC addresses               |
|-------------------------------|
| MAC Header + IP Header +      |
| TCP Header + HTTP Header +    |
| Data                          |
+-------------------------------+
| 1. Physical Layer              |
| - Data: Bits                  |
| - Media: Electrical signals,  |
|   light pulses, radio waves   |
| - Transmission of raw bits    |
| - Media, signal, and binary   |
|   transmission                |
|-------------------------------|
|  10010111...                  |
+-------------------------------+
```