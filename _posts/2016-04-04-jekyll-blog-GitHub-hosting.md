---
layout: post
title:  "Jekyll Blog and Free Hosting on GitHub!"
date:   2016-04-04 18:31:00
categories: jekyll update
comments: true
disqus_identifier: A7655498-AB9E-40BF-A0D5-E5C6DE6BBF28
tags: [jekyll, disqus]
published: false
---

Making a personal website using GitHubs free Hosting for the Jekyll Sites

Create a blog with naming convention of yyyy-mm-dd-name-of-the-blog.md and save it in \_posts directory


execute in the terminal

> [!NOTE]
> If not using the gem File

```sh
jekyll build
jekyll serve
```

### Making a personal website using GitHubs free Hosting for the Jekyll Sites

1. Ruby (Pre requisites for Jekyll) : https://jekyllrb.com/docs/installation/
2. Jekyll - for static site and blogging

### Build the site
```
bundle install

bundle exec jekyll serve
```

Incase of any issue,

```sh
export LDFLAGS="-L/usr/local/opt/libffi/lib" && \
export PKG_CONFIG_PATH="/usr/local/opt/libffi/lib/pkgconfig" && \
bundle install
```
