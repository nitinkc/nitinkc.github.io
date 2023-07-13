---
# layout: static
title:  "Configuring profile"
date: 2023-07-12 22:10:00
categories: ['Developer tools']
tags: ['Developer tools']
---

On Mac with iTerm2 and ZSH

### Order of file read with ZSH

```shell
/etc/zshenv    # Read for every shell
~/.zshenv      # Read for every shell except ones started with -f

/etc/zprofile  # Global config for login shells, read before zshrc
~/.zprofile    # User config for login shells
/etc/zshrc     # Global config for interactive shells

~/.zshrc       # User config for interactive shells
/etc/zlogin    # Global config for login shells, read after zshrc
~/.zlogin      # User config for login shells
~/.zlogout     # User config for login shells, read upon logout
/etc/zlogout   # Global config for login shells, read after user logout file
```

### Two types of shells: login shells and interactive shells

.bash_profile ->  login shell

.bashrc -> non-login interactive shell.

When you start a sub-shell (by typing a shell's name at the command-prompt), you get a "non-login interactive shell".
It can be started within a login shell or in an existing shell session.

# Semlink the files to be consistent with further edits

Assuming the [project](https://github.com/nitinkc/SystemEnvironment) is cloned in $HOME/Programming folder on a new mac

The following commands will symlink the files and be modified for later use on other macs
```sh
# ~ refers to $HOME Directory
ln -s $HOME/Programming/SystemEnvironment/mac/.zshenv ~
ln -s $HOME/Programming/SystemEnvironment/mac/.zshrc ~
# personal settings
ln -s $HOME/Programming/SystemEnvironment/mac/.my_aliases ~
ln -s $HOME/Programming/SystemEnvironment/mac/.profile ~
# Global Git settings
ln -s $HOME/Programming/SystemEnvironment/mac/.gitconfig ~
ln -s $HOME/Programming/SystemEnvironment/mac/.gitconfig-learn ~
ln -s $HOME/Programming/SystemEnvironment/mac/.gitconfig-work ~
ln -s $HOME/Programming/SystemEnvironment/mac/.gitignore_global ~

#Keep these two for the Terminal (incase iTerm is not to be used)
ln -s $HOME/Programming/SystemEnvironment/mac/.bashrc ~
ln -s $HOME/Programming/SystemEnvironment/mac/.bash_profile ~
```

* $PATH variable, a list directory names separated by colon (:) characters
* The superuser has `/sbin` and `/usr/sbin` entries for easily executing system administration commands.

# OS X: Change your PATH environment variable

### Setting Temporary Environmental Variables in OS X
`export PATH=$PATH:~/bin`

### Adding a Temporary Location
`PATH=/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/bin`

### Adding in a Permanent Location
create a .bash_profile or .profile file in the home directory and set the path in the files as.
`sh export PATH="/usr/local/<my_package>/bin:$PATH" `

# Load the default .profile

* -s is a file test operator for checking if a file exists and has **a non-zero size**. Works with the double brackets syntax ([[ ... ]])
* -f is a file test operator for checking if a file exists and is a **regular file**. Works with []. the -f operator is not compatible with the double brackets syntax ([[ ... ]])

* The && (AND operation) ensures that the next command is executed only if the previous command (the file test) evaluates to true.

* The dot (.) is a special command in Bash that is used to "source" or include the content of another file into the current script

* The single brackets are used for basic conditional expressions.

* The double brackets are part of an extended conditional expression syntax available in Bash,

```shell
if [[ -s "$HOME/.profile" ]]; 
    then . "$HOME/.profile"
fi

# Above can also be written as 
[[ -s "$HOME/.profile" ]] && source "$HOME/.profile"
# OR
[[ -s "$HOME/.profile" ]] && . "$HOME/.profile"\
```
