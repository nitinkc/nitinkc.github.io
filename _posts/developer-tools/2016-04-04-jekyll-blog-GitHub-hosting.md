---
title:  "Jekyll Blog and Free Hosting on GitHub!"
date:   2016-04-04 18:31:00
categories: ['Developer tools']
tags: ['Developer tools']
sidebar:
  nav: "algo"
---

{% include toc title="Index" %}

Making a personal website using GitHub's free Hosting for the Jekyll Sites
Create a blog with naming convention of yyyy-mm-dd-name-of-the-blog.md and save it in \_posts directory

On a new machine (mac) use this link

[Install Jekyll](https://jekyllrb.com/docs/installation/)

execute in the terminal

> [!NOTE]
> If not using the gem File

```sh
bundle exec jekyll build
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