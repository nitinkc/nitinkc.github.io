---
title: "Cassandra - Column-Oriented Database"
date: 2025-05-08 11:02:00
categories: [System Design]
tags: [System Design]
---

{% include toc title="Index" %}

- MongoDB **stores** data as documents in a **BSON (Binary JSON)** format and **displayed** in **JSON**
- ideal for applications where schema evolution is frequent.
- `use training` - For testing

# Document Structure
The values in a document can be any data type, including strings, objects, arrays, booleans, nulls, dates, ObjectIds, and more. 

```json
{ 
  "_id": 1, //UUID, default added if not explicitly used
  "name": "AC3 Phone",//String 
  "colors" : ["black", "silver"], //Array
  "price" : 200, //Integer
  "available" : true //Boolean
}
```

The MongoDB Shell uses **a Node REPL environment**. 
- can use JavaScript variable declaration, function declaration, and loops.

# insertOne va insertMany()
```yaml
db.grades.insertOne({
  student_id: 654321,
  products: [
    {
      type: "exam",
      score: 90,
    },
    {
      type: "homework",
      score: 59,
    },
    {
      type: "quiz",
      score: 75,
    },
    {
      type: "homework",
      score: 88,
    },
  ],
  class_id: 550,
})
```

# Find a doc
- Find a Document with Equality
```yaml
db.zips.find({ _id: ObjectId("5c8eccc1caa187d17ca6ed16") })
```

- `$in` clause
```yaml
db.zips.find({ city: { $in: ["PHOENIX", "CHICAGO"] } })
```

- comparison operators: `$gt`, `$lt`, `$lte`, and `$gte.`
```yaml
db.sales.find({ "items.price": { $gt: 50}})
db.sales.find({ "items.price": { $lt: 50}})
db.sales.find({ "customer.age": { $lte: 65}})
db.sales.find({ "customer.age": { $gte: 65}})
```

- Find Documents with an Array That Contains a Specified Value
  -  "InvestmentFund" is not enclosed in square brackets, so MongoDB returns all documeants within the products array that contain the specified value.
```json
db.accounts.find({ products: "InvestmentFund"})
```

- Use the `$elemMatch` operator to find all documents that contain the specified subdocument.
```json
db.sales.find({
  items: {
    $elemMatch: { name: "laptop", price: { $gt: 800 }, quantity: { $gte: 1 } },
  },
})
```

- Find a Document by Using Implicit `$and`
```json
db.routes.find({ "airline.name": "Southwest Airlines", stops: { $gte: 1 } })
```

- Find a Document by Using the $or Operator
```json
db.routes.find({
  $or: [{ dst_airport: "SEA" }, { src_airport: "SEA" }],
})
```

- Use the $and operator to use multiple $or expressions in your query.
```json
db.routes.find({
  $and: [
    { $or: [{ dst_airport: "SEA" }, { src_airport: "SEA" }] },
    { $or: [{ "airline.name": "American Airlines" }, { airplane: 320 }] },
  ]
})
```

The following query will return documents where the genre field is equal to a scalar value of Historical, 
and it will also return documents that have an array value equal to Historical, such as `["Historical", "Fiction"]`.
```json
db.books.find({ genre: "Historical" })
```

#  Replacing a Document in MongoDB
use the replaceOne() method. The replaceOne() method takes the following parameters:

- filter: A query that matches the document to replace.
- replacement: The new document to replace the old one with.
- options: An object that specifies options for the update.

```json
db.books.replaceOne(
  {
    _id: ObjectId("6282afeb441a74a98dbbec4e"),
  },
  {
    title: "Data Science Fundamentals for Python and MongoDB",
    isbn: "1484235967",
    publishedDate: new Date("2018-5-10"),
    thumbnailUrl:
      "https://m.media-amazon.com/images/I/71opmUBc2wL._AC_UY218_.jpg",
    authors: ["David Paper"],
    categories: ["Data Science"],
  }
)
```

# Updating a Document

