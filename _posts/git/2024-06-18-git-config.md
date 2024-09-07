---
title:  "Git Config"
date:   2024-06-18 13:30:00
categories: ['Git']
tags: ['Git']
---
{% include toc title="Index" %}

[https://blog.gitbutler.com/fosdem-git-talk/](https://blog.gitbutler.com/fosdem-git-talk/)

![](https://www.youtube.com/watch?v=aolI_Rz0ZqY)

# Create multiple Git Config
To ensure multiple git or bitbucket repositories work seamlessly with respective userId's on one machine, 
configure the global git file in such a way that it picks up right user name for specific repositories.
with global `.gitconfig` file in home folder `~`
```sh
[includeIf "gitdir:~/Documents/ClonedCodeWork/"]
	path = .gitconfig-work
[includeIf "gitdir:~/Programming/"]
	path = .gitconfig-learn
```
`gitdir` takes the folder where multiple projects can reside from same repository (eg: bitbucket enterprise server)

- create the files and open in a text editor
    ```sh
    touch ~/.gitconfig-learn | open .gitconfig-learn
    touch ~/.gitconfig-work  | open .gitconfig-work
    ```
- Update the (relevant) information as needed in both the file under `[user]` tag
    ```sh
    [user]
        email = xxx@xxx.com
        name = Your Name
    ```
  
> While using git clients (github desktop, source tree etc), ensure that it does not overwrite the git config file

# Create global GitIgnore via separate file
- Create `.gitignore_global` file in the home directory `~` 
    ```shell
    touch ~/.gitignore_global
    ```
- add files that needs to be globally ignored
-  ```sh
   *~
   .DS_Store
   ```
- Configure Git to Use the Global `.gitignore` File
    ```shell
    git config --global core.excludesFile '~/.gitignore_global'
    ```

# templatedir
The `git config --global init.templatedir` command is used to set a global configuration option in Git 
that specifies a directory template to be used when **initializing new repositories**. 

**Template Directory**: When you initialize a new Git repository with git init, 
Git **copies** files from the directory specified by `init.templatedir` into the **.git directory of the new repository**. 
```text
~/.git-templates/
    ├── hooks/
    ├── info/
    └── attributes/
```
This allows you to pre-configure new repositories with certain files, including 
- Git hooks, 
- configuration files, etc.

### Summary Commands
```shell
# Create Template Directory
mkdir -p ~/.git-templates/hooks ~/.git-templates/info ~/.git-templates/attributes

# Add Files to the Template Directory:**
touch ~/.git-templates/hooks/pre-commit #example hook
chmod +x ~/.git-templates/hooks/pre-commit
touch ~/.git-templates/.gitmessage # for message template
touch ~/.git/info/exclude # global gitignore

# Set the Global Configuration:**
git config --global init.templatedir '~/.git-templates'
# Configure Git to use the commit message template by default:
git config --global commit.template '~/.git-templates/.gitmessage'
```

## Configure Git to Use the Global Hooks Directory:
This setting ensures that the hooks from `~/.git-templates/hooks` are copied to
the `.git/hooks` directory in every **new repository** you create.

```shell
mkdir -p ~/.git-templates/hooks
#Create a pre commit hook file and set its permissions
touch ~/.git-templates/hooks/pre-commit
chmod +x ~/.git-templates/hooks/pre-commit

git config --global init.templatedir '~/.git-templates'
```

## Create global GitIgnore via templated dir
File names present under `.git/info/exclude` are ignored 

```shell
# ~/.git-templates/info/exclude
# Local excludes that are not tracked by git
*.log
*.tmp
*.idea
.DS_Store
```

## Default Commit Message Templates
```shell
# ~/.git-templates/.gitmessage
# Commit message template
Jira-Id:
Summary:
Description:
```

- Configure Git to use the template by default:
  ```shell
  git config --global commit.template '~/.git-templates/.gitmessage'
  ```

- To check for a local commit template setting
  ```shell
  git config --get commit.template
  ```
- To remove a local commit template setting
  ```shell
  git config --unset commit.template
  ```

# Creating global alias
- Creating Alias
  ```shell
  git config --global alias.cob 'checkout -b'
  ```
- Using the alias
  ```shell
  git cb new-branch-name
  ```
- Removing alias
  ```shell
  git config --global --unset alias.co
  ```
- Check all Alias
  ```shell
  git config --global --get-regexp alias
  # check individual
  git config --global --get alias.cb
  ```


