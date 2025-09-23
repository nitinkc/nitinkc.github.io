---
categories: Microservices
date: 2024-04-19 21:00:00
tags:
- Spring Boot
title: ssl Security Certificate Issue
---

{% include toc title="Index" %}

Solution for the issue on Local microservice testing
Caused by: `javax.net.ssl.SSLHandshakeException`: PKIX path building failed:
`sun.security.provider.certpath.SunCertPathBuilderException`:
unable to find valid certification path to requested target

Certificate issue for Mac and Windows users when opening GKE URLs from UI:
![postmanSsl.png]({{ site.url }}/assets/images/postmanSsl.png)

# Update Postman Certificate Authority (Mac)

Download the certificate from the web browser
![sslDownload.png]({{ site.url }}/assets/images/sslDownload.png)

##### Update CA Certificate

For Macbook double-click, and it will install or open `Key Chain Access`
![ssl-keychain.png]({{ site.url }}/assets/images/ssl-keychain.png)

Export the certificate from Keychain access and Save it as pem file

If you would like to convert your binary .cer file to an ascii .pem file run
this command

```shell
openssl x509 -inform der -in "My_Enterprise_Root_CA.cer" -out "My_Enterprise_Root_CA.pem"
```

# Application

![sslIssueFix.png]({{ site.url }}/assets/images/sslIssueFix.png)

# Postman Settings

Turn On/Off based on the certificate

![sslPemFileinPostman.png]({{ site.url }}/assets/images/sslPemFileinPostman.png)

# Install the certificate in JDK

When developing microservice that needs connection to GKE endpoints,
the local machines need have cert imported to java keystore.

path of jdk installation:
/Library/Java/JavaVirtualMachines/jdk-11.0.8.jdk/Contents/Home/lib/security/cacerts.

please execute the command with the path added in it:

```shell
sudo keytool -import -file /Users/${UserName}/Documents/My_Enterprise_Root_CA.cer \
-keystore /Users/${UserName}/Library/Java/JavaVirtualMachines/corretto-21.0.3/Contents/Home/lib/security/cacerts
```

if it asks for 2 passwords then

- 1st password would be your mac/windows login password
- 2nd password would be "changeit"