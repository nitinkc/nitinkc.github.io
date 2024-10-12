---
title:  "Terminal Setup"
date:   2021-02-01 14:00:00
categories: ['Developer tools','MacBook']
tags: ['Developer tools','Macbook']
---

{% include toc title="Index" %}

### Unix shell and Framework installation

Install any of the available shell

```sh
brew install --cask iterm2 
brew install --cask wezterm
brew install --cask alacritty
```

Instead of using the Mac default Bash shell, preferred here is zsh with multiple
plugin support.

* Install latest version of zsh using brew and verify the version.

```sh
brew install zsh
zsh --version
```

with zsh installed, the default profile will be from .zshrc file, where
customized profiles can be added

- Make zsh as system’s default shell

```sh
chsh -s $(which zsh)
```

- Verify:

```sh
echo $SHELL
```

expected result: **/bin/zsh**

- Install oh-my-zsh using [https://ohmyz.sh/#install](https://ohmyz.sh/#install)

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

### Eza instead of ls

[https://formulae.brew.sh/formula/eza](https://formulae.brew.sh/formula/eza)

```sh
brew install eza
```

### Install zshrc plugins

Standard plugins are at `$ZSH/plugins/` or `~/.oh-my-zsh/plugins`

Custom plugins may be added to `$ZSH_CUSTOM/plugins/` or
`~/.oh-my-zsh/custom/plugins`

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

- [Time Warrior](https://timewarrior.net/docs/install/)

```sh
brew install timewarrior
```

# iTerm-2 shortcuts

| **Shortcut** | **For**                    |
|:-------------|:---------------------------|
| **⌘ ,**      | Open Preferences           |
| **⌘ D**      | Split Windows Vertically   |
| **⌘ ⇧ D**    | Split Windows Horizontally |
| **⌘ ;**      | Auto completion            |
| **⌘ ⇧ H**    | Paste History              |
| **⌘ ⌥ B**    | Show Interactive History   |
| **⌥ ⌘ Drag** | Select Rectangular Block   |

Once iTerm is set with above plugins, other terminals can simply be installed
and with its corrosponding configs

# Alacritty

[https://www.josean.com/posts/how-to-setup-alacritty-terminal](https://www.josean.com/posts/how-to-setup-alacritty-terminal)

[https://www.josean.com/posts/7-amazing-cli-tools](https://www.josean.com/posts/7-amazing-cli-tools)

# WezTerm

[https://www.josean.com/posts/how-to-setup-wezterm-terminal](https://www.josean.com/posts/how-to-setup-wezterm-terminal)

## References

[Follow This Link](https://medium.com/swlh/power-up-your-terminal-using-oh-my-zsh-iterm2-c5a03f73a9fb)

[Follow this link as well](https://towardsdatascience.com/customising-the-mac-terminal-to-increase-productivity-and-improve-the-interface-894f6d86d573)

[detailed link](https://towardsdatascience.com/the-ultimate-guide-to-your-terminal-makeover-e11f9b87ac99)