### updateOne()
The `updateOne()` method accepts a filter document, an update document, and an optional options object.
MongoDB provides update operators and options to help you update documents with `$set`, `upsert`, and `$push`.

- $set - The `$set` operator replaces the value of a field with the specified value/
```json
db.podcasts.updateOne(
    {
      _id: ObjectId("5e8f8f8f8f8f8f8f8f8f8f8"),
    },
    
    {
        $set: {
        subscribers: 98562,
        },
    }
)
```

- upsert - The upsert option creates **a new document** if no documents match the filtered criteria. 
```json
db.podcasts.updateOne(
  { title: "The Developer Hub" },
  { $set: { topics: ["databases", "MongoDB"] } },
  { upsert: true }
)
```

- $push - The `$push` operator adds a new value to the hosts array field.
```json
db.podcasts.updateOne(
  { _id: ObjectId("5e8f8f8f8f8f8f8f8f8f8f8") },
  { $push: { hosts: "Nic Raboy" } }
)
```

##### Problems with updateOne
- CHECK : 2 roubnd trips, one to find the doc adn then to update


###  Updating MongoDB Documents by Using findAndModify()
The `findAndModify()` method is used to find and replace a single document in MongoDB. 
It accepts a filter document, a replacement document, and an optional options object. 
- Guarantees current versions of the document


```json
db.podcasts.findAndModify({
  query: { _id: ObjectId("6261a92dfee1ff300dc80bf1") },
  update: { $inc: { subscribers: 1 } },
  new: true,
})
```

### updateMany()
To update multiple documents, use the updateMany() method. 
This method accepts a filter document, an update document, and an optional options object.
```json
db.books.updateMany(
  { publishedDate: { $lt: new Date("2019-01-01") } },
  { $set: { status: "LEGACY" } }
)
```

### Deleting a record
- `deleteOne`
```yaml
db.podcasts.deleteOne({ _id: Objectid("6282c9862acb966e76bbf20a") })
```

- `deleteMany()`
```yaml
db.podcasts.deleteMany({category: “crime”})
```

### Sort & Limit

```yaml
db.companies.find({ category_code: "music" }).sort({ name: 1 });
# Return data on all music companies, sorted alphabetically from A to Z. Ensure consistent sort order
db.companies.find({ category_code: "music" }).sort({ name: 1, _id: 1 });
```
- Limit
```yaml
# Return the three music companies with the highest number of employees. 
# Ensure consistent sort order.
db.companies
  .find({ category_code: "music" })
  .sort({ number_of_employees: -1, _id: 1 })
  .limit(3);
```


### 
how to return selected fields from a query

```yaml
```
### Aggregation Framework
MongoDB's aggregation framework allows you to perform advanced operations such 
as filtering, grouping, sorting, and projecting. 

This is similar to SQL GROUP BY and JOIN operations.

##### a. Grouping Data
Use aggregation to group users by age and calculate the average age:

```java
Aggregation aggregation = Aggregation.newAggregation(
    Aggregation.group("age").avg("age").as("averageAge"),
    Aggregation.project("averageAge").and("age").previousOperation()
);

AggregationResults<AverageAge> results = mongoTemplate.aggregate(aggregation, User.class, AverageAge.class);
```

##### b. Filtering and Sorting
combine match and sort stages to filter and sort data
```java
Aggregation aggregation = Aggregation.newAggregation(
    Aggregation.match(Criteria.where("age").gt(20)),
    Aggregation.sort(Sort.by(Sort.Order.asc("name"))),
    Aggregation.limit(10)
);

List<User> users = mongoTemplate.aggregate(aggregation, User.class, User.class).getMappedResults();
```

### Embedded Documents
use embedded documents for denormalized models.
```java
public class User {
    private String name;
    private String email;
    private Address address; // Embedded document
}
```


## Redis (Key-Value Store)
Redis is an in-memory key-value store, known for its speed and simplicity.
Ideal for caching, session management, and real-time data scenarios.

