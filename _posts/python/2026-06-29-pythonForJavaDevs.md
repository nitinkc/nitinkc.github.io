---
title: Python Internals for Java Developers: A Tour Under the Hood
date: 2026-06-29 11:15:28
categories:
- Python
tags:
- Programming
- Fundamentals
---

{% include toc title="Index" icon="cog" %}


*An advanced comparative look at CPython's runtime, aimed at engineers who already know how the JVM works.*

You already know that "the language" and "the runtime" are two different things. Java the language is statically typed with explicit compilation to bytecode, executed by the JVM with a JIT, generational GC, and a memory model spec'd down to the happens-before relationship. Python — specifically CPython, the reference implementation — solves the same general problem (run high-level code fast-ish, manage memory, support OOP, support concurrency) with a wildly different set of trade-offs. The fastest way for you to get fluent in Python internals is to map each CPython mechanism onto the JVM mechanism you already understand, then study where the mapping breaks.

This post does exactly that, in five parts: the execution model, the object model, memory management, the concurrency story, and the dynamic dispatch machinery.

## 1. Execution Model: Bytecode Without a JIT (Usually)

Java compiles `.java` to `.class` bytecode ahead of time via `javac`. The JVM loads classes, verifies bytecode, interprets it initially, and the JIT (C1/C2, or Graal) profiles hot methods and compiles them to native machine code at runtime — tiered compilation.

CPython also compiles to bytecode, but the pipeline looks different. Source goes through a tokenizer, then a parser that builds an AST (this changed in 3.9+ to a PEG parser instead of the old LL(1) grammar), then a compiler pass that walks the AST and emits bytecode for a **stack-based virtual machine**. That bytecode is cached as `.pyc` files in `__pycache__`, keyed by a hash or mtime of the source — conceptually similar to how you might cache compiled classes, except there's no separate `javac` step the user runs; it happens transparently and lazily, per module, on import.

The critical difference: **CPython has no JIT by default.** The bytecode is interpreted by a giant C function called the *evaluation loop* — `_PyEval_EvalFrameDefault` in `ceval.c` — which is essentially a massive switch statement (in newer versions, a computed-goto dispatch table for speed) over opcodes. Every `LOAD_FAST`, `BINARY_ADD`, `CALL_FUNCTION` you'd see in `dis.dis()` output gets dispatched here, one opcode at a time, with no native code generation. This is why naive Python is typically 30-100x slower than equivalent Java for CPU-bound work: you're paying interpreter dispatch overhead on every single operation, where the JVM's JIT has long since inlined and devirtualized your hot path into machine code.

This is also why **PyPy** exists — it's a Python implementation with a tracing JIT, and it gets you JVM-like speedups for hot loops. And as of Python 3.11+, CPython itself ships a "specializing adaptive interpreter" (PEP 659): the interpreter rewrites bytecode in-place to specialized, faster variants once it observes the types involved at a call site (e.g., `BINARY_ADD` becomes `BINARY_ADD_INT` after it sees two ints). That's a much lighter-weight cousin of what HotSpot's tiered JIT does, more inline caching than true native compilation, but it closes some of the gap. Python 3.13 added an experimental JIT (copy-and-patch) behind a build flag, but it's not the default and nowhere near Graal-level sophistication yet.

```
Java:    source.java → javac → .class bytecode → JVM interprets → JIT compiles hot paths → native code
CPython: source.py   → compile() → .pyc bytecode → ceval.c interprets, forever (mostly)
```

## 2. The Object Model: Everything Is a `PyObject*`

In the JVM, primitives (`int`, `boolean`, `double`) are unboxed by default and live on the stack or inline in objects; only when you box them (`Integer`, autoboxing) do they become heap objects with identity and a vtable pointer. Reference types are objects with a header (mark word + klass pointer in HotSpot) followed by fields.

CPython has no unboxed primitives at the language level. **Every single value is a `PyObject*`** — a pointer to a heap-allocated C struct. Every `PyObject` starts with this header:

```c
typedef struct _object {
    Py_ssize_t ob_refcnt;   // reference count
    PyTypeObject *ob_type;  // pointer to the type object
} PyObject;
```

