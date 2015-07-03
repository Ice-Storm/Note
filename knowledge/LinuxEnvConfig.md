Linux Enviroment Configure
==========================
［TOC］

＃yum
yum是一个包管理系统，和apt-get类似，但是包的名字和apt-get的有点不同，当不知道需要的包的名字的时候，可以使用

    yum provides ［command name］ 或
    yum whatprovides ［command name］

＃ifconfig
最小化安装centos 7后没有ifconfig，可以使用替代命令：
    
    ip addr
    ip link

如果要安装ifconfig，使用

    yum provides ifconfig 或
    yum whatprovides ifconfig

获得软件包名字**net-tools**，然后使用yum安装。

＃systemctl
systemctl是一个新的机制，用来代替原来的initrc机制。

