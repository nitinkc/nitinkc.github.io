# Create Multiple config for GCP Accounts

Inorder to create a new profile, always use `gcloud init` and follow the prompts.
select the project, by either providing the number given or by provifing the exact project ID.


To change from one profile to another

```shell
alias gcpLocal='gcloud config configurations activate local'
alias gcpNitin='gcloud config configurations activate learn'
```

Check all the users and the active user will have an asterisk
```
gcloud auth list
```
After Switching. change the account with the correspoding profile
```
gcloud config set account ACCOUNT
```
Ensure that the default login is set
```
gcloud auth application-default login

# Check Token
gcloud auth application-default print-access-token
```
Follow this link https://stackoverflow.com/questions/53306131/difference-between-gcloud-auth-application-default-login-and-gcloud-auth-logi

### Check all the config available on the system
```
gcloud config configurations list
```

### Switch to a different profile

```
gcloud config configurations activate [CONFIG_NAME]
```

### Set another project within same GCloud account
```
gcloud config set project <PROJECT ID>
```


### Add new GCP Account
In case a new GCP Account is to be added, use following to create a new configuration and initialize

```
gcloud config configurations create [CONFIG_NAME]

gcloud init
```
Select re-initialize the config just created and login as a new user and get redirected into web Browser for GCP Console login


To check the GCP properties of the active user use
```
gcloud config list
```

```
# If no account is given, it revokes the current account
gcloud auth revoke
```
## Delete a configuration
```
gcloud config configurations delete <CONFIG_NAME>>
```


## After Finishing 
```
gcloud spanner instances delete development-nc
# if current user is to be revoked
#gcloud auth revoke
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

## Switching to Learning profile from work profile
```

```