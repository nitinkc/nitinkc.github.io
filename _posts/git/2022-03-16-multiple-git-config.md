---
title:  "Git Config - global "
date:   2022-02-01 11:30:00
categories: ['Git']
tags: ['Git']
---

{% include toc title="Index" %}

# Create multiple Git Config

To ensure multiple git or bitbucket repositories to work seamlessly with one machine, configure the global git file in such a way that it picks up right user name for specific projects under a folder.

For example, between work and personal repositores, code check-in using correct user id is maintained with following config :-

with global gitconfig file (.gitconfig in home folder ~)
```sh
[includeIf "gitdir:~/Documents/ClonedCodeWork/"]
	path = .gitconfig-work
[includeIf "gitdir:~/Programming/"]
	path = .gitconfig-learn
```

`gitdir` takes the folder where multiple projects can reside from same repository (eg: bitbucket enterprise server)

create the files and open in a text editor
```sh
touch .gitconfig-learn | open .gitconfig-learn
touch .gitconfig-work  | open .gitconfig-work
```

Update the (relevant) information as needed in both the file under `[user]` tag
```sh
[user]
	email = xxx@xxx.com
	name = Your Name
```

Note: While using git clients (github desktop, source tree etc), ensure that it does not overwrite the git config file

# Create global GitIgnore
Create .gitignore_global file and add files that needs to be globally ignored

```sh
*~
.DS_Store
```
