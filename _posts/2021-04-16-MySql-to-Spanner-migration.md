---
# layout: static
title:  "MySql to Spanner Migration using HarbourBridge"
date:   2021-04-16 01:25:00
categories: GCP
tags: [Google Cloud Platform]
---

# Import MySql data dump into Spanner using HarbourBridge

Install GO using the download option and setting the path into profile as
```shell
export GOPATH=/usr/local/go
export PATH=$GOPATH/bin:$PATH
````

and install harbourbridge using 'git clone https://github.com/cloudspannerecosystem/harbourbridge\ncd harbourbridge'
and directly CD into harbourbridge directory. If needed, the go installation option can be used as given 
[here](https://github.com/cloudspannerecosystem/harbourbridge#installing-harbourbridge) and 
set the environment variable as follows.
```shell
export X=$GOPATH/bin/harbourbridge
export PATH=$X/bin:$PATH
```

After the setup, ensure the GCP profile is set to the intended account, with intended project and intended spanner instance
```shell
gcloud init

# Create new configuration 'learn'
# login with new account
# should get a list of project after logging in
# This will also ensure that the 'learn' config is enabled and ready to be used

project name : mera-chandrayaan-2021

#Ensure that the current user is credentiated
gcloud auth application-default login

# Create Spanner Instance
gcloud spanner instances create development-nc --config=regional-us-central1 \
--description="Spanner DB Instance" --nodes=1

# Create Database
gcloud spanner databases create spanner-db --instance=development-nc

```

After everything is set in order, pick up the correct schema from MySql DB that needs importing. Ensure that MySql DB is 
running and keep the user and password ready. Follow the steps

```shell
mysqldump classicmodels -u root -p | $GOPATH/bin/harbourbridge -driver=mysqldump
```

here classicmodels is the schema name.

The log would look like
```text
 mysqldump classicmodels -u root -p | $GOPATH/bin/harbourbridge -driver=mysqldump
Enter password: Using driver (source DB): mysqldump
Using Google Cloud project: mera-chandrayaan-2021
Using only available Spanner instance: development-nc
Using Cloud Spanner instance: development-nc

WARNING: Please check that permissions for this Spanner instance are
appropriate. Spanner manages access control at the database level, and the
database created by HarbourBridge will inherit default permissions from this
instance. All data written to Spanner will be visible to anyone who can
access the created database. Note that mysqldump table-level and row-level
ACLs are dropped during conversion since they are not supported by Spanner.


Generating schema: 100%
Wrote schema to file 'mysqldump_2021-04-16_699a-f26b.schema.txt'.
Wrote session to file 'mysqldump_2021-04-16_699a-f26b.session.json'.
Creating new database mysqldump_2021-04-16_699a-f26b in instance development-nc with default permissions ... done.
Writing data to Spanner: 100%
Updating schema of database mysqldump_2021-04-16_699a-f26b in instance development-nc with foreign key constraints ...: 100%
Processed 192956 bytes of mysqldump data (56 statements, 3864 rows of data, 0 errors, 0 unexpected conditions).
Schema conversion: EXCELLENT (all columns mapped cleanly).
Data conversion: EXCELLENT (all 3864 rows written to Spanner).
See file 'mysqldump_2021-04-16_699a-f26b.report.txt' for details of the schema and data conversions.
```
