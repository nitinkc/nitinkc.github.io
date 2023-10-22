---
title:  "Method Reference"
date:   2022-11-18 08:30:00
categories: ['Java']
tags: ['Java']
# classes: single
# layout: splash
---

{% include toc title="Index" %}

Method reference only works where there is a possibility of passing a Lambda as an argument.

Lambda can be replaced by method reference

## The Four Kinds of Method References

1 |**Ref. to a static method**                                        | Pass arguments to call a static method, using the same arguments.								                                                                                       
2 |**Ref. to an instance method of a specific object**                | Passing a Method Reference to a method on another instance <br/>Produces a lambda that takes exactly as many arguments as the method expects                                            
3 |**Ref. to an instance method of an any object of a specific type** | Passing a method reference that takes parameters. <br/>It takes the first argument from the lambda and uses it to invoke a method, passing the remaining arguments as method parameters
4 |**Ref. to a constructor**                                          | Takes the params of Lambda and passes them to a constructor

| **#** | **Lambda**         				  			                    | **Example Lambda**                                                                                             | **Method Ref style**        | **Method Reference**                                                                                                   |
|:------|:------------------------------------------------|:---------------------------------------------------------------------------------------------------------------|:----------------------------|:-----------------------------------------------------------------------------------------------------------------------|
| **1** | (param) -> Class.staticMethod(param)            | `(x,y) -> Math.hypot(x,y)` <br/> `x -> System.out.println(x)` <br/> `(str) -> MyStringUtils.isPalindrome(str)` | SomeClass::staticMethod     | `Math::hypot` <br/> `System.out :: print` <br /> `MyStringUtils :: isPalindrome`                                       |
| **2** | (param) -> object.instanceMethod(param)         | `() -> someString.toUpperCase()` <br/> `(a,b) -> myApp.appendStrings(a,b)` <br/> `() -> obj.test()`            | someObject::instanceMethod  | `someString::toUpperCase` <br/> `myApp::appendStrings` <br/> `obj :: test`                                             | 
| **3** | (object, param) -> object.instanceMethod(param) | `s -> s.toUpperCase()` <br/> `(String a, String b) -> a.compareToIgnoreCase(b)`                                | SomeClass::instanceMethod   | `String::toUpperCase` <br/> `String::compareToIgnoreCase` <br/> `employees.stream().sorted(Employee::salaryDifference)`|
| **4** | (param) -> new ClassName(param)                 | `() -> new Employee()`                                                                                         | SomeClass::new              | `Employee::new`                                                                                                          |

**Instance method** are methods which can only be invoked through an object of the class. It needs an object if a class to be called.

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

Comparator<EmployeeSimple> salaryComparator = (e1, e2) -> Double.compare(e1.getSalary(), e2.getSalary());
Comparator<EmployeeSimple> salaryComparatorMethodRef =  EmployeeSimple::salaryDifference;
list.stream().sorted(EmployeeSimple::salaryDifference).forEach(System.out::println);

public int salaryDifference(final EmployeeSimple other) {
    return this.getSalary().compareTo(other.getSalary());
}
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