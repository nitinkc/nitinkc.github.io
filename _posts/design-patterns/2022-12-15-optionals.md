
A good design reads like a story and not like a puzzle


Removing the Nulll null is a smell

>> Do not return a null, instead return an empty *collection*. Effective Java


## What if we have a single value?

* Instead of returning null return Option<T>
* If a method will always have a single value as a result *donot use* Optional.

Do's and Dont's



//If a method may or may not have a single value as a
//result, then use Optional.

//If the result is a collection, then don't use Optional.

//Don't use Optional<T> as a parameter to methods
//If needed, use overloading instead.

//There is little reason to use Optional as a field.

