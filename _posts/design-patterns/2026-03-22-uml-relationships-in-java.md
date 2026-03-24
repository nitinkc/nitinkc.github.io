---
title: "UML Relationships in Java"
date: 2026-03-22 17:45:00
categories: [design-patterns]
tags: [uml, java]
---

{% include toc title="Index" %}

## Conceptual overview (UML basics)

`Association -> Aggregation -> Composition`

![](https://upload.wikimedia.org/wikipedia/commons/2/21/UML_association%2C_aggregation_and_composition_examples_for_a_bicycle.png){:
width="50%" height="50%" .align-right}
Wikipedia : Sometimes aggregation is referred to as composition when the
distinction between ordinary composition and aggregation is unimportant.

> **Association**: **"can-call"** - connection between classes, like a
> friendship.

> **Aggregation**: **"has-a"** relationship, where one class has (but doesn't
> own) instances of another class.

> **Composition**: **"composed of"** relationship (**Whole-Part**), where one
> class is composed of (and owns) instances of another class.

---

## Association (concept)

[https://www.uml-diagrams.org/association.html?context=class-diagrams](https://www.uml-diagrams.org/association.html?context=class-diagrams)

- General relationship
- No specific ownership or lifecycle dependency
- One-to-one, one-to-many, or many-to-many
- Represented by a simple line connecting classes

For example, a Department class may be associated with an Employee class to
represent that employees belong to different departments.

@startuml
class Department {
// Attributes and methods of Department
}

class Employee {
// Attributes and methods of Employee
}

Department -- Employee
@enduml
{: .align-right}

### Association (one-way) + multiplicity 

**Code snippet (one-to-many link)**

@startuml
class Employee {
- name: String
- id: int

  + Employee(name: String, id: int)
  + getName(): String
  + getId(): int
    }

class Department {
- employees: List<Employee>

  + Department(employees: List<Employee>)
  + addEmployee(employee: Employee): void
  + removeEmployee(employee: Employee): void
  + getEmployees(): List<Employee>
    }

Department "1" -- "0..*" Employee
@enduml
{: .align-right}

```java
public class Department {
    private List<Employee> employees;

    public Department(List<Employee> employees) {
        this.employees = employees;
    }
}

@Data
public class Employee {
    private String name;
    private int id;
}
```

### Association (two-way)

**Code snippet (bidirectional link)**
```java
public class User {
    private Email email;

    public User(Email email) {
        this.email = email;
    }
}

public class Email {
    private User recipient;

    public Email(User recipient) {
        this.recipient = recipient;
    }
}
```

@startuml
class User {
- email: Email

  + User(email: Email)
  + sendEmail(content: String): void
    }

class Email {
- recipient: User

  + Email(recipient: User)
  + send(content: String): void
    }

User -- Email : both call each other
@enduml
{: .align-right}

### N-ary association

**Code snippet (three participants)**
```java
public class Meeting {
    private final Person host;
    private final Room room;
    private final CalendarDay day;

    public Meeting(Person host, Room room, CalendarDay day) {
        this.host = host;
        this.room = room;
        this.day = day;
    }
}
```

@startuml
class Person
class Room
class CalendarDay
class Meeting

Person "1" -- "0..*" Meeting
Room "1" -- "0..*" Meeting
CalendarDay "1" -- "0..*" Meeting
@enduml
{: .align-right}

---

## Has-A relationship: composition vs. aggregation (concept)
Composition and Aggregation both represent a **"has-a"** relationship between classes, but they differ in ownership and dependency.

### Aggregation (empty diamond)

@startuml
class Car {
// Containing class
}

class Wheel {
// Contained class
}

Car o-- "4" Wheel
@enduml
{: .align-right}

- Special form of **association**
- "Whole-part" relationship
- **Weaker ownership**: The part class is less tightly bound to the whole class.
- Dependency: Parts can exist independently and be shared among multiple
  containing classes.
- **Example**: 
  - A University "has-a" Department. Departments may continue to exist independently even if the University closes.
  - A Car class may have wheels, where wheels are parts of the car but can exist independently.

```java
// Contained class
public class Wheel {
    // Attributes and methods of the wheel
}

// Containing class
public class Car {
    private final List<Wheel> wheels; // Aggregation relationship

    public Car(List<Wheel> wheels) {
        this.wheels = wheels; // Assigning wheels passed as parameter
    }
}
```

### Composition (filled diamond)
- Also known as **whole-part** Has-a relationship
- **Strong ownership**: The part class is tightly bound to the whole class.
- Part class's lifecycle is controlled by the whole class
- Indicated by a filled diamond (◆)

A Car class may have an Engine, where the Engine is a part of the Car and cannot exist independently. If the Car is destroyed, the Engine ceases to exist.

```java
// Contained class
public class Engine {
    // Attributes and methods of the engine
}

// Containing class
public class Car {
    private final Engine engine; // Composition relationship

    public Car() {
        this.engine = new Engine(); // Creating engine instance within Car
    }
}
```
@startuml
class Engine {
// Contained class
}

class Car {
- engine: Engine

  + Car()
    }

Car *-- Engine
@enduml
{: .align-right}

A House class may have rooms, where rooms are parts of the house and
  cannot exist without the house. If the House is destroyed, Rooms cease to exist.

```java
public class House {
    private List<Room> rooms;

    public House() {
        this.rooms = new ArrayList<>();
    }
}
```

@startuml
class Room {
// Room class definition
}

class House {
- rooms: List<Room>

  + House()
}

House *-- "1..*" Room
@enduml
{: .align-right}

#### Multiplicity
- Denotes the number of instances of one class related to the number of
  instances of another class.
- Represented with a number at one end of the line and a "*" (asterisk) at the
  other end.

@startuml
class Department {
- employees: List<Employee>

  + Department(employees: List<Employee>)
}

class Employee {
// Contained class
}

Department "1" *-- "0..*" Employee
@enduml
{: .align-right}

```java
// Example of multiplicity in a relationship
public class Department {
    private final List<Employee> employees; // One-to-many relationship

    public Department(List<Employee> employees) {
        this.employees = employees;
    }
}
```
--- 

## Generalization - IS-A (empty arrowhead)
Generalization/Inheritance represents an "is-a" relationship, where the subclass
inherits attributes and behaviors from the superclass.
- Denoted by an empty arrowhead pointing from the subclass
  to the superclass.
- Indicates an "is-a" relationship.
- IS-A: The property of an object being an instance of a data type.
- Subclass inherits attributes and behaviors from the superclass.

### Generalization/Inheritance (implements)
- The Is-A relationship test is also known as INHERITANCE test.
- This holds true for a child that is a subclass of any parent, be it a direct subclass or a distant child.

```java
// Parent class
public class Vehicle {
    // Attributes and methods common to all vehicles
    public Vehicle(String manufacturer, int year) { }
}

// Child class inheriting from Vehicle
public class Car extends Vehicle {
    // Additional attributes and methods specific to cars
    public Car(String manufacturer, int year, String model, int mileage) {
        super(manufacturer, year);
    }
}

public class Boat extends Vehicle {
  public Boat(String manufacturer, int year, String type, int length) {
    super(manufacturer, year);
  }
```

@startuml
class Vehicle {
String manufacturer
int year

    + Vehicle(manufacturer: String, year: int)
    + accelerate(): void
    + brake(): void
}

class Car {
String model
int mileage

    + Car(manufacturer: String, year: int, model: String, mileage: int)
    + honk(): void
    + brake(): void
}

class Boat {
String type
int length

    + Boat(manufacturer: String, year: int, type: String, length: int)
    + raiseAnchor(): void
    + lowerAnchor(): void
    + brake(): void
}

Vehicle <|-- Car
Vehicle <|-- Boat
@enduml
{: .align-right}

### Generalization/realization (extends)
- We use the _multi-inheritance_ property of **interfaces** to preserve the IS-A relationship.
  - For example, a Cat is an Animal, and a Cat is also a Pet.

**Code snippet (interface realization)**
```java
public interface Animal {
    void eat();
    void sleep();
}

public interface Pet {
    void play();
    void cuddle();
}

public class Cat implements Animal, Pet {
    public void eat() { }
    public void sleep() { }
    public void play() { }
    public void cuddle() { }
}
```

@startuml
interface Animal {
void eat();
void sleep();
}

interface Pet {
void play();
void cuddle();
}

class Cat {
implements Animal, Pet
}

Animal <|-- Cat
Pet <|-- Cat
@enduml
{: .align-right}


---

## Dependency (dashed line with arrow)

@startuml
class Engine {
// Independent class
}

class Car {
  + drive(engine: Engine): void
}

Car ..> Engine : drive(engine)
@enduml
{: .align-right}

- Denoted by a dashed line with an arrow pointing from the dependent class to
  the independent class.
- Represents a using or **"uses-a"** relationship, where one class depends on
  another class for its implementation.
- Dependencies are typically indicated by method parameters, local variables, or
  return types.

  ```java
  // Dependent class
  public class Car {
      public void drive(Engine engine) { // Dependency on Engine class
          // Implementation of drive method using Engine
      }
  }
  ```

**Code snippet (constructor injection + usage)**
```java
private final Engine engine;

public Car(Engine engine) {
    this.engine = engine;
}

public void drive() {
    engine.start();
}
```

@startuml
class Engine {
- horsepower: int
- fuelType: String

  + Engine(horsepower: int, fuelType: String)
  + start(): void
  + stop(): void
    }

class Car {
- engine: Engine

  + Car(engine: Engine)
  + drive(): void
  + stop(): void
    }

Car ..> Engine : engine
@enduml
{: .align-right}

# Using << >> for Annotations:

@startuml
interface Drivable {
// Interface
}

class Car {
// Dependent class implementing an interface
}

Car ..> Drivable : <<implements>>
@enduml
{: .align-right}

- Used to indicate properties or qualifiers of a relationship or dependency.
- Often used with dependencies to specify the nature of the relationship, such
  as <<interface>>, <<implementation>>, <<association>>, etc.

For example, if class A implements interface B, you would write "<<implements>>"
near the dashed line between class A and interface B.

```java
// Dependent class implementing an interface
public class Car implements Drivable { // <<implements>> annotation
    // Implementation of methods from Drivable interface
}
```

{% gist nitinkc/e364de658e4f8d28719df76a8dbf4c5b %}


## Elaborate end-to-end model

```java
public class Car extends Vehicle implements Drivable {
    private List<Wheel> wheels;
    private Engine engine;

    public Car(String manufacturer, String model, List<Wheel> wheels, Engine engine) {
        super(manufacturer, model);
        this.wheels = wheels;
        this.engine = engine;
    }
}

public class Boat extends Vehicle implements Drivable {
    private Engine engine;
    private Rudder rudder;

    public Boat(String manufacturer, String model, int length, String type, Engine engine, Rudder rudder) {
        super(manufacturer, model);
        this.engine = engine;
        this.rudder = rudder;
    }
}
```

@startuml
class Vehicle {
- manufacturer: String
- model: String

     + Vehicle(manufacturer: String, model: String)
     + accelerate(speed: int): void
     + brake(): void
}

interface Drivable {
+ start(): void
+ stop(): void
}

class Wheel {
- size: int
- type: String

     + Wheel(size: int, type: String)
     + rotate(): void
}

class Engine {
- horsepower: int
- fuelType: String

     + Engine(horsepower: int, fuelType: String)
     + start(): void
+ stop(): void
}

class Car {
- wheels: List<Wheel> // Aggregation: Car "has-a" List of Wheel objects
- engine: Engine // Aggregation: Car "has-a" Engine object
- speed: int

     + Car(manufacturer: String, model: String, wheels: List<Wheel>, engine: Engine)
     + drive(): void
}

class Boat {
- length: int
- type: String
- engine: Engine // Aggregation: Boat "has-a" Engine object
- rudder: Rudder // Aggregation: Boat "has-a" Rudder object

     + Boat(length: int, type: String, engine: Engine, rudder: Rudder)
     + navigate(): void
}

class Rudder {
// Rudder class definition
}

Vehicle <|-- Car : Inheritance (IS-A)
Vehicle <|-- Boat : Inheritance (IS-A)
Car o-- Wheel : Aggregation
Drivable <|.. Car : Implementation
Drivable <|.. Boat : Implementation
Car o-- Engine : Aggregation
Boat o-- Engine : Aggregation
Boat o-- Rudder : Aggregation
@enduml



# References

[https://www.visual-paradigm.com/guide/uml-unified-modeling-language/uml-aggregation-vs-composition/](https://www.visual-paradigm.com/guide/uml-unified-modeling-language/uml-aggregation-vs-composition/)

![](https://cdn-images.visual-paradigm.com/guide/uml/uml-aggregation-vs-composition/uml-association-aggregation-composition.png)
![uml.png](https://www.uml-diagrams.org/class-diagrams/class-diagram-domain-overview.png)

![Cheatsheet](https://khalilstemmler.com/img/blog/object-oriented/uml/uml-class-diagram-cheat-sheet.png)