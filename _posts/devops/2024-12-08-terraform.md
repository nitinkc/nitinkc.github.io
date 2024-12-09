---
title:  "Terraform"
date:   2024-12-08 10:14:00
categories: ["DevOps","GitOps"]
tags: ["DevOps","GitOps"]
---




```bash
terraform validate

terraform fmt

terraform show json

terraform providers

terraform output

terraform refresh

terraform plan

terraform graph
```

# Graphviz

```bash
brew install graphviz

terraform graph | dot -Tsvg > graph.svg
```

# Life cycle

| S.No| Life cycle             | Description                                          |
|:----|:-----------------------|:-----------------------------------------------------|
| 1   | create_before_destroy  | Create the resource first and then destroy older     |
| 2   | prevent_destroy        | Prevents destroy of a resource                       |
| 3   | ignore_changes         | Ignore Changes to Resource Attributes (specific/all) |

# Data Source

| Resource                                  | Data Source                |
|:------------------------------------------|:---------------------------|
| Keyword: resource                         | Keyword: data              |
| Creates, Updates, Destroys Infrastructure | Only Reads Infrastructure  |
| Also called Managed Resources             | Also called Data Resources |