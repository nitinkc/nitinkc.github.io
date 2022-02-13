---
# layout: static
title:  "Spanner Database"
date:   2021-04-08 02:15:00
categories: GCP
tags: [Google Cloud Platform]
---

For making full use of the free tier, The Database and it's corrosponding instance need to be up and running only while development and testing.
Always delete the instance after the experimentation is done

```shell
### Delete Instance
gcloud spanner instances delete development-nc
```

The following commands can be run.

```shell
# Costs 90 cents an hours
gcloud spanner instances create development-nc --config=us-central1 \
    --description="Spanner DB Instance" --nodes=1


gcloud spanner databases create spanner-db --instance=development-nc
```

If needed :

```shell
### Update instance
gcloud spanner instances update [INSTANCE-ID] --description=[INSTANCE-NAME]

### Update the number of nodes
gcloud spanner instances update [INSTANCE-ID] --nodes=[NODE-COUNT]
```

## Using Emulator

```shell
# Start the Emulator
gcloud emulators spanner start

# Create config for Emulator and set the variables
gcloud config configurations create emulator
gcloud config set auth/disable_credentials true
gcloud config set project tat-twam-asi
gcloud config set api_endpoint_overrides/spanner http://localhost:9020/

# Create Spanner instance on Emulator
gcloud spanner instances create development-nc  \
--config=emulator-config --description="Learning Spanner on Emulator" --nodes=1

# Create database for testing
gcloud spanner databases create spanner-db --instance=development-nc

# After Creating tables and inserting data, validate like 
 gcloud spanner databases execute-sql spanner-db --instance=development-nc \
--sql='SELECT SingerId, AlbumId, AlbumTitle FROM Albums'

```


# After the work is done
```shell
 gcloud spanner instances delete development-nc  

 gcloud config configurations activate local  

# Check the emulator config, copy the name and delete it for cleanup process
gcloud config configurations list   

gcloud config configurations delete emulator 

#Stop the emulator
ctrl C to stop the running instance
```