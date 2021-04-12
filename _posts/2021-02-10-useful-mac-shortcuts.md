---
# layout: static
title:  "Useful Mac settings"
collection : Developer tools
date: 2021-02-10 02:15:00
categories:
tags: [System Design]
---

## Toggle Hidden files
Command + Shift + Period

or
```sh
alias showFiles='defaults write com.apple.finder AppleShowAllFiles YES;killall Finder /System/Library/CoreServices/Finder.app'
alias hideFiles='defaults write com.apple.finder AppleShowAllFiles NO;killall Finder /System/Library/CoreServices/Finder.app'
```
