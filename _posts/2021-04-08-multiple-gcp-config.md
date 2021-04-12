# Create Multiple config for GCP Accounts

```shell
alias gcpLocal='gcloud config configurations activate local'
alias gcpNitin='gcloud config configurations activate learn'
```
### Check all the config available on the system
```
gcloud config configurations list
```

### Switch to a different profile

```
gcloud config configurations activate [CONFIG_NAME]
```

### Add new GCP Account
In case a new GCP Account is to be added, use following to create a new configuration and initialize

```
gcloud config configurations create [CONFIG_NAME]

gcloud init
```

Select re-initialize the config just created and login as a new user and get redirected into web Browser for GCP Console login

Check all the users and the active user will have an asterisk
```
gcloud auth list
```

To check the GCP properties of the active user,
```
gcloud config list
```


## Delete a configuration
```
gcloud config configurations delete <CONFIG_NAME>>
```
