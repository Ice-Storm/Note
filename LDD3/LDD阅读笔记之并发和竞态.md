内核中的并发和竞态
=================
[TOC]

一般驱动程序运行在内核态中，只能调用内核空间中提供的函数，因此在处理并发和竞态时不能使用用户空间提供的库，如pthread库，内核有着自己的一套内部实现机制。

#并发及其管理
现代Linux系统中存在大量的并发来源，因此会导致可能的竞态。SMP系统甚至可能在不同的处理器上同时执行我们的代码。内核代码是可抢占的，因此，我们的驱动程序代码可能在任何时候丢失对处理器的独占，而拥有处理器的进程可能正在调用我们的驱动程序代码。设备中断是异步事件，也会导致代码的并发执行。内核还提供了很多可延迟代码执行的机制。比如

- workqueue（工作队列）
- tasklet（小任务）
- timer（定时器）

这些机制使得代码可以在任何时刻执行，而不管当前进程在做什么。在现代的热插拔世界中，设备可能会在我们正在使用时消失。

大部分竞态可通过使用内核的并发控制原语，并应用几个基本的原理来避免。

##竞态的产生
竞态通常作为对资源的共享访问结果而产生。当两个执行线程需要访问相同的数据结构（或硬件资源）时，混合的可能性就永远存在。因此在设计自己的驱动程序时，**第一个要记住的规则**是，只要可能，就应该****避免资源的共享**。如果没有并发的访问，也就不会有竞态的产生。

但是有时共享是必须的。硬件资源本质上就是共享的，而软件资源经常需要对其他执行线程可用。我们还要清楚，全局变量并不是共享数据的唯一途径，只要我们的代码将一个指针传递给了内核的其他部分，一个新的共享就可能建立。因此，**共享就是现实的生活**

##资源共享的硬规则
在单个执行线程职位共享硬件或软件资源的任何时候，因为另外一个线程可能产生对该资源的不一致观察，因此必须显示地管理对该资源的访问。
还有一个重要的规则，当内核代码创建了一个可能和其他内核部分共享的对象时，该对象必须在还有其他组件引用自己时保持存在（并正确工作）。

#信号量和互斥体
在计算机科学中，信号量是一个众所周知的概念。一个信号量本质上是一个整数值，它和一对函数联合使用，这一对函数通常称为P和V。希望进入临界区的进程将在相关信号量上调用P；如果信号量的值大于0，该值减一，进程继续。相反，进程等待其他人释放该信号量。对该信号量的解锁通过V完成；该函数增加信号量的值，并在必要时唤醒等待的进程。

当信号量用于互斥时，信号量初始化为1。Linux内核中几乎所有的信号量均用于互斥。

##Linux信号量的实现
Linux内核遵守上述语义提供了信号量的是实现，然而在术语上存在一些差异。要使用信号量，内核代码必须包括<asm/semaphore.h>。想关的类型是struct semaphore；实际的信号量可通过几种途径来声明和初始化。其中之一是直接创建信号量，这通过sema_init完成：

```c    
    void sema_init(struct semaphore, * sem, int val);
```

其中val是赋予一个信号量的初始值，不过信号量常被用于互斥模式，内核提供了辅助函数和宏。

```c
    DECLARE_MUTEX(name);
    DECLARE_MUTEX_LOCDED(naem);
```

一个称为name的信号量变量初始化为1（使用DECLARE_MUTEX）或者0（DECLARE_MUTEX_LOCKED）。

如果互斥体必须在运行时被初始化，应使用下面的函数之一：

```c
    void init_MUTEX(struct semaphore * sem);
    void init_MUTEX_LOCKED(struct semaphore * sem);
```

在Linux世界中，P函数被称为down——或者这个名字的其他变种。

```c
    void down(struct semaphore * sem);
    int down_interruptible(struct semaphore * sem);
    int down_trylock(struct semaphore * sem);
```

down减少信号量的值，并在必要时一直等待。down_interruptible完成相同工作，但是操作可中断。**可中断版本几乎是我们始终要使用的版本**，它允许等待在某个信号量上的用户空间进程 **可被用户中断**。非中断操作是建立不可杀进程(ps输出中的"D state")的好方法，但会让用户感到懊恼。使用可中断操作需要额外小心，如果操作被中断，该函数会返回0值，而调用这不会拥有该信号量。对down_interruptible的正确使用需要始终检查返回值，并作出相应的响应。

>注意：这里的interruptible指的是用户可以发信号中断，uninterrputible指的是用户不可以发信号中断，但是内核可以中断它，否则系统会死锁。

