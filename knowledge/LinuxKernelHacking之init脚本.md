rc.d自启动学习
=============
[TOC]

linux有一套自己的完整启动流程。
本文假设inittab中设置的init tree为：
    
         /etc
           |--rc.d
               |--rc0.d
               |--rc1.d
               |--rc2.d
               |--rc3.d
               |--rc4.d
               |--rc5.d
               |--rc6.d
               |--init.d

#简单开机流程
1. 加载 BIOS 的硬件信息，并取得第一个开机装置的代号；
2. 读取第一个开机装置的 MBR 的 boot Loader (亦即是 lilo, grub, spfdisk 等等)
   的开机信息；
3. 加载 Kernel 操作系统核心信息， Kernel 开始解压缩，并且尝试驱动所有硬件装置；
4. Kernel 执行 init 程序并取得 run-level 信息；
5. init 执行 /etc/rc.d/rc.sysinit 档案；
6. 启动核心的外挂模块 (/etc/modprobe.conf)；
7. init 执行 run-level 的各个批次档( Scripts )；
8. init 执行 /etc/rc.d/rc.local 档案；
9. 执行 /bin/login 程序，并等待使用者登入；
10. 登入之后开始以 Shell 控管主机。

#init启动
init是系统启动的第二个进程，负责系统的初始化工作。
init读取/etc/inittab，执行rc.sysinit脚本.
>注意：文件名不是一定的，有些unix甚至会将语句直接卸载inittab中

rc.sysinit脚本做了很多工作：

- init $PATH
- config network
- start swap functon
- set hostname
- check root filesystem, repair if needed
- check root space
……

rc.sysinit根据inittab中的设置执行rc?.d脚本。
linux是多用户系统，getty是多用户与单用户的分水岭，在getty之前运行的是系统脚本。
##init的六个级别介绍
    0：停机
    1：单用户形式，只root进行维护
    2：多用户，不能使用net file system
    3：完全多用户
    5：图形化
    6：重启

##关于rc.d
所有启动脚本放置在/etc/rc.d/init.d下，rc?.d中放置的是init.d中脚本的链接，
命名格式是：

    S{number}{name}
    K{number}{name}

S开始的文件向脚本传递start参数；
K开始的文件向脚本传递stop参数；
num决定执行的顺序。

##启动脚本实例
这是一个用来启动httpd的/etc/rc.d/init.d/apache脚本：

    #!/bin/bash
    ……

它接受start，stop，restart，status参数，然后建立rc?.d的链接：

    cd /etc/rc.d/init.d&&
    ln -sf ../init.d/apache ../rc0.d/K28apache&&
    ln -sf ../init.d/apache ../rc1.d/K28apache&&
    ln -sf ../init.d/apache ../rc2.d/K28apache&&
    ln -sf ../init.d/apache ../rc3.d/S32apache&&
    ln -sf ../init.d/apache ../rc4.d/S32apache&&
    ln -sf ../init.d/apache ../rc5.d/S32apache&&
    ln -sf ../init.d/apache ../rc6.d/K28apache

##关于rc.local
经常使用的rc.local则完全是习惯问题，不是标准。各个发行版有不同的实现方法，
可以这样实现：

    touch /etc/rc.d/rc.local
    chmod +x /etc/rc.d/rc.local
    ln -sf /etc/rc.d/rc.local /etc/rc.d/rc1.d/S999rc.local &&
    ln -sf /etc/rc.d/rc.local /etc/rc.d/rc2.d/S999rc.local &&
    ln -sf /etc/rc.d/rc.local /etc/rc.d/rc3.d/S999rc.local &&
    ln -sf /etc/rc.d/rc.local /etc/rc.d/rc4.d/S999rc.local &&
    ln -sf /etc/rc.d/rc.local /etc/rc.d/rc5.d/S999rc.local &&
    ln -sf /etc/rc.d/rc.local /etc/rc.d/rc6.d/S999rc.local

#bash启动脚本

- /etc/profile
- /etc/bashrc
- ~/.bash_profile
- ~/.bashrc

以上几个是bash启动脚本，一般用来设置单用户的启动环境，也可以实现开机单用户
的程序，但要明确它们都是属于bash范畴而不是系统范畴。
具体作用介绍如下：

- /etc/profile和~/.bash_profile是在启动一个交互登录shell的时候被调用。
- /etc/bashrc和~/.bashrc是在启动一个交互非登录shell启动时被调用。
- ~/.bash_logout在用户注销登录的时候被读取。

一个交互的登录shell会在/bin/login成功登录后运行。一个交互的非登录shell是
通过简单的命令行来运行，如/bin/bash。一般一个非交互的shell出现在运行shell
脚本的时候，因为不需要等待输入只是执行脚本程序。

#开机程序的自动启动
系统脚本可以放在/etc/rc.d/init.d中并建立/etc/rc.d/rc?.d链接，也可以直接放
置在rc.local中。
init.d脚本包含完整的start，stop，status，reload等参数，是标准做法。
为特定用户使用的程序放置在~/中的bash启动脚本中。

设置系统自动启动，在/etc/init.d/下创建smsafe文件

    #!/bin/bash
    # chkconfig: 35 95 1
    # description: script to start/stop smsafe
    case 1instart)sh/opt/startsms.sh;;stop)sh/opt/stopsms.sh;;∗)echo"Usage:0 (start|stop)"
    ;;
    esac

更改权限

    # chmod 775 smsafe
加入自动启动

    # chkconfig –add smsafe
查看自动启动设置

    # chkconfig –list smsafe
    smsafe 0:off 1:off 2:off 3:on 4:off 5:on 6:off
以后可以用以下命令启动和停止脚本

    # service smsafe start 启动
    # service smsafe stop 停止


#补充
##登录提示信息

    /etc/motd
通过修改该文件可以显示登录提示信息。