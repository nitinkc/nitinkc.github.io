
git remote add github https://github.com/Suchismita-Deb/Java-Journey.git
git remote add bitbucket https://bitbucket.davita.com/scm/\~nichaurasia/design-patterns.git

git remote set-url --push github https://github.com/Suchismita-Deb/Java-Journey.git
git remote set-url --push bitbucket https://bitbucket.davita.com/scm/\~nichaurasia/design-patterns.git

```editorconfig

[core]
repositoryformatversion = 0
filemode = true
bare = false
logallrefupdates = true
ignorecase = true
precomposeunicode = true
[remote "origin"]
url = https://bitbucket.davita.com/scm/~nichaurasia/design-patterns.git
fetch = +refs/heads/*:refs/remotes/origin/*
pushurl = https://github.com/Suchismita-Deb/Java-Journey.git

[branch "main"]
remote = origin
merge = refs/heads/main
[remote "github"]
url = https://github.com/Suchismita-Deb/Java-Journey.git
fetch = +refs/heads/*:refs/remotes/github/*
pushurl = https://github.com/Suchismita-Deb/Java-Journey.git
[remote "bitbucket"]
url = https://bitbucket.davita.com/scm/~nichaurasia/design-patterns.git
fetch = +refs/heads/*:refs/remotes/bitbucket/*
pushurl = https://bitbucket.davita.com/scm/~nichaurasia/design-patterns.git


```


```shell
git pull github
git pull bitbucket

git fetch bitbucket
git fetch github

git merge origin/main
git merge bitbucket/main
git merge github/main

git push bitbucket main
git push bitbucket main
```