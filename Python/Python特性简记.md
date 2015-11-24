Python3特性简记
=============

Python和C语言结合紧密，很多特点都类似C语言，所以在思考Python的语法特点时可以借鉴C语言的语法特性，相互联系印证。

1.系统函数名被用户定义覆盖后怎么办？
可以通过主动import buildins模块，用模块内的函数恢复。

#数据类型
1. 支持整型、浮点数、complex、decimal、fraction、boolean(immutable)
2. 字符串str类型(immutable)，bytes(binary data), bytearray(mutable variant of bytes)
3. ==(compare value), is(compare object) 

#数据结构
1. list(mutable) [1,2,3]
2. dict(mutable) {1:"one", 2:"two"}
3. sets(mutable) {1,2,3}
4. tuple(immutable) (1,2,3)
5. bytearray(mutable) b''
6. 列表推导 [i for i in range(10)]
7. 字典推导 {x: x**2 for x in range(10)}

#变量声明与定义
1. 不需要提前声明，也不需要指定类型，也没有var等修饰符
2. 变量赋值都是传递引用，要拷贝可以调用copy模块的copy和deepcopy
3. del var删除变量

#函数声明与调用
1.
```python
def fun(arg, *argv, **key):
    pass
```

2.
```python
fun(1,2,3,{1:'one',2:'two'})
```

3. Python的语句结构靠缩进。

 
#程序结构
1. if/else
2. while/until
3. for i in range(10):
4. with fun() as ret:

#文件操作
1. open/read/write/input/print

#XML文件
xml/xmllib

#正则表达式
import re

#数据库
sqlite3

#杂项
1. 格式化输出: "%d" % 1
2. 调用外部命令: `command`
3. 时间日期: import time
4. 随机数和程序输入参数: import random

##针对语言类型补充：
###类的声明和使用
1.
```python
class A(object):
    def __init__(self):
        pass

    def fun(self):
        pass
```
2.
```python
a = A
```

###异常处理
try:
<语句>        #运行别的代码
except <名字>：
<语句>        #如果在try部份引发了'name'异常
except <名字>，<数据>:
<语句>        #如果引发了'name'异常，获得附加的数据
else:
<语句>        #如果没有异常发生
finally:
             #退出try时总会执行

###多线程
import thread

###核心库
os, sys, re, time, thread

###标准库


#常见陷阱
Python的变量作用域分为四种，LEGB，分别是local，enclose scopes，global，build-in，for循环之类的代码块不存在作用域，(Ruby的for循环也不是个局部作用域)如：

```python
for i in range(10):
    x = 10

print(i,x)      #9, 10
```