So `x = 5` doesn't put `5` on a stack slot the way Java would; it allocates (or reuses — see below) a `PyLongObject` on the heap, and the local variable `x` in the frame is a pointer to it. This is the single biggest reason Python is memory-hungry and slow for numeric work compared to Java: a Java `int[]` is a contiguous block of 4-byte values; a Python `list` of ints is an array of pointers to separately-heap-allocated `PyLongObject`s, each of which carries a refcount, a type pointer, and arbitrary-precision digit storage — easily 28+ bytes for a single small integer.

`ob_type` is roughly analogous to the JVM's klass pointer — it's how Python knows "what type is this object," and it's how method dispatch works (more in section 5). Every type — `int`, `str`, your custom classes — is itself a `PyTypeObject`, which is itself a `PyObject` (specifically an instance of `type`, the metaclass). This reflexivity — "classes are objects, and the class of a class is `type`" — is conceptually similar to `java.lang.Class<T>`, except in Java, `Class` objects are a separate, special reflection mechanism bolted onto a statically-typed system. In Python, the metaclass mechanism *is* the object system; there's no separate "reflection API," because introspection is just normal object access.

**CPython optimization worth knowing:** small integers from -5 to 256 are pre-allocated and cached at interpreter startup (`small_ints` array). `x = 5; y = 5` gives you `x is y == True` not because of value equality but because both point to the *same cached object* — this is CPython's version of Java's `Integer` cache for `-128..127` via `Integer.valueOf()`, except Python applies this trick pervasively, not just to one boxed wrapper type, because everything is already boxed.

## 3. Memory Management: Reference Counting + Cycle Detector, Not Generational GC

Here's where the architectures diverge hardest. The JVM's GC (G1, ZGC, Shenandoah, whatever you're running) is a **tracing collector**: it periodically walks the object graph from GC roots, marks reachable objects, and reclaims everything else. Allocation is typically a bump-pointer in TLAB (thread-local allocation buffer), and deallocation happens in batches during a GC pause (or concurrently, for the fancier collectors).

CPython's primary mechanism is **reference counting**. That `ob_refcnt` field in every `PyObject` header is incremented every time a new reference is taken (assignment, passing to a function, storing in a container) and decremented when a reference goes out of scope. When it hits zero, the object is **immediately and deterministically deallocated** — no GC pause, no stop-the-world, the memory is freed right then in that line of code. This is much closer to C++'s `shared_ptr` than to anything in the JVM. It's also why `__del__` (Python's destructor-ish hook) fires deterministically and predictably in CPython — something you cannot rely on with `finalize()`/`Cleaner` in Java, where the GC decides when (or if) to run it.

The catch: reference counting alone cannot collect cycles. A linked list node pointing to itself, or two objects each holding a reference to the other, will never hit a refcount of zero even if nothing else in the program can reach them. So CPython layers a secondary **generational tracing garbage collector** (the `gc` module) on top, specifically to find and break reference cycles. It only has to consider "container" objects (anything that can hold references to other objects — lists, dicts, instances, etc.), not every object, because non-container types like `int` and `str` can never participate in a cycle. This generational collector works in 3 generations, much like the JVM's young/old generation split, with the same underlying assumption (the "weak generational hypothesis": most objects die young), but it's there only as a backstop for cycles, not as the primary allocation/reclamation mechanism the way it is in Java.

Practical consequence for you as a Java dev: in Java, holding a reference 10ms longer than necessary is usually harmless because GC handles it. In Python, refcounting means memory pressure and deallocation timing are much more directly tied to your code's reference lifetimes — which is great for predictability but means reference cycles (common in things like parent/child object graphs, observer patterns, doubly linked structures) are a real and recurring footgun if you disable or don't trust the cyclic GC.

## 4. Concurrency: The GIL vs. the JMM

This is usually the biggest culture shock. Java's memory model gives you real OS-level threads, true parallel execution across cores, and a formally specified happens-before relationship you use `volatile`, `synchronized`, and `java.util.concurrent` to navigate. Multiple Java threads can execute bytecode on different cores simultaneously, genuinely in parallel.

CPython has the **Global Interpreter Lock (GIL)**: a single mutex that ensures only one thread executes Python bytecode at a time, period, regardless of how many cores you have. Threads still exist as real OS threads, and they're genuinely useful for I/O-bound concurrency (the GIL is released during blocking I/O calls, network requests, file reads, `time.sleep`, and inside many C extensions like NumPy during heavy computation) — but for CPU-bound pure-Python code, multithreading in CPython gives you *no* parallelism. Two threads doing `for i in range(10**8): x += 1` will not run faster than one; they'll actually run slightly *slower* due to GIL contention overhead (the GIL switches roughly every 5ms by default, or every N bytecode instructions in older versions).

