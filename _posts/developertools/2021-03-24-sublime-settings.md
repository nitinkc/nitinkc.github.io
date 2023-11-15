---
# layout: static
title:  "Sublime Settings"
date:   2021-03-24 18:07:00
categories: ['Developer tools']
tags: ['Developer tools']
---
{% include toc title="Index" %}

# Make sublime default editor on mac

- Assuming sublime version 4
- no restart needed

```shell
brew install duti

duti -s com.sublimetext.4 public.plain-text all 
duti -s com.sublimetext.4 public.data all

duti -s com.sublimetext.4 public.unix-executable all # set executable scripts to open with subl
```

# Sublime Editor Settings

Working from home, with the desk set up right next to an large window, the
dark theme feels a little too dark. To change the color themes
Goto :

```
Sublime Text -> Preferences -> Color Scheme -> and pick between available Completions
```

To install an external theme,

Open Command Pallete `Tools -> Command Pallete` or `cmd+Shift+P` and Execute

```
Install Package Control
```

Open Command Pallete again, after the Package Control installation and search the theme of choice
e.g. ayu and once the theme is installed, activate the theme by :

`ayu: Activate theme`

With the theme installed,

Set Theme, Color Scheme Font size etc. from
```
Sublime Text -> Preferences -> Color Scheme
Sublime Text -> Preferences -> Theme
```

Theme: ayu-light.sublime-theme
Color Scheme : ayu-mirage.sublime-theme


## Sublime plugins

Add package control and then using the installation of package control, continue installing the rest of the softwares,

Add \[Package Control\]\(https:\/\/packagecontrol.io\/installation\)
