udev文件系统和sysfs文件系统
========================
Linux按照功能对文件系统的目录结构进行了良好的规划。/dev 是设备文件的存放目录，devfs 和 udev 分别是Linux 2.4 和 Linux 2.6 生成设备文件节点的方法，前者运行于内核空间，后者运行于用户空间。

#devfs
devfs在2.4被引入，引入时被工程师给予高度评价，它的出现使得设备驱动程序能自主地管理它自己的设备文件。
devfs具有如下优点：
- 可以通过程序在设备初始化时在/dev 目录下创建设备文件，卸载设备时将它删除。
- 设备驱动程序可以指定设备名、所有者和权限位，用户控件程序仍可以修改所有者和权限位。
- 不再需要为设备驱动程序分配主设备号以及处理次设备号，在程序中可以直接给register_chrdev()传递0主设备号以获得下面这些函数来进行设备文件的创建和删除工作。

```c
/* 创建设备目录 */
devfs_handle_t devfs_mk_dir(devfs_handle_t dir, const char *name, void *info);
/* 创建设备文件 */
devfs_handle_t devfs_register(devfs_handle_t dir, const char *name, unsigned int flags, unsigned int major, unsigned int minor, umode_t mode, void *ops, void *info);
/* 撤销设备文件 */
void devfs_unregister(devfs_handle_t de);
```
在2.4的设备驱动编程中，分别在模块加载时和卸载时创建和撤销设备文件是普遍采用并大力推荐的好方法。

```c
static devfs_handlt_t devfs_handle;

static int __init xxx_init(void) {
	int ret;
	int i;
	/* 在内核中注册设备 */
	ret = register_chrdev(XXX_MAJOR, DEVICE_NAME, xxx_fops);
	if(ret<0) {
		printk(DEVICE_NAME "can't register major number\n");
		return ret;
	}
	/* 创建设备文件 */
	devfs_handle = devfs_register(NULL, DEVICE_NAME, DEVFS_FL_DEFAULT,
	XXX_MAJOR, 0, S_IFCHR|S_IRUSR|S_IWUSR, &xxx_fops, NULL);
	...
	printk(DEVICE_NAME " initialized\n");
	return 0;
}

static void __exit xxx_exit(void) {
	devfs_unregister(devfs_handle); /* 撤销设备文件 */
	unregister_chrdev(XXX_MAJOR, DEVICE_NAME); /* 注销设备 */
}
moudle_init(xxx_init);
module_exit(xxx_exit);
```
#udev
尽管devfs有这样和那样的优点，但是，在2.6中，devfs被认为是过时的方法，并被抛弃，udev取代了它。
有以下几点原因：
- devfs所做的工作被确信可以在用户态完成。
- devfs被加入内核之时，大家期望它的质量可以迎头赶上。
- devfs被发现了一些可修复和不可秀发的bug。
- 可修复bug已经修复，不可修复的相当长一段时间没有改观
- devfs的维护者和作者对它感到失望并且已经停止对代码的维护工作。
- 策略不能位于内核空间，linux设置中强调的一个基本观点是机制和策略分离。

udev完全在用户态工作，利用设备加入或移除时内核所发送的热插拔事件（hotplug event）来工作。在热插拔时，设备的详细信息会由内核输出到位于/sys 的 sysfs 文件系统。udev的设备命名策略、权限控制和事件处理都是在用户态下完成的。

devfs和udev的另一个显著区别在于：采用devfs，当访问一个并不存在的/dev 节点时，devfs 能自动加载对应的驱动，而udev不这样做，因为设计者认为Linux应该在设备被发现的时候加载驱动模块，而不是在它被访问的时候。

##mdev
mdev是udev的轻量级版本，常被用于嵌入式系统。

#sysfs和Linux设备模型
Linux2.6引入了sysfs文件系统，sysfs被看成是与proc、devfs和devpty同类型的文件系统，该文件系统是一个虚拟的文件系统，它可以产生一个包括所有硬件的层级视图，与提供进程的状态信息的proc文件系统十分类似。



