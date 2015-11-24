Configure Nginx
===============
[TOC]

#Nginx虚拟主机配置
虚拟主机使用特殊的软硬件技术，它把一台服务器分成多台虚拟的主机，每台虚拟主机可以是一个独立的网站，可以具有独立的域名，具有完整的Internet服务器功能（WWW、FTP、Email等），从网站访问者角度看，每台虚拟主机和一台独立主机完全一样。

利用虚拟主机，不用为每个要运行的网站提供一台单独的Nginx服务器或单独运行一组Nginx进程。虚拟主机提供了在同一台服务器、同一组Nginx进程上运行多个网站的功能。

一个简化的Nginx虚拟主机配置文件如下：
    
    http {
        server {
            listen 80 default;
            server_name _ *;
            access_log  logs/default.access.log combined;
            location / {
                index   index.html;
                root    /data0/htdocs/htdocs;
            }
        }
    }

跟Apache一样，Nginx可以配置多种类型的虚拟主机：
- 基于IP的虚拟主机
- 基于域名的虚拟主机
- 基于端口的虚拟主机

##配置基于IP的虚拟主机
Linux、FreeBSD都允许添加IP别名。IP别名背后的概念很简单：可以在一块物理网卡上绑定多个IP地址。这样就能够在使用单一网卡的同一个服务器上运行多个基于IP的虚拟主机。设置IP别名也很容易，只须配置系统上的网络接口，让它监听额外的IP地址。在Linux系统上，可以使用标准的网络配置工具：

    #ifconfig eth0:1 192.168.1.1
    #route add -host 192.168.1.1 dev eth0:1
    #ifconfig eth0:2 192.168.1.2
    #route add -host 192.168.1.2 dev eth0:2

这时在eth0网卡设备上添加了两个IP别名192.168.1.1和192.168.1.2。
使用ifconfig命令可以查看该服务器的IP地址，其中有eth0、eth0:1、eth0:2、lo。本地回环lo的IP地址为127.0.0.1。

删除IP别名：

    #ifconfig eth0:1 down
    #ifconfig eth0:2 down

>注意：本地回环代表设备的本地虚拟接口，主要作用有两个：一是测试本机的网络配置，能PING通127.0.0.1说明本机网卡和IP协议安装都没有问题。另一个是把本地作为server运行时可以连接该IP。

该IP别名会在系统重新后消失，如果要长期使用，可以在rc.local中添加配置命令。

接下来基于两个IP别名配置Nginx配置文件，提供纯静态HTML支持的虚拟主机：

    http {
        #第一个
        server {
            #监听的IP和端口
            listen      192.168.1.1:80；
            #主机名称
            server_name 192.168.1.1;
            #访问日志文件存放路径
            access_log  logs/server1.access.log     combined;
            location / {
                #默认首页文件，顺序从左到右，如果找不到index.html文件，则找index.htm
                index index.html index.htm;
                #HTML网页文件存放的目录
                root /data0/htdocs/server1;
            }
        }
        #第二个
        server {
            listen      192.168.1.2:80;
            server_name 192.168.1.2;
            access_log  logs/server3.access.log combined;
            location /{
                index index.html index.htm;
                root  /data0/htdocs/server3.com;
            }
        }
    }

一段server{...}对应一个虚拟主机。监听IP和端口也可以不写IP，写成“listen 80”，则表示监听服务器上所有IP，可通过server_name区分不同的虚拟主机。

#配置基于域名的虚拟主机
基于域名的虚拟主机是最常见的一种虚拟主机。只需要配置你的DNS服务器，将每个主机名映射到正确的IP地址，

#Nginx的信号控制
* TERM,INT 快速关闭
* QUIT 从容关闭
* HUP 平滑重启，重新加载配置文件
* USR1 重新打开日志文件，在切割日志时用途较大
* USR2 平滑升级可执行程序
* WINCH 从容关闭工作进程