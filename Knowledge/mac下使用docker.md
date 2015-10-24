Mac下使用docker
===============
[英文官方安装指南](https://docs.docker.com/installation/mac/)

Docker是当下十分火的一向技术，Docker使用了Linux-specific内核特定，所以在Mac OS X无法直接本地运行。但是可以通过安装Boot2Docker application实现。Boot2Docker包含了Virtual Box VM,Docker和Boot2Docker管理工具。

在Mac上运行Docker需要一台虚拟机的帮助，Docker Client运行在本地，Docker Daemon运行在虚拟机中，Boot2Docker作为一个管理工具在本地运行。

#安装Boot2Docker
最简便的方式就是直接用brew安装，自动解决依赖。

```
$ brew install boot2docker
```

>Note: 安装过程中需要安装go语言包，这个包需要翻墙才能安装。

#初始化docker

```
$ boot2docker init
$ boot2docker start
$ $(boot2docker shellinit)
```

#测试docker

```
$ docker run hello-world
```
如果一切正常，那么docker的简单安装就完成了，docker的具体使用可以参考官网文档或
[私活利器，docker快速部署node.js应用](https://cnodejs.org/topic/53f494d9bbdaa79d519c9a4a)

#排错
如果出现如：error in run: Failed to get machine "boot2docker-vm": machine does not exist之类的错误，可以使用

```
$ boot2docker -v info
$ sudo boot2docker -v info   #第一个命令不行再使用
```  
根据得到的环境变量判断Virtual Box的设置可能存在的问题，调整Virtual Box的设置，然后重装boot2docker，这是目前比较有效的解决方案。

