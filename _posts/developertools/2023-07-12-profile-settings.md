---
# layout: static
title:  "MacBook : Configuring shell profile"
date: 2023-07-12 22:10:00
categories: ['Developer tools','MacBook']
tags: ['Developer tools','Macbook']
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

Output of the iTerm2 shell running on my macbook

```log
Loading .zshenv file ....
Loading .profile file ....
Loading .my_aliases file ....
Loading .zprofile file ....
Loading .zshrc file ....
Loading .oh-my-zsh file ....
Loading .p10k.zsh file ....
Loading .iterm2_shell_integration file ....
```

### Two types of shells: login shell and interactive shell

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
ln -s $HOME/Programming/SystemEnvironment/mac/.zprofile ~

# Global Git settings
ln -s $HOME/Programming/SystemEnvironment/mac/.gitconfig ~
ln -s $HOME/Programming/SystemEnvironment/mac/.gitconfig-learn ~
ln -s $HOME/Programming/SystemEnvironment/mac/.gitconfig-work ~
ln -s $HOME/Programming/SystemEnvironment/mac/.gitignore_global ~

#Keep these two for the Terminal (incase iTerm is not to be used)
ln -s $HOME/Programming/SystemEnvironment/mac/.bashrc ~
ln -s $HOME/Programming/SystemEnvironment/mac/.bash_profile ~

# Sublime make it availabe in PATH
ln -s /Applications/Development/Sublime\ Text.app/Contents/SharedSupport/bin /usr/local/bin/.
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

# Alias

Few Alias are created by zsh which is annoying so locate the file `~/.oh-my-zsh/lib/directories.zsh`

you can locate the alias using ack search
```shell
ack "it2api=/Users/nichaurasia/.iterm2/it2api" --ignore-dir=Library ~
```

# Load the default .profile

Keep the alias in the profile file and then just load the profile.
```shell
[[ -s "$HOME/.profile" ]] && . "$HOME/.profile"
```

* The && (AND operation) ensures that the next command is executed only if the previous command (the file test) evaluates to true.
* The dot (.) is a special command in Bash that is used to "source" or include the content of another file into the current script


* `-s` is a file test operator for checking if a file exists and has **a non-zero size**. Works with the double brackets syntax (`[[ ... ]]`)
* The double brackets are part of an extended conditional expression syntax available in Bash,
```shell
[[ -s "$HOME/.profile" ]] && . "$HOME/.profile"
```

* `-f` is a file test operator for checking if a file exists and is a **regular file**. Works with []. the -f operator is not compatible with the double brackets syntax (`[[ ... ]]`)
* The single brackets are used for basic conditional expressions.
```shell
[ -f "$HOME/.profiler" ] && echo "File '$HOME/.profile' exists."
```

* The `-e` flag is a test operator that checks for file existence.
```shell
test -e $HOME/.profiler && source $HOME/.profiler
```

##### Bash code with -s
```shell
if [[ -s "$HOME/.profile" ]] && [ -f "$HOME/.profile" ]; then
    echo "File '$HOME/.profile' exists, is a regular file, and has a non-zero size."
    source $HOME/.profile
else
    echo "File '$HOME/.profile' does not meet both conditions."
fi

# Above can also be written as 
[[ -s "$HOME/.profile" ]] && [ -f "$HOME/.profile" ] &&  echo "File '$HOME/.profile' exists, is a regular file, and has a non-zero size."; source $HOME/.profile || echo "File '$HOME/.profiled' does not meet both conditions."

# OR without echo and else
[[ -s "$HOME/.profile" ]] && . "$HOME/.profile"
```

##### Bash code with -f
```shell
# Reduced Syntax
[ -f "$HOME/.profile" ] && echo "File '$HOME/.profile' exists."; . "$HOME/.profile" || echo "File '$HOME/.profile' does not exist"

# Syntax with test of existance -e
test -e $HOME/.profile && echo "File '$HOME/.profile' exists."; . "$HOME/.profile" || echo "File '$HOME/.profile' does not exist"
```