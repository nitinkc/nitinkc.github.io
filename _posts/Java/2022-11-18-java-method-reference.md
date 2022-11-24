---
title:  "Method Reference"
date:   2022-11-18 08:30:00
categories: ['Java']
tags: ['Java']
classes: single
layout: splash
---

Method reference only works where there is a possibility of passing a Lambda as an argument.

Lambda can be replaced by method reference

## The Four Kinds of Method References

| **Description**                                                                                                                                                                                                                                                   | **Lambda**         				  			  | **Example Lambda**                                                                                                                                                                              | **Method Ref style**       | **Method Reference**                                                                                              |
|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------|-------------------------------------------------------------------------------------------------------------------|
| **Ref. to a static method** <br/> Take arguments and invoke a static method on a class passing exactly the same arguments								                                                                                                                                 |(param) -> Class.staticMethod(param)			  | (x,y) -> Math.hypot(x,y) <br/> x -> System.out.println(x) <br/> (str) -> MyStringUtils.isPalindrome(str)                                                                                        | SomeClass::staticMethod    | Math::hypot <br/> System.out :: print <br /> MyStringUtils :: isPalindrome                                        |
| **Ref. to an instance method of a particular object** <br/>Passing a Method Reference to a method on another instance <br/>Produces a lambda that takes exactly as many arguments as the method expects                                                           |(param) -> object.instanceMethod(param) 		  | () -> someString.toUpperCase() <br/> (a,b) -> myApp.appendStrings(a,b) <br/> () -> obj.test()                                                                                                   | someObject::instanceMethod | someString::toUpperCase <br/> myApp::appendStrings <br/> obj :: test                                              |
| **Ref. to an instance method of an arbitrary object of a particular type** <br/>Passing a Reference of a Method That Takes Parameters <br/>Take the first argument from the lambda, and use that to invoke a method, passing remaining arguments as method params |(object, param) -> object.instanceMethod(param) | s -> s.toUpperCase() <br/> (String a, String b) -> a.compareToIgnoreCase(b) <br/>  employees.stream().sorted((e1, e2) -> Double.compare(e1.getSalary(), e2.getSalary()))                     | SomeClass::instanceMethod  | String::toUpperCase <br/> String::compareToIgnoreCase <br/> employees.stream().sorted(Employee::salaryDifference) |
| **Ref. to a constructor** <br/>Takes the params of Lambda and passes them to a constructor                                                                                                                                                                        |(param) -> new ClassName(param)				  | () -> new Employee()                                                                                                                                                                            | SomeClass::new             | Employee::new                                                                                                     |

**Instance method** are methods which can only be invoked through an object of the class. It needs an object if a class to be called.

## Reference to an instance method of a particular object

<details>
    <summary> 
    View Functional Interface & Class
    </summary>
{% gist nitinkc/9e72f492d1dc4ccd37870e5989788c55 %}
</details>

By creating a class and using its method to be passed as a Lambda


Declare the Lambda directly
```java
Display<Integer> displayDeclaredHere = (a, b) -> System.out.println("method reference in java 8 : " + (a + b));
displayDeclaredHere.displayResults(5,55);
```

The Lambda can extracted as a private method

```java
Display displayExtractedSameClass = getDisplay();//this::getDisplay works with non-static classes
displayExtractedSameClass.displayResults(10,20);

private static Display getDisplay() {
    return (a, b) -> System.out.println("method reference in java 8 : " + a + b);
}
```
Taking the definition into another class, or using another class to define the interface
```java
MethodReferences obj = new MethodReferences();
// Reference to the method using the object of the class myMethod
Display<Integer> displayInstanceMethodParticularObject = ((a,b) -> obj.myMethod(a,b));//putting the definition in object of another class
// Calling the method inside the functional interface Display
displayInstanceMethodParticularObject.displayResults(1,3);
```

calling the same via method reference
```java
Display<Integer> displayReferenceInstanceMethodParticularObject = obj::myMethod;
displayReferenceInstanceMethodParticularObject.displayResults(6,6);
```

# Examples

```java
MethodReferences myApp = new MethodReferences();
// Calling the method with a lambda expression
System.out.println(myApp.playBiFunction("Hello ", "World!", (a, b) -> a.concat(b)));
```

Reference to an instance method of an **arbitrary object** of a particular type
```java
System.out.println(myApp.playBiFunction("Hello ","World!", String::concat));
```
Reference to an **instance method** of a particular object
```java
System.out.println(myApp.playBiFunction("Hello ","World!", ((a,b) -> myApp.appendStrings(a,b))));
System.out.println(myApp.playBiFunction("Hello ","World!", myApp::appendStrings));
```
Reference to a static method
```java
System.out.println(myApp.playBiFunction("Hello ", "World!", MethodReferences::staticAppendStrings));
```

Calling Static method From Math Library
```java
System.out.println(myApp.playBiFunction(3.0,4.0, (x,y) -> Math.hypot(x,y)));
// Reference to a static method
System.out.println(myApp.playBiFunction(3.0,4.0, Math::hypot));
```