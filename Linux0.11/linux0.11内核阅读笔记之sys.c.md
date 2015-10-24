《Linux0.11内核完全注释》读书笔记之fork.c
----------------------------------------------
[TOC]

setuid()事实上同时设置了uid和euid通过setreuid()
```c
int sys_setuid(int uid)
{
	return sys_setreuid(uid, uid)
}

int sys_setreuid(int ruid, int euid)
{
	int old_ruid = current->uid;
	if(ruid>0){
		if((current->euid==ruid) ||       //Linux: Unprivileged users may only 
										  //set the real user ID to the real 
										  //user ID or the effective user ID.
										  //所以新的版本不能用euid设置uid
			(old_ruid == ruid) ||
			suser())					  
			current->uid = ruid;
	} 
	if(euid>0){
		if((old_ruid==euid) ||
			(current->euid==euid) ||
			suser())					  //没有suid?
			current->euid =euid;
		else{
			current->uid = old_ruid;	  //如果euid设置不成功，则回滚uid
			return(-EPERM);
		}
	}
	return 0;
}
```
>**注意：**这里的setuid中root用户无法改变id，而新的实现可以。

setgid的实现也类似，不过setregid不允许把egid设置到gid上。

```c
int sys_setgid(int gid)
{
	return(sys_setregid(gid, gid));
}

int sys_setregid(int rgid, int egid)
{
	if(rgid>0){
		if((current->gid == rgid)||
			suser())
			current->gid = rgid;
		else
			return(-EPERM);
	}
	if(egid>0){
		if((current->gid == egid)||
			(current->egid) ||
			(current->sgid == egid) ||
			suser())
				current->egid = egid;
		else
			return(-EPERM);
	}
	return 0;
}
```
>**注意：** uid和euid只能在进程内设置，不能设置其他人的。当fork()时进程
复制了uid和euid，执行execve()时确定是否改变euid。因此用sudo命令运行程序
时，先fork()，子进程的uid和euid都被设置成0，然后execve()，euid可能会因
程序文件的set-uid-ID改变。