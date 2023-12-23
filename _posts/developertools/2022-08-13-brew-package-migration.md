---
# layout: static
title:  "MacBook : Brew Package Migration"
date:   2022-08-13 10:41:00
categories: ['Developer tools']
tags: ['Developer tools']
---
{% include toc title="Index" %}

# Show top level packages without dependencies
```sh
brew leaves | xargs -n1 brew desc --eval-all
```

Taking all the brew packages from one machine to another machine can be achieved via brew bundle
```sh
# Run on old machine to gather all the installed packages
brew bundle dump --describe --global #Creates ~/.Brewfile with all installed package information
```

Run the following to install the packages from [BrewFile](https://github.com/nitinkc/SystemEnvironment/blob/master/mac/.Brewfile) 
```sh
brew bundle install --global #--global -> Read the Brewfile from ~/.Brewfile.
```

### Brew maintenance

```shell
brew update && brew outdated && brew upgrade && brew cleanup

# or create alias for repetitive usages
buou='brew update && brew outdated && brew upgrade && brew cleanup'
```
### Common Brew packages used

| Tool             | Details                                                               | 
|:-----------------|:----------------------------------------------------------------------|
| cmatrix          | Console Matrix                                                        |
| csshx            | Cluster ssh tool for Terminal.app                                     |
| exa              | Modern replacement for 'ls'                                           |
| ffmpeg           | Play, record, convert, and stream audio and video                     |
| figlet           | Banner-like program prints strings as ASCII art                       |
| gcc              | GNU compiler collection                                               |
| gifsicle         | GIF image/animation creator/editor                                    |
| git              | Distributed revision control system                                   |
| git-gui          | Tcl/Tk UI for the git revision control system                         |
| gradle@6         | Open-source build automation tool based on the Groovy and Kotlin DSL  |
| groovysdk        | SDK for Groovy - a Java-based scripting language                      |
| jenkins-lts      | Extendable open-source CI server                                      |
| jq               | Lightweight and flexible command-line JSON processor                  |
| kafka            | Open-source distributed event streaming platform                      |
| libfido2         | Provides library functionality for FIDO U2F & FIDO 2.0, including USB |
| libxslt          | C XSLT library for GNOME                                              |
| maven            | Java-based project management                                         |
| minikube         | Run a Kubernetes cluster locally                                      |
| mongodb-community| High-performance, schema-free, document-oriented database             |
| nghttp2          | HTTP/2 C Library                                                      |
| nginx            | HTTP(S) server and reverse proxy, and IMAP/POP3 proxy server          |
| node@14          | Platform built on V8 to build network applications                    |
| openjdk@8        | Development kit for the Java programming language                     |
| pandoc           | Swiss-army knife of markup format conversion                          |
| pipes-sh         | Animated pipes terminal screensaver                                   |
| protobuf         | Protocol buffers (Google's data interchange format)                   |
| rtmpdump         | Tool for downloading RTMP streaming media                             |
| screen           | Terminal multiplexer with VT100/ANSI terminal emulation               |
| six              | Python 2 and 3 compatibility utilities                                |
| starship         | Cross-shell prompt for astronauts                                     |
| task             | Feature-rich console based todo list manager                          |
| telnet           | User interface to the TELNET protocol                                 |
| timewarrior      | Command-line time tracking application                                |
| tree             | Display directories as trees (with optional color/HTML output)        |
| wget             | Internet file retriever                                               |
| xpdf             | PDF viewer                                                            |
| youtube-dl       | Download YouTube videos from the command-line                         |
| yt-dlp           | A youtube-dl fork with additional features and fixes                  |
| zsh              | UNIX shell (command interpreter)                                      |