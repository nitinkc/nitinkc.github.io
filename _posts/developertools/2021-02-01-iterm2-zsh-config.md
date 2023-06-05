---
title:  "iTerm2 Set up with zsh on Mac"
date:   2021-02-01 14:00:00
categories: ['Developer tools']
tags: ['Developer tools']
---

{% include toc title="Index" %}

## Setting Mac Terminal environment for Development


### Unix shell and Framework installation

Between iTerm and Hyper, iTerm is preferred here. Download and install iTerm

```sh
brew install --cask iterm2 
```

Instead of using the Mac default Bash shell, preferred here is zsh with multiple plugin support.

* Install latest version of zsh using brew and verify the version.

```sh
brew install zsh
zsh --version
```

with zsh installed, the default profile will be from .zshrc file, where customized profiles can be added

* Make zsh as system’s default shell

```sh
chsh -s $(which zsh)
```
* Verify:

```sh
echo $SHELL
expected result: /bin/zsh
```

* Install oh-my-zsh using [this link](https://ohmyz.sh/#install)

### Install Powerline 10k

```sh
git clone https://github.com/romkatv/powerlevel10k.git $ZSH_CUSTOM/themes/powerlevel10k
```
Run either
```
p10k configure
```
OR

Edit `~/.zshrc` and `set ZSH_THEME="powerlevel10k/powerlevel10k"`.

### Exa insted of ls
```sh
brew install exa
```
Add this to .zshrc file

```
if [ -x "$(command -v exa)" ]; then
    alias ls="exa"
    alias la="exa --long --all --group"
fi
```
### Install plugins

* [Auto suggestions](https://github.com/zsh-users/zsh-autosuggestions/blob/master/INSTALL.md#oh-my-zsh)

* [Syntax Highlighting](https://github.com/zsh-users/zsh-syntax-highlighting/blob/master/INSTALL.md)

* [Zsh Completions](https://github.com/zsh-users/zsh-completions/#Manual%20installation)

* [Zsh history substring](https://github.com/zsh-users/zsh-history-substring-search)

* [Zsh Apple touchbar](https://github.com/zsh-users/zsh-apple-touchbar)

```sh
brew install zsh-syntax-highlighting zsh-completions
```

in case of issues

```sh
git clone https://github.com/zsh-users/zsh-autosuggestions ~/.oh-my-zsh/custom/plugins/zsh-autosuggestions
git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ~/.oh-my-zsh/custom/plugins/zsh-syntax-highlighting
```

[Time Warrior](https://timewarrior.net/docs/install/)

```sh
brew install timewarrior
```

##### Order of file read with ZSH

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

### For regular Shell

##### Global settings:
```shell
/etc/profile
/etc/bashrc
```

##### Personal settings:
```
~/.bash_profile OR  ~/.bash_login OR ~/.profile
~/.bashrc
~/.bash_aliases
```

.bash_profile ->  login shell

.bashrc -> non-login shell.

When you start a sub-shell (by typing a shell's name at the command-prompt), you get a "non-login shell".

When a "login shell" starts up, it reads the file

"/etc/profile" and

then "~/.bash_profile" or "~/.bash_login" or "~/.profile"
(whichever one exists - it only reads one of these, checking for them in the order mentioned).

When a "non-login shell" starts up, it reads the file "/etc/bashrc" and then the file "~/.bashrc".

# Semlink the files to be consistent with further edits
Assuming the project is cloned in $HOME/Programming folder on a new mac

The following commands will symlink the files and be modified for later use on other macs
```sh
# ~ refers to $HOME Directory
ln -s $HOME/Programming/SystemEnvironment/mac/.my_aliases ~
ln -s $HOME/Programming/SystemEnvironment/mac/.profile ~
ln -s $HOME/Programming/SystemEnvironment/mac/.zshrc ~

#Keep these two for the Terminal (incase iTerm is not to be used)
ln -s $HOME/Programming/SystemEnvironment/mac/.bashrc ~
ln -s $HOME/Programming/SystemEnvironment/mac/.bash_profile ~
```

* $PATH variable, a list directory names separated by colon (:) characters
* The superuser has /sbinand /usr/sbin entries for easily executing system administration commands.


# OS X: Change your PATH environment variable

### Setting Temporary Environmental Variables in OS X
`export PATH=$PATH:~/bin`

### Adding a Temporary Location
`PATH=/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/bin`

### Adding in a Permanent Location
create a .bash_profile or .profile file in the home directory and set the path in the files as.
`sh export PATH="/usr/local/<my_package>/bin:$PATH" `



## References

[Follow This Link](https://medium.com/swlh/power-up-your-terminal-using-oh-my-zsh-iterm2-c5a03f73a9fb)

[Follow this link as well](https://towardsdatascience.com/customising-the-mac-terminal-to-increase-productivity-and-improve-the-interface-894f6d86d573)

[detailed link](https://towardsdatascience.com/the-ultimate-guide-to-your-terminal-makeover-e11f9b87ac99)