This is why the standard CPU-bound parallelism story in Python is **multiprocessing**, not multithreading — spin up separate OS processes (each with its own interpreter, own GIL, own memory space) and communicate via pickling and IPC, which is a much heavier-weight model than Java's shared-memory threads.

Two things worth knowing if you're tracking the cutting edge: **PEP 703**, which made the GIL optional ("free-threaded" builds, `python3.13t`), landed as an experimental, non-default build option in 3.13 and is being hardened further; the long-term plan is for it to eventually become the default, but as of now you have to explicitly opt in, and the ecosystem (C extensions especially) is still catching up. Until that lands as default and stabilizes, assume any CPython you're handed has a GIL.

The GIL exists largely *because* of reference counting: incrementing/decrementing `ob_refcnt` from multiple threads without locking is a data race, and locking every single refcount operation individually would be far slower than one big lock. So sections 3 and 4 are causally linked — it's a direct architectural consequence, not an arbitrary design choice, and it's exactly the kind of thing the free-threaded build had to solve (it uses biased reference counting and per-object locks instead).

## 5. Dynamic Dispatch: Dunder Methods vs. Vtables

Java's virtual method dispatch is resolved via a **vtable** lookup on the object's class — fast, O(1), and the whole point of `virtual`/`final`/devirtualization optimizations the JIT performs once it's confident about the concrete type at a call site.

Python's dispatch for operators and built-in protocols works through **dunder methods** (`__add__`, `__len__`, `__iter__`, `__getattr__`, etc.) looked up not on the instance, but on the **type**, and for built-in operations, CPython actually bypasses the instance `__dict__` lookup entirely and goes through C-level "slots" on the `PyTypeObject` (`tp_as_number->nb_add`, etc.) for speed — this is the closest thing CPython has to a vtable, and it's exactly why redefining `__add__` on an *instance* (`obj.__add__ = ...`) silently does nothing for operators like `+`, while redefining it on the *class* works. This trips up almost every Java developer the first time, because in Java there's no equivalent ambiguity — methods are always resolved through the class/vtable, never shadowed by an instance field of the same name in a way that breaks dispatch.

Regular attribute and method access (`obj.method()`) is a different and slower path: it walks `obj.__dict__`, then the type's MRO (Method Resolution Order, computed via C3 linearization for multiple inheritance — a genuinely more principled algorithm than Java's single-inheritance-plus-interfaces model, since Python supports full multiple inheritance and needs a deterministic way to resolve diamond problems). This dict-based lookup is also why Python instances are comparatively memory-heavy and why accessing `obj.x` is slower than a Java field access — there's no fixed-offset memory layout the way HotSpot lays out object fields; it's a hash table lookup, unless the class uses `__slots__` to opt into a fixed-layout, more Java-like representation (which also saves the per-instance `__dict__` overhead, making `__slots__` worth knowing if you're optimizing object-heavy Python code).

## Summary Table

| Concept | Java/JVM | CPython |
|---|---|---|
| Compilation | AOT to bytecode, JIT at runtime | Bytecode compiled lazily, mostly interpreted |
| Primitives | Unboxed by default | Everything boxed (`PyObject*`) |
| Memory reclamation | Tracing GC (generational) | Refcounting, primary; tracing GC for cycles only |
| Object destruction | Non-deterministic (`finalize`/Cleaner) | Deterministic (`__del__` on refcount 0) |
| Threading | Real parallelism, JMM, `volatile`/locks | GIL serializes bytecode execution (until free-threaded builds) |
| CPU-bound parallelism | Threads | Processes (or free-threaded 3.13+) |
| Method dispatch | Vtable, class-based, fast | Type-level slots (operators) or dict+MRO walk (general) |
| Multiple inheritance | Not allowed (interfaces only) | Allowed, resolved via C3 linearization |

## Where to Look Next

If you want to go further than reading about it, `dis.dis(your_function)` will show you the actual bytecode the way `javap -c` shows you JVM bytecode — pull up something simple and compare it side by side with what you'd expect from `javac`. `sys.getrefcount(obj)` lets you watch reference counting happen live. And reading `Include/object.h` and `Python/ceval.c` in the CPython source tree (it's plain, fairly readable C, not unapproachable) will make everything in this post concrete rather than abstract — which, as a language internals person, is really the only way any of this sticks.
