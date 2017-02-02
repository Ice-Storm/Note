Docker 常用命令
==============
# docker command line 
## tag

	#docker tag <id> <name>[:tag]

这个命令不是字面上的为 images 定义 tag，而是定义 name 和 tag。


# Dockerfile

## ENTRYPOINT
Docfile中的 ENTRYPOINT 和 CMD 不同。

ENTRYPOINT 表示每次进入都要执行的命令，是一个表示一个进入点，只有最后一个有效。每次开启 container，都要执行一遍 ENTRYPOINT。

在 docker 中命令行参数会被传给 ENTRYPOINT，如：

```shell
FROM ubuntu
ENTRYPOINT ["top", "-b"]
```

```shell
docker --rm -it top -H
＃ 实际命令就是 top -b -H
```

## CMD

CMD 也只能有一个，多个的情况下最后一个有效。CMD 作为容器的默认命令提供。

CMD 也可以为 ENTRYPOINT 提供参数，一般是可变动参数，用户如果不输入参数，那么就使用 CMD 中的参数，否则就使用用户输入的参数，如：

```shell
FROM ubuntu
ENTRYPOINT ["top", "-b"]
CMD ["-c"]
```
## WORKDIR

WORKDIR 表示当前的工作目录，会影响之后的所有命令。如果指定的目录不存在，系统会自动创建。

##VOLUME
VOLUME 命令一般用于一个动态环境，如服务器，可以把运行一段时间的容器保存成镜像，不包含VOLUME 里的数据，或者可以方便几个环境共享 VOLUME，不用运行时用命令创建，不用显式指定主机目录，只要运行时指定指定容器目录就可以共享。

### 数据共享
VOLUME 除了常用的和主机共享数据之外，还可以和其他容器共享数据。

如果要授权一个容器访问另一个容器的Volume，我们可以使用-volumes-from参数来执行docker run。

```shell
$ docker run -it -h NEWCONTAINER --volumes-from container-test debian /bin/bash
root@NEWCONTAINER:/# ls /data
test-file
root@NEWCONTAINER:/#
```

### 权限与许可
通常你需要设置Volume的权限或者为Volume初始化一些默认数据或者配置文件。要注意的关键点是，在Dockerfile的VOLUME指令后的任何东西都不能改变该Volume，比如：

```dockerfile
FROM debian:wheezy
RUN useradd foo
VOLUME /data
RUN touch /data/x
RUN chown -R foo:foo /data
```

该Docker file不能按预期那样运行，我们本来希望touch命令在镜像的文件系统上运行，但是实际上它是在一个临时容器的Volume上运行。

```dockerfile
# ubuntu-base
FROM ubuntu
RUN mkdir /myvol
RUN echo "hello world" > /myvol/greeting
VOLUME /myvol
```

```
FROM ubuntu-base
RUN echo "test" > /myvol/test
```

当执行 docker run 时， /myvol 下只有 greeting，没有 test，因为 VOLUME 有先后顺序，容器运行时挂载的是那一层的文件，在上面几层创建的文件都无法看到。

>Note: If any build steps change the data within the volume after it has been declared, those changes will be discarded.

如下所示方法可以正常工作：

```dockerfile
FROM debian:wheezy
RUN useradd foo
RUN mkdir /data && touch /data/x
RUN chown -R foo:foo /data
VOLUME /data
```

### 挂载
常见的挂载参数有两种：

```shell
$ docker run -it -v $(pwd) ubuntu bash
$ docker run -it -v $(pwd):/path/to/mount ubuntu bash
```

第一种方法是为容器内部添加一个卷，属于 root:root，其他人只读。
第二种方式挂载后目录权限改变，变成 1000:staff。




