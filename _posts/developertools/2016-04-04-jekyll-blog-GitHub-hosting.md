---
categories: Developer tools
date: 2016-04-04 18:31:00
tags:
- Developer tools
title: Jekyll Blog and Hosting on GitHub
---

{% include toc title="Index" %}

Create a blog with naming convention of yyyy-mm-dd-name-of-the-blog.md and save
it in \_posts directory

On a new machine (mac) use this link

[Install Jekyll](https://jekyllrb.com/docs/installation/)

> If not using the gem File

```sh
bundle exec jekyll build
jekyll serve
```

### Making a personal website 
using GitHub's free Hosting for the Jekyll Sites

1. Ruby (Pre requisites for Jekyll) : https://jekyllrb.com/docs/installation/
2. Jekyll - for static site and blogging

### Build the site

```
bundle install
bundle exec jekyll serve
```

In case of any issue,

```sh
export LDFLAGS="-L/usr/local/opt/libffi/lib" && \
export PKG_CONFIG_PATH="/usr/local/opt/libffi/lib/pkgconfig" && \
bundle install
```