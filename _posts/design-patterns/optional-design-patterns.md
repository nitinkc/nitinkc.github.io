
    public List<EmployeeSimple> countByName()

Do not return a null, instead return an empty *collection*. Effective Java

```java
//return Collections.emptyList();

//using Static Factory - takes care of empty List
return List.of();//Returns an unmodifiable list containing zero elements.
```
Instead of returning null return Optional<T>

    public  EmployeeSimple countByName()

If a method will always have a single value as return **donot use** Optional.

var a = SampleData.getSimpleEmployees();

        //a = "Nitin";//Strict type checking


* Don't use Optional<T> as a parameter to methods. If needed, use overloading instead.
```java
    public static void methodName(String str)
    public static void methodName(Optional<String> name); //Anti-pattern - DO NOT DO THIS
```

Optional in the argument will force/punish the programmers/users when the method is invoked
```java
        methodName(Optional.of(str));
        methodName(Optional.empty());
```

use this
```java
public static void methodName(Optional<String> name); //Anti-pattern - Split into the below


public static void methodName1(String name){
        return;
    }

public static void methodName(){ //Overloaded
        return;
}
```

* There is little reason to use Optional as a field.

