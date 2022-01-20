---
# layout: static
title:  "Useful MS Excel Tools"
date:   2022-01-17 21:55:00
categories: Excel
tags: [Excel]
---

## Contents

{% include toc title="Index" %}

## Compare multiple columns together for equality

```excel
=AND(EXACT(A1:D1,A1))
```

Hit **^Ctrl ⇧Shift ↵Return** to get the result, if the cell values are equal, it will display TRUE, otherwise, it will display FALSE, 

![]({{ site.url }}/assets/images/excel_multi_col_compare.png)


Comparing two cells 
```excel
=EXACT(A1,D1)
```
## Proper

Make a String in camel case.

![]({{ site.url }}/assets/images/proper.png)


## VLookUp, HLookUp & XLookUp

> The columns to be searched should be the First column
> Also, if there are multiple values, then only the first one in the order wil be returned


=VLOOKUP arguments 

**Scenario**: *Column X and Y are present in a large set of Data. If a few valus of X is given, find the corrosponding values of Y against X.*

**Solution**: *Column X(present in a Range or in a Table, as first Column) and Y (using VLOOKUP)*

* First argument is the value to lookup in the large set of data.
* Second argument is the range or table to look for the value.
* Then, the index of the column where the lookup value is located (indexing begins from 1 for X)
* Finally FALSE to find an exact match.

![]({{ site.url }}/assets/images/vlookup.png)

## Find Duplicates

![]({{ site.url }}/assets/images/duplicates.png)

