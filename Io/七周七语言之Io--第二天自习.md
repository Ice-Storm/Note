七周七语言之Io--第二天自习
======================

这一的自习习题完成的晚了点，因为Io坑爹的交互式终端和io文件对换行符的处理不同，在交互终端中换行符尝尝被忽略，所以终端中的程序行为会变得不可理解，替换成分号后程序才正常工作。

1. 写一个斐波纳挈程序，计算第n个数。
* 递归版

```io
fib := method(n,
    if(n<3, return 1, return fib(n-1)+fub(n-2))
    )
```
* 非递归版本

```io
fib := method(n,
    sum := 1;
    pre1 := 1;
    pre2 := 1;
    for(i, 3, n, sum = pre1 + pre2; pre1 = pre2; pre2 = sum);
    return sum
    )
```

2. 分母为0时让运算符返回0

```io
Number systemDivision := Number getSlot("/")
Number / := method(num,
    if(num==0, return 0, return self systemDivision(num)))
```

3. 写一个程序，把二维数组中的所有数相加。

```io
sum := method(ll,
    r := 0;
    ll foreach(l, l foreach(n, r = r + n));
    return r
    )
```

4. 对列表增加一个名为myAverage的槽，以计算列表中所有数字的平均值。

```io
List myAverage := method(
    if(self isEmpty) then(return 0);
    sum := 0;
    self foreach(n,
        if(n type != "Number") then(Exception raise("not a number"));
        sum = sum + n;
        );
    return sum / (self size)
    )
```

5. 对二维列表写一个原型。该原型的dim(x, y)方法可为一个包含y个列表的列表分配内存，其中每个列表都有x个元素，set(x,y)可设置列表中的值，get(x,y)方法可返回列表中的值。

```io
Matrix := Object clone
Matrix dim := method(x,y,
    self data := List clone;
    for(i, 1, y, 
        inner := List clone;
        for(j, 1, x, inner push(nil));
        data push(inner)
        )
    )
Matrix set := method(x,y,v,
    inner := self data at(y);
    inner atPut(x, v);
    return self
    )
Matrix get := method(x,y,
    return self data at(y) at(x)
    )
```

6. 写一个转置方法
以下代码在交互式终端中报错，不明白错误原因。

```io
Matrix transpose := method(
    if(self data isEmpty) then(return nil);
    outerLen := self data size;
    innerLen := self data at(0) size;

    newData :=  Matrix clone
    newData dim(innerLen, outerLen);
    for(i, 0, outerLen-1, 
        for(j, 0, outerLen-1,
            newData set(j,i,self get(i,j));
        )
    );
    self data = newData data
)
```

对于Io的课后习题就做到这，由于Io简陋的交互式终端和落后的文档社区，想深入学习Io细节会遇到不少困难和深坑，个人觉得习题做到这已经能够体会到Io的设计思想，就没有必要继续在一门不太可能会用到的语言上继续花时间跳坑了，剩余习题就直接阅读别人的代码进行了解了。

Io，有缘再会吧！
