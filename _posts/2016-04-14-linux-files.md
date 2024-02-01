---
title:  "Linux Files"
date:   2016-04-14 20:11:00
categories: ['Developer tools']
tags: ['Developer tools']
---

| Directory                       | Description
|:--------------------------------| :---
| /                               | Root
 | /boot                           | For Linux kernel and boot loader files.The kernel is a file called **vmlinuz**.
 | /etc                            | Configuration files (All **text files**).<br><br> **/etc/passwd** Here users are defined & essential information for each user is kept like username, password (**Encrypetd & stored in shadow**), group id, userid, user id info, home directory, command shell etc... .<br> Password is stored in `/etc/shadow` file not in `/etc/passwd` <br> **/etc/fstab** table of devices that get mounted when your system boots. defines your disk drives.<br> **/etc/hosts** Lists the network host names and IP addresses that are intrinsically known to the system. <br> **/etc/init.d** This directory contains the scripts that start various system services at boot time.
 | /bin <br>/usr/bin               | contains most of the executable programs for the system. /bin : system requires to operate, /usr/bin contains applications for the system's users.
 | /sbin<br> /usr/sbin             | Executables for system administration by the superuser.
 | /usr                            | Things that support user applications <br> **/usr/share/X11** Support files for the X Windows system<br> **/usr/share/dict** Dictionaries for the spelling checker. Ckeck `look` and `ispell`.<br>**/usr/share/doc** documentation files in a variety of formats.<br>**/usr/share/man** Place for man pages.<br> **/usr/src** Source code files.(if kernel source code package is installed)
 | /usr/local<br> /usr/local/bin   | Used for the installation of software for local machine.
 | /var                            | Files that change as the system is running. <br> **/var/log** log files updated as the system runs. <br> **/var/spool** This directory is used to hold files that are queued for some process, such as mail messages and print jobs. Eg: local email is first stored in `/var/spool/mail`
 | /lib                            | shared libraries (like .dll in Windows)
 | /dev                            | Devices (as files) that are available to the system. /dev/sda (/dev/hda on older systems) is the first IDE hard drive.
 | /proc                           | processes running on the system.  Many of these entries can be viewed. Eg. `/proc/cpuinfo`. This entry will tell you what the kernel thinks of your CPU.
 | /media <br> /mnt                |  The /media directory is used for mount points. This process of attaching (*devices attached to the file system tree in various places*) a device to the tree is called **mounting**. For a device to be available, it must first be mounted. <br><br>When your system boots, it reads a list of mounting instructions in the file /etc/fstab, which describes which device is mounted at which mount point in the directory tree. This takes care of the hard drives, but you may also have devices that are considered temporary, such as CD-ROMs and floppy disks. Since these are removable, they do not stay mounted all the time. The /media directory is used by the automatic device mounting mechanisms found in modern desktop oriented Linux distributions. <br><br>On systems that require manual mounting of removable devices, the **/mnt** directory provides a convenient place for **mounting these temporary devices**. You will often see the directories /mnt/floppy and /mnt/cdrom. To see what devices and mount points are used, type mount.
|