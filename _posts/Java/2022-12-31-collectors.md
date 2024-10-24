---
title:  "Collectors"
date:   2022-12-31 05:00:00
categories: ['Java']
tags: ['Java']
---

{% include toc title="Index" %}

### Collect

Collect the data into a list using the mose used method
`collect(Collectors.toList())`

Pass a kep mapper function adn value mapper function to create a map
`.collect(Collectors.toMap(Function.identity(), String::length))`

If data need to be passed to a client, its a good idea to use unmodifiable
collection
`.collect(Collectors.toUnmodifiableList())`

Returns an immutable list containing only one specified object
`Collections.singletonList(s)`

```java
String s = parentDto.getStringList().get(0);
parentDto.setStringList(Collections.singletonList(s));
```

### Partitioning

Split the collection into 2 groups.

`Collectors.partitioningBy` accepts a predicate and returns a map with one key
for `true` with all the values
with true results and another with false results.

```java
List<Integer> list = Arrays.asList(1,2,1,3,3,4,5,6,7,8,6,5,4,3,2,1);
Map<Boolean, List<Integer>> collect = list.stream()
        .collect(partitioningBy(number -> number % 2 == 0));
        System.out.println(collect);//{false=[1, 1, 3, 3, 5, 7, 5, 3, 1], true=[2, 4, 6, 8, 6, 4, 2]}
```

Predicate can be extracted out and can be passed as an argument

```java
Map<Boolean, List<Integer>> listMap = employees.stream()
                .filter(Objects::nonNull).filter(emp -> null != emp.getAge())
                .filter(emp -> null != emp.getAge())
                //.collect(partitioningBy(x -> evenAgedEmpPredicate.test(x)));
                .collect(partitioningBy(evenAgedEmpPredicate));
```

### GroupingBy

`Collectors.groupingBy` takes a function as first parameter that determines the
key od the return map
and another Collector that can have the vlaues. The collector can be another
operation that returns a collector
like filtering, mapping, filtering etc.

```java
List<Integer> list = Arrays.asList(1,2,1,3,3,4,5,6,7,8,6,5,4,3,2,1);

//Find frequency of all the numbers
Map<Integer,Long> map = list.stream()
     //.collect(groupingBy(element -> element, counting()));// Function.identity() Equivalent to an i in a for loop
       .collect(Collectors.groupingBy(Function.identity(), counting()));//collect takes a COLLECTOR as parameter. any method that returns a collector can be used

System.out.println(map);//{1=3, 2=2, 3=3, 4=2, 5=2, 6=2, 7=1, 8=1}
```

map (with streams) takes a `Stream<T>` returns `Stream<R>`. It transforms from
one style to another
mapping (with collectors) -> transforming in the middle of reduce

filter -> Acts on Streams, filtering -> Acts on reduce operation with collector

### Filtering

`Collectors.filtering()` takes a predicate as a first argument and another
Collector as second argument.

```java
List<Integer> list = List.of(1,2,1,3,3,4,5,6,7,8,6,5,4,3,2,1);
List<Integer> evenNumberList = list.stream()
      .collect(filtering(number -> number % 2 == 0, toList()));
System.out.println(evenNumberList);//[2, 4, 6, 8, 6, 4, 2]
```

### Mapping

`Collectors.mapping` takes a function (as first parameter) based on which the
transformation happens
and a Collector as second parameter

```java
List<Integer> list = List.of(1,2,1,3,3,4,5,6,7,8,6,5,4,3,2,1);
List<Integer> doubleNumberList = list.stream()
        .distinct()//Finds unique elements 
        .collect(Collectors.mapping(number -> number * 2 , Collectors.toList()));
System.out.println(doubleNumberList);//[2, 4, 6, 8, 10, 12, 14, 16]
```

### Flat Mapping

flatMapping applies the map first and then does the flattening.
`Collectors.flatMapping` takes a Stream (like an iterator)
as first input and takes Collector as second parameter. With the mapping
function, use of Stream.of or collections.stream()

The method signatures of map from Stream and flatMap of Collectors looks like
below

```java
 <R> Stream<R> flatMap(Function<? super T, ? extends Stream<? extends R>> mapper); 
 <R> Stream<R> map    (Function<? super T, ? extends R> mapper)
```

```java
List<String> list = List.of("one", "two wings", "three tyres", "four turbo combustion engine");
//Fnd a list of each word separated without space
List<String> collect = list.stream()
        .collect(
                flatMapping(str -> Stream.of(str.split(" ")), toList()
                )
        );
System.out.println(collect);//[one, two, wings, three, tyres, four, turbo, combustion, engine]
```

## Do's and Scenarios

* If you have a one-to-one function , use a map to go from `Stream<T>` to
  `Stream<R>`

```java
List<Integer> numbers = List.of(1,2,3,4);

//one-to-one function
//Stream<T>.map(oneToOneFunction) ==> Stream<R>
 List<Integer> collect = numbers.stream()
      .map(element -> element * 2)//Takes a Stream of <T> and returns a Stream of <R>
      .collect(Collectors.toList());
System.out.println(collect);//[2, 4, 6, 8]
```

* If you have a one-to-many function , use a map to go from `Stream<T>` to
  `Stream<Collection<R>>`

```java
//one-to-many
//Stream<T>.map(oneToManyFunction) ==> Stream<List<R>>
List<List<Integer>> collect = numbers.stream()
        .map(element -> List.of(element + 1, element - 1))
        .collect(Collectors.toList());
System.out.println(collect);//[[2, 0], [3, 1], [4, 2], [5, 3]]
//use Case : Given a list of employees, give the personal email id and official email id as pair
```

