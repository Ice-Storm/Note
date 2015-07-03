Ruby中的变量
===========
一种编程语言中最常使用的元素就是变量，因此仔细了解Ruby的变量特点就很有必要，下面详细介绍Ruby中的变量特点。

#常用变量种类
* Numeric
* String
* Array
* Boolean
* Symbol
* Hash

#变量的作用域
以$开头的变量是全局变量，@和@@开头的变量分别属于对象和类，没有前缀的是局部变量，首字母大写的一般是常量，常量的可见域类似全局变量。Ruby objects的instance variables在object外部不可见。

类中局部变量和方法重名时，局部变量变量优先。
for和while之类的循环内部不是一个局部变量作用域（和C++有区别）。
##Class Instance Variables
除了Class Variables和Instance Variables外，还有一个Class Instance Variables。这是由于在Class内部，Method外部定义Instance Varables，这个变量由于self并不是指向objcet，所以成了Class Instance Variables。

#常量
首字母大写的为常量，一般常量习惯全部大写，但是也有首字母大写的，如String、Hash这些类；它们都是系统内部的类，根据以上规则，它们都是常量。在类中定义的常量属于类，可以通过::访问，如Math::PI，::操作符用来访问类或模块中的常量，::PI表示当前模块或类中的常量PI，Ruby默认全局环境是在Object类下，也就是全局下的上述常量可以表示成Object::PI。

常量有两条限制：
1. 对已经存在的常量赋值，Ruby会给出警告，但是仍会执行。
2. 对常量的赋值不允许在方法内执行。

不会创建未初始化常量

    N = 100 if false     #N不会创建
    n = 100 if false     #n会创建，值为nil

#变量访问
Ruby对象内部的变量被进行了压缩，对外部只暴露了方法。所以访问内部变量必须经过方法。

    class A
        def initialize()
            @x = 10
        end
        def x
            @x
        end
    end
    a = A.new
    a.x

如上式所示，经过良好定义的方法，对它进行调用从表面上看和直接访问变量相同，但实际上是调用了方法，通过这种方式Ruby统一了类的访问形式。

-=，+=等操作符都是缩写，并不是实际的方法，如以下两条语句相同：

    o.[x] -= 2
    o.[]=(x, o.[](x)-2)
#Boolean
Ruby中的Boolean类型同C语言和Python这些语言中的不同，需要注意，Ruby中的true不等于1，false也不等于0，Boolean类型和Numeric类型不同，不能等同，在判断语句中，除了false和nil被当成false外，其他都是true。

```ruby
if 0
    print 'true'
end
#print true 在这里if 0为真。
```
#并行赋值
Ruby的并行赋值把Array作为对象进行拆分，Python的并行赋值以Sequent为对象进行拆分。
如在Ruby中：
```ruby
#ruby
a, b = 'abc' #a='abc' b=nil
```
而在Pyhont中：
```python
#python
a, b = 'abc' #error, Python中变量数目必须对等或用*
a, b = 'ab'  #a = 'a', b = 'b'
```

```ruby
#ruby
x, y = y, x
x, y, z = 1, 2, 3

x = 1, 2, 3     #x=[1,2,3]
x, = 1, 2, 3    #x=1
x, y = 1, 2, 3  #x=1,y=2
x, y = [1, 2]   #x=1, y=2
x, y = 1        #x=1, y=nil
x,   = [1, 2]   #x=1
x, y, z = 1, *[2,3] #x=1,y=2,z=3
x, *y = 1, 2, 3 #x=1, y=[2,3]
x, *y = 1, 2    #x=1, y=[2]
x, *y = 1       #x=1, y=[]
*x, y = 1, 2, 3 #x=[1,2], y=3
*x, y = 1       #x=[], y=1
x, y, *z = 1, *[2,3,4] #x=1,y=2,z=[3,4]
```
##并行赋值中的括号
```ruby
x, (y,z) = a, b
#同
x = a
y, z = b

x, (y, z) = 1, [2, 3]  #x=1,y=2,z=3
```
#语法陷阱
```ruby
puts x,y=1,2        #error, 三个参数
puts (x,y=1,2)      #error, 函数调用，三个参数
puts((x,y=1,2))     #正常调用
```