最后一个版本(down_trylock)**永远不会休眠**；如果信号量在调用时不可获得，会立即返回一个非零值。

当互斥操作完成后，必须返回信号量，Linux等价于V函数的操作时up:

```c
void up(struct semaphore * sem);
```

调用up后，调用者不再拥有该信号量。任何拿到信号量的线程都必须通过一次（只有一次）对up的调用而释放信号量。如果在拥有一个信号量时发生错误，必须在将错误状态返回给调用者之前释放。

##读取者/写入者信号量
信号量对所有的调用者执行互斥，而不管每个线程到想做什么。但是，许多人物可以划分为两种不同的工作类型：一些任务只需要读取受保护的数据，而其他的则必须做出修改。允许多个并发的读取者是可能的，只要它们之中没有哪个要做修改。这样做可以大大提高性能。

Linux内核为这种情况提供了一种特殊的信号量类型，称为"rwsem"（或者reader/writer semaphore）。在驱动程序中使用rwsem的机会比较少，但偶尔比较有用。

使用rwsem必须包含<linux/rwsem.h>。相关的数据类型是struct rw_semaphore；一个rwsem对象必须运行时通过下面的函数显式初始化：

    void init_rwsem(struct rw_semaphore * sem);

初始化的rwsem才可以使用。

```c
    void down_read(struct rw_semaphore * sem);
    int down_read_trylock(struct rw_semaphore * sem);
    void up_read(struct rw_semaphore * sem);
```

针对写入者的接口类似于读取者接口：

```c
    void down_write(struct rw_semaphore * sem);
    int down_write_trylock(struct rw_semaphore * sem);
    void up_write(struct rw_semahore * sem);
    void downgrade_write(struct rw_semaphore * sem);
```

当某个快速改变获得了写入者锁，而其后是更长时间的只读访问的话我们可以在结束修改之后调用downgrade_write，来允许其他读取者的访问。

一个rwsem可允许一个写入者或无限多个读取者拥有该信号量。写入者拥有更高的优先级；如果有大量的写入者竞争该信号量，这种实现会导致读取者“饿死”，即长期拒绝读取者的访问，因此最好在需要写访问很少且写入者只会短期拥有信号量的时候使用rwsem。

#completion
内核编程中常见的一种模式是，在当前线程之外初始化某个活动，然后等待该活动结束，在这种情况下，我们可以使用信号量同步这两个任务。

但信号量并不是适用这种情况最好工具。通常使用中，试图锁定某个信号量的代码会发现该信号量几乎重视可用；而如果存在针对该信号量的严重竞争，性能将会受到影响，这是我们需要重新审视锁定机制。

上述考虑导致内核中出现了“completion”接口。completion是一种轻量级的机制，它允许一个线程告诉另一个线程某个工作已经完成。代码必须包含<linux/completion.h>。可以利用下面的接口创建completion：

```c
    DECLARE_COMPLETION(my_completion);
```
如果要动态的创建和初始化completion，则使用下面的方法：

```c
    struct completion my_completion;
    init_completion(&my_completion);
```
要等待completion，可进行以下调用：

```c
    void wait_for_completion(struct completion * c);
```

该函数执行一个非中断调用，如果没人完成该任务，等待一直不返回，则将产生一个不可杀进程。wait_for_completion等待在completion上。如果加了interruptible，就表示线程等待可被外部发来的信号打断；如果加了killable，就表示线程只可被kill信号打断；如果加了timeout，表示等待超出一定时间会自动结束等待，timeout的单位是系统所用的时间片jiffies(多为1ms)。

另一方面，实际的completion事件可以通过调用下面函数之一来触发：

```c
    void complete(struct completion * c);
    void complete_all(struct completion * c);
```

completion只会唤醒一个等待线程，而complete_all允许唤醒所有等待线程。

一个completion通常是一个单次设备；也就是说，它只会被使用一次然后被丢弃。但是如果仔细处理，completion结构也可以被重复使用。

还有一个特殊的函数：

```c
    void complete_and_exit(struct completion * c, long retbval);
```

#自旋锁
信号量对互斥来讲是非常有用的工具，但它不是内核提供的唯一的这类工具。相反，大多数锁定通过称为“自旋锁(spinlock)”的机制实现。和信号量不同，自旋锁可在不能休眠的代码中使用，比如中断处理例程。在正常使用的情况下，自旋锁通常可以提供比信号量更高的性能。但是也带来了其他一组不同的使用限制。

在概念上，自旋锁非常简单。一个自旋锁是一个互斥设备，它只能有两个值，“锁定”和“解锁”。代码希望获得锁时，如果所被其他人锁定，则代码进入忙循环并重复检查这个锁，知道该锁可用为止。这个循环就是“自旋”部分。

