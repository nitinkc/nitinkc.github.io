# Add multiple remote Repo
git remote add bb https://nitinc@bitbucket.org/nitinc/git-tests-bb.git
git remote add gh https://github.com/nitinkc/git-tests.git

## Apply actions
git remote set-url --push gh https://github.com/nitinkc/git-tests.git
git remote set-url --push bb https://bitbucket.davita.com/scm/\~nichaurasia/design-patterns.git

```editorconfig
[core]
repositoryformatversion = 0
filemode = true
bare = false
logallrefupdates = true
ignorecase = true
precomposeunicode = true
[remote "origin"]
url = https://github.com/nitinkc/git-tests.git
fetch = +refs/heads/*:refs/remotes/origin/*
pushurl = https://github.com/nitinkc/git-tests.git
[branch "main"]
remote = origin # both #Goes to pushing both
merge = refs/heads/main
[remote "bb"]
url = https://nitinc@bitbucket.org/nitinc/git-tests-bb.git
fetch = +refs/heads/*:refs/remotes/bb/*
pushurl = https://nitinc@bitbucket.org/nitinc/git-tests-bb.git
[remote "gh"]
url = https://github.com/nitinkc/git-tests.git
fetch = +refs/heads/*:refs/remotes/gh/*
pushurl = https://github.com/nitinkc/git-tests.git
[remote "both"]
url = https://github.com/nitinkc/git-tests.git
url = https://nitinc@bitbucket.org/nitinc/git-tests-bb.git
fetch = +refs/heads/*:refs/remotes/origin/*
pushurl = https://github.com/nitinkc/git-tests.git
pushurl = https://nitinc@bitbucket.org/nitinc/git-tests-bb.git

[user]
name = nitin
email = gs.nitin@gmail.com
[pull]
rebase = false

```


```shell
git pull gh
git pull bb

git fetch gh
git fetch bb

git merge origin/main
git merge bb/main
git merge gh/main

git push bb main
git push gh main
```


## Scenario 1

```shell
create a new branch <feature/git-squash-commit-test>

# Sets the default repo to BitBucket
git push --set-upstream bb feature/git-squash-commit-test

# After some commits 
git push #takes the changes to bb
pit push 
```

# Logs
```log
❯ git push
Enumerating objects: 5, done.                                                                                    ─╯
Counting objects: 100% (5/5), done.
Delta compression using up to 16 threads
Compressing objects: 100% (3/3), done.
Writing objects: 100% (3/3), 280 bytes | 280.00 KiB/s, done.
Total 3 (delta 2), reused 0 (delta 0), pack-reused 0
remote: Resolving deltas: 100% (2/2), completed with 2 local objects.
To https://github.com/nitinkc/git-tests.git
   86870ce..85d75b5  main -> main
Enumerating objects: 5, done.
Counting objects: 100% (5/5), done.
Delta compression using up to 16 threads
Compressing objects: 100% (3/3), done.
Writing objects: 100% (3/3), 280 bytes | 280.00 KiB/s, done.
Total 3 (delta 2), reused 0 (delta 0), pack-reused 0
To https://bitbucket.org/nitinc/git-tests-bb.git
   86870ce..85d75b5  main -> main
╭─░▒▓    ~/Downloads/git-tests ─
```