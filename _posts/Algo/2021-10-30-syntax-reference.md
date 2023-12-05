---
title:  "Syntax Reference"
date:   2021-10-30 21:55:00
categories: Algorithms
tags: [Algorithms]
---

{% include toc title="Index" %}

# Syntax Reference for Coding Interviews


### Boolean Logic (multiple if statements into switch)
{% gist nitinkc/96387a9700c9c58185a969ae48bfdc45 %}


### For Loop Traps
{% gist nitinkc/382798a984e00a732d86a12a6637e0a2 %}


### Reading, Parsing and Type Checking Command Line Inputs.
```java
// Assuming 2 command line arguments <Nitin 29>
if (args.length == 0 || args.length > 2) {
  System.err.println("Incorrect Number of arguments passed");
  System.exit(-1);
}
String name = args[0];
int age = Integer.parseInt(args[1]);
```

### Running time of a method
```java
System.currentTimeMillis();//type long, from Jan 1 1970
System.nanoTime();
```

### Random
```java
import java.util.Random;

// Math.random() - returns a double value with a positive sign, greater than or equal to 0.0 and less than 1.0
 double randomValue = Math.random();//  0.0 and less than 1.0.
System.out.println("Random value: " + randomValue);

Random generator = new Random(); //or new Random(123), 123 being the seed
//generator.nextInt(5);//range 0 to 5, add 1 to get range 1 to 6 (dices)
int throw = generator.nextInt(5) + 1;

generator.nextInt(); // 2^31 to 2^31 -1
generator.nextDouble();//Range: 0.0 to 1.1
```

## Java Input

### Key Board Input

```java
import java.util.Scanner;
 Scanner in = new Scanner(System.in);

 /* Input Problem occurs when a mix of int and strings are given
 The extra invocation is done to get rid of previous \n */
 int n = in.nextLine();
 in.nextLine(); //To avoid INPUT Problem
 String str = in.nextLine();

 in.nextLine();//reads entire line of in
 in.next();//next character upto but not including space

/* NO METHOD TO READ A SINGLE CHARACTER */
 char a = in.nextLine.charAt(0);
```

### File Input

```java
//Open the File
 File myFile = new File("/nitin/a.txt");
 Scanner in = new Scanner(myFile);
 //Instead of System.in, take the file to read

//Read from the File
 String str = in.nextLine();
//OR
 while (in.hasNext());
 System.out.println(in.nextLine());

//Close the File
 in.close();
```

## Output File Handling

### Writing text to File
```java
import java.io.PrintWriter;
 final String FILENAME = "nitin.txt";
//Surrounding with try catch!!
 PrintWriter output = new PrintWriter(FILENAME);

 output.println("Nitin"); output.println("Chaurasia");

//To avoid erasing files that already exist
 PrintWriter pw = new PrintWriter(new FileWriter("nitin.txt", true));
```

### Appending Text to file
```java
FileWriter fw = new FileWriter("Names.txt", true);
PrintWriter pw = new PrintWriter(fw);
//OR
PrintWriter pw = new PrintWriter(new FileWriter("Names.txt, true"));
```

### Reading Data from a file
```java
File myFile = new File("customer.txt");
Scanner ipFile = new Scanner(myFile); //instead of System.in
```