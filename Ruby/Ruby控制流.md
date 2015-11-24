Ruby控制流
==========

控制流一共有以下几部分：
* Conditionals
* Loops
* Iterators and blocks
* Flow-altering statments like return and break
* Exceptions
* The special-case BEGIN and END statements
* The esoteric control structures known as fibers and continuations

#Conditionals
##if/unless
    if expression [then]
        code
    [else|elsif expression
        code]
    end

    name = if       x== 1 then "one"
           elsif    x== 2 then "two"
           else     x== 3 then "three"
           end

    code if expreesion

##case
Ruby的case语句和C语言不同，不允许fall through，允许使用非常量作为跳转条件。
    case
    when x ==1 
        "one"
    when x == 2
        "two"
    when x == 3
        "three"
    end

    case x
    when 1              #等同x===1
        "one"
    when 2
        "two"
    when 3
        "three"
    [else
        "many"]
    end

#Loops
##while|until
    <when|until> expression [do]
        code
    end

    begin  
        code
    end <when|until> conditional

    puts a.pop [until|while a.empty?] 

##for

    for variable [, variable ...] in expression [do]
       code
    end

##break
终止最内部的循环。如果在块内调用，则终止相关块的方法（方法返回 nil）。

##next
跳到最内部循环的下一个迭代。如果在块内调用，则终止块的执行（yield 或调用返回 nil）。

##redo
重新开始最内部循环的该次迭代，不检查循环条件。如果在块内调用，则重新开始 yield 或 call。

##retry
如果 retry 出现在 begin 表达式的 rescue 子句中，则从 begin 主体的开头重新开始。

    begin
       do_something # 抛出的异常
    rescue
       # 处理错误
       retry  # 重新从 begin 开始
    end
如果 retry 出现在迭代内、块内或者 for 表达式的主体内，则重新开始迭代调用。迭代的参数会重新评估。

    for i in 1..5
       retry if some_condition # 重新从 i == 1 开始
    end

    for i in 1..5
       retry if  i > 2
       puts "Value of local variable is #{i}"
    end

#Itetators and Enumerable Objects
##Ruby each 迭代器
each 迭代器返回数组或哈希的所有元素。
语法

    collection.each do |variable|
       code
    end
为集合中的每个元素执行 code。在这里，集合可以是数组或哈希。

实例

    ary = [1,2,3,4,5]
    ary.each do |i|
       puts i
    end

each 迭代器总是与一个块关联。它向块返回数组的每个值，一个接着一个。值被存储在变量 i 中，然后显示在屏幕上。

##Ruby collect 迭代器（map）
collect 迭代器返回集合的所有元素。

语法

    collection = collection.collect
collect 方法不需要总是与一个块关联。collect 方法返回整个集合，不管它是数组或者是哈希。

    a = [1,2,3,4,5]
    b = Array.new
    b = a.collect
注意：collect 方法不是数组间进行复制的正确方式。这里有另一个称为 clone 的方法，用于复制一个数组到另一个数组。

当您想要对每个值进行一些操作以便获得新的数组时，您通常使用 collect 方法。例如，下面的代码会生成一个数组，其值是 a 中每个值的 10 倍。

    a = [1,2,3,4,5]
    b = a.collect {|x| 10*x}

##Other

    3.times { puts "thank you!" }
    [1,2,3].map { |x| x*x }
    factorial = 1
    2.upto(n) { |x| factorial *= x}
    (1..2).zip("a".."b") #=>[[1,"1"],[2,"b"]]
    loop { yield enumerators.map { |e| e.next } }

#throw/catch
Ruby的throw/catch和java和C++的不同，多用来进行跳转，错误处理常用raise和rescue。
