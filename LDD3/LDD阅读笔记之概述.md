LDD3阅读笔记-概述
===============
[TOC]

在编写驱动程序时，程序员应该特别注意下面这个基本概念：编写访问硬件的
内核代码时，不要给用户强加任何特定策略。

    不带策略的驱动程序包括一些典型的特征：同时支持同步和异步操作、驱动
    程序能够被多次打开、充分利用硬件特性，以及不具备用来”简化任务“的或
    提供与策略相关的软件层等。不带策略是软件设计者的一个共同目标。

#内核功能划分

- 进程管理
- 内存管理
- 文件系统
- 设备控制
- 网络功能

![内核功能划分][1]

#可装载模块

Linux内核支持好几种模块类型（或者类），包括但不限于设备驱动程序。

Linux将设备分成三种类型：

- 字符设备
- 块设备
- 网络接口


#用户空间和内核空间

CPU拥有不同的操作级别，Unix利用这个特性，使用了这样两个级别。当处理器
存在多个级别时，Unix使用最高级别和最低级别。内核运行在最高级别。我们通
常将运行模式称作内核空间和用户空间。这两个术语不仅说明两种模式具有不同
的优先级等级,而且还有自己的内存映射。

每当应用程序执行系统调用或被硬件中断挂起，Unix将执行模式从用户空间切
换到内核空间。执行系统调用的代码运行在进程上下文中，代表进程执行操作，
而处理硬件中断的内核代码是异步的，**与任何一个特定进程无关**。

模块化代码在内核空间中运行，通常来讲，一个驱动程序要执行先前讲述过的两
类任务：模块中的某些函数作为系统调用的一部分执行，而其他负责中断处理。

#内核中的并发

Linux内核代码（包括驱动程序代码）必须是可重入的，它必须能过同时运行
在多个上下文中。

#当前进程

current是一个指向struct task_struct的指针，指向当前正在运行的进程。
如果需要，内核代码可以通过current获得与当前进程相关的信息。

实际上，与早期Linux内核版本不同，2.6中的current不再是一个全局变量。
为了支持SMP系统，内核开发者设计列一种能找到运行在相关cpu上的当前进程
的机制。这样，一种不依赖与特定架构的机制通常是，将指向task_struct结构
的指针隐藏在内核栈中。这种实现的细节同样也对其他内核子系统隐藏，设备驱
动系统只要包含<linux/sched.h>头文件即可引用当前进程。

```c
printk(KERN_INFO "The process is \"%s\" (pid %i)\n",
        current->comm, current-pid);
```

#其他细节

应用程序在虚拟内存中布局，具有很大的一块栈，但是内核只有非常小的栈，它
可能只和一个4096字节大小的页那样小。我们自己的函数必须和整个内核空间
**调用链**一同共享这个栈。因此，如果我们需要大的结构，应该在调用是动态
分配。

内核API中具有两个下划线前缀(__)的函数通常是接口的底层组件，应谨慎使用。

内核代码不能实现浮点数运算。

##编译模块
>详细信息见Linux Kernel Hacking之Building External Modules。

```shell
Example:
--> filename: Kbuild
obj-m  := 8123.o
8123-y := 8123_if.o 8123_pci.o 8123_bin.o

--> filename: Makefile
ifneq ($(KERNELRELEASE),)
# kbuild part of makefile
include Kbuild

else
# normal makefile
KDIR ?= /lib/modules/`uname -r`/build

default:
    $(MAKE) -C $(KDIR) M=$$PWD

# Module specific targets
genbin:
    echo "X" > 8123_bin.o_shipped

endif
```

##装载和卸载模块

Command:

- insmod 装载模块，不自动解决依赖
- modprobe 和insmod类似，自动解决依赖
- rmmod 卸载模块

自动加载机制：

    kmod是一个用户空间守护进程，内核依赖它使用内核函数来添加模块。

##版本依赖

缺少modversions的情况下，我们的模块要针对链接的每个版本的内核重新
编译。

内核不会假定一个给定的模块是针对正确的内核版本构造的。我们在**构造过程**
中可以将自己的模块和当前内核树中的一个文件（即vermagic.o）链接；该目标
文件包含大量有关内核信息，包括目标内核版本、编译器版本以及一些重要
配置变量的设置。在**试图装载模块**时，这些信息可以用来检查模块的兼容性。

```shell
#insmod hello.ko
Error insert './hello.ko': -1 Invaild module format
```
查看系统日志文件（/var/log/messages或系统配置使用的文件），将看到导致
装载失败的具体原因。

##内核符号表

