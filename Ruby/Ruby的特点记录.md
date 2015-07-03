Ruby 的特点记录
==============

Ruby是一门纯面向对象语言；Ruby中的语句都是表达式，这点跟函数式编程的思想类似。
Ruby很多地方都体现了多态性，很多地方的参数并不要求指定的类型，只要能提供必须的方法就能正常工作，如"this is a #{value}"中的value并不要求特定的类型，只要能够提供to_s放发，就能进行字符串替换。
#数据类型
1. 支持整数、浮点数、大数、Complex、Rational（immutable）
2. 字符串是mutable的，可以设置编码，对应String类
3. 字符串判断相等== 和?eql都可以
4. True/False/Nil
5. 有一种Symbol类型

#数据结构
1. 对应Array和Hash
2. 初始化分别是[1, 2, 3]和{“one”=>1, “two”=>2, “three”=>3}（还有其他方式）
3. 遍历方式: xx.each {|x| print x}（迭代器的灵活使用）

#变量声明与定义
1. 根据变量名区分全局变量、局部变量、类变量和实例变量。Ruby对于不同变量的命名有契约规则
2. 不需要提前声明，也不需要指定类型，也没有var等修饰符

#函数声明与调用
1.    

```ruby
def foo()
    puts “hello world”  
end
```
2.     

```ruby
foo()
```
3. 语句可以不要终止符’;’，有时函数调用中的圆括号可以被省略
4. Ruby没有提供位置参数，但是Hash参数可以模仿类似功能

```ruby
sequence(:m=>3, :n=>3)
```
#程序结构
1. 条件式 if/elsif/else/end unless
2. 循环 while/do/end until
3. 循环 for var in collection do end
4. ruby的迭代/枚举功能很强大

#文件操作
File/Dir/FileTest

#XML文件
rexml/document足够用了

#正则表达式
正则操作符： =~ 
Regexp类：/ /

#数据库
Mysql/Ruby据说不错

#杂项
1. puts/print/printf
2. `外部命令`
3. Time.now
4. srand/rand
5. ARGV
6. "#{code}"

#类的声明和实例化
```ruby
class A
    code
end
class B < A
    code
end
b = B.new
```
#异常处理
```ruby
begin
    code
    [raise]
rescue
    [retry]
else
    code
ensure
    code
end 
```
#多线程
```ruby 
Thread.new {
    code
}
Fiber.new {
    code
}
```
#核心库

#标准库