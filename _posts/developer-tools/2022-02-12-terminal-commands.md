---
# layout: static
title:  "Terminal Commands"
date:   2022-02-12 23:23:00
categories: ['Developer tools']
tags: ['Developer tools']
---
{% include toc title="Index" %}


## Apply settings

After making changes to `.zshrc` apply the changes to iTerm (which uses zsh).

```sh
exec zsh
```

exa instead of ls `brew install exa`
adds a few extra alias
```sh
if [ -x "$(command -v exa)" ]; then
    alias ls="exa"
    alias la="exa --long --all --group"
fi
```
Matrix Screen saver for terminal
```sh
cmatrix
cmatrix -c
```

## Folder Related

Creating folders

``` mkdir -p dir1/dir2/dir3 ``` creation of a whole hierarchy of folders in one step

``` rm -rf MyStuff``` Deleting a folder

``` rm foo bar "New Folder" ``` Deleting multiple files. 

## File and folder management

* chown ("change owner") - to change the owner of a file or folder
* chmod ("change mode") - to change the permissions of a file or folder
* ln ("link") - to make a link to a file or folder
* find - to search the filesystem for files or folders matching given criteria
* mdfind - to search for files or folders using the "Spotlight" meta-data
* locate - to see where certain files are located (uses a database that is updated periodically)
* du ("disk usage") - to show the amount of disk space used by a file or folder

## File content
* more - to display the contents of a file page by page (press Return to go down one line, press * space to go down one page)
* cat ("concatenate") - to display the full contents of a file or to concatenate two or more files * into one
* head - to display the first part of a file
* tail - to display the last part of a file
* mdls - display the meta-data for a file
* xattr - display the extended attributes for a file
* diff - to compare two text files (or, with the "-r" option, two folders)
* cmp - to compare two binary files
* grep ("global regular expression print") - to search inside a file for lines matching a given * pattern
* sed ("stream editor") - to modify the text that is streaming through a pipe
* sort - to sort the lines of text files
* uniq - to filter out repeated lines of text files
* fold - to wrap long lines of text files (useful when printing)
* hexdump - to show the contents of a file as hexadecimal numbers
* textutil - convert plain text to HTML or RTF (and vice versa)


## Network

To check internet speed
	○ Cmd + spaec (spotlight)
	○ Open Network utility

* Netstat
* Ping
* Lookup
* Traceroute
* Whois
* Finger
* Portscan

get default (Wifi router address). User wifi name and password to login into the wifi
```sh
netstat -nr | grep default OR 
route -n 
```

Finder From Terminal?
Opening a Finder window from Terminal
```sh
open . 
open /usr 
```

All Computers in the network

```
arp -a
```

* ```ifconfig``` ("interface configure") - to display and configure network interface parameters
* ping - to send a test packet to another computer (amusing article about the history of this * command)
* traceroute - to see the route taken by packets across a network
* host - to find out the IP address corresponding to a hostname or viceversa
* curl - to download contents of a document via a URL
* ftp - command-line FTP client
* ssh ("secure shell") - remote login to another computer

## OS Commands
Top
Kill -9

``` uptime ``` To check the time since last start

``` caffeinate -t 3600 ``` To stop mac from sleep

name of the OS/print hardware name

```sh
uname

uname -m
```
``` sudo Purge ``` Clear RAM

Find CPU related info

```sh
sysctl -n machdep.cpu.brand_string

system_profiler | grep Processor

sysctl -a | grep machdep.cpu

sysctl hw.cpufrequency # query the CPU speed
``` 


## Displaying Current Environment & Shell Variables in Mac OS X
get a list of environmental variables
```
printenv
```
complete list of shell variables, the ‘set’ command:
```
set 
```
To show a list including the "shell variables" you can enter the next command:
```
( set -o posix ; set ) | less
```
The output of these commands can be lengthy so you may wish to pipe the output through the less or more commands.

Bash History
```sh
history |grep "defaults"
```
Find out the shell
```sh
finger $USER
echo $0
echo $SHELL
```


'find' with 'xargs' command. xargs works on the result of the find command

```sh
find . -name "*.java" -print0 | xargs -0 wc
```

It's slightly trickier to use 'xargs' when the command you want to run takes other arguments and the list of files has to come before those other arguments. For example, if you wanted to copy all those ".java" files to a different folder, you'd want to use the 'cp' command. But it has the form:
cp file1 file2 file3 ... destinationFolder

To get 'xargs' to insert the list of files at a specified place in the command line, you use the "-J" option and supply your choice of placeholder - for example:
```sh
find . -name "*.java" -print0 | xargs -0 -J % cp % destinationFolder 
```

## Processes
* ps ("process status") - to see detailed info about the processes running
* top - to get a summary of the processes running and resource consumption
* kill - to terminate a process identified by process-id (or to send other signals)
* killall - to terminate a process identified by program name
* lsof ("list open files") - show which files (and sockets) are open by which program
* fs_usage ("filesystem usage") - show which programs are accessing (reading or writing) the * filesystem
* dtrace - trace any system activity (processes or file access). Start by reading 'man -k dtrace'

## System Info
* hostname - reports the name of your Mac
* sw_vers - reports the OS X version that you are using
* system_profiler - reports on the hardware and software that is on your Mac (i.e. a command-line * version of the "System Profiler" utility)
* sysctl -a - reports values of the kernel parameters
* Disk management
* df - shows info (including the amount of free space) about mounted disks
* diskutil - versatile disk management utility (info, formatting, mounting, repairing, etc)

## Misc
* date - to display the current date and time (in various formats)
* sleep - to pause execution for a given number of seconds (useful in scripts)
* wc ("word count") - to display the number of characters, words, and lines in a text file
* pbcopy ("pasteboard copy") - copy to the clipboard from "standard input"
* pbpaste ("pasteboard paste") - paste from the clipboard to "standard output"
* xargs - pass arguments to another command (useful in pipes)
* defaults - read or write preference settings
* id - report info about your user account (numeric user-id, group ids, etc)
* sudo ("superuser do") - execute a command with 'root' privileges
* su ("switch user") - start a new shell using a different user account
* man ("manual") - to display detailed information about a command.