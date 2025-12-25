---
title: GCP - Free Tier Setup
date: 2021-02-16 23:00:00
categories:
- GCP
tags:
- Setup
---

{% include toc title="Index" %}

- Project Creation
    - name : project-phoenix
    - Billing export
        - Billing -> Billing Export -> Edit Settings -> Create new Dataset
      ```sql
      select project.name as project, service.description as resource, round(sum(cost)) as total_cost
      from precise-slice-436003-r4.billing
      ```
- Service Account keys
    - Compute Engine -> VM Engine -> Enable (This will create a service account
      as its process of enabling)
    - IAM -> Service Account -> Locate the service account, click adn goto
      Keys -> add new kepo adn download
- Cloud shell setup - gcloud configurations
    - `gcloud init` and follow the prompt. Use the relevant GCP account when
      prompted on the browser
    - switch to the config created above
      `gcloud config configurations activate gitops`