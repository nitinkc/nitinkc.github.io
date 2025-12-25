---
title: Java Compilation Process & JVM Architecture
date: 2024-08-21 00:17:00
categories:
- Java
tags:
- JVM
- Architecture
---

{% include toc title="Index" %}

No preprocessing in Java

The Java compiler does not have a preprocessor in the same way that C or C++
compilers do.
In languages like C and C++, a preprocessor is used to handle directives like
`#define`, `#include`, and `#ifdef`, which are processed before the actual
compilation begins.

In Java, the compilation process involves several stages to transform Java
source code into bytecode that can be executed by the Java Virtual Machine (
JVM).

Below are the six stages of the Java compiler:

```
.java file
  |
  v
Compilation => Source Code → Lexical Analysis → Syntax Analysis → Semantic Analysis → Intermediate Code Generation → Code Optimization → Code Generation → Bytecode (.class files)
  |
  v
.class file
  |
  v
 execution and output

```

## 1. Lexical Analysis

The lexical analysis stage breaks down the raw source code into **tokens**.
Tokens are the smallest units of meaning in the source code, such as keywords,
identifiers,
operators, and literals.

**Process**:

- **Buffering**: Take complete source program in the form of a buffer.
- **Tokenization**: After buffering, The compiler reads the source code
  character by character and groups them into tokens.
    - during tokenization, all metadata related to code, like comments, are
      removed
    - if metadata is needed till the runtime, go for **Annotations**
- **Examples**: Keywords (`public`, `class`), identifiers (`MyClass`, `main`),
  operators (`+`, `=`), and literals (`42`, `"Hello"`).

**Output**: A sequence of tokens that represent the source code in a structured
format.

## 2. Syntax Analysis (Parsing)

Syntax analysis checks the tokens against the grammatical rules of the Java
language.
It builds a syntax tree (or parse tree) that represents the grammatical
structure of the source code.

**Process**:

- **Parsing**: The compiler uses the tokens to create a tree-like structure that
  represents the
  syntactical organization of the source code.
- **Syntax Tree**: The tree shows the hierarchical relationships between various
  components of the code (e.g., expressions, statements).

**Output**: An abstract syntax tree (AST) or parse tree that reflects the
grammatical
structure of the source code.

## 3. Semantic Analysis

Semantic analysis ensures that the source code adheres to the rules of Java
semantics,
such as type checking, scope resolution, and method resolution.

**Process**:

- **Type Checking**: Verifies that operations are performed on compatible
  types (e.g., adding two integers).
- **Scope Resolution**: Ensures variables and methods are declared before they
  are used.
- **Method Resolution**: Checks that method calls match method signatures.

**Output**: An annotated syntax tree or abstract syntax tree (AST) that includes
information about the semantics of the code.

## 4. Intermediate Code Generation

This stage translates the AST into an intermediate representation (IR) that
is more abstract than machine code but more detailed than the source code.

**Process**:

- **Intermediate Representation**: Converts the syntax tree into a lower-level,
  intermediate form that is easier to manipulate for optimization and code
  generation.
- **Examples**: Three-address code or bytecode.

**Output**: Intermediate code that serves as a bridge between the high-level
source code and the low-level machine code.

## 5. Code Optimization

Code optimization improves the efficiency of the intermediate code.
This stage aims to enhance performance and reduce resource usage.

**Process**:

- **Optimization Techniques**: Includes methods such as dead code elimination,
  loop optimization, and inlining functions.
- **Refinement**: The intermediate code is refined to make it faster and more
  efficient.

**Output**: Optimized intermediate code that is more efficient in terms of
execution time and resource usage.

## 6. Code Generation

Code generation translates the optimized intermediate code into machine code
or bytecode that can be executed by the JVM.

**Process**:

- **Bytecode Generation**: For Java, this involves generating bytecode
  instructions that the JVM can execute.
- **Machine Code Generation**: In other languages, this would involve generating
  machine code for the target processor.

**Output**: Java bytecode files (`.class` files) that are ready to be executed
by the JVM.

# JVM Architecture

JVM is divided into three main subsystems:

- ClassLoader
- Runtime Data Area (Memory Area)
- Execution Engine

[https://www.linkedin.com/pulse/jvm-architecture-how-internally-work-ali-as-ad/](https://www.linkedin.com/pulse/jvm-architecture-how-internally-work-ali-as-ad/)