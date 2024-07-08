---
title:  "peer-to-peer communication"
date:   2024-06-29 21:02:00
categories: [System Design]
tags: [System Design]
---

```plantuml!
actor PeerA
actor PeerB

PeerA -> DirectoryServer : Request for peers
DirectoryServer --> PeerA : Respond with PeerB info

PeerA -> PeerB : Initiate Handshake
PeerB -> PeerA : Acknowledge Handshake

PeerA -> PeerB : Establish Session (Agree on protocol, ports, etc.)

PeerA -> PeerB : Data Exchange
PeerB -> PeerA : Data Exchange
```