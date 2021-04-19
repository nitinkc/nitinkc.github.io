---
# layout: static
title:  "Handling Multiple GCP Configs"
date:   2021-04-08 02:15:00
categories: GCP
tags: [Google Cloud Platform]
---

# Create Multiple config for GCP Accounts

Inorder to create a new profile, always use `gcloud init` and follow the prompts.
select the project, by either providing the number given or by provifing the exact project ID.


To change from one profile to another

```shell
alias gcpLocal='gcloud config configurations activate local'
alias gcpNitin='gcloud config configurations activate learn'
```

Check all the users and the active user will have an asterisk
```shell
gcloud auth list
```
After Switching. change the account with the correspoding profile
```shell
gcloud config set account ACCOUNT
```
Ensure that the default login is set
```shell
gcloud auth application-default login

# Check Token
gcloud auth application-default print-access-token
```

Follow this link https://stackoverflow.com/questions/53306131/difference-between-gcloud-auth-application-default-login-and-gcloud-auth-logi

### Check all the config available on the system
```shell
gcloud config configurations list
```

### Switch to a different profile

```shell
gcloud config configurations activate [CONFIG_NAME]
```

### Set another project within same GCloud account
```shell
gcloud config set project <PROJECT ID>
```


### Add new GCP Account
In case a new GCP Account is to be added, use following to create a new configuration and initialize

```shell
gcloud config configurations create [CONFIG_NAME]

gcloud init
```
Select re-initialize the config just created and login as a new user and get redirected into web Browser for GCP Console login


To check the GCP properties of the active user use
```shell
gcloud config list
```

```shell
# If no account is given, it revokes the current account
gcloud auth revoke
```
## Delete a configuration
```shell
gcloud config configurations delete <CONFIG_NAME>>
```

### See listings
```shell
gcloud auth list
gcloud config list
gcloud config configurations list
gcloud spanner instance-configs list
```

## Switching to Learning profile from work profile

```shell
gcloud init

# Create new configuration 'learn'
# login with new account
# should get a list of project after logging in
# This will also ensure that the 'learn' config is enabled and ready to be used

project name : tat-twam-asi

#Ensure that the current user is credentiated
gcloud auth application-default login

# Create Spanner Instance
gcloud spanner instances create development-nc --config=regional-us-central1 \
--description="Spanner DB Instance" --nodes=1

# Create Database
gcloud spanner databases create spanner-db --instance=development-nc

```

# After Finishing 
```shell
gcloud spanner instances delete development-nc
# if current user is to be revoked
# gcloud auth revoke
gcloud auth revoke nitin.gcp.learn@gmail.com

#Go Back to the profile that is to be used, now
gcloud config configurations activate local

#Set profile if needed
#gcloud config set account ACCOUNT

#Clean up the profile to avoid any issues
gcloud config configurations delete learn

#Ensure logging into the current profile
gcloud auth application-default login
```