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

Assuming the [project](https://github.com/nitinkc/SystemEnvironment) is cloned in `$HOME/Programming` folder on a new mac

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

## Additional Change your PATH environment variable

Setting Temporary Environmental Variables in OS X
create a .bash_profile or .profile file in the home directory and set the path in the files as.

```shell
export PATH=$PATH:~/bin
export PATH="/usr/local/<my_package>/bin:$PATH"
```
Adding a Temporary Location

```shell
PATH=/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/bin
```

# Load the default .profile

Keep the alias in the profile file and then just load the profile.
```shell
[[ -s "$HOME/.profile" ]] && . "$HOME/.profile"
```

* -s is a file test operator for checking if a file exists and has **a non-zero size**. Works with the double brackets syntax ([[ ... ]])
* -f is a file test operator for checking if a file exists and is a **regular file**. Works with []. the -f operator is not compatible with the double brackets syntax ([[ ... ]])

* The && (AND operation) ensures that the next command is executed only if the previous command (the file test) evaluates to true.

* The dot (.) is a special command in Bash that is used to "source" or include the content of another file into the current script

* The single brackets are used for basic conditional expressions.

* The double brackets are part of an extended conditional expression syntax available in Bash,

Bash code with -s
```shell
if [[ -s "$HOME/.profile" ]]; 
    then . "$HOME/.profile"
fi

# Above can also be written as 
[[ -s "$HOME/.profile" ]] && source "$HOME/.profile"
# OR
[[ -s "$HOME/.profile" ]] && . "$HOME/.profile"
```
Bash code with if....else with -s

```shell
if [[ -s "$HOME/.profile" ]] && [ -f "$HOME/.profile" ]; then
    # Code to execute if both conditions are true
    echo "1. File '$HOME/.profile' exists, is a regular file, and has a non-zero size."
else
    # Code to execute if either condition is false
    echo "File '$HOME/.profile' does not meet both conditions."
fi

[[ -s "$HOME/.profiled" ]] && [ -f "$HOME/.profile" ] && echo "1.1 File '$HOME/.profile' exists." || echo "1.1 File '$HOME/.profiled' does not meet both conditions."
```

Bash code with -f
```shell
[ -f $(brew --prefix)/etc/profile.d/autojump.sh ] && . $(brew --prefix)/etc/profile.d/autojump.sh

# The next line updates PATH for the Google Cloud SDK.
if [ -f '$(brew --prefix)/etc/profile.d/autojump.sh' ];
  then . '$(brew --prefix)/etc/profile.d/autojump.sh';
fi
```

Bash code with if...else with -f switch

```shell
if [ -f "$HOME/.profile" ]; then
    echo "2. File '$HOME/.profile' exists, is a regular file, and has a non-zero size."
else
    echo "File '$HOME/.profile' does not meet both conditions."
fi

# Reduced Syntax
[ -f "$HOME/.profiler" ] && echo "3. File '$HOME/.profile' exists." || echo "3. File '$HOME/.profiler' does not meet both conditions."

```