自旋锁的真实实现更复杂一些，“测试并设置”的操作必须是原子的。在超线程处理器上还必须仔细处理避免死锁。因此，实际的自旋锁实现由于Linux所支持的架构不同而不同。

自旋锁最初是为了多处理器系统上设计的，如果非抢占式的单处理器系统进入某个锁上的自旋状态，则会永远自旋下去。出于对此原因考虑，非抢占是的单处理器系统上的自旋锁被有华为不做任何事情，但改变IRQ掩码状态的例程是个例外。

##自旋锁API介绍
自旋锁原语需要包含<linux/spinlock.h>。实际的所具有spinlock_t类型。使用前需要初始化，可以在编译时通过下面的代码静态初始化：

```c
    spinlock_t my_lock = SPIN_LOCK_INLOCKED;
```
或在运行时，调用下面的函数初始化：

```c
    void spin_lock_init(spinlock_t * lock);
```

在进入临界区之前，我们的代码必须调用下面的函数获得锁：

```c
    void spin_lock(spinlock_t * lock);
```

>注意：所有的自旋锁等待本质上都是不可中断的。一旦调用了spin_lock，在获得锁之前一直处于自旋状态。

释放已经获得的锁，可将锁传递给下面的函数：

```c
    void spin_unlock(spinlock_t * lock);
```

还有其他许多自旋锁函数。

##自旋锁和原子上下文
假定我们的驱动程序获得了一个自旋锁，然后在临界区内丢掉了处理器，这样，我们的代码见拥有这个自旋锁，并且在可预见的未来，它不会释放任何时间。如果其他某个线程试图获得相同的锁，在最好的情况下，该线程要等待（在处理器上自旋）很长时间。在最坏情况下，系统将整个进入死锁状态。

因此，适用于自旋锁的核心规则是：任何时候自旋锁的代码必须是原子的，它不能休眠，事实上，它不能因为任何原因放弃处理器，**除了服务中断以外（某些情况下此时也不能放弃处理器）**。

内核抢占的情况由自旋锁代码本省处理。任何时候，只要内核代码拥有自旋锁，在相关处理器上的抢占就会被禁止。甚至在单处理器上也是如此。

在拥有锁的时候避免休眠有时很难做到；许多内核函数可以休眠，而且此行为也始终没有文档来很好的说明。

还有一种情形：驱动程序正在执行，并且已经获得了一个锁，这个锁控制着设备访问，同时产生了一个中断，在中断调用例程中也要获得这个锁，这是合法的，但是在中断例程自旋时，非中断代码没有任何机会来释放这个锁，处理器会永远自旋下去。（异步信号安全）。

为了避免这种陷阱，我们需要在拥有自旋锁时禁止中断（仅在本地cpu上）。

自旋锁使用的最后一个重要的规则是，自旋锁必须在可能的最短时间内拥有。

##自旋锁函数
锁定一个自旋锁的函数实际有四个：

```c    
    void spin_lock(spinlock_t * lock);
    void spin_lock_irqsave(spinlock_t * lock, unsigned long flags);
    void spin_lock_irq(spinlock_t * lock);
    void spin_lock_bh(spinlock_t * lock);
```

spin_lock_irqsave会在获得自旋锁之前禁止中断（只在本地处理器上），而先前的中断保存在flags中。如果我们能确保在释放自旋锁时应启动中断，则可使用spin_lock_irq，最后，spin_lock_bh在获得锁之前禁止软件中断，但是会让硬件中断保持打开。

如果我们拥有一个自旋锁，它可被运行在（硬件或软件）中断上下文中的代码获得，则必须使用某个禁止东段的spin_lock形式，如果我们不会再硬件中断中访问自旋锁，但可能在软件中断中（例如，以tasklet的形式运行的代码）中访问，则应该使用spin_lock_bh，一变在安全避免死锁的同时还能服务硬件中断。

释放自旋锁的方式也有四种，和获取对应：

```c
    void spin_unlock(spinlock_t * lock);
    void spin_unlock_irqstore(spinlock_t * lock, unsigned lng flags); //？
    void spin_unlock_irq(spinlock_t * lock);
    void spin_unlock_bh(spinlock_t * lock);
```

>注意：我们必须在同一个函数中调用spin_lock

```
_irqsave和spin_unlock_irqstore，否则可能在某些架构上出现问题。
```

还有如下非阻塞的自旋锁操作：

```c
    int spin_trylock(spinlock_t * lock);
    int spin_trylock_bh(spinlock_t * lock);
```

