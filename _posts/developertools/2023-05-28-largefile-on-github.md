---
# layout: static
title:  "Large Files on Github"
date:   2022-01-22 21:55:00
categories: ['Developer tools']
tags: ['Developer tools']
---

Github allows max file size of 25 MB so

From local, to upload a file larger than 25 MB,

1. Zip the larger file (ex. data.sql) into a zip (data.sql.zip)

2. Create a split zip archive (creates files named zip, z01, z02...) from the larger archive created in step #1
```sh
# -s for size, -x for exclusion
zip data.sql.zip -x "*.DS_Store" --out mySql_dump.zip -s 25m
```

After cloning the multipart zip :-

1. First, combine the split archive to a single archive:

```sh
`zip -s 0 mySql_dump.zip --out unsplit-data-dump.zip`
```
Extract the single archive using unzip: Either run the following command or double click the single archive file.

```sh
unzip unsplit-data-dump.zip
```
