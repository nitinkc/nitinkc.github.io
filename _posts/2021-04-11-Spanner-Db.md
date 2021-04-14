---
# layout: static
title:  "Spanner Database"
date:   2021-04-08 02:15:00
collection : GCP
categories: 
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
