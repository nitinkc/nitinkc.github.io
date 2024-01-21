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



Session  Behavioural

$$
\huge[ 
4. Transport\\
5. Network\\
6. DataLink\\
\right]
$$

$$
\LARGE{

4. Transport 
5. Network
6. DataLink
$$