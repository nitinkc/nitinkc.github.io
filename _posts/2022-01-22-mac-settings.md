---
# layout: static
title:  "Mac UI Settings"
date:   2022-01-22 21:55:00
categories: Shortcuts
tags: [Shortcuts]
---

# Necessasary UI Settings

### Show Full directory path on Finder: 

File path at the top of the tool bar on finder window

```sh
defaults write com.apple.finder _FXShowPosixPathInTitle -bool true; killall Finder
```
Execute the command on terminal and the file path would appear like :-

![]({{ site.url }}/assets/images/filePath.png)


### Useful toolbar items

![]({{ site.url }}/assets/images/mac_toolbar.png)


### Show Path Bar

Path Bar appears on the bottom of the Finder Window

![]({{ site.url }}/assets/images/pathbar.png)


 Open **Finder** and go to View > Show Path Bar.

![]({{ site.url }}/assets/images/pathbar_set.png){:height="400px" width="200px"}

