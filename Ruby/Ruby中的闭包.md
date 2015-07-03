Ruby中的闭包（Closures）
===========

procs和lambdas在Ruby中是一个闭包。

#Blocks
block不能单独存在，必须放在一个方法调用后面。如果方法不是迭代器，没有调用yield，则block会被忽略。

    1.upto(10) {|x| puts x}
    1.upto(10) do |x|
        puts x
    end
    words.sort! {|x,y| y.length <=> x.length}   

block中不要显示调用return，否则可能会跳出当前控制流，造成不想要的结果，可以用next或break替代。next继续进行迭代，这次迭代返回next后面的值，break跳出返回break后面的值。
block是一个闭包，所以产生了一个封闭的变量作用域， 