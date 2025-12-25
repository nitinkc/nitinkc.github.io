---
categories: Developer Tools
date: 2021-02-10 02:15:00
tags:
- MacOS
- Configuration
- Setup
- MacBook
title: Configuring a new MacBook
---

## Contents

{% include toc title="Index" %}

# Configuring Java development Environment

Installing the following tools and configuring them ensures maximum ease of
development

1. Install [Brew Package manager](https://brew.sh/)
2. Create
   personalized [profiles and configure alias](https://github.com/nitinkc/SystemEnvironment/tree/master/mac)

- Terminal              [Configuring Terminal]({% post_url
  /developertools/2021-02-01-terminal-config %})
- Profile Settings   [Set Local profile, alias etc.]({% post_url
  /developertools/2023-07-12-profile-settings %})
- IntelliJ Settings  [Configuring IntelliJ]({% post_url
  /developertools/intelliJ/2021-02-07-inteliJ-Idea-CE-settings %})
- Git config         [Configuring global git congig]({% post_url
  /git/2024-06-18-git-config %})
- Sublime              [Configuring Sublime Editor]({% post_url
  /developertools/2021-03-24-sublime-settings %})
- Brew Package       [Migrating brew packages]({% post_url
  /developertools/2022-08-13-brew-package-migration%} )
- [Macbook Settings]({% post_url /developertools/2022-01-22-mac-settings%})

The following tools help making the develop environment much more conducive to
work.

# Useful Office Productivity tool

| Tool              | Details                                                                                   | 
|:------------------|:------------------------------------------------------------------------------------------|   
| Alfred 4 for Mac  |                                                                                           | 
| gemini 2          | Scan the mac for duplicates                                                               |
| PhotoSweeper      |                                                                                           |
| Amphetamine       | keeping the mac active and prevent it from locking                                        |
| Flycut            | Clipboard manager                                                                         |
| JumpCut           | ^^                                                                                        |
| Flux              | Whitelight manager, based on location. Redundant with latest mac OS                       |
| TimeOut           | Rest your eyes based on Pomodoro Cycles                                                   |
| Kap               | Screen Recorder, Screenshot for emails                                                    |
| Giphy Capture     | Screen Recorder to GIF for email attachments                                              |
| Rectangle         | Move and resize windows in macOS                                                          |
| Cheatsheet        | Reveal Mac shortcuts, if you hold command (⌘) key for a few seconds in a software context |
| CustomShortcuts 	 | Define your own shortcuts                                                                 |
| DBeaver           | Open source DB client for all                                                             |
| ItsYCal           | View Calander and Time like Windows on ToolBar on top                                     |
| ***XMind***       | [MindMapping tool](http://www.xmind.net/download/mac/)                                    |
| Transmission      | for Peer to peer Torrent transfer. Setup your own server                                  |
| caffeinate        | Keep Your Mac awake                                                                       |
| Amphetamine       | ^^                                                                                        |
| CCleaner          | Clean temp files                                                                          |

# Mac Shortcuts

Press `Shift-Command-5` (macOS Mojave or later) and invoke the screen capture
panel.

Click on `Options` and choose `Other Location` to choose a destination.

## Toggle Hidden files

`Command + Shift + Period`

or

```sh
alias showFiles='defaults write com.apple.finder AppleShowAllFiles YES;killall Finder /System/Library/CoreServices/Finder.app'
alias hideFiles='defaults write com.apple.finder AppleShowAllFiles NO;killall Finder /System/Library/CoreServices/Finder.app'
```

[Further Macbook settings - Alias](https://github.com/nitinkc/SystemEnvironment/blob/master/mac/.my_aliases)