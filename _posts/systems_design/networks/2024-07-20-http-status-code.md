---
categories:
- System Design
date: 2024-07-20 21:02:00
tags:
- HTTP
- REST
- API
- Java
title: Http Status Codes & Java Exceptions
---

{% include toc title="Index" %}

- HTTP 401 -> Invalid
- Http 301 -> Redirect (Moved Permanently, stores in cache, less server load)
    - Clients should update their bookmarks.
- HTTP 302 -> Found (Temporary Redirect) - Redirect (used to track click rates)
    - The resource requested is temporarily under a different URL. The client
      should use the original URL for future requests.
- HTTP 503 -> Service Unavailable
- HTTP 101 -> Changed Protocol (used in WebSockets)
    - The server is switching protocols as requested by the client. This is
      often used to switch to WebSocket protocol.

# Http 429

- Too Many Requests (used in Rate limiting algo)

The exception `java.net.SocketException: Too many open files`
typically indicates that the operating system's limit on the number of **open
file descriptors** has been exceeded.
This can happen if your application or the underlying system is trying to open
more files (like network connections in this case)
than the allowed limit.

This is a subclass of `IOException` and is typically thrown when a
socket-related operation encounters an error.

In the context of networking in Java, this usually happens when your application
is making network connections (like HTTP requests) and
each connection opens a file descriptor internally. If your application or
system attempts to open more connections than the operating
system allows, a SocketException with this message can be thrown.

Operating System Limit: Every operating system has a limit on how many files (
including sockets) can be opened simultaneously by a process. This limit is set
to prevent resource exhaustion and to maintain system stability.

By default, macOS sets a soft limit of 256 file descriptors per process. This
can be checked and adjusted using the following commands:

Check current limits:

```shell
ulimit -n
```

Set a higher limit temporarily (e.g., 1024):

```shell
ulimit -n 1024
```

Set a higher limit permanently (in macOS):
You can modify system-wide or user-specific limits in macOS using configuration
files like /etc/sysctl.conf, /etc/launchd.conf, or modifying user's shell
profile (~/.bash_profile, ~/.zshrc, etc.).

On Windows, the limit for open file descriptors (or handles) is much higher
compared to macOS, and it's typically not a common source of errors like on
Unix-based systems. Windows has a per-process limit of 2048 handles by default,
but this can be extended if necessary.

```java
try {
    return Business.blockingDbCall(2);
} catch (IOException e) {
    System.err.println("Error in dbCall: " + e.getMessage());
    if (e.getMessage().contains("429")) {
        return "Default dbCallResult (Too Many Requests)";
    } else if (e.getMessage().contains("503")) {
        return "Default dbCallResult (Service Unavailable)";
    }
    throw new RuntimeException(e); // Propagate other exceptions
}
```