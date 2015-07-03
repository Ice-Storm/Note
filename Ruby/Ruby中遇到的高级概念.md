Ruby中遇到的高级概念
==================


#Continuations

    $lines = {}
    def line(symbol)
        callcc {|c| $lines[symbol]=c}
    end
    def goto(symbol)
        $line[symbol].call
    end

    i = 0
    line 10
    puts i += 1
    goto 10 if i<5

    line 20
    puts i-= 1
    goto 20 if i>0

#block
block不检查参数个数。block内的return会直接从当前迭代器内返回，而不是返回到迭代器。

    3.times {|x| print x}
    &:symbol    #=>proc

#Procs
Proc类似工作方式类似block，block和lambda都是Proc的实例。proc不检查参数个数
return不仅会从proc返回，还会从当前方法返回，类似代码块。

    def invoke(&b)
        b.call
    end

    def invoke
        Proc.new.call
    end

##curry
返回proc并设置第一个参数

##arity
返回参数个数


#Lambdas
lambda方法会创建一个Proc实例，lambda是Kernel模块的方法。lambda检查参数个数，行为类似函数，return会直接从lambda返回。

    is_positive = lambda {|x| x>0}
    succ = ->(x){ x+1 }
    succ.call(1)
    succ.(1)
    data.sort &->(a,b){b-a}

#Singleton Methods

    o = "message"
    def o.printme      #define a singleton method for the object
        puts self
    end
    o.printme

Math.sin和File.delete都是singleton methods。Math是Module的一个对象常量，File是Class的对象常量，但是它们都有自己的方法，这些方法就是singleton methods，这个概念是随着类也是一个对象的概念产生的。

#Bindings
Bind储存了Ruby中的环境，和eval配合使用可以改变程序工作方式。

    def mutiplier(n)
        lambda {|data| data.collect{|x| x*n}}
    end
    doubler = mutiplier(2)
    eval("n=3", doubler.binding)
    OR
    doubler.binding.eval("n=3")
    puts doubler([1,2,3])   #[3,6,9]

#Method Objects
Ruby的methods和blocks是可执行的数据结构，不是对象。但是Ruby还有Method object。

    m = 0.method(:succ)     #A Method representing the succ method of Fixnum 0
    puts m.call
    puts m[]
注意method object不是闭包的，不能访问外部变量。