* If you have a one-to-many function , use a flatMap to go from `Stream<T>` to
  `Stream<R>`

```java
//one-to-many function
//Stream<T>.map(oneToManyFunction) ==> Stream<R> (not Stream of List of R)
List<Integer> numbers = List.of(1,2,3,4);

List<Integer> collect = numbers.stream()
        .flatMap(element -> List.of(element + 1, element - 1).stream())
        .collect(Collectors.toList());
System.out.println(collect);//[2, 0, 3, 1, 4, 2, 5, 3]
```

For the next sections the following object structure and values are used

```java
EmployeeSimple(name=John, age=20, salary=65000.0, level=C, experience=5)
EmployeeSimple(name=Wayne, age=20, salary=65430.0, level=C, experience=4)
EmployeeSimple(name=Dow, age=30, salary=74445.0, level=B, experience=6)
EmployeeSimple(name=Jane, age=35, salary=76546.0, level=B, experience=5)
EmployeeSimple(name=Don, age=35, salary=90000.0, level=A, experience=10)
EmployeeSimple(name=Wayne, age=20, salary=65430.0, level=C, experience=4)
EmployeeSimple(name=John, age=23, salary=75430.0, level=B, experience=5)
EmployeeSimple(name=John, age=32, salary=85430.0, level=C, experience=12)
EmployeeSimple(name=null, age=null, salary=null, level= , experience=0)
EmployeeSimple(name=null, age=99, salary=85430.0, level=C, experience=12)
EmployeeSimple(name=null, age=35, salary=90000.0, level=A, experience=10)
```

### min, max & minBy maxBy

Min and Max of Streams return Optional.

```java
// Max and Min return Optional Integer
OptionalInt max = employees.stream()
        .filter(Objects::nonNull).filter(emp -> null != emp.getName()).filter(emp -> null != emp.getAge())
        .mapToInt(EmployeeSimple::getAge)
        .max();//35
```

With Collectors, the method is minBy and maxBy which returns an Optional of
Collector

```java
 // MaxBy and MinBy return Optional of the Object
EmployeeSimple maxBy = employees.stream()
        .filter(Objects::nonNull).filter(emp -> null != emp.getName()).filter(emp -> null != emp.getAge())
        .collect(Collectors.maxBy(
                Comparator.comparing(
                        EmployeeSimple::getAge))).orElse(new EmployeeSimple());
System.out.println(maxBy);//EmployeeSimple(name=Jane, age=35, salary=76546.0, level=B, experience=5)
        
EmployeeSimple minBy = employees.stream()
        .filter(Objects::nonNull).filter(emp -> null != emp.getName()).filter(emp -> null != emp.getAge())
        .collect(Collectors.minBy(Comparator.comparing(EmployeeSimple::getAge)))
        .orElse(new EmployeeSimple());
System.out.println(minBy);//EmployeeSimple(name=John, age=20, salary=65000.0, level=C, experience=5)
```

##### collectingAndThen

For Scenarios where the requirement is to get the entire object/collector first
and then do the map operations, use `collectingAndThen`

In the example below, the person with the max age is found first, and then the
name is taken out of the result and returned.

```java
// Find the name of the Person with max age
String maxByName = employees.stream()
        .filter(Objects::nonNull).filter(emp -> null != emp.getName()).filter(emp -> null != emp.getAge())
        .collect(
                Collectors.collectingAndThen(
                        Collectors.maxBy(Comparator.comparing(EmployeeSimple::getAge)),//Collector as the first argument
                        emp -> emp.map(EmployeeSimple::getName)//Mapping Function as the second argument
                                .orElse("")//maxBy returns an optional so use orElse for
                    )
                );
System.out.println(maxByName);//Jane

employees.stream().forEach(System.out::println);
```

```java
Map<String, Integer> byName =
     employeeSimples.stream()
             .filter(Objects::nonNull).filter(emp -> null != emp.getAge()).filter(emp -> null != emp.getName())
             .collect(groupingBy(
                             EmployeeSimple::getName, //First Argument of Grouping By
                             collectingAndThen(//Collector as Second Argument of Grouping By
                                     Collectors.counting(),//Collector as First argument of CAT (collectingNThen)
                                     Long::intValue // finisher function as second Argument
                             )//CollectingAndThen returns a Collector, so it can be further continued
        //Function.identity() can be used if there is no mapper/transformer/convertor/enricher needed
        )
             );

System.out.println(byName);//{Wayne=2, Don=1, John=3, Jane=1, Dow=1}
```

### Composing

* groupingBy, mapping takes a function as first argument and a Collector second
  argument
* groupingBy and mapping (apply a Function, and then Collector as a second
  argument)
* collectingAndThen (Collection, then use a Function as a second argument)
* teeing(Collector, Collector, operation)
* filtering takes a predicateas first argument and a Collector second argument
* It means, first apply the function or Predicate and then Collect
* collectingAndThen -> Collector as first argument adn then Function as second
  argument
* Teeing -> Java 12 - to combine 2 collectors together

### Joining

```java
List<String> strings = List.of("java", "is", "cool");
String message = String.join(" ", strings);
System.out.println(message);//Java is cool
        
String test = strings.stream()
        .collect(Collectors.joining(","));
System.out.println(test);//java,is,cool
```
