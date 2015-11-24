《Linux0.11内核完全注释》读书笔记之系统执行框架图
----------------------------------------------
[TOC]

#信号处理方式

```flow
t_i=>start: _time_interrupt
ret=>end: return
d_t=>condition: do_timer, 
				current has time left?
r_f_s_c=>operation: ret_from_sys_call
d_s=>operation: do_signal

con=>condition: time_count
ret2=>end: return
sch=>operation: schedule
t_i->d_t
d_t(no)->sch
d_t(yes)->r_f_s_c
r_f_s_c->d_s->ret
```

```flow
int=>start: int 0x80
r_f=>end: ret_from_sys_call
s_c=>operation: _system_call
sys_xx=>operation: sys_xx
judge=>condition: need reschedule?
resch=>operation: reschedule

int->s_c->sys_xx->judge
judge(no)->r_f
judge(yes)->resch->r_f
```

```flow
do_sig=>start: do_signal
ret=>operation: return to user mode
sig_h=>operation: signal_handler
restore=>operation: restore()
					recover register and env for user
user=>end: user program

do_sig->ret->sig_h->restore->user
```

>**注意** 当程序从do_signal返回后，先从内核堆栈弹出返回地址跳到信号处理函数处
执行，当从信号处理函数返回时从用户栈弹出之前设置的restore()地址，对环境进行清理，
最后返回到用户程序时就像什么都没发生。
进程间状态还原有TSS实现，进程内进行过信号处理后的现场还原由restore函数实现。，主
要负责寄存器和信号掩码的复原。