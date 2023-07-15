---
title:  "MacBook : iTerm2 Set up with zsh on Mac"
date:   2021-02-01 14:00:00
categories: ['Developer tools','MacBook']
tags: ['Developer tools','Macbook']
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

### Exa instead of ls
```sh
brew install exa
```
Add this to .zshrc file

```shell
if [ -x "$(command -v exa)" ]; then
    alias ls="exa"
    alias la="exa --long --all --group"
fi
```

### Install zshrc plugins

Standard plugins are at `$ZSH/plugins/` or `~/.oh-my-zsh/plugins`

Custom plugins may be added to `$ZSH_CUSTOM/plugins/` or `~/.oh-my-zsh/custom/plugins`

Pluions can be added to the `.zshrc` file lile below
```shell
plugins=(git autojump zsh-autosuggestions zsh-syntax-highlighting)
```

Some plugins have to be installed before adding to the plugins array

```sh
brew install zsh-syntax-highlighting zsh-completions
brew install autojump
```

in case of issues

```sh
git clone https://github.com/zsh-users/zsh-autosuggestions ~/.oh-my-zsh/custom/plugins/zsh-autosuggestions
git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ~/.oh-my-zsh/custom/plugins/zsh-syntax-highlighting
```

Follow the documentation for further instructions.

* [Auto suggestions](https://github.com/zsh-users/zsh-autosuggestions/blob/master/INSTALL.md#oh-my-zsh)
* [Autojump plugin](https://github.com/ohmyzsh/ohmyzsh/tree/master/plugins/autojump)
* [git plugin](https://github.com/ohmyzsh/ohmyzsh/tree/master/plugins/git)
* [Syntax Highlighting](https://github.com/zsh-users/zsh-syntax-highlighting/blob/master/INSTALL.md)
* [Zsh Completions](https://github.com/zsh-users/zsh-completions/#Manual%20installation)
* [Zsh history substring](https://github.com/zsh-users/zsh-history-substring-search)
* [Zsh Apple touchbar](https://github.com/zsh-users/zsh-apple-touchbar)

[Time Warrior](https://timewarrior.net/docs/install/)

```sh
brew install timewarrior
```

## References

[Follow This Link](https://medium.com/swlh/power-up-your-terminal-using-oh-my-zsh-iterm2-c5a03f73a9fb)

[Follow this link as well](https://towardsdatascience.com/customising-the-mac-terminal-to-increase-productivity-and-improve-the-interface-894f6d86d573)

[detailed link](https://towardsdatascience.com/the-ultimate-guide-to-your-terminal-makeover-e11f9b87ac99)


