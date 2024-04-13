---
title:  "JVM Arguments"
date:   2024-04-09 12:30:00
categories: ['Java']
tags: ['Java']
---



# Compilation

`-XX:+PrintCompilation`

* -XX means it's an advanced option
* a plus or a minus indicates if we want the option to be switched on or off
* and then the option name in `SentenceCase`


`-XX:+UnlockDiagnosticVMOptions -XX:+LogCompilation`
* creates a log file like `hotspot_pid1234.log`


`-XX:-TieredCompilation` : Turn off the Tiered Compilation


```shell
java -XX:+PrintFlagsFinal
```
Check the following flags

- `CICompilerCount` -  how many threads are available to run the compiling process
- `CompileThreshold` - the number of times a method/code needs to run before it is natively compiled
```log
bool C1ProfileVirtualCalls                    = true                                   {C2 product} {default}
bool C1UpdateMethodData                       = true                                   {C2 product} {default}
intx CICompilerCount                          = 12                                        {product} {ergonomic}
bool CICompilerCountPerCPU                    = true                                      {product} {default}
intx CompileThreshold                         = 10000                                  {pd product} {default}
```