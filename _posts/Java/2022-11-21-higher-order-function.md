---
title:  "Higher Order Functions"
date:   2022-11-21 13:43:00
categories: ['Java']
tags: ['Java']
---
{% include toc title="Index" %}

### Higher-order functions 

A common higher-order function is reduce, which is more commonly known as a fold. 
This function reduces a list to a single value.


|compose|f1.compose(f2) -> first run f2, then pass the result to f1||
|andThen|f1.andThen(f2) -> first run f1, then pass the result to f2. So, f2.andThen(f1) is same as f1.compose(f2).||
|identity|Function.isdentity() creates a function whose apply method just returns the argument unchanged||

Methods that Return Functions

Two common examples are filter and map.





