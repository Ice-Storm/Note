OpenGL的矩阵堆栈(用于固定管线编程)
===============
[TOC]

OpenGL的矩阵堆栈指的就是内存中专门用来存放矩阵数据的某块特殊区域。一般说来，矩阵堆栈常用于构造具有继承性的模型，即由一些简单目标构成的复杂模型。矩阵堆栈对复杂模型运动过程中的多个变换操作之间的联系与独立十分有利。因为所有矩阵操作函数如glLoadMatrix(),glMultMatrix(),glLoadIdentity()等只处理当前矩阵，这样堆栈中下面的其它矩阵就不受影响。堆栈操作函数有以下两个：

```c
void glPushMatrix(void);
```

该函数表示将所有矩阵一次压入堆栈中，当前矩阵和栈顶矩阵相同；压入的矩阵数不能太多，否则出错。

```c
void glPopMatrix(void);
```

该矩阵表示弹出堆栈顶部的矩阵作为当前矩阵；当堆栈中仅存一个矩阵时，不能进行弹出操作，否则出错。

#OpenGL维护两个栈：投影变换栈，模-视变换栈。
投影： glOtrho() gluPerspective() glMatrixMode(GL_PROJECTION)
模-视变换： glTranslate() glRotate() glScale() glMatrixMode(GL_MODELVIEW)

glMatrixMode(GL_MODELVIEW or GL_PROJECTION)执行后参数所指的矩阵栈就成为了当前矩阵栈，以后的矩阵栈操纵命令将作用于它。

#使用场景
在计算行星的运动转换矩阵之前，都会先调用glPushMatrix，把控制太阳运动的矩阵先存储起来。在每画出一个行星之后，并且画出另一颗行星之前，它会调用glPopMatrix把太阳的矩阵重设再取出来使用。因为每个行星都是以太阳的坐标系为基准在运动，所以在计算个别行星的运动矩阵之前，都要先把矩阵的内容还原成太阳的矩阵。

