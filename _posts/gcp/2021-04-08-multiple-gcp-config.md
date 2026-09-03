---
title: Multiple config for GCP Accounts
date: 2021-04-08 02:15:00
categories:
- GCP
tags:
- Configuration
---

{% include toc title="Index" %}

## Check all available configs 

```shell
gcloud config configurations list
```

- To check the GCP properties of the active user use
    ```shell
    gcloud config list
    ```
  
- To change from one existing profile to another existing profile
    ```shell
    gcloud config configurations activate [CONFIG_NAME]
    ```

    ```shell
    alias gcpLocal='gcloud config configurations activate local'
    alias gcpNitin='gcloud config configurations activate learn'
    ```

- After Switching. change the account with the corrosponding profile
    ```shell
    gcloud config set account ACCOUNT
    ```

- If your current project is [abc] and you want to change this setting by running:
    ```shell
    # View the Currently Active Project
    gcloud config get project
    
    # List All GCP Projects You Have Access To
    gcloud projects list
    
    # Switch to a Different Project within same GCloud account
    gcloud config set project PROJECT_ID
    ```

- Check all the users and the active user will have an asterisk
    ```shell
    gcloud auth list
    ```
  
### Login

```shell
# For CLI
gcloud auth login

# For code
gcloud auth application-default login 

# Check Token
gcloud auth application-default print-access-token
```

#### Summary of GCP gcloud Authentication Methods

| Capability          | `gcloud auth login`                        | `gcloud auth application-default login`                                   |
|:--------------------|:-----------------------------------------|:------------------------------------------------------------------------|
| Primary Target      | The gcloud CLI itself.                   | Code and SDKs running locally.                                          |
| Ideal Use Case      | Running `gcloud` commands from terminal. | Testing code locally that will eventually run on a server.              |
| Credential Location | ~/.config/gcloud/                        | `~/.config/gcloud/application_default_credentials.json`                 |
| SDK Accessibility   | ❌ No.                                   | Yes. Automatically picked up by Application Default Credentials (ADC).  |


## Create a new config
In order to create a new profile, always use `gcloud init` and follow the  prompts.

select the project, by either providing the number given or by providing the exact project ID.

### Add new GCP Account

In case a new GCP Account is to be added, use following to create a new
configuration and initialize

```shell
gcloud config configurations create [CONFIG_NAME]

gcloud init
```

Select re-initialize the config just created and login as a new user and get redirected into web Browser for GCP Console login


## Delete a configuration

```shell
gcloud config configurations delete <CONFIG_NAME>>
```

```shell
# If no account is given, it revokes the current account
gcloud auth revoke
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
# if profile not initiated
gcloud init

# Create new configuration 'learn'
# login with new account
# should get a list of project after logging in
# This will also ensure that the 'learn' config is enabled and ready to be used

project name : tat-twam-asi

# Ensure that the current user is credentiated
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