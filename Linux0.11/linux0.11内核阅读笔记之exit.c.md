《Linux0.11内核完全注释》读书笔记之exit.c
----------------------------------------------
[TOC]

```c
int sys_waitpid(pid_t pid, unsigned long *stat_addr, int options)
{
	int flag, code; 			//flag标志用于后面表示所选出的子进程处于就绪或睡眠
	struct task_struct **p;

	verify_area(stat_addr, 4);
repeat:
	flag=0;
	for(){	//扫描任务
		...
	}
	if(flag){                   //表示找到的进程正在运行或睡眠
		if(options&WNOHANG)		//若options = WNOHANG，则立即返回
			return 0;
		current->state=TASK_INTERRUPTIBLE;
		schedule();
		if(!(current->signal &= ~(1<<(SIGCHLD-1))))
			goto repeat;
		else
			return -EINTR;     //返回出错码（中断的系统调用）
							   //为什么不repeat？
	}
	return -ECHILD；           //没有找到符合的子进程
}
```