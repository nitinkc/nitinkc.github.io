---
# layout: static
title:  "Configuring a new MacBook for Dev Productivity"
date: 2021-02-10 02:15:00
categories: ['Developer tools']
tags: ['Developer tools']
---

## Contents

{% include toc title="Index" %}

# Configuring Java development Environment

Installing the following tools and configuring them ensures maximum ease of development

1. Install Brew Package manager
2. Create personalized [profiles and configure alias](https://github.com/nitinkc/SystemEnvironment#readme)

| Tool | Details | 
| :---| :---    |   
|Iterm		|[Configuring iTerm]({{ site.baseurl }} {% post_url /developerTools/2021-02-01-iterm2-zsh-config %})|
|IntelliJ	|[Configuring IntelliJ]({% post_url /2021-02-07-inteliJ-Idea-CE-settings-and-useful-shortcuts %})|
|Sublime	|[Configuring Sublime Editor]({% post_url 2021-03-24-Sublime-Settings %})|


The following tools helps a lot making the develop environment much more conducive to work. 


# Useful Office Productivity tool

| Tool | Details | 
| :---| :---    |   
|Alfred 4 for Mac 	| | 
|gemini 2 			| Scan the mac for duplicates|
|PhotoSweeper 		||
|Amphetamine 		| keeping the mac active and prevent it from locking|
|Flycut /JumpCut 	| Clipboard manager|
|Flux 				| Whitelight manager, based on location. Redundant with latest mac OS|
|TimeOut 			| Rest your eyes based on Pomodoro Cycles|
|Kap 				| Screen Recorder, Screenshot for emails|
|Giphy Capture		| Screen Recorder to GIF for email attachments|
|Rectangle 			| Move and resize windows in macOS|
|Cheatsheet			| Reveal Mac shortcuts, if you hold command (⌘) key for a few seconds in a software context|
|CustomShortcuts 	| Define your own shortcuts|
|DBeaver			| Open source DB client for all|
|ItsYCal			| View Calander and Time like Windows on ToolBar on top|
|[***XMind***](http://www.xmind.net/download/mac/)|MindMapping tool|
|Transmission|for Peer to peer Torrent transfer. Setup your own server|


# Mac Shortcuts

Press Shift-Command-5 (macOS Mojave or later) and invoke the screen capture panel.

Click on Options and choose "Other Location" to choose a destination.


## Toggle Hidden files

Command + Shift + Period

or
```sh
alias showFiles='defaults write com.apple.finder AppleShowAllFiles YES;killall Finder /System/Library/CoreServices/Finder.app'
alias hideFiles='defaults write com.apple.finder AppleShowAllFiles NO;killall Finder /System/Library/CoreServices/Finder.app'
```