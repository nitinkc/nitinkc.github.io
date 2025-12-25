---
categories: System Design
date: 2024-06-14 11:02:00
tags:
- Payment
- QR Code
- FinTech
- Mobile Payments
title: Scan to Pay
---

{% include toc title="Index" %}

Scan to pay process

# Dynamic QR Code

Merchant generates a QR code (one time single payment) and displays it to the
user

Merchant sends total amount and OrderId to the Payment Service Provider (PSP)
Gateway
The PSP Sends tghe info the database and generates a one time usable QR Code URL

The PSP Returns the QA Code URL to the Cashiers computer

Consumer Scans and pays

Consumer opens up digital wallet app and scans the code

Total amount is displayed adn consumer clicks the pay button
Wallet app notifies the PSP that the QR code has been paid

the PSP notifies the merchant that the consumer has paid the given QR Code

# Static QR Code for multiple payment