insmod使用公共内核符号表来解析模块中未定义的符号。公共内核符号表包含
了所有的全局内核项（即函数和变量）的地址，这是实现模块化驱动程序所必须
的。当模块被装入内核，它所导出的任何符号都会变成内核符号表的一部分。

新模块可以使用我们自己导出的符号，这样我们可以在其他模块上层叠新模块。

![并口层叠驱动][2]

    modprobe是处理层叠模块的一个实用工具。

如果一个模块需要向其他模块到处符号，则应该使用下面的宏。

```c
EXPORT_SYMBOL(name);
EXPORT_SYMBOL_GPL(name);
```

##模块的二进制结构

模块使用ELF二进制格式，模块包含了几个而外的段，普通程序或库中不会出现。

- __ksymtab __ksymtab_gpl和 __ksymtab_gpl_future段包含一个符号表，
  包括了模块导出的所有符号。
- __kcrctab __kcrctab_gpl和 __kcrctab_gpl_future包含模块所有导出
  函数的校验和。（除非内核配置启用了版本控制特性，否则不会建立上述段）。

#预备知识

所有的模块都要包含以下代码：
```c
#include <linux/module.h>
#include <linux/init.h>
```

尽管不是严格要求的，但是模块应该指定代码所使用的许可证
```c
MODULE_LICENSE("GPL");
```

>注：内核能识别的许可证包括“GPL”、“GPL v2”等。

其他还能在模块中包含的信息有MODULE_AUTHOR， MODULE_DESCRIPTON，
MODULE_VERSION，MODULE_ALIAS以及MODULE_DEVICE_TABLE。

>注：这些信息通过__attribute__关键字存储在模块特殊段里。

##初始化和关闭

```c
static int __init initialization_function(void)
{
    /*there is init code*/
}
module_init(initialization_function);
```
__init和 __initdata的使用是可选的，虽然有点繁琐，但是是值得的，可以
提示内核这是初始化函数。在内核代码中还可能遇到__devinit和 __devinitdata
，只有未被配置为支持热插拔设备的情况下，这两个标记才会被翻译为__init和
__initdata。

##清除函数

```c
static void __exit clean_function(void){}
module_exit(cleanup_funcfion);
```

清除函数没有返回值，__exit修饰词标记该代码仅用于模块卸载（编译器将把
该函数放在特殊的ELF段中）。如果模块不允许卸载，则__exit的函数会被简单
的丢弃。

>注：如果模块未声明清除函数，则该模块不允许卸载。

##初始化过程中的错误处理

模块代码必须始终检查返回值，并确保所请求的操作已真正成功。如果在注册
设施时遇到任何错误，首先要判断模块是否可以继续初始化。如果无法继续装载
，则要回滚操作，将之前任何注册工作撤销掉。

##模块装载竞争

始终需要铭记：在注册完成之后，内核的某些部分可能会立即使用我们刚刚注册
的任何设施。因此，在首次注册完成之后，代码就应该准备好被内核的其他部分
调用；在用来支持某个设施的所有内部初始化完成之前，不要注册任何设施。

还必须考虑当初始化失败而内核的某些部分已经使用了某块所注册的某个设施
时应该如何处理。

##模块参数

```c
static char *whom = "world"
static int howmany = 1;
module_param(howmany, int, S_IRUGO);
module_param(whom, charp, S_IRUGO);
```

```shell
insmod hellop howmany=10 whom="Mom"
```

>注：S_IRUGO任何人可以从/sys/module读取参数，但是不能修改。

#用户空间编写驱动

用户空间驱动程序优点如下

- 可以和整个C库链接
- 可以使用通常的调试器调试驱动程序代码。
- 如果用户空间驱动程序被挂起，则简单杀死它就行了。
- 和内核内存不同，用户内存可以换出。
- 良好设计的驱动程序仍然支持对设备的并发支持。
- 如果编写闭源驱动，用户空间驱动更加容易避免因为修改内核接口而导致
  不明确的许可问题。

>例如USB驱动程序可以在用户空间编写；具体可参考libusb项目。

用户空间驱动还有以下缺点：

- 中断在用户空间中不可用。
- 只有通过mmap映射/dev/mem才能直接访问内存，但只有特权用户可以执行。
- 只有在调用ioperm或iopl后才能访问I/O端口。
- 响应时间慢。
- 如果驱动程序被换出内存，响应时间慢的难以忍受。
- 用户空间不能处理一些非常重要的设备。

>有一种情况适合在用户空间中处理，这就是当我们准备处理一种新的、
 不常见的硬件时，在用户空间研究如何管理这个设备而不用担心挂起
 整个设备。

[1]: image/a_split_view_of_the_kernel.png
[2]: image/stacking_of_parallel_port_driver_modules.png