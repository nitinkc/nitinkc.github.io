---
# layout: static
title:  "Hosting personal website on home router"
date:   2022-01-22 21:55:00
categories: ['Developer tools']
tags: ['Developer tools']
---

# Port Forwarding on Home Router

In order to use the web server truly as a remote web server, we have to make it accessible outside the LAN. This can be achieved via port forwarding.

Configure the router to forward ports. If an external client sends a request over a particular port of the router, the router can pass it along to different IP addresses.

An excellent article can be found [here](http://www.howtogeek.com/66214/how-to-forward-ports-on-your-router/)

Suppose office ip address is `2601:641:101:1800:cc28:72aa:64:a454` 

The comcast business router default values are
http://10.1.10.1/
user: cusadmin
password: highspeed

![port forwarding]({{ site.url }}/assets/images/prot-forward.JPG)

Here the server IP address is the address of the computer inside the LAN running HTTP Server


# ssh-enabled

* Login to router and enable port forwarding for SSH on port 80.
* Find out the Routers ip-address. This address is exposed to the outside world. Find [ipv4/ipv6](http://ipv4.whatismyv6.com/) address.
* Check the status of the ports at [You get Signal](http://www.yougetsignal.com/tools/open-ports/)
* Login from any computer in the world using `ssh synergy@67.170.249.191`where 67.170.249.191 is the Router address.


# Publish Website

Publish your website by keeping the index.html of the project in the directory /var/www/html.

If the Port Forwarding is set to Port 80 in the Router, you can access the website using your IP Address from any where in the world.

eg: http://67.170.249.191

Using DDNS service, you can register this IP address with a Domain Name String.

# DNS

Since it is harder to remember IP addresses like 67.170.249.191, use DDNS service. You can find service providers, both paid and free. One free provider is 


