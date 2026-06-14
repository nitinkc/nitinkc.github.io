---
title: Passwords in DB
date: 2024-06-13 11:02:00
categories:
- System Design
tags:
- Security
- Database
---

{% include toc title="Index" %}

![](https://www.youtube.com/watch?v=zt8Cocdy15c)

# OWASP guidelines for storing Passwords into the DB

[OWASP guidelines](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html#:~:text=Hashing%20and%20encryption%20can%20keep,appropriate%20approach%20for%20password%20validation.)

### One way Password **Hashing** Algorithm

- slower thus discourages Brute force att
- MD5, SHA-1 -> Fast, less secured so shouldn't be used

Vulnerable to pre-computation attacks like
- rainbow tables
- databased-based lookups

### Adding Salt to Password

Salt: Unique Randomly generated String

Hash (password + Salt) -> Ensures that the hash is unique to each password

makes pre-computation attacks unattractive

PAssword mnatching

Inm the DB, salt and hash value is kept in two columns

when the uses tries to login, the salt is fetched, added to the password user
input, and hash value is calculated and matched with the DB column