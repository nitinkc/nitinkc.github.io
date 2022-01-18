---
# layout: static
title:  "USeful MS Excel Tools"
date:   2022-01-17 21:55:00
categories: Excel
tags: [Excel]
---

## Compare multiple columns together for equality


```excel
=AND(EXACT(A1:D1,A1))
```

![]({{ site.url }}/assets/images/excel_multi_col_compare.png)


press Ctrl + Shift + Enter to get the result, if the cell values are equal, it will display TRUE, otherwise, it will display FALSE, 