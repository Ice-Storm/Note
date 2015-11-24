Ruby杂记
========

#其他细节
Ruby是一门纯面向对象的语言，一切皆是对象，类型也是Class类型的对象。与Python相比，Ruby的很多方法都内置到了类中，而Python则是提供全局函数。
Ruby中的所有运算符都是函数方法，基本都可以被重载。
Ruby中可以直接定义函数，但是定义的函数是属于一个隐含的Object类的。
Ruby的函数结尾可以定义标点=、?、!，其中!这个标点的功能我觉得最有用，如果一个函数结尾加上了!表示要注意，这个函数会改变调用这个函数的类，比如 *sort*和 *sort!*。
Ruby的继承靠include关键字或<。
构造函数的名字是initialize，相比Python，成员函数的定义省略了self参数。
if语句可以放在任何语句后面作为条件。
Ruby的函数如果没有参数可以省略括号。
Ruby标识符支持非ASCII字符。
Ruby中的语句都是表达式，跟函数式编程的思想类似。

#Numeric
Ruby和Python都可以表示无限精度的整数，自动类似转换，并直接提供迭代函数，不用像Python一样使用Range
    
    2.upto(10) {|x| puts x}


#String
Ruby可以用=begin和=end嵌入其他内容，包括html和文档。
Ruby的所有类都是开放的，包括系统提供的类都可以自由修改，并且提供了很多能够重载的运算符。
Ruby和Python都可以用单引号或双引号包裹字符串,Ruby的双引号字符串中可以嵌入Ruby代码。
Ruby为了方便嵌入网页使用，还提供了%q,%Q,%代替引号代表字符串，如：

    %q(this is a string)
    %Q<this is also string>
    %!Just use a _different_ delimiter\!!
    %(A mismatched paren \(must be escaped)
 
Ruby还有一种字符串称为Here Document

    greeting = <<HERE + <<THERE + "World"
    Hello
    HERE
    There
    THERE
    #=>"Hello\nThere\nWorld"

    document = <<'# # #'
    Hello
    # # #

    document = <<-'# # #'
    Hello
        # # #

Ruby中提供了快速执行shell命令的方法如`ls`，``同样支持插入Ruby代码：

    listing = `#{"ls"}`  #注意，#{}被代码的返回值替换

Ruby中的字符串和Python中的不同，Ruby中字符串是易变的，在同一个loop中的字符串每次都是不一样的：

    10.times {puts "test".object_id}
    str = "test"
    str[0] = 'a' #id 不变
并且修改字符串的值后，object id不变，仍然是同一个id。Python中的字符串是常量，不支持直接用下标修改。

Ruby中单字符表示：
    ?A #在1.9以后的Ruby中就是长度为1的字符串'A'

Ruby对字符串处理有很多加强，如可以直接用以下语法：
```ruby
    s = "hello"
    s[0..2]         #=>"hel"
    s["e"] = 'a'    #=>"e"
    s               #=>"hallo"
```
String提供多重迭代器，each_byte,each_char,each_line，1.9后支持多字节字符，length方法返回多字节字符长度，bytesize返回字节长度。[]方法按多字节字符为单位访问，getbyte按单字节访问。

#Array
Ruby对于Array内的字符串也有特殊的符号加强表示：

    white = %w[This is a test] #=>["This", "is", "a", "test"]

Ruby的很多函数都是返回迭代器，很方便和代码块配合使用，在这一点上比Python更方便。

    count = Array.new(3) {|i| i+1} #=>[1,2,3]
Array的各种方便的用法：
    
    a = ('a'..''e).to_a # Range convert to ['a','b','c','d','e']
    a[0..2]             #=>['a','b','c']
    a[0]                #=>'a'
    a[0,0]              #=>['a']
    a[0..1] = [1,2]     
    a                   #=>[1,2,'c','d','e']
    a[0] = [1,2]        #=>[[1,2],2,'c','d','e']
    a = [1,2] + [3,4]   #=>[1,2,3,4] 创建新的array
    a = a + 9           #Error, righthand must array
    a << 9              #=>[1,2,3,4,9]
    [1,2] - [1]         #=>[2] ，begin with copy of its lefthand array 
    [0] * 3             #=>[0,0,0]
    [1,2] | [3,4]       #=>[1,2,3,4]
    [1,2] & [1,3]       #=>[1]

#Hashes
Hash就是一种键值映射的数据结构。

    num = Hash.new
    numbers["one"] = 1
    numbers["two"] = 2
    number = {"one"=>1, "two"=>2}
    number = {:one => 1, :two => 2} #Symbol objects work more efficiently
    number = {one:1, two:2}         #同上

Hash可以使用各种数据类型做为Key，这点比Python自由，但是使用mutable类型的Key会影响Hash的正确定，因此在mutable Key变化后要对Hash调用rehash，或者直接对mutable变量调用freeze，保证数据的一致性，这里有一个特例，String在Ruby里作为一个mutable对象，会copy一份作为hash的key。

>The result is a syntax much like that used by JavaScript objects.

#Ranges

    1..10           #The integers 1 through 10, including 10
    1.0...10.0      #The number between 1.0 and 10.0,, excluding 10.0
    cold_war = 1945..1989
    cold_war.include? 1991
    (1..10).each {|i| puts i}

Ranges端点隐含着大小关系，必须能用操作符<=>比较，返回-1，0，1, begin必须小于end，否则内部为空，也就是Ranges默认为递增的。
除了要比较大小，如果是离散变量，提供 *succ* ，可以进行迭代，如interger，但是在判断值是否在该范围内是比较麻烦，需要不断掉用succ来判断；如果是连续变量无法进行迭代，但可以直接通过比较大小判断值的是否在范围内，如floting-point。
    
    'a'.succ    #=>'b'

#Symbols
Ruby解释器内部用了很多symbols表来存储所有的类，替代String进行加速，Ruby程序也可以使用Symbol，开头加上冒号表示

    :symbol
    :"symbol"
    :'another long symbol'
    s = "string"
    sym = :"#{s}"
Symbols可以使用%s定义

    %s["]   #Same as :'"'

Symbols可以查找方法名
    
    o.respond_to? :each #查找是否有each方法
to_sym，intern和to_s，id2name可以在String和Symbol中相互转换。通过Symbol调用方法：

    name = :size
    if o.respond_to? name
        o.send(name)
    end
Symbol和object不同，相同的字符串有相同的symbol但是object可以不同。
用字符串作为标识时可以考虑转换成symbol提高效率。

    "AM".to_sym == :AM      #=>true


#True, False, and Nil
true，flase和nil都是单实例。

#Objects
Ruby是纯面向对象语言，所有的值都是对象，所有对象都继承自Object类。和Python类似的是Ruby中参数的传递和变量赋值一般是传递引用。
Ruby中类也是一个对象，所以可以直接用下面的语句判断类型：

    o.class == String  #true if o is a String
    o.instance_of? String  #true if o is a String

以上方法只能判断直接类型，判断一个类是否是该对象的祖先可以用以下方式：

    x= 12
    x.is_a? Fixnum  #=>true
    x.is_a? Interger    #=>true
    x.is_a? Numeric #=>true
    x.is_a? Objects#=>true
    Numeric === x   #=>ture

##equal?
equal?方法是object定义的一个比较重要的方法，比较是否是同一个object

    a = "Ruby"
    b = c = "Ruby"

    a.equal?(c) #false
    b.equal?(c) #true: b and c refer to the same object
    c.object_id == b.object_id
继承自object的类不会重载改方法。
object默认提供==方法比较是否是同一个object，但是它的许多子类都重载了该方法，可以比较其他内容。
eql?方法和==类似，但是提供更加严格的限制：

    1.eql? 1.0      #=>false

#===
===符号被称为"case equality"，在case语句中用来测试是否符合条件。
Range定义===判断一个值是否在范围内，Regexp定义===判断字符串是否符合正则表达式，Class定义===判断object是否是类的实例。Symbol定义===判断右操作数是否有相同的symbol。

    (1..10) === 5   #true
    /\d+/ ==="123"  #true
    String === "s"  #true
    :s === "s"      #true
===常用在case语句中。

#类型转换
Ruby提供很多隐式类型转换函数，如to_str,to_ary,to_hash，这些在需要时被隐式调用，还提供try_convert转换函数，如

    a = "asd"
    b = [1]
    Array.try_convert(a)    #=>nil
    Array.try_convert(b)    #=>[1]

调用to_ary转换成array，返回array或nil。

#Boolean
Ruby中的bool类型和C语言之类的不同，其他类型一般没有方法直接转换成bool，但是在条件语句中可以进行bool判断，除了false和nil外都是true，如""是true类型，0是true类型。
    
    if 0
        puts "true"
    end
    #true

#clone and dup
两个方法的作用都是复制对象，该对象内的对其他对象的引用也会被复制成引用。两个方法的作用有些不同，clone是完全复制，包括frozen和tainted state（用于web应用中，标记对象被不被信任的用户使用），dup只复制tainted state。clone还复制sigleton方法，但是dup不复制。

#taint
方便web使用，标记不被信任的对象，可以传染。

#Expressions and Operators
大多数语言的低级表达式和高级语句是不同的，比如在控制循环语句控制程序流程，但是没有返回值。但是在Ruby中，它们之间没有明显的区别，所有语句都可以当成表达式计算值，这样方便了一些语句的连接：

    puts "hello world" if true

##Variable References
以$开头的变量是全局变量，@和@@开头的变量分别属于对象和类。

#Enumerator
internal iterator如果没有给出block，则会返回enumerator，如

    1.upto(10)      #=>Enumerator
一个对象可以产生多个enumerator，通过enumerator可以方便访问对象的数据，而且不会改变对象内部数据。

#Self关键字
Return the trace object during event。

#Invokeing Methods

    "hello".send :upcase
    Math.send(:sin, Math::PI/2)     #=>1.0

#coerce
Numeric方法，当前Numeric方法不认识参数时，调用参数的coerce方法，可以实现交换率。

#函数
Ruby函数的调用可以省略括号，因此在Python中使用的函数赋值语句就不能使用了，需要alias代替。

```ruby
def fun()
    print 'hello'
end
f = fun      #print 'hello', f=nil
alias f fun;
fun          #print 'hello'
f            #=>nil
f()          #print 'hello'
```



