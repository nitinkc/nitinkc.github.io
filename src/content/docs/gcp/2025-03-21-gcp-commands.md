---
title: GCP Commands
date: 2025-03-21 05:00:00
categories:
- GCP
tags:
- Commands
- CLI
---

{% include toc title="Index" %}

gcloud compute instances list --sort-by=ZONE
# VM Instance
```shell
gcloud compute instances create vpc-demo-instance1 --machine-type=e2-medium --zone "ZONE" --subnet vpc-demo-subnet1
```
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

# VPC & Cloud Interconnect

```shell
# create a VPC network called vpc-demo
gcloud compute networks create vpc-demo --subnet-mode custom

# create subnet vpc-demo-subnet1 in the region REGION 1
gcloud compute networks subnets create vpc-demo-subnet1 \
--network vpc-demo --range 10.1.1.0/24 --region "us-east1"

# Create subnet vpc-demo-subnet2 in the region REGION 2:
gcloud compute networks subnets create vpc-demo-subnet2 \
--network vpc-demo --range 10.2.1.0/24 --region us-central1

# Create a firewall rule to allow all custom traffic within the network:
gcloud compute firewall-rules create vpc-demo-allow-custom \
  --network vpc-demo \
  --allow tcp:0-65535,udp:0-65535,icmp \
  --source-ranges 10.0.0.0/8

# Create a firewall rule to allow SSH, ICMP traffic from anywhere
gcloud compute firewall-rules create vpc-demo-allow-ssh-icmp \
    --network vpc-demo \
    --allow tcp:22,icmp
```
### Create HA VPN

In Cloud Shell, create an HA VPN in the vpc-demo & on-prem network
```shell
gcloud compute vpn-gateways create vpc-demo-vpn-gw1 --network vpc-demo --region "REGION"
gcloud compute vpn-gateways create on-prem-vpn-gw1 --network on-prem --region "REGION"
# Output
Creating VPN Gateway...done.   
NAME: vpc-demo-vpn-gw1
INTERFACE0: 35.242.117.95
INTERFACE1: 35.220.73.93
NETWORK: vpc-demo
REGION: "REGION"
```
View details of the vpc-demo-vpn-gw1 gateway to verify its settings:
```shell
gcloud compute vpn-gateways describe vpc-demo-vpn-gw1 --region "REGION"
gcloud compute vpn-gateways describe on-prem-vpn-gw1 --region "Region"
```

### Create Cloud Routers
Create a cloud router in the vpc-demo & on-prem network
```shell
gcloud compute routers create vpc-demo-router1 \
    --region "REGION" \
    --network vpc-demo \
    --asn 65001
    
gcloud compute routers create on-prem-router1 \
    --region "REGION" \
    --network on-prem \
    --asn 65002
```

### Create VPN Tunnels
```shell
# Create the first VPN tunnel in the vpc-demo network:

gcloud compute vpn-tunnels create vpc-demo-tunnel0 \
    --peer-gcp-gateway on-prem-vpn-gw1 \
    --region "REGION" \
    --ike-version 2 \
    --shared-secret [SHARED_SECRET] \
    --router vpc-demo-router1 \
    --vpn-gateway vpc-demo-vpn-gw1 \
    --interface 0

# Create the second VPN tunnel in the vpc-demo network:
gcloud compute vpn-tunnels create vpc-demo-tunnel1 \
    --peer-gcp-gateway on-prem-vpn-gw1 \
    --region "REGION" \
    --ike-version 2 \
    --shared-secret [SHARED_SECRET] \
    --router vpc-demo-router1 \
    --vpn-gateway vpc-demo-vpn-gw1 \
    --interface 1
    
# Create the first VPN tunnel in the on-prem network:
gcloud compute vpn-tunnels create on-prem-tunnel0 \
    --peer-gcp-gateway vpc-demo-vpn-gw1 \
    --region "REGION" \
    --ike-version 2 \
    --shared-secret [SHARED_SECRET] \
    --router on-prem-router1 \
    --vpn-gateway on-prem-vpn-gw1 \
    --interface 0
    
# Create the second VPN tunnel in the on-prem network:
gcloud compute vpn-tunnels create on-prem-tunnel1 \
    --peer-gcp-gateway vpc-demo-vpn-gw1 \
    --region "REGION" \
    --ike-version 2 \
    --shared-secret [SHARED_SECRET] \
    --router on-prem-router1 \
    --vpn-gateway on-prem-vpn-gw1 \
    --interface 1
```

### Create Border Gateway Protocol (BGP) peering for each tunnel

Create the router interface for tunnel0 in network vpc-demo:
```shell
gcloud compute routers add-interface vpc-demo-router1 \
--interface-name if-tunnel0-to-on-prem \
--ip-address 169.254.0.1 \
--mask-length 30 \
--vpn-tunnel vpc-demo-tunnel0 \
--region "REGION"
```
Create the BGP peer for tunnel0 in network vpc-demo:
```shell
gcloud compute routers add-bgp-peer vpc-demo-router1 \
--peer-name bgp-on-prem-tunnel0 \
--interface if-tunnel0-to-on-prem \
--peer-ip-address 169.254.0.2 \
--peer-asn 65002 \
--region "REGION"
````
Create a router interface for tunnel1 in network vpc-demo:
```shell
gcloud compute routers add-interface vpc-demo-router1 \
--interface-name if-tunnel1-to-on-prem \
--ip-address 169.254.1.1 \
--mask-length 30 \
--vpn-tunnel vpc-demo-tunnel1 \
--region "REGION"
```

Create the BGP peer for tunnel1 in network vpc-demo:
```shell
gcloud compute routers add-bgp-peer vpc-demo-router1 \
--peer-name bgp-on-prem-tunnel1 \
--interface if-tunnel1-to-on-prem \
--peer-ip-address 169.254.1.2 \
--peer-asn 65002 \
--region "REGION"
```

Create a router interface for tunnel0 in network on-prem:
```shell
gcloud compute routers add-interface on-prem-router1 \
--interface-name if-tunnel0-to-vpc-demo \
--ip-address 169.254.0.2 \
--mask-length 30 \
--vpn-tunnel on-prem-tunnel0 \
--region "REGION"
```

Create the BGP peer for tunnel0 in network on-prem:
```shell
gcloud compute routers add-bgp-peer on-prem-router1 \
--peer-name bgp-vpc-demo-tunnel0 \
--interface if-tunnel0-to-vpc-demo \
--peer-ip-address 169.254.0.1 \
--peer-asn 65001 \
--region "REGION"
```
Create a router interface for tunnel1 in network on-prem:
```shell
gcloud compute routers add-interface  on-prem-router1 \
--interface-name if-tunnel1-to-vpc-demo \
--ip-address 169.254.1.2 \
--mask-length 30 \
--vpn-tunnel on-prem-tunnel1 \
--region "REGION"
```

Create the BGP peer for tunnel1 in network on-prem:
```shell
gcloud compute routers add-bgp-peer  on-prem-router1 \
--peer-name bgp-vpc-demo-tunnel1 \
--interface if-tunnel1-to-vpc-demo \
--peer-ip-address 169.254.1.1 \
--peer-asn 65001 \
--region "REGION"
```
View details of Cloud Router vpc-demo-router1 to verify its settings:
```shell
gcloud compute routers describe vpc-demo-router1 \
    --region "REGION"
gcloud compute routers describe on-prem-router1 \
    --region "REGION"
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
Check k8s commands