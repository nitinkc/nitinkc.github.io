# nitinkc.github.io

Clone the code, goto root directory.

Build site using default _config.yml file:

```sh
bundle install 

#Serve site at http://localhost:4000
bundle exec jekyll serve
```

```sh
#Deletes Jekyll generated old ./_site cache folder
bundle exec jekyll clean or 
rm -rf _site 

#Build site into ./_site
bundle exec jekyll build --trace --verbose
bundle exec jekyll build

#Build site as production, default is development
JEKYLL_ENV=production bundle exec jekyll build

#Build site into ./_site and for watch changes
bundle exec jekyll build --watch
```
 
[Text using Symbols](https://fsymbols.com/generators/encool/)

Liquid Templating Language. Add Font matter to the top of the page

---
# front matter tells Jekyll to process Liquid
---

To expand the main content to the right, filling the space of what is normally occupied by the table of contents. Add the following to a post or page’s YAML Front Matter:

classes: wide

sudo bundle install --path vendor/bundle 


added in default.html in navigation and in head.html in include
<!-- Added to allow font awesome icons -->
<script src="https://use.fontawesome.com/releases/v5.0.2/js/all.js"></script>   

kill running process occupying 
lsof -P | grep ':4000' | awk '{print $2}' | xargs kill -9

SiteMap : https://developers.google.com/search/docs/advanced/sitemaps/build-sitemap


pandoc -f docx -t markdown Buying\ a\ bigger\ machine.docx -o x.md  