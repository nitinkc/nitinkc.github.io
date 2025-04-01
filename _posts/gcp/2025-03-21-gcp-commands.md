---
title: "GCP Commands"
date: 2025-03-21 05:00:00
categories: [ GCP ]
tags: [ GCP ]
---

gcloud compute instances list --sort-by=ZONE


```shell
export LOCATION=US

gcloud storage buckets create -l $LOCATION gs://$DEVSHELL_PROJECT_ID

# Retrieve a banner image from a publicly accessible Cloud Storage location:
gcloud storage cp gs://cloud-training/gcpfci/my-excellent-blog.png my-excellent-blog.png

gcloud storage cp my-excellent-blog.png gs://$DEVSHELL_PROJECT_ID/my-excellent-blog.png

gsutil acl ch -u allUsers:R gs://$DEVSHELL_PROJECT_ID/my-excellent-blog.png
```

# SSH

```shell
gcloud compute ssh vm-internal --zone us-central1-f --tunnel-through-iap


```

```shell
gcloud auth list
gcloud config list project

gcloud services enable run.googleapis.com

gcloud config set compute/region us-east4

LOCATION="us-east4"

gcloud builds submit --tag gcr.io/$GOOGLE_CLOUD_PROJECT/helloworld

gcloud container images list

gcloud auth configure-docker

gcloud run deploy --image gcr.io/$GOOGLE_CLOUD_PROJECT/helloworld --allow-unauthenticated --region=$LOCATION

# Delete
gcloud container images delete gcr.io/$GOOGLE_CLOUD_PROJECT/helloworld
gcloud run services delete helloworld --region=us-east4
```


The Cloud Console is a graphical user interface and Cloud Shell is a command-line tool. Both tools allow you to interact with Google Cloud. Even though the Cloud Console can do things Cloud Shell can't do and vice-versa, don’t think of them as alternatives, but think of them as one extremely flexible and powerful interface.

```shell
 gcloud storage buckets create gs://chapribucket
 
 gcloud storage cp test.png  gs://chapribucket2
 
 gcloud compute regions list
 
 INFRACLASS_REGION=[YOUR_REGION]
 
```


# Networks

```shell
gcloud compute networks create managementnet --project=qwiklabs-gcp-00-eb0d1773ac6c --subnet-mode=custom --mtu=1460 --bgp-routing-mode=regional --bgp-best-path-selection-mode=legacy

gcloud compute networks subnets create managementsubnet-us --project=qwiklabs-gcp-00-eb0d1773ac6c --range=10.240.0.0/20 --stack-type=IPV4_ONLY --network=managementnet --region=us-east1

gcloud compute networks create privatenet --subnet-mode=custom

gcloud compute networks subnets create privatesubnet-us --network=privatenet --region=us-east1 --range=172.16.0.0/24

gcloud compute networks subnets create privatesubnet-notus --network=privatenet --region=asia-southeast1 --range=172.20.0.0/20

gcloud compute networks list

gcloud compute networks subnets list --sort-by=NETWORK

# firewall
gcloud compute --project=qwiklabs-gcp-00-eb0d1773ac6c firewall-rules create managementnet-allow-icmp-ssh-rdp --direction=INGRESS --priority=1000 --network=managementnet --action=ALLOW --rules=tcp:22,tcp:3389 --source-ranges=0.0.0.0/0

gcloud compute firewall-rules create privatenet-allow-icmp-ssh-rdp --direction=INGRESS --priority=1000 --network=privatenet --action=ALLOW --rules=icmp,tcp:22,tcp:3389 --source-ranges=0.0.0.0/0
```


```shell
gcloud compute ssh vm-internal --zone us-central1-f --tunnel-through-iap
```


#Debian

```shell
free

sudo dmidecode -t 17

nproc

lscpu


```


# ACL with buckets

### Copy the file to the bucket and configure the access control list
```shell
gcloud storage cp setup.html gs://$BUCKET_NAME_1/

gsutil acl get gs://$BUCKET_NAME_1/setup.html  > acl.txt
cat acl.txt

# set the access list to private and verify the results
gsutil acl set private gs://$BUCKET_NAME_1/setup.html
gsutil acl get gs://$BUCKET_NAME_1/setup.html  > acl2.txt
cat acl2.txt

#  update the access list to make the file publicly readable
gsutil acl ch -u AllUsers:R gs://$BUCKET_NAME_1/setup.html
gsutil acl get gs://$BUCKET_NAME_1/setup.html  > acl3.txt
cat acl3.txt
```

