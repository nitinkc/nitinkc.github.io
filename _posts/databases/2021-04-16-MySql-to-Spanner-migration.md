---
# layout: static
title:  "MySql to Spanner Migration using HarbourBridge"
date:   2021-04-16 01:25:00
categories: GCP
tags: [Google Cloud Platform, Database]
---

# Import MySql data dump into Spanner using HarbourBridge

[MySQL to Cloud Spanner via HarbourBridge](https://opensource.googleblog.com/2020/09/mysql-to-cloud-spanner-via-harbourbridge.html)

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

[Follow this link for argument options](https://github.com/cloudspannerecosystem/harbourbridge/blob/master/mysql/README.md#using-harbourbridge-with-mysqldump)
```shell
# Importing Data directly from running instance of MySql
mysqldump employees -u root -p | $GOPATH/bin/harbourbridge -driver=mysqldump -dbname employees-db

# if sql dump file is provided
#harbourbridge -driver=mysqldump < dump.sql
harbourbridge -driver=mysqldump -instance development-nc -dbname hr < hrDB.txt
# If the database name is to be chosen, it can be priovided like below. The db should not exist
#mysqldump classicmodels -u root -p | harbourbridge -driver=mysqldump -instance my-spanner-instance -dbname my-spanner-database-name

mysqldump classicmodels -u root -p | harbourbridge -driver=mysqldump -instance development-nc -dbname spanner-db
```
here classicmodels is the schema name.


# Importing Employees Database.

Import the Data into MySql and then use harbourBridge to migrate the data into Spanner

[Download the Sample Data here](https://github.com/datacharmer/test_db)

Schema : 
https://github.com/datacharmer/test_db/blob/master/images/employees.jpg

```shell
mysqldump employees -u root -p | $GOPATH/bin/harbourbridge -driver=mysqldump -dbname employees-db
```