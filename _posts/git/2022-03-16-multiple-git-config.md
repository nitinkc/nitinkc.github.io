---
title:  "Multiple Git Config"
date:   2022-02-01 11:30:00
categories: ['Git']
tags: ['Git']
---

{% include toc title="Index" %}

To ensure multiple git or bitbucket repositories to work seemlessly with one machine, configure the global git file in such a way that it picks up right user name for specific projects under a folder.

For example, betweek work and personal repositores, code checkin using correct user id is maintained with following confog :-

with global; gitconfig file (.gitconfig in home folder ~)
```sh
[includeIf "gitdir:~/Documents/ClonedCodeWork/"]
	path = .gitconfig-work
[includeIf "gitdir:~/Programming/"]
	path = .gitconfig-learn
```

`gitdir` takes the folder where mulpile projects can reside from same repository (eg: bitbucket enterprise server)

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

Note: While using git clients (github desktop, source tree etc), ensure that it does not overwrite the got config file