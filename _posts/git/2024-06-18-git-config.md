---
categories: Git
date: 2024-06-18 13:30:00
tags:
- Configuration
- Settings
- Setup
- Commands
title: Git Config
---

{% include toc title="Index" %}

[https://blog.gitbutler.com/fosdem-git-talk/](https://blog.gitbutler.com/fosdem-git-talk/)

![](https://www.youtube.com/watch?v=aolI_Rz0ZqY)

# Check existing git configs

```shell
git config --list
```

# Create multiple Git Config

With single repo and user
`git config --global user.name "John Doe" && git config --global user.email "john.doe@example.com"`
would suffice

`--global` writes a system-wide config file and `--local` (the default) that
writes to `.git/config` in the project repo.

```shell
git config  user.name "John Doe" 
#Or
git config --local user.name "John Doe" 
```

To ensure multiple git or bitbucket repositories work seamlessly with respective
userId's on one machine,
configure the global `.gitconfig` such that it picks up right id for specific
repo.

global `.gitconfig` file is located in home folder `~`

- with commnd
    - Add Config
      ```shell
      git config --file ~/.gitconfig-work user.name "Your Name"
      git config --file ~/.gitconfig-work user.email "xxx@xxx.com"
      ```
    - Add the config file
      ```shell
      git config --global includeIf.gitdir:~/ClonedCodeWork/.path .gitconfig-work
      git config --global includeIf.gitdir:~/Programming/.path .gitconfig-learn
      ```
- manually
    - create the files and open in a text editor
        ```shell
        touch ~/.gitconfig-learn | open .gitconfig-learn
        touch ~/.gitconfig-work  | open .gitconfig-work
        ```
    - Update the (relevant) information as needed in both the file under
      `[user]` tag
        ```shell
        [user]
            email = xxx@xxx.com
            name = Your Name
        ```
    - Or, Manually add the config
      ```shell
      [includeIf "gitdir:~/Documents/ClonedCodeWork/"]
      path = .gitconfig-work
      [includeIf "gitdir:~/Programming/"]
      path = .gitconfig-learn
      ```

- Check
  ```shell
  git config --global --get-regexp includeIf
  ```

`gitdir` takes the folder where multiple projects can reside from same
repository (eg: bitbucket enterprise server)

> While using git clients (github desktop, source tree etc), ensure that it does
> not overwrite the git config file

# Create global GitIgnore via separate file

- Create `.gitignore_global` file in the home directory `~`
    ```shell
    touch ~/.gitignore_global
    ```
- add files that needs to be globally ignored
  ```sh
   *~
   .DS_Store
   ```
- Configure Git to Use the Global `.gitignore` File
    ```shell
    git config --global core.excludesFile '~/.gitignore_global'
    ```

# templatedir

**Template Directory**: When you initialize a new Git repository with git init,
Git **copies** files from the directory specified by `init.templatedir` into the
**.git directory of the new repository**.

The `git config --global init.templatedir` command is used to set a global
configuration option in Git
that specifies a directory template to be used when **initializing new
repositories**.

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

### For Existing Repositories:

Need to manually copy the hooks from the global directory into each repository's
`.git/hooks` directory.

```shell
for repo in $(find /path/to/your/repos -type d -name '.git'); do
  cp ~/.git-templates/hooks/* $repo/hooks/
done
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

# Branch Sorter

- sort by `objectsize`, `authordate`, `committerdate`, `creatordate`, or
  `taggerdate` with the `--sort` option
  ```shell
  git branch --sort=-committerdate
  ```

- Set it as a default with the `branch.sort` config setting
  ```shell
  git config --global branch.sort -committerdate
  ```

> the -committerdate has a leading - not a double dash.

# Column UI

Set the default response in Columns. Try with `git branch`

```shell
git config --global column.ui auto
```

`git column`

```shell
seq 1 12 | git column --mode=column --padding=10
1           2           3           4           5           6           7           8           9           10          11          12   

 seq 1 12 | git column --mode=column --padding=5
1      2      3      4      5      6      7      8      9      10     11     12            
```

# Safe Force Pushing

```shell
git config --global alias.fpush push --force-with-lease
```

# Git Maintenance

[Git Maintenance]({{ site.baseurl }}{% post_url
/git/2023-11-14-git-maintenance %}