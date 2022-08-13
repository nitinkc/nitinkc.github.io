---
# layout: static
title:  "Brew Package Migration"
date:   2022-08-13 10:41:00
categories: ['Developer tools']
tags: ['Developer tools']
---
{% include toc title="Index" %}

Taking all the brew packages from one machine to another machine can be achieved via

```sh
# Run on old machine to gather all the installed packages
brew bundle dump --describe --global #Creates ~/.Brewfile with all installed package information

#--global -> Read the Brewfile from ~/.Brewfile.

brew bundle install --global

```