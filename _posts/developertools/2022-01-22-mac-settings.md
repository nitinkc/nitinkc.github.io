---
# layout: static
title:  "Mac UI Settings"
date:   2022-01-22 21:55:00
categories: ['Developer tools']
tags: ['Developer tools']
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

Enabling the Path Bar for the OS X Finder
    • From a Finder window, pull down the “View” menu and select “Show Path Bar”
you can double-click the individual folders to jump directly to them, and you can even drag and drop files and folders to them

Path Bar appears on the bottom of the Finder Window

![]({{ site.url }}/assets/images/pathbar.png)


 Open **Finder** and go to View > Show Path Bar.

![]({{ site.url }}/assets/images/pathbar_set.png){:height="400px" width="200px"}

### Show Library folder

```sh
chflags nohidden ~/Library/;killall Finder;
```

### Show Hidden Files

```sh
defaults write com.apple.finder AppleShowAllFiles YES
```

### Disable Delete message
```sh
defaults write com.apple.finder NSUserKeyEquivalents {"Move to Trash"="\U007F"}
```

### Change Screenshot File Type
```sh
alias screenShotType='defaults write com.apple.screencapture type -string "png"'
```
### Change Screenshot Location
```sh
alias screenTypeDir='defaults write com.apple.screencapture location /Users/nitin/Downloads'
```

Activate the two aliases
```shell
screenShotType
screenTypeDir
```
### Terminal from Finder

Open the Keyboard system preferences and click on the “Shortcuts” tab. 

Add Terminal (or iTerm2) shortcuts to the Services menu by
* clicking on the “Services” category
* scroll down to “Files and Folders” 
* enable “New Terminal at Folder” and “New Terminal Tab at Folder.”

![]({{ site.url }}/assets/images/set_keyboard_shortcut.png)

![]({{ site.url }}/assets/images/treminal_from_finder.png)


Command prompt Variables: PS1, PS2, PS3, PS4 and PROMPT_COMMANDPS1

PS1 – Default interactive prompt 

echo $PS1

export PS1="\W]\$ "

\W   The basename of $PWD.

\$   If you are not root, inserts a "$"; if you are root, you get a "#"  (root uid = 0)

This change can be made permanent by placing the "export" definition in your ~/.bashrc file.


