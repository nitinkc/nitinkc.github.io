---
title:  "Method Reference"
date:   2022-11-18 08:30:00
categories: ['Java']
tags: ['Java']
---


* Lambda expression can access static variables, instance variables,
* effectively final variables and effectively Final local variables

For Simpler one liner Lambdas, with or without parameters


```java
.map(w ->  vcw.toLowerCase())

.map(String :: toLowerCase())
```

And it turns out that when we have any one of these four forms but notice it must be exactly these four forms we don't
get to reorder the arguments or anything like that

private static final Pattern WORD_BREAK = Pattern.compile("\\W+");

//Word break is an object .flatMap( l -> WORD_BREAK.splitAsStream(l))
.flatMap(WORD_BREAK::splitAsStream)


## The Four Kinds of Method References

| **Description**                                                                                                        | **Lambda**         				  			  | **Example Lambda**              | **Method Ref**             | **Method Reference**    |
|------------------------------------------------------------------------------------------------------------------------|------------------------------------------------|--------------------------------|----------------------------|-------------------------|
| Take arguments and invoke a static method on a class passing exactly the same arguments								 |(param) -> Class.staticMethod(param)			  | x -> Math.cos(x)               | SomeClass::staticMethod    | Math::cos               |
| Produces a lambda that takes exactly as many arguments as the method expects                                           |(param) -> object.instanceMethod(param) 		  | () -> someString.toUpperCase() | someObject::instanceMethod | someString::toUpperCase |
| Take the first argument from the lambda, and use that to invoke a method, passing remaining arguments as method params |(object, param) -> object.instanceMethod(param) | s -> s.toUpperCase()           | SomeClass::instanceMethod  | String::toUpperCase     |
| Takes the params of Lambda and passes them to a constructor                                                            |(param) -> new ClassName(param)				  | () -> new Employee()           | SomeClass::new             | Employee::new           |

## Reference to an instance method of a particular object

<details>
    <summary> 
    View Functional Interface & Class
    </summary>
{% gist nitinkc/9e72f492d1dc4ccd37870e5989788c55 %}
</details>

By creating a class and using its method to be passed as a Lambda
```java

MethodReferencesExample obj = new MethodReferencesExample();
// Reference to the method using the object of the class myMethod
Display display = ((a,b) -> obj.myMethod(a,b));//A Lambda needs a Functional Interface (Display)
display = obj::myMethod;//method reference

// Calling the method inside the functional interface Display
display.displayResults(1,3);
```