##读取者/写入者自旋锁
内核提供自旋锁的读取者/写入者形式，具有rwlock_t类型，在<linux
/spinlock.h>中定义。我们可以用下面两种方式声明和初始化它们：

```c
    rwlock_t my_rwlock = RW_LOCK_UNLOCKED;

    rwlock_t my_rwlock;
    rwlock_init(&my_rwlock);
```

其他还有一系列函数和普通自旋锁类似，但是以read或write开头，如：

```c
    void read_lock(rwlock_t * lock);
    read_lock_irqsave(rwlock_t * lock, unsigned long flags) //？
```

##锁陷阱
我们很难驾轻就熟的使用锁,以下是可能导致错误的东西。

###不明确的规则
恰当的锁定模式需要清晰和明确的规则。当我们创建了一个可被并行访问的对象时，应该同时定义用来控制访问的锁。锁定模式必须一开始就安排好，否则其后的改进将会非常困难。

为了让锁定正常工作，必须编写一些函数假定调用者已经获取了相关的锁。通常，内部的静态函数可通过该方式编写，而提供给外部调用的函数则必须显示的处理锁定。在编写那些假定的调用者已处理了锁定的内部函数时，我们自己应该显示说明这种假设。

###锁的顺序规则
使用大量锁的系统中，代码通常需要一次拥有多个锁。

但是拥有多个锁可能很危险，两个线程以不同的顺序获取锁可能会进入死锁。解决方法也很简单，在必须获取多个锁时，应该始终以相同的顺序获得。只要遵守这个约定，如上所述的死锁就可以避免。

有帮助的规则有两个。如果我们必须获得一个局部锁和一个更中心位置的锁，则应该首先获取自己的局部锁。如果我们拥有信号量和自旋锁的组合，则必须首先获得信号量；在拥有自旋锁是调用down是个严重的错误。

#除了锁之外的办法
Linux内核提供了大量有用的锁原语，它们却让内核步履蹒跚。在某些情况下，原子的访问不需要完整的锁。

##免锁算法
有些时候我们可以重新构造算法，从根本上避免使用锁。

经常用于免锁的生产者/消费者任务的数据结构之一是循环缓冲区（circular buffer）。在这个算法中，一个生产者将数据放入数组的结尾，而消费者从另一端移走数据。到达数组尾部的时候，生产者绕回数组的头部。

如果仔细实现，在没有多个生产者和消费者的情况下，循环缓冲区不需要锁。生产者是唯一允许修改写入索引以及指向数组位置的线程。只要写入者在更新写入索引之前将新的值保存到缓冲区，则读取者将始终看到一致的数据。同时消费者是唯一可访问读取索引以及该索引指向位置的数据线程。

##原子变量
有时，共享的资源可能恰好是一个简单的整数值。通常，即使下面的简单操作也需要锁定：

```c    
    n_op++;
```
某些处理器可以以原子方式执行这类自加操作，但是我们不能指望它。针对这种情况，内核提供了一种原子的整数类型，称为atomic_t，定义在<asm/atomic.h>中。

atomitc_t变量在所有内核支持的架构上保存一个int值，但是由于某些处理器上这种数据类型的工作方式有些限制，因此变量中记录大于24位的整数。这种操作速度非常快，因为只要可能，它们就会被编译成单个机器指令。
```c
    void atomic_set(atomic_t *v, int i); //将v的值设置为i
    atomic_t v = ATOMIC_INIT(0);         //编译时利用宏静态初始化
    int atomic_read(atomic_t *v);
    void atomic_add(int i, atomic_t *v);
    void atomic_sub(int i, atomic_t *v);
    void atomic_inc(atomic_t *v);
    void atomic_dec(atomic_t *v);
    int atomic_inc_and_test(atomic_t *v);
    int atomic_dec_and_test(atomic_t *v);
    int atomic_sub_and_test(atomic_t *v);  //执行操作并测试结果，如果为0返回true。
    int atomic_add_negative(int i, atomic_t *v); //结果为负时返回true
    int atomic_add_return(inti i, atomic_t *v);
    int atomic_sub_return(inti i, atomic_t *v);
    int atomic_inc_return(inti i, atomic_t *v);
    int atomic_dec_return(inti i, atomic_t *v); //返回新的值给调用者
```

##位操作
为了实现位操作，内核提供了一组可原子的修改和测试单个位的函数。因为整个操作但单个步骤中，因此不会受到中断。这些函数依赖具体的架构，因此在<asm/bitops.h>中声明。

##其他机制
- seqlock linux/seqlock.h
- 读取-复制-更新 linux/rcupdate.h
