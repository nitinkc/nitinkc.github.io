---
title:  "Java Mailing API"
date:   2022-08-23 23:35:00
categories: ['Java']
tags: ['Java']
---

{% include toc title="Index" %}

# Sending Email with an attachment via Java Mailing API

Set up the properties either from the properties file or via final variables

```java
private static final String EMAIL_HOST = "xxxx.xxxx.com";
private static final int EMAIL_PORT = 25;
private static final String EMAIL_FROM = "test.test@test.com";
private static final String PERSONAL_NAME = "Automatic Report Sending Service"
```

We can create a method that can be used to send emails from service `sendJavaEmail(String to, String subject, String msg, String pathToAttachment)`

Initially set up the properties 
```java
Properties emailProps = new Properties();
emailProps.put("mail.smtp.auth", false);
emailProps.put("mail.smtp.starttls.enable", "false");
emailProps.put("mail.smtp.host", EMAIL_HOST);
emailProps.put("mail.smtp.port", EMAIL_PORT);
emailProps.put("mail.smtp.ssl.trust", EMAIL_HOST);
```

Create a mail session
```java
Session session = Session.getInstance(emailProps);
```

Set up message with email ids, subject line
```java
Message message = new MimeMessage(session);
message.setFrom(new InternetAddress(EMAIL_FROM,PERSONAL_NAME));
message.setRecipients(Message.RecipientType.TO, InternetAddress.parse(to));
message.setSubject(subject);
```

Prepare the body part 
```java
BodyPart messageBodyPart = new MimeBodyPart();
messageBodyPart.setText(msg);
```

Prepare the attachment
```java
MimeBodyPart mimeBodyPart = new MimeBodyPart();
mimeBodyPart.setContent(msg, "text/html");
mimeBodyPart.attachFile(pathToAttachment);
```

Set up the Multipart message by adding the attachment and the email body
```java
Multipart multipart = new MimeMultipart();
multipart.addBodyPart(mimeBodyPart);
multipart.addBodyPart(messageBodyPart);
```

Finally, prepare the message with all the contents
```java
message.setContent(multipart);
```

Send the email
```java
Transport.send(message);
```

The invoking method can then use this simple invocation and as per the properties set, the email will be sent

```java
javaEmailService.sendJavaEmail("test.test@test.com","Some Daily Report "+ ZonedDateTime.now(ZoneOffset.UTC).format(DateTimeFormatter.ofPattern("E dd.MM.yyyy HH:MM:SSS a z")), "Mic Testing...1...2....3...",CSV_LOCATION);

```