### Customer-supplied encryption keys (CSEK)

```python
-- create AES-256 base-64 key.
python3 -c 'import base64; import os; 
print(base64.encodebytes(os.urandom(32)))'
```

```shell
# The encryption controls are contained in a gsutil configuration file named .bot
gsutil config -n

nano .boto

#set encryption_key= and decryption_1 keys

gsutil cp setup2.html gs://$BUCKET_NAME_1/
gsutil cp setup3.html gs://$BUCKET_NAME_1/
```

### Enable lifecycle management
```shell
gsutil lifecycle get gs://$BUCKET_NAME_1

nano life.json
```
life.json
```json
{
  "rule":
  [
    {
      "action": {"type": "Delete"},
      "condition": {"age": 31}
    }
  ]
}
```

```shell
gsutil lifecycle set life.json gs://$BUCKET_NAME_1

gsutil lifecycle get gs://$BUCKET_NAME_1
```

### Enable versioning
```shell
gsutil versioning get gs://$BUCKET_NAME_1
gsutil versioning set on gs://$BUCKET_NAME_1

gcloud storage ls -a gs://$BUCKET_NAME_1/setup.html

```

### Synchronize a directory to a bucket
```shell
mkdir firstlevel
mkdir ./firstlevel/secondlevel
cp setup.html firstlevel
cp setup.html firstlevel/secondlevel

# sync the firstlevel directory on the VM with your bucket
gsutil rsync -r ./firstlevel gs://$BUCKET_NAME_1/firstlevel
```

# VPC
```shell
gcloud compute networks create vpc-demo --subnet-mode custom

gcloud compute networks subnets create vpc-demo-subnet1 \
--network vpc-demo --range 10.1.1.0/24 --region "us-east1"

gcloud compute networks subnets create vpc-demo-subnet2 \
--network vpc-demo --range 10.2.1.0/24 --region us-central1

# Create a firewall rule to allow all custom traffic within the network:
gcloud compute firewall-rules create vpc-demo-allow-custom \
  --network vpc-demo \
  --allow tcp:0-65535,udp:0-65535,icmp \
  --source-ranges 10.0.0.0/8
  
gcloud compute firewall-rules create vpc-demo-allow-ssh-icmp \
    --network vpc-demo \
    --allow tcp:22,icmp
```

# Connect K8S

```shell
gcloud container clusters get-credentials cluster-1 --zone us-central1-c --project qwiklabs-gcp-04-9b06733dbf8c

kubectl get nodes

gcloud artifacts repositories create devops-demo \
    --repository-format=docker \
    --location=us-central1

gcloud auth configure-docker us-central1-docker.pkg.dev
```


# Creating cluster
```shell
export my_region=us-central1
export my_cluster=autopilot-cluster-1

gcloud container clusters create-auto $my_cluster --region $my_region
```

This comm and creates a .kube directory in your home directory if it doesn't already exist. In the .kube directory, the command creates a file named config if it doesn't already exist, which is used to store the authentication and configuration information. The config file is typically called the kubeconfig file.
```shell
gcloud container clusters get-credentials $my_cluster --region $my_region
```


```shell
kubectl config view

kubectl cluster-info

kubectl config current-context

kubectl config get-contexts

kubectl config use-context gke_${DEVSHELL_PROJECT_ID}_us-central1_autopilot-cluster-1
```

However, in the future you may have more than one cluster in a project. You can use this approach to switch the active context when your kubeconfig file has the credentials and configuration for several clusters already populated. This approach requires the full name of the cluster, which includes the gke prefix, the project ID, the location, and the display name, all concatenated with underscores.
```shell
source <(kubectl completion bash)
```

### Use kubectl to deploy Pods to GKE
```shell
kubectl create deployment --image nginx nginx-1

kubectl get pods

kubectl top node

export my_nginx_pod=[your_pod_name]
kubectl describe pod $my_nginx_pod
```


```shell
nano ~/test.html
kubectl cp ~/test.html $my_nginx_pod:/usr/share/nginx/html/test.html

kubectl expose pod $my_nginx_pod --port 80 --type LoadBalancer

kubectl get services

git clone https://github.com/GoogleCloudPlatform/training-data-analyst
ln -s ~/training-data-analyst/courses/ak8s/v1.1 ~/ak8s
cd ~/ak8s/GKE_Shell/


kubectl apply -f ./new-nginx-pod.yaml
kubectl exec -it new-nginx -- /bin/bash
kubectl port-forward new-nginx